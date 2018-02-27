from breadboarder.core.breadboard import Breadboard
from breadboarder.core.project import Project
from breadboarder.core.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    svg = project.svg()
    write(svg, 'svg/bb.svg')


draw_breadboard()