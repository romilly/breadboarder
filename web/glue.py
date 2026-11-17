import sys, json
if '/pkg' not in sys.path:
    sys.path.insert(0, '/pkg')
from breadboarder.author.illustrator import Illustrator
from breadboarder.core.host import Host

def render(code):
    """Run DSL code that defines `project`; return SVG and port positions as JSON."""
    ns = {}
    exec(code, ns)
    project = ns['project']
    illustrator = Illustrator(640, 480)
    for step in project.steps():
        illustrator.take(step)
    seen, ports = set(), []
    for name, value in ns.items():
        if isinstance(value, Host) and id(value) not in seen:
            seen.add(id(value))
            for port_name, port in value._ports.items():
                loc = port.location()
                ports.append([name, port_name, loc.x, loc.y])
    return json.dumps({'svg': illustrator.svg(), 'ports': ports})
