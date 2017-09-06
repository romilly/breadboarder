from breadboarder.core.breadboard import Breadboard
from breadboarder.core.project import Project, write

from breadboarder.core.components import Wire


def test_breadboard():
    project = Project()
    breadboard = Breadboard()
    project.add(breadboard)
    breadboard.connect(Wire('red'), 'TP3','a10')
    svg = project.svg()
    write(svg, 'svg/bb.svg')

test_breadboard()
