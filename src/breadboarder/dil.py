# draw Dual In Line IC chip (like ATMegas 328)
from xml.etree.ElementTree import Element

from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Point, Rectangle, GroupedDrawable, Text, Drawable


def atMega328():
    labels = ('~RST','RXD','TXD','PD2','PD3','PD4','VCC','GND','XTAL1','XTAL2','PD5','PD6','PD7','PB0',
            'PB1','PB2','PB3','PB4','PB5','AVCC','AREF','GND','PC0','PC1','PC2','PC3','PC4','PC5')
    return DIL(28,'ATmega328',labels)


class DIL(GroupedDrawable):
    def __init__(self, pins, name, labels):
        GroupedDrawable.__init__(self,svg_id='IC')
        self.pin1 = Point(0, 0)
        self.pins = pins
        self.name = name
        self.labels = labels
        self.flipped = False
        self.add_parts()

    def pins_per_side(self):
        return int(self.pins/2)

    def center(self):
        return self.start + self.extent().scale(0.5)

    def width(self):
        return 4 + Breadboard.PITCH * (self.pins_per_side()-1)

    def height(self):
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


class Dimple(Drawable):
    def __init__(self, center, radius):
        Drawable.__init__(self, center)
        self.radius = radius

    def svg(self):
        return Element("path", {'d': 'M %d %d A %d %d 0 1 1 %d %d' % (self.start.x, self.start.y-self.radius,
                                            self.radius, self.radius, self.start.x, self.start.y+self.radius)})

