import abc

from breadboarder.helpers.color_codes import ColorCode
from .breadboard import Breadboard
from .project import Point, GroupedDrawable, Rectangle, Line, Circle, Text, horizontal_line, Drawable


# TODO: button needs a small offset
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

    def __init__(self, svg_id, body, ports):
        GroupedDrawable.__init__(self, svg_id=svg_id)
        self.body_width = 3 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        start, end = ports
        start = start.location()
        end = end.location()
        self.body = body
        self.add_elements(start, end)
        self.move_to(start)

    def add_elements(self, start, end):
        vector = end - start
        length = vector.r()
        offset = self.add_wire(length)
        self.add_bands(self.body)
        self.body.add_text(self.text())
        self.rotate(vector.theta(), start)
        self.add(self.body.move_to(offset))

    def add_wire(self, length):
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0, 0), length, color='grey', stroke_width=2, linecap='round'))
        return offset

    def add_bands(self, body):
        # default is to do nothing
        pass

    @abc.abstractmethod
    def text(self):
        pass


class Body(GroupedDrawable):
    def __init__(self, fill):
        GroupedDrawable.__init__(self)
        self.body_width = 3 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        self.rectangle = Rectangle(self.body_width, self.body_height, fill=fill)
        self.add(self.rectangle)
        self.band_positions = [5 + 5*i for i in range(3)]
        self.band_positions.append(self.body_width - 3)

    def add_text(self, text):
        self.add(Text(text, self.rectangle.center() + Point(0, 1.5),
             anchor='middle', color='grey', size=3))

    def add_band(self, color, index=-1):
        self.add(band(color, self.band_positions[index]))


def band(color, location):
        band_width = 2
        band_height = Breadboard.PITCH
        return Rectangle(band_width, band_height, fill=color, stroke=color).move_to(Point(location, 0))


class Diode(TwoPinComponent):
    def __init__(self, name, *ports):
        self.name = name
        TwoPinComponent.__init__(self, 'diode', Body('black'), ports)

    def add_bands(self,body):
        body.add_band('gray')

    def text(self):
        return self.name


class Resistor(TwoPinComponent):
    def __init__(self, resistance, tolerance, *ports):
        self.resistance = resistance
        self.coder = ColorCode()
        self.tolerance = tolerance
        TwoPinComponent.__init__(self, 'Resistor', Body('beige'), ports)


    def text(self):
        return ' '.join([self.resistance, self.tolerance])

    def add_bands(self,body):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        for (i, color) in enumerate(band_colors):
            body.add_band(color, i)
        body.add_band(self.coder.tolerance_band(self.tolerance), -1)


# class Crystal(TwoPinComponent):
#     def __init__(self, frequency, *ports):
#         self.frequency = frequency
#         self.body_width = 2 * Breadboard.PITCH
#         TwoPinComponent.__init__(self, 'Crystal', 'black', ports)
#
#     def build_body(self):
#         body = GroupedDrawable(svg_id='crystal body')
#         rectangle = Rectangle(self.body_width, self.body_height, fill='lightgray', stroke='gray', rx='4', ry='4')
#         body.add(rectangle)
#         return body, (rectangle.center())
#
#     def text(self):
#         return self.frequency

