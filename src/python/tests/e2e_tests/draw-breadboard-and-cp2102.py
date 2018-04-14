from breadboarder.core.breadboard import Breadboard
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90, Point(40, 400)).move_to(Point(40,400))
    project.add(cp)
    svg = project.element()
    write(svg, 'svg/two-hosts.svg')


draw_breadboard()