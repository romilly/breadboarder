import abc
from .project import Point, GroupedDrawable, Rectangle, Line, Circle, Text, horizontal_line
from .breadboard import Breadboard
from breadboarder.helpers.color_codes import ColorCode

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

    def __init__(self, svg_id, ports):
        GroupedDrawable.__init__(self, svg_id=svg_id)
        self.body_width = 3 * Breadboard.PITCH
        self.body_height = Breadboard.PITCH
        start, end = ports
        start = start.location()
        end = end.location()
        self.add_elements(start, end)
        self.move_to(start)

    def add_elements(self, start, end):
        vector = end - start
        length = vector.r()
        offset = self.add_wire(length)
        body, center = self.build()
        body.add(Text(self.text(), center + Point(0, 1.5),
                      anchor='middle', color='grey', size=3))
        self.rotate(vector.theta(), start)
        self.add(body.move_to(offset))

    def add_wire(self, length):
        total_wire_length = length - self.body_width
        offset = Point(total_wire_length, -self.body_height).scale(0.5)
        self.add(horizontal_line(Point(0, 0), length, color='grey', stroke_width=2, linecap='round'))
        return offset

    @abc.abstractmethod
    def build(self):
        return (None, None)

    @abc.abstractmethod
    def text(self):
        pass


class BandedTwoPinComponent(TwoPinComponent):
    __metaclass__ = abc.ABCMeta

    def __init__(self, svg_id, ports):
        self.band_width = 2
        self.band_height = Breadboard.PITCH-1
        TwoPinComponent.__init__(self, svg_id, ports)

    def colored_band(self, loc, color):
            return Rectangle(self.band_width, self.band_height, fill=color,
                             stroke=None).move_to(Point(loc, 0.5))


class Diode(BandedTwoPinComponent):
    def __init__(self, model, *ports):
        self.model = model
        BandedTwoPinComponent.__init__(self, 'diode', ports)


    def build(self):
        body = GroupedDrawable(svg_id='diode body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='black')
        body.add(rectangle)
        self.add_bands(body)
        return body, (rectangle.center())

    def add_bands(self,body):
        body.add(self.colored_band(2, 'gray'))


    def text(self):
        return self.model


class Resistor(BandedTwoPinComponent):
    def __init__(self, resistance, tolerance, *ports):
        self.resistance = resistance
        self.coder = ColorCode()
        self.tolerance = tolerance
        BandedTwoPinComponent.__init__(self, 'Resistor', ports)

    def build(self):
        body = GroupedDrawable(svg_id='resistor body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='beige')
        body.add(rectangle)
        self.add_bands(body)
        return body, (rectangle.center())

    def text(self):
        return ' '.join([self.resistance, self.tolerance])

    def add_bands(self,body):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        for (i, band) in enumerate(band_colors):
            body.add(self.colored_band(5 + 5 * i, band))
        body.add(self.colored_band(self.body_width - 3, self.coder.tolerance_band(self.tolerance)))


class Crystal(TwoPinComponent):
    def __init__(self, frequency, *ports):
        self.frequency = frequency
        self.body_width = 2 * Breadboard.PITCH
        TwoPinComponent.__init__(self, 'Crystal', ports)

    def build(self):
        body = GroupedDrawable(svg_id='crystal body')
        rectangle = Rectangle(self.body_width, self.body_height, fill='lightgray', stroke='gray', rx='4', ry='4')
        body.add(rectangle)
        return body, (rectangle.center())

    def text(self):
        return self.frequency

