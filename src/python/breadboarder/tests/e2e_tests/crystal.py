from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Crystal
from breadboarder.core.project import Project
from breadboarder.core.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(Crystal('16Mz', breadboard['g24'], breadboard['a24']))
    svg = project.svg()
    write(svg, 'svg/xtal.svg')


draw_breadboard()