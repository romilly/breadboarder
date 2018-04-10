# draw Dual In Line IC chip (like ATMegas 328)
from xml.etree.ElementTree import Element

from .breadboard import Breadboard
from breadboarder.svg.svg import Point, Rectangle, GroupedDrawable, Text, Drawable


# TODO: similar defs of extend, center. Move to Drawable, which would need width() and height()?

def atMega328(port):
    labels = ('~RST','RXD','TXD','PD2','PD3','PD4','VCC','GND','XTAL1','XTAL2','PD5','PD6','PD7','PB0',
            'PB1','PB2','PB3','PB4','PB5','AVCC','AREF','GND','PC0','PC1','PC2','PC3','PC4','PC5')
    return DIL(28,'ATmega328', port, labels)

def pcf8574(port):
    labels = ('A0', 'A1', 'A2', 'P0', 'P1', 'P2','P3','Vss','P4','P5','P6','P7','~INT','SCL','SDA','Vdd')
    return DIL(16,'PCF8574',port, labels)


class DIL(GroupedDrawable):
    def __init__(self, pins, name, port, labels):
        GroupedDrawable.__init__(self,svg_id='IC')
        self.pins = pins
        self.name = name
        self.labels = labels
        self.add_parts()
        self.move_to(port.location() - Point(2, -1)) # for visual correctness

    def pins_per_side(self):
        return int(self.pins/2)

    def center(self):
        return self.extent().scale(0.5)

    def width(self):
        return 4 + Breadboard.PITCH * (self.pins_per_side()-1)

    def height(self):
        return 3 * (Breadboard.PITCH - 1) -2

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


class Dimple(Drawable):
    def __init__(self, center, radius):
        Drawable.__init__(self, center)
        self.radius = radius

    def element(self):
        return Element("path", {'d': 'M %d %d A %d %d 0 1 1 %d %d' % (self.top_left.x, self.top_left.y - self.radius,
                                                                      self.radius, self.radius, self.top_left.x, self.top_left.y + self.radius)})



