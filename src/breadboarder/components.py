from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Point, GroupedDrawable, Rectangle, Line, Circle, Text, horizontal_line
from breadboarder.helpers.color_codes import ColorCode

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
        width = Breadboard.PITCH * 2
        height = Breadboard.PITCH * 3 - 6
        rectangle = Rectangle(width, height)
        self.add(rectangle)
        self.add(Circle(rectangle.center(), Breadboard.PITCH, fill='green'))

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
        Line.__init__(self, Point(0,0),Point(0,0), color, stroke_width=3, linecap='round')

    def connect(self, positions):
        start, end = positions
        self.move_to(start)
        self.set_end(end)
        return self


class Crystal(GroupedDrawable, Component):
    def __init__(self, frequency):
        GroupedDrawable.__init__(self, svg_id='Crystal')
        self.frequency = frequency
        self.end = Point(0,0)
        self.body_width = 2 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH

    def connect(self, positions):
        start, end = positions
        self.move_to(start)
        self.set_end(end)
        self.add_elements()
        return self

    def set_end(self, end):
        self.end = end

    def add_elements(self):
        # coordinates are relative to the Crystal's's start
        extent = self.end - self.start
        length = extent.r()
        theta = extent.theta()
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0,0), length, color='grey', stroke_width=2, linecap='round'))
        body = GroupedDrawable(svg_id='resistor body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='gray', stroke='lightgray', rx='4', ry='4')
        body.add(rectangle)
        body.add(Text(self.frequency, rectangle.center()+Point(0,1.5), anchor='middle', color='black', size=3))
        self.rotate(theta, self.start)
        self.add(body.move_to(offset))


class Resistor(GroupedDrawable, Component):
    def __init__(self, resistance):
        GroupedDrawable.__init__(self, svg_id='Resistor')
        self.band_height = Breadboard.PITCH-1
        self.band_width = 2
        self.body_width = 3 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        self.resistance = resistance
        self.end = Point(0,0)
        self.coder = ColorCode()

    def connect(self, positions):
        start, end = positions
        self.move_to(start)
        self.set_end(end)
        self.add_elements()
        return self

    def set_end(self, end):
        self.end = end

    def add_elements(self):
        # coordinates are relative to the Resistor's start
        extent = self.end - self.start
        length = extent.r()
        theta = extent.theta()
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0,0), length, color='grey', stroke_width=2, linecap='round'))
        body = GroupedDrawable(svg_id='resistor body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='beige')
        body.add(rectangle)
        self.add_bands(body)
        body.add(Text(self.resistance, rectangle.center()+Point(0,1.5), anchor='middle', color='grey', size=3))
        self.rotate(theta, self.start)
        self.add(body.move_to(offset))

    def add_bands(self,body):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        for (i, band) in enumerate(band_colors):
            body.add(Rectangle(self.band_width, self.band_height, fill=band, stroke=None).move_to(Point(5 + 5*i,0.5)))
