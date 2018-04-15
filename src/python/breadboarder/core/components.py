import abc
import math

from breadboarder.helpers.color_codes import ColorCode
from breadboarder.svg.path import Path, arc
from breadboarder.svg.svg import Point, GroupedDrawable, Rectangle, Line, Circle, Text, PITCH


class Button(GroupedDrawable):
    def __init__(self, *ports):
        GroupedDrawable.__init__(self, svg_id='Button')
        if len(ports) is not 1:
            raise Exception('buttons only need one position for insertion') # for now :)
        width = PITCH * 2 + 3
        height = PITCH * 3 - 6
        rectangle = Rectangle(width, height)
        self.add(rectangle)
        self.add(Circle(rectangle.center()-Point(PITCH, PITCH), PITCH, fill='green'))
        self.move_to(ports[0].location()  - Point(1.5, 1.5))

    def width(self):
        return 4 + PITCH * 2

    def height(self):
        return PITCH * 2


# TODO: Change to composition (using Path) rather than scummy inheritance
class Wire(Line):
    def __init__(self, color, *ports):
        start, end = ports
        Line.__init__(self, start.location(), end.location(), color, stroke_width=3, linecap='round')


# TODO: this is a mess; maybe some methods/properties belong in Body.
class TwoPinComponent(GroupedDrawable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, svg_id, body, ports):
        GroupedDrawable.__init__(self, svg_id=svg_id)
        self.leg_gap = PITCH
        length, start, vector = self.dimensions(ports)
        # Offset is where the midpoint of the body should be
        offset = Point(length - body.width, -body.height).scale(0.5)
        self.add_wires(length, body.connection_point() + offset)
        self.add_bands(body)
        body.add_text(self.text())
        if vector.theta() != 0:
            self.rotate(vector.theta(), start)
        self.add(body.move_to(offset))
        self.move_to(start)

    def dimensions(self, ports):
        p1, p2 = ports
        start = p1.location()
        end = p2.location()
        vector = end - start
        length = vector.r()
        return length, start, vector

    def add_wires(self, length, center):
        self.add(Line(Point(0, 0), center, color='grey', stroke_width=2, linecap='round'))
        self.add(Line(Point(length, 0), center, color='grey', stroke_width=2, linecap='round'))

    # TODO: remove this smell
    def add_bands(self, body):
        # default is to do nothing
        pass

    @abc.abstractmethod
    def text(self):
        pass


class Body(GroupedDrawable):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        GroupedDrawable.__init__(self)

    @abc.abstractmethod
    def center(self):
        pass

    @abc.abstractmethod
    def connection_point(self):
        pass

    def add_text(self, text):
        self.add(Text(text, self.center() + Point(0, 1.5),
             anchor='middle', color='grey', size=3))


class RectangularBody(Body):
    def __init__(self, fill, rounded=False):
        Body.__init__(self)
        self.width = 3 * PITCH
        self.height = PITCH
        self.rectangle = Rectangle(self.width, self.height, fill=fill, rounded=rounded)
        self.add(self.rectangle)
        self.band_positions = [5 + 5*i for i in range(3)]
        self.band_positions.append(self.width - 3)

    def add_band(self, color, index=-1):
        self.add(band(color, self.band_positions[index]))

    def center(self):
        return self.rectangle.center()

    def connection_point(self):
        return self.center()


def band(color, location):
        band_width = 2
        band_height = PITCH -2
        return Rectangle(band_width, band_height, fill=color, stroke=color).move_to(Point(location, 1))


class Diode(TwoPinComponent):
    def __init__(self, name, *ports):
        self.name = name
        TwoPinComponent.__init__(self, 'diode', RectangularBody('black'), ports)

    def add_bands(self,body):
        body.add_band('gray')

    def text(self):
        return self.name


class Resistor(TwoPinComponent):
    def __init__(self, resistance, tolerance, *ports):
        self.resistance = resistance
        self.coder = ColorCode()
        self.tolerance = tolerance
        TwoPinComponent.__init__(self, 'Resistor', RectangularBody('beige'), ports)

    def text(self):
        return ' '.join([self.resistance, self.tolerance])

    def add_bands(self,body):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        for (i, color) in enumerate(band_colors):
            body.add_band(color, i)
        body.add_band(self.coder.tolerance_band(self.tolerance), -1)


class Crystal(TwoPinComponent):
    def __init__(self, frequency, *ports):
        self.frequency = frequency
        TwoPinComponent.__init__(self, 'Crystal', RectangularBody('lightgray', rounded=True), ports)

    def text(self):
        return self.frequency


class LedBody(Body):
    def __init__(self, color):
        Body.__init__(self)
        self.radius = 0.5*PITCH
        f = 1.35 # radius of perimiter/inner radius
        pr = self.radius * f  # perimeter radius
        py = math.sqrt(f*f - 1)*self.radius
        self.width = 2*self.radius
        self.height = 2*self.radius
        self.circle = Circle(Point(0, 0), self.radius, fill=color)
        perimeter = Path(Point(2*self.radius,  self.radius-py),
                         arc(pr, pr, 0, 1, 0, 0, 2*py), fill=color, opacity='0.6')
        self.add(perimeter)
        self.add(self.circle)

    def center(self):
         return self.circle.center()

    def connection_point(self):
        return self.center()


class LED(TwoPinComponent):
    def __init__(self, color, *ports):
        TwoPinComponent.__init__(self, 'LED', LedBody(color=color), ports)


class CapacitorBody(Body):
    def __init__(self, color):
        Body.__init__(self)
        self.radius = PITCH
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.circle = Circle(Point(0,0), self.radius, fill=color)
        self.add(self.circle)
        self.body_offset = Point(0, -2 * self.radius)
        self.move_to(self.body_offset)

    def center(self):
        return self.circle.center()

    def connection_point(self):
        return self.center() + self.body_offset



class DiskCapacitor(TwoPinComponent):
    def __init__(self, capacitance, *ports):
        self.capacitance = capacitance
        TwoPinComponent.__init__(self, 'Capacitor', CapacitorBody(color='goldenrod'), ports)

    def text(self):
        return self.capacitance