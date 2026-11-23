"""Python side of the browser editor: run DSL code, report parts and ports,
and rewrite the code when a part is dragged."""
import ast
import importlib
import json
import re
import sys

if '/pkg' not in sys.path:
    sys.path.insert(0, '/pkg')

from breadboarder.author.illustrator import Illustrator
from breadboarder.core.host import Host
from breadboarder.core.project import Component, Part
from breadboarder.core.units import PITCH
from svg.point import Point
from svg.transform import Translation

PORT_REF = re.compile(r"""(\w+)\[(['"])(\w+)\2\]""")
MOVE_TO = re.compile(r"move_to\(\s*Point\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)\s*\)")
SNAP_TOLERANCE = 1.0


class _Tracker(ast.NodeTransformer):
    """Wrap every call so we learn which source span produced each Part."""

    def __init__(self, line_starts):
        self.line_starts = line_starts

    def offset(self, line, col):
        return self.line_starts[line - 1] + col

    def visit_Call(self, node):
        self.generic_visit(node)
        start = self.offset(node.lineno, node.col_offset)
        end = self.offset(node.end_lineno, node.end_col_offset)
        return ast.Call(func=ast.Name('_bb_track', ast.Load()),
                        args=[node, ast.Constant(start), ast.Constant(end)], keywords=[])


def _run(code):
    """Execute code, returning its namespace and {id(part): [(start, end), ...]}.

    Offsets are byte offsets into code encoded as UTF-8 (as ast reports them)."""
    source = code.encode('utf-8')
    line_starts, total = [], 0
    for line in source.splitlines(keepends=True):
        line_starts.append(total)
        total += len(line)
    line_starts.append(total)
    tree = ast.fix_missing_locations(_Tracker(line_starts).visit(ast.parse(code)))
    spans = {}

    def track(value, start, end):
        if isinstance(value, Part):
            spans.setdefault(id(value), []).append((start, end))
        return value

    ns = {'_bb_track': track}
    exec(compile(tree, '<editor>', 'exec'), ns)
    return ns, spans


def _parts(ns):
    return [step for step in ns['project'].steps() if step.is_part()]


def render(code):
    """Run DSL code that defines `project`; return SVG, ports and parts as JSON."""
    ns, _ = _run(code)
    illustrator = Illustrator(640, 480)
    for step in ns['project'].steps():
        illustrator.take(step)
    seen, ports = set(), []
    for name, value in ns.items():
        if isinstance(value, Host) and id(value) not in seen:
            seen.add(id(value))
            for port_name, port in value._ports.items():
                loc = port.location()
                ports.append([name, port_name, loc.x, loc.y])
    parts = [{'name': type(p).__name__,
              'kind': 'host' if isinstance(p, Host) else 'component'}
             for p in _parts(ns)]
    return json.dumps({'svg': illustrator.svg(), 'ports': ports, 'parts': parts})


def move(code, index, dx, dy):
    """Return code rewritten so that part number `index` moves by (dx, dy).

    Raises ValueError if the part can't be moved there."""
    ns, spans = _run(code)
    part = _parts(ns)[index]
    if id(part) not in spans:
        raise ValueError('Cannot find the code that created this part')
    if isinstance(part, Host):
        start, end = max(spans[id(part)], key=lambda s: s[1] - s[0])  # whole chain
        ex, ey = _move_to_change(part, dx, dy)
        return _replace(code, start, end, lambda text: _move_host(text, ex, ey))
    if isinstance(part, Component):
        start, end = min(spans[id(part)], key=lambda s: s[1] - s[0])  # constructor call
        return _replace(code, start, end, lambda text: _move_component(text, ns, dx, dy))
    raise ValueError('This part cannot be moved')


def _replace(code, start, end, rewrite):
    source = code.encode('utf-8')
    text = source[start:end].decode('utf-8')
    return (source[:start] + rewrite(text).encode('utf-8') + source[end:]).decode('utf-8')


def _fmt(value):
    value = round(value)
    return str(int(value))


def _move_to_change(host, dx, dy):
    """How much to change the host's last move_to so it moves (dx, dy) on screen.

    Earlier transforms (e.g. a rotate) can turn the move_to's frame, so measure
    the effect of unit changes and invert that 2x2 linear map."""
    translations = [t for t in host.transformations if isinstance(t, Translation)]
    added = not translations
    if added:  # a new move_to would be appended last
        host.transformations.append(Translation(Point(0, 0)))
    last = host.transformations[-1] if added else translations[-1]
    original = last.vector

    def origin_after(ux, uy):
        last.vector = original + Point(ux, uy)
        return host.location_of(Point(0, 0))

    try:
        o, px, py = origin_after(0, 0), origin_after(1, 0), origin_after(0, 1)
    finally:
        last.vector = original
        if added:
            host.transformations.pop()
    a, c = px.x - o.x, px.y - o.y   # screen effect of +1 in move_to x
    b, d = py.x - o.x, py.y - o.y   # screen effect of +1 in move_to y
    det = a * d - b * c
    return (d * dx - b * dy) / det, (a * dy - c * dx) / det


def _move_host(text, dx, dy):
    matches = list(MOVE_TO.finditer(text))
    if not matches:
        return '%s.move_to(Point(%s, %s))' % (text, _fmt(dx), _fmt(dy))
    m = matches[-1]
    x, y = float(m.group(1)) + dx, float(m.group(2)) + dy
    return text[:m.start()] + 'move_to(Point(%s, %s))' % (_fmt(x), _fmt(y)) + text[m.end():]


def _nearest_port(host, x, y, limit):
    best, best_d = None, limit
    for name, port in host._ports.items():
        loc = port.location()
        d = ((loc.x - x) ** 2 + (loc.y - y) ** 2) ** 0.5
        if d < best_d:
            best, best_d = name, d
    return best


def _move_component(text, ns, dx, dy):
    refs = list(PORT_REF.finditer(text))
    if not refs:
        raise ValueError('This part is not plugged into anything I can move')
    hosts = []
    for ref in refs:
        host = ns.get(ref.group(1))
        if not isinstance(host, Host) or ref.group(3) not in host._ports:
            raise ValueError('Cannot understand %s' % ref.group(0))
        hosts.append(host)
    # snap: move the first end to the socket nearest its dragged position
    first = hosts[0][refs[0].group(3)].location()
    target = _nearest_port(hosts[0], first.x + dx, first.y + dy, limit=PITCH)
    if target is None:
        raise ValueError('%s would not land on a socket or pin' % refs[0].group(0))
    snapped = hosts[0][target].location()
    sdx, sdy = snapped.x - first.x, snapped.y - first.y
    if abs(sdx) < SNAP_TOLERANCE and abs(sdy) < SNAP_TOLERANCE:
        return text
    pieces, last = [], 0
    for ref, host in zip(refs, hosts):
        loc = host[ref.group(3)].location()
        new_name = _nearest_port(host, loc.x + sdx, loc.y + sdy, SNAP_TOLERANCE)
        if new_name is None:
            raise ValueError('%s would not land on a socket or pin' % ref.group(0))
        pieces.append(text[last:ref.start()])
        pieces.append('%s[%s%s%s]' % (ref.group(1), ref.group(2), new_name, ref.group(2)))
        last = ref.end()
    pieces.append(text[last:])
    return ''.join(pieces)


# The palette: parts the editor can add. `template` gets the port references
# as {0}, {1}, ... and the wire colour as {colour}. `name` (default: kind) is
# the class or function to import. One-port parts have a `footprint`: where
# their pins sit relative to that port, so we can check they all land on
# sockets of the same host.
COMPONENTS = 'breadboarder.core.components'
HEADER = 'breadboarder.core.header'
DIL_SPAN = 3 * PITCH - 3      # top row of pins to bottom row (see DIL.height)
FOOTPRINT_TOLERANCE = 3.0


def dil_footprint(pins):
    per_side = pins // 2
    return [(PITCH * i, 0) for i in range(per_side)] + [(PITCH * i, DIL_SPAN) for i in range(per_side)]


def row_footprint(pins):
    return [(PITCH * i, 0) for i in range(pins)]


def pico_footprint():
    """Pins 1-20 along pin 1's row, pins 40-21 along the row five letters on."""
    from breadboarder.core.breadboard import Breadboard
    board = Breadboard()
    span = board['h1'].location().y - board['c1'].location().y
    return row_footprint(20) + [(x, span) for x, _ in row_footprint(20)]


PICO = 'breadboarder.core.pico'


PALETTE = [
    {'kind': 'Wire', 'label': 'Wire', 'module': COMPONENTS,
     'template': "Wire('{colour}', {0}, {1})", 'ports': 2},
    {'kind': 'Resistor', 'label': 'Resistor', 'module': COMPONENTS,
     'template': "Resistor('10k', '5%', {0}, {1})", 'ports': 2},
    {'kind': 'LED', 'label': 'LED', 'module': COMPONENTS,
     'template': "LED('red', {0}, {1})", 'ports': 2},
    {'kind': 'Diode', 'label': 'Diode', 'module': COMPONENTS,
     'template': "Diode('1N4148', {0}, {1})", 'ports': 2},
    {'kind': 'DiskCapacitor', 'label': 'Capacitor', 'module': COMPONENTS,
     'template': "DiskCapacitor('100n', {0}, {1})", 'ports': 2},
    {'kind': 'Crystal', 'label': 'Crystal', 'module': COMPONENTS,
     'template': "Crystal('16MHz', {0}, {1})", 'ports': 2},
    {'kind': 'atMega328', 'label': 'ATmega328', 'module': COMPONENTS,
     'template': "atMega328({0})", 'ports': 1, 'footprint': dil_footprint(28)},
    {'kind': 'pcf8574', 'label': 'PCF8574', 'module': COMPONENTS,
     'template': "pcf8574({0})", 'ports': 1, 'footprint': dil_footprint(16)},
    {'kind': 'header6', 'name': 'header', 'label': '6-pin header', 'module': HEADER,
     'template': "header(6, {0})", 'ports': 1, 'footprint': row_footprint(6)},
    {'kind': 'Potentiometer', 'label': 'Trimmer pot', 'module': COMPONENTS,
     'template': "Potentiometer('10k', {0})", 'ports': 1, 'footprint': row_footprint(3)},
    {'kind': 'RotaryPotentiometer', 'label': 'Rotary pot', 'module': COMPONENTS,
     'template': "RotaryPotentiometer('10k', {0})", 'ports': 1, 'footprint': row_footprint(3)},
    {'kind': 'RgbLed', 'label': 'RGB LED', 'module': COMPONENTS,
     'template': "RgbLed({0})", 'ports': 1, 'footprint': row_footprint(4)},
    {'kind': 'Pico', 'label': 'Pico', 'module': PICO,
     'template': "Pico({0})", 'ports': 1, 'footprint': pico_footprint()},
    {'kind': 'PicoW', 'label': 'Pico W', 'module': PICO,
     'template': "PicoW({0})", 'ports': 1, 'footprint': pico_footprint()},
    {'kind': 'Pico2', 'label': 'Pico 2', 'module': PICO,
     'template': "Pico2({0})", 'ports': 1, 'footprint': pico_footprint()},
    {'kind': 'Pico2W', 'label': 'Pico 2 W', 'module': PICO,
     'template': "Pico2W({0})", 'ports': 1, 'footprint': pico_footprint()},
    # Hosts: placed by clicking a point; `var` is the base of the variable name.
    {'kind': 'Breadboard', 'label': 'Breadboard', 'module': 'breadboarder.core.breadboard',
     'host': True, 'var': 'breadboard', 'ports': 0},
    {'kind': 'CP2102', 'label': 'CP2102', 'module': 'breadboarder.core.cp2102',
     'host': True, 'var': 'cp', 'ports': 0},
    {'kind': 'FtdiFriend', 'label': 'FTDI Friend', 'module': 'breadboarder.core.ftdi_friend',
     'host': True, 'var': 'ftdi', 'ports': 0},
    {'kind': 'Explorer', 'label': 'Explorer', 'module': 'breadboarder.core.explorer',
     'host': True, 'var': 'explorer', 'ports': 0},
]


def palette():
    """The palette entries the page shows, as JSON."""
    return json.dumps([{'kind': e['kind'], 'label': e['label'], 'ports': e['ports'],
                        'host': e.get('host', False)} for e in PALETTE])


def _entry(kind):
    entry = next((e for e in PALETTE if e['kind'] == kind), None)
    if entry is None:
        raise ValueError('Unknown part %s' % kind)
    return entry


def add_part(code, kind, refs, colour='red'):
    """Return code with a project.add(...) line for a new part plugged into refs.

    refs are port references as code, e.g. "breadboard['a3']"."""
    entry = _entry(kind)
    if len(refs) != entry['ports']:
        raise ValueError('%s needs %d ports' % (entry['label'], entry['ports']))
    if 'footprint' in entry:
        ns, _ = _run(code)
        problem = _footprint_problem(ns, entry, refs[0])
        if problem:
            raise ValueError(problem)
    code = _ensure_import(code, entry['module'], entry.get('name', kind))
    line = 'project.add(%s)' % entry['template'].format(*refs, colour=colour)
    return code.rstrip() + '\n' + line + '\n'


def _port_from_ref(ns, ref):
    m = PORT_REF.fullmatch(ref)
    host = ns.get(m.group(1)) if m else None
    if not isinstance(host, Host) or m.group(3) not in host._ports:
        raise ValueError('Cannot understand %s' % ref)
    return host, host[m.group(3)]


def _footprint_problem(ns, entry, ref):
    """None if every pin of a one-port part lands on a socket, else why not."""
    host, port = _port_from_ref(ns, ref)
    loc = port.location()
    for dx, dy in entry['footprint']:
        if _nearest_port(host, loc.x + dx, loc.y + dy, FOOTPRINT_TOLERANCE) is None:
            return "The %s's pins would not all land on sockets there" % entry['label']
    return None


def preview(code, kind, ref):
    """Draw a one-port part plugged into ref, without changing the code.

    Returns JSON {svg, ok, message}: svg is the part's <g> element."""
    from xml.etree.ElementTree import tostring
    entry = _entry(kind)
    ns, _ = _run(code)
    name = entry.get('name', kind)
    ns[name] = getattr(importlib.import_module(entry['module']), name)
    part = eval(entry['template'].format(ref), ns)
    problem = _footprint_problem(ns, entry, ref)
    return json.dumps({'svg': tostring(part.element()).decode('utf-8'),
                       'ok': problem is None, 'message': problem or ''})


def _ensure_import(code, module, name):
    """Add `from module import name` after the last top-level import, unless
    the code already defines or imports name."""
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if any((alias.asname or alias.name) == name for alias in node.names):
                return code
        elif isinstance(node, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                return code
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    same_module = [n for n in imports if isinstance(n, ast.ImportFrom) and n.module == module]
    after = (same_module or imports)[-1:]  # beside its module's import if there is one
    lines = code.splitlines(keepends=True)
    at = after[0].end_lineno if after else 0
    return ''.join(lines[:at] + ['from %s import %s\n' % (module, name)] + lines[at:])


def add_host(code, kind, x, y):
    """Return code with a new host, under a fresh variable name, placed at (x, y)."""
    entry = _entry(kind)
    if not entry.get('host'):
        raise ValueError('%s is not placed by position' % entry['label'])
    ns, _ = _run(code)
    name, n = entry['var'], 1
    while name in ns:
        n += 1
        name = '%s%d' % (entry['var'], n)
    code = _ensure_import(code, entry['module'], kind)
    code = _ensure_import(code, 'svg.point', 'Point')
    lines = '%s = %s().move_to(Point(%s, %s))\nproject.add(%s)\n' % (name, kind, _fmt(x), _fmt(y), name)
    return code.rstrip() + '\n' + lines


def host_preview(kind):
    """Draw a host at the origin, as JSON {svg}; the page moves it under the pointer."""
    from xml.etree.ElementTree import tostring
    entry = _entry(kind)
    host = getattr(importlib.import_module(entry['module']), kind)()
    return json.dumps({'svg': tostring(host.element()).decode('utf-8')})
