from breadboarder.core.project import Project
from breadboarder.svg.point import Point
from breadboarder.svg.svg import CompositeItem, Line, write, GroupedDrawable, Text, Rectangle


class Grid(GroupedDrawable):
    def __init__(self, color='black'):
        GroupedDrawable.__init__(self)
        for i in range(-5, 6):
            self.add(Line(Point(-50,10*i),Point(50, 10*i), color=color))
            self.add(Line(Point(10*i,-50),Point(10*i, 50), color=color))
            self.add(Text('%d' % i, Point(2, 4+10*i), color=color, size=3))
            self.add(Text('%d' % i, Point(2+10*i, -2), color=color, size=3))

class Box(GroupedDrawable):
    def __init__(self):
        GroupedDrawable.__init__(self)
        self.add(Rectangle(30,20))
        self.add(Grid('grey'))


def draw_grid():
    project = Project()
    grid = Grid()
    project.add(grid)
    project.add(Box().rotate(-90).move_to(Point(2,3)))
    svg = project.element()
    write(svg, 'svg/spike.svg')


draw_grid()