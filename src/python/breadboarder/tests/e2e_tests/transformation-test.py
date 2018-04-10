from breadboarder.core.breadboard import Breadboard
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(120, 20))
    project.add(breadboard)
    cp2102 = CP2102().rotate(90).move_to(Point(20, -100))
    project.add(cp2102)
    svg = project.element()
    write(svg, 'svg/transformed.svg')


draw_breadboard()