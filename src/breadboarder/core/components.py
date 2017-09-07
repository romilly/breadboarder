import abc
from .project import Point, GroupedDrawable, Rectangle, Line, Circle, Text, horizontal_line
from .breadboard import Breadboard
from breadboarder.helpers.color_codes import ColorCode


class Button(GroupedDrawable):
    def __init__(self, *ports):
        GroupedDrawable.__init__(self, svg_id='Button')
        if len(ports) is not 1:
            raise Exception('buttons only need one position for insertion') # for now :)
        width = Breadboard.PITCH * 2
        height = Breadboard.PITCH * 3 - 6
        rectangle = Rectangle(width, height)
        self.add(rectangle)
        self.add(Circle(rectangle.center(), Breadboard.PITCH, fill='green'))
        self.move_to(ports[0].location())

    def width(self):
        return 4 + Breadboard.PITCH * 2

    def height(self):
        return Breadboard.PITCH * 2


class Wire(Line):
    def __init__(self, color, *ports):
        start, end = ports
        Line.__init__(self, start.location(), end.location(), color, stroke_width=3, linecap='round')


class TwoPinComponent(GroupedDrawable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, ports, svg_id):
        GroupedDrawable.__init__(self, svg_id=svg_id)
        start, end = ports
        start = start.location()
        end = end.location()
        self.add_elements(start, end)
        self.move_to(start)

    @abc.abstractmethod
    def add_elements(self, start, end):
        pass


class Resistor(TwoPinComponent):
    def __init__(self, resistance, tolerance, *ports):
        self.band_height = Breadboard.PITCH-1
        self.band_width = 2
        self.body_width = 3 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        self.resistance = resistance
        self.coder = ColorCode()
        self.tolerance = tolerance
        TwoPinComponent.__init__(self, ports, svg_id='Resistor')

    def add_elements(self, start, end):
        # coordinates are relative to the Resistor's start
        vector = end - start
        length = vector.r()
        offset = self.add_wire(length)
        body, rectangle = self.add_body()
        self.add_bands(body)
        body.add(Text(self.text(), rectangle.center() + Point(0, 1.5),
                      anchor='middle', color='grey', size=3))
        self.rotate(vector.theta(), start)
        self.add(body.move_to(offset))

    def text(self):
        return ' '.join([self.resistance, self.tolerance])

    def add_body(self):
        body = GroupedDrawable(svg_id='resistor body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='beige')
        body.add(rectangle)
        return body, rectangle

    def add_wire(self, length):
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0, 0), length, color='grey', stroke_width=2, linecap='round'))
        return offset

    def add_bands(self,body):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        for (i, band) in enumerate(band_colors):
            body.add(self.colored_band(5 + 5 * i, band))
        body.add(self.colored_band(self.body_width - 3, self.coder.tolerance_band(self.tolerance)))

    def colored_band(self, loc, tolerance_band_color):
        return Rectangle(self.band_width, self.band_height, fill=tolerance_band_color,
                         stroke=None).move_to(Point(loc, 0.5))


class Crystal(TwoPinComponent):
    def __init__(self, frequency, *ports):
        self.frequency = frequency
        self.body_width = 2 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        TwoPinComponent.__init__(self, ports, svg_id='Crystal')

    def add_elements(self, start, end):
        # coordinates are relative to the Crystal's's start
        extent = end - start
        length = extent.r()
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0,0), length, color='grey', stroke_width=2, linecap='round'))
        body = GroupedDrawable(svg_id='resistor body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='gray', stroke='lightgray', rx='4', ry='4')
        body.add(rectangle)
        body.add(Text(self.frequency, rectangle.center()+Point(0,1.5), anchor='middle', color='black', size=3))
        self.rotate(extent.theta(), start)
        self.add(body.move_to(offset))

