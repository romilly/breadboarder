from breadboarder.core.project import Component
from breadboarder.core.units import PITCH
from svg.point import Point
from svg.svg import Rectangle, Text


class Header(Component):

    def instruction(self):
        return 'Insert pin 1 of the %s (%s) into %s' % (self.description(), self.id(),
                                                        self.connected_ports[0].describe_location())

    def description(self):
        return self.name

    def __init__(self, pins, name, port):
        Component.__init__(self,[port])
        self.pins = pins
        self.name = name
        self.labels = [str(i + 1) for i in range(self.pins)]
        self.add_parts()
        self.move_to(port.location() - Point(2, -1)) # for visual correctness

    def id_prefix(self):
        return 'H'

    def part_type(self):
        return 'Male Header'

    def pins_per_side(self):
        return self.pins

    def center(self):
        return self.extent().scale(0.5)

    def width(self):
        return 4 + PITCH * (self.pins_per_side()-1)

    def height(self):
        return PITCH

    def add_parts(self):
        self.add(Rectangle(self.width(), self.height(), fill='grey', stroke='grey').move_to(Point(0,-2.5)))
        self.add(Text(self.name,(self.center()+ Point(0, 2)), color='lightgrey', anchor='middle',size=4))
        for i in range(0, self.pins_per_side()):
            x = PITCH*i
            self.add(Rectangle(4, 2,fill='white').move_to(Point(x,0)))
            # self.add(Rectangle(4, 2,fill='white').move_to(Point(x,self.height()+1)))
            self.add(Text(self.labels[i], Point(x+3,self.height()-1),size=2, anchor='start').rotate(-90))
            # self.add(Text(self.labels[self.pins-(i+1)], Point(x+3, 1),size=2,anchor='end').rotate(-90))
            # self.add(Dimple(Point(0, self.center().y), 2))

    def extent(self):
        return Point(self.width(), self.height())

def header(pins, port):
    return Header(pins, '%d-pin male header' % pins, port)