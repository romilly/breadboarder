"""Python side of the browser editor: run DSL code, report parts and ports,
and rewrite the code when a part is dragged."""
import ast
import json
import re
import sys

if '/pkg' not in sys.path:
    sys.path.insert(0, '/pkg')

from breadboarder.author.illustrator import Illustrator
from breadboarder.core.host import Host
from breadboarder.core.project import Component, Part
from breadboarder.core.units import PITCH

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
        return _replace(code, start, end, lambda text: _move_host(text, dx, dy))
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
