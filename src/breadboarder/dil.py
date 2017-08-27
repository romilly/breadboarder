# draw Dual In Line IC chip (like ATMegas 328)
from xml.etree.ElementTree import Element

from breadboarder.breadboard import Breadboard
from breadboarder.drawing import CompositeItem, Point, Rectangle, GroupedDrawable, Text


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
            #             g.append(text(36, y + 4, labels[max_pin_index-i]))

    def extent(self):
        return Point(self.width(), self.height())

#     pins_per_side = int(pins/2)
#     max_pin_index = pins - 1
#     pins_wanted, labels_wanted = ((False, False), (True, False), (False, True), (True, True))[style]
#     g = Element("g", style='fill:none;stroke:black;stroke-width:2;font-size:3pt')
#     g.append(rect(0,-5,30,10 * pins_per_side,2))
#     g.append(dimple(15,-5,4,2))
#     if name:
#         cx = 15
#         cy = -5 + 5 * pins_per_side
#         g.append(rotate(-90, cx, cy, text(cx, cy, name, 'middle', 'lightgray')))
#     for i in range (0, pins_per_side):
#         y = -2 + 10*i
#         g.append(rect(-4, y, 4, 4, 1, fill='white'))
#         g.append(rect(30, y, 4, 4, 1, fill='white'))
#         if labels_wanted and pins_wanted:
#             g.append(text(-10, y + 4, labels[i],'end'))
#             g.append(text(36, y + 4, labels[max_pin_index-i]))
#         if pins_wanted:
#             g.append(text(2, y + 4, str(i+1)))
#             g.append(text(28, y + 4, str(pins-i),'end'))
#         if labels_wanted and not pins_wanted:
#             g.append(text(2, y + 4, labels[i]))
#             g.append(text(28, y + 4, labels[max_pin_index-i],'end'))
#     return g

# def dimple(cx, cy, radius, stroke_width=1):
#     return Element("path", {'d': 'M %d %d A %d %d 0 1 0 %d %d' % (cx-radius, cy, radius, radius, cx+radius, cy)})

labels = ('~RST','RXD','TXD','PD2','PD3','PD4','VCC','GND','XTAL1','XTAL2','PD5','PD6','PD7','PB0',
            'PB1','PB2','PB3','PB4','PB5','AVCC','AREF','GND','PC0','PC1','PC2','PC3','PC4','PC5')
