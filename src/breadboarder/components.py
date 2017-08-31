from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Point, GroupedDrawable, Rectangle, Line, Circle

"""
def button(left, right, y, label):
    width = right - left
    swidth = 12
    radius = 2
    wlength = (width - swidth)/2
    sleft = left + wlength
    sright = sleft + swidth
    mid = (sleft + sright)/ 2
    twire = wire(sleft, y+4, sright, y+4)
    vwire = wire(mid, y, mid, y+4)
    lwire = wire(left, y+10, sleft, y+10)
    lcirc = circle(sleft+radius, y+10, radius, style='stroke:black;fill:none')
    rwire = wire(sright, y+10, right, y+10)
    rcirc = circle(sright-radius, y+10, radius, style='stroke:black;fill:none')
    txt = text(right+2, y+6, label)
    return group(twire, vwire, lwire, lcirc, rwire, rcirc, txt, style='font-size:4pt')
"""


class Component():
    def connect(self, positions):
        raise Exception('My Subclass should have implemented this method')


class Button(GroupedDrawable, Component):
    def __init__(self):
        GroupedDrawable.__init__(self, svg_id='Button')
        width = Breadboard.PITCH * 3
        height = Breadboard.PITCH * 3 - 6
        self.add(Rectangle(width, height))
        self.add(Circle(self.center(), Breadboard.PITCH, fill='green'))

    def connect(self, positions):
        if len(positions) is not 1:
            raise 'buttons only need one position for insertion' # for now :)
        self.move_to(positions[0])
        return self

    def width(self):
        return 4 + Breadboard.PITCH * 2

    def height(self):
        return Breadboard.PITCH * 2

    def extent(self):
        return Point(self.width(), self.height())

    def center(self):
        return self.start + self.extent().scale(0.5)


class Wire(Line, Component):
    def __init__(self, color='black'):
        Line.__init__(self, Point(0,0),Point(0,0), color, stroke_width=3)

    def connect(self, positions):
        start, end = positions
        self.move_to(start)
        self.set_end(end)
        return self

