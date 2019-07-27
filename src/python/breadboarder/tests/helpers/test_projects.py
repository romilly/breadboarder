from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, atMega328, LED
from breadboarder.core.project import Project
from svg.point import Point


def test_project():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(
            Wire('red', breadboard['d9'], breadboard['g11']),
            atMega328(breadboard['f3']),
            LED('red', breadboard['g12'], breadboard['g17']))
    return project