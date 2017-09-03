# draw Dual In Line IC chip (like ATMegas 328)
from xml.etree.ElementTree import Element

from breadboarder.breadboard import Breadboard
from breadboarder.components import Component
from breadboarder.drawing import Point, Rectangle, GroupedDrawable, Text, Drawable, Circle


# TODO: similar defs of extend, center. Move to Drawable, which would need width() and height()?

def atMega328():
    labels = ('~RST','RXD','TXD','PD2','PD3','PD4','VCC','GND','XTAL1','XTAL2','PD5','PD6','PD7','PB0',
            'PB1','PB2','PB3','PB4','PB5','AVCC','AREF','GND','PC0','PC1','PC2','PC3','PC4','PC5')
    return DIL(28,'ATmega328',labels)

def pcf8574():
    labels = ('A0', 'A1', 'A2', 'P0', 'P1', 'P2','P3','Vss','P4','P5','P6','P7','~INT','SCL','SDA','Vdd')
    return DIL(16,'PCF8574',labels)


class DIL(GroupedDrawable, Component):
    def __init__(self, pins, name, labels):
        GroupedDrawable.__init__(self,svg_id='IC')
        self.pin1 = Point(0, 0)
        self.pins = pins
        self.name = name
        self.labels = labels
        self.add_parts()

    def pins_per_side(self):
        return int(self.pins/2)

    def center(self):
        return self.start + self.extent().scale(0.5)

    def width(self):
        return 4 + Breadboard.PITCH * (self.pins_per_side()-1)

    def height(self):
        # TODO The height is fixed, and does not depend on start.y! Change this
        return self.start.y + 3 * (Breadboard.PITCH - 1) -2

    def add_parts(self):
        self.add(Rectangle(self.width(), self.height(), fill='grey', stroke='grey'))
        self.add(Text(self.name,(self.center()+ Point(0, 2)), color='lightgrey', anchor='middle',size=4))
        for i in range(0, self.pins_per_side()):
            x = Breadboard.PITCH*i
            self.add(Rectangle(4, 2,fill='white').move_to(Point(x,-2.5)))
            self.add(Rectangle(4, 2,fill='white').move_to(Point(x,self.height()+1)))
            self.add(Text(self.labels[i], Point(x+3,self.height()-1),size=2, anchor='start').rotate(-90))
            self.add(Text(self.labels[self.pins-(i+1)], Point(x+3, 1),size=2,anchor='end').rotate(-90))
            self.add(Dimple(Point(0, self.center().y), 2))

    def extent(self):
        return Point(self.width(), self.height())

    def connect(self, positions):
        if len(positions) is not 1:
            raise Exception('DIL only needs one position for insertion')  # for now :)
        self.move_to(positions[0] - Point(2, -1))
        return self


class Dimple(Drawable):
    def __init__(self, center, radius):
        Drawable.__init__(self, center)
        self.radius = radius

    def svg(self):
        return Element("path", {'d': 'M %d %d A %d %d 0 1 1 %d %d' % (self.start.x, self.start.y-self.radius,
                                            self.radius, self.radius, self.start.x, self.start.y+self.radius)})



