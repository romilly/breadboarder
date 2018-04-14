from breadboarder.core.breadboard import Port
from breadboarder.core.project import Project
from breadboarder.svg.point import Point
from breadboarder.svg.svg import Line, write, GroupedDrawable, Text, Rectangle
from breadboarder.transformations.transform import Translation, Rotation

SPACING = 50

def p(x,y):
    return Point(x,y).scale(SPACING)

def s(distance):
    return distance*SPACING

class Grid(GroupedDrawable):
    def __init__(self, color='black',opacity=1.0):
        GroupedDrawable.__init__(self, opacity=opacity)
        for i in range(-5, 6):
            self.add(Line(p(-5,i),p(5, i), color=color, linecap='round'))
            self.add(Line(p(i,-5),p(i, 5), color=color))
            self.add(Text('%d' % s(i), Point(2, 4+s(i)), color=color, size=3))
            self.add(Text('%d' % s(i), Point(2+s(i), -2), color=color, size=3))


class Box(GroupedDrawable):
    def __init__(self):
        GroupedDrawable.__init__(self)
        self.ports = {}
        self.add(Rectangle(s(3),s(2)))
        self.add(Grid('grey', opacity=0.8))
        self.add_port('A',Port(self, Point(5,5)))

    def add_port(self, key, port):
        self.ports[key] = port

    def __getitem__(self, key):
        return self.ports[key]

class Example():
    def __init__(self, number, *transformations):
        self.number = number
        self.transformations = transformations

    def draw_grid(self):
        project = Project(300, 300, view_box=(-150, -150, 300, 300))
        grid = Grid()
        project.add(grid)
        box = Box()
        box.transformations = self.transformations
        project.add(box)
        location = box['A'].location()
        project.add(Text('A(%5.2f,%5.2f)' % location.cartesian_coordinates(), location + Point(0, 5), color='grey'))
        svg = project.element()
        write(svg, 'svg/grid%d.svg' % self.number)


def draw_grids():
    Example(1).draw_grid()
    Example(2, Translation(Point(10, 20))).draw_grid()
    Example(3, Rotation(90)).draw_grid()
    Example(4, Rotation(45)).draw_grid()
    Example(5, Rotation(45,Point(10,20)),Translation(Point(10,20))).draw_grid()


draw_grids()