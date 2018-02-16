from xml.etree.ElementTree import tostring

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.project import Project
from breadboarder.core.svg import Point


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    svg = project.svg()
    return tostring(svg)

print(draw_breadboard())