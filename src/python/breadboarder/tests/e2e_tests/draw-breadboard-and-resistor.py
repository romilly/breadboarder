from breadboarder.core.breadboard_apl import Breadboard
from breadboarder.core.components import Wire
from breadboarder.core.project import Project
from breadboarder.core.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(Wire('red', breadboard['g1'], breadboard['TP1']))
    svg = project.element()
    write(svg, 'svg/bb-apl.svg')


draw_breadboard()