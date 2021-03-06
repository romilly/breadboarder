from breadboarder.core.breadboard import Breadboard
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    svg = project.build_svg()
    write(svg, 'svg/bb-apl.svg')


draw_breadboard()