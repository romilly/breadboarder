from breadboarder.author.illustrator import Illustrator
from breadboarder.core.breadboard import Breadboard
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.project import Project
from svg.svg import Point, write


def draw_breadboard():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90, Point(40, 400)).move_to(Point(40,400))
    project.add(cp)
    illustrator = Illustrator()
    for step in project.steps():
        illustrator.take(step)
    write(illustrator.svg(), 'svg/two-hosts.svg')


draw_breadboard()