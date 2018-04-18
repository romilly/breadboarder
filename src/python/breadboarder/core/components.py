from abc import ABCMeta, abstractmethod
import math

from breadboarder.core.project import Component
from breadboarder.helpers.color_codes import ColorCode
from breadboarder.svg.path import Path, arc
from breadboarder.svg.svg import Point, GroupedDrawable, Rectangle, Line, Circle, Text, PITCH, Dimple


class Button(Component):
    def id_prefix(self):
        return 'B'

    def part_type(self):
        return 'Button'

    def lab_instruction(self):
        return 'Insert the button with the top left pin in %s' %  self.connected_ports[0].describe_location()

    def __init__(self, port):
        Component.__init__(self, [port])
        width = PITCH * 2 + 3
        height = PITCH * 3 - 6
        rectangle = Rectangle(width, height)
        self.add(rectangle)
        self.add(Circle(rectangle.center()-Point(PITCH, PITCH), PITCH, fill='green'))
        self.move_to(port.location()  - Point(1.5, 1.5))

    def width(self):
        return 4 + PITCH * 2

    def height(self):
        return PITCH * 2


def title_case(color):
    return color[0].upper()+color[1:]


# TODO: using Path instead of Line
class Wire(Component):

    def lab_instruction(self):
        return 'Connect a %s from %s to %s' % (self.description(),
                                             self.connected_ports[0].describe_location(),
                                             self.connected_ports[1].describe_location())

    def __init__(self, color, *ports):
        Component.__init__(self, ports)
        start, end = ports
        self.color = color
        self.add(Line(start.location(), end.location(), color, 3, 'round'))

    def id_prefix(self):
        return 'JW'

    def part_type(self):
        return 'Jumper Wire'

    def description(self):
        return '%s %s' % (title_case(self.color), self.part_type())


# TODO: this is a mess; maybe some methods/properties belong in Body.
class TwoPinComponent(Component):
    def description(self):
        return '(%s)' % (self.text())

    __metaclass__ = ABCMeta

# TODO: remove svg_id
    def __init__(self, svg_id, body, ports):
        Component.__init__(self, ports)
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

    def text(self):
        return ''

    def full_description(self):
        return '%s %s: %s' % (self.part_type(), self.id(), self.description())

    def lab_instruction(self):
        return 'Connect a %s from %s to %s' % (
                self.full_description(),
                self.connected_ports[0].describe_location(),
                self.connected_ports[1].describe_location())


class Body(GroupedDrawable):
    __metaclass__ = ABCMeta

    def __init__(self):
        GroupedDrawable.__init__(self)

    @abstractmethod
    def center(self):
        pass

    @abstractmethod
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

    def add_bands(self, colors):
        for (color, index) in zip(colors, [0, 1, 2, -1]):
            self.add_band(color, index)

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
    def id_prefix(self):
        return 'D'

    def part_type(self):
        return 'Diode'

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

    def id_prefix(self):
        return 'R'

    def part_type(self):
        return 'Resistor'

    def text(self):
        return ' '.join([self.resistance, self.tolerance])

    def add_bands(self,body):
        bands = self.find_bands()
        body.add_bands(bands)

    def find_bands(self):
        band_colors = self.coder.bands_for(self.coder.parse(self.resistance))
        tolerance_band = self.coder.tolerance_band(self.tolerance)
        return band_colors+[tolerance_band]

    def description(self):
        return '%s (%s)' % (self.text(), ' '.join(map(title_case, self.find_bands())))


class Crystal(TwoPinComponent):
    def id_prefix(self):
        return 'X'

    def part_type(self):
        return 'Crystal'

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
    def id_prefix(self):
        return 'LED'

    def part_type(self):
        return 'LED'

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

    def id_prefix(self):
        return 'C'

    def part_type(self):
        return 'Capacitor'

    def text(self):
        return self.capacitance

# TODO: similar defs of extend, center. Move to Drawable, which would need width() and height()?

def atMega328(port):
    labels = ('~RST','RXD','TXD','PD2','PD3','PD4','VCC','GND','XTAL1','XTAL2','PD5','PD6','PD7','PB0',
            'PB1','PB2','PB3','PB4','PB5','AVCC','AREF','GND','PC0','PC1','PC2','PC3','PC4','PC5')
    return DIL(28,'ATmega328', port, labels)

def pcf8574(port):
    labels = ('A0', 'A1', 'A2', 'P0', 'P1', 'P2','P3','Vss','P4','P5','P6','P7','~INT','SCL','SDA','Vdd')
    return DIL(16,'PCF8574',port, labels)


class DIL(Component):

    def lab_instruction(self):
        return 'Insert pin 1 of the %s (%s) into %s' % (self.description(), self.id(),
                                                        self.connected_ports[0].describe_location())

    def description(self):
        return self.name

    def __init__(self, pins, name, port, labels):
        Component.__init__(self,[port])
        self.pins = pins
        self.name = name
        self.labels = labels
        self.add_parts()
        self.move_to(port.location() - Point(2, -1)) # for visual correctness

    def id_prefix(self):
        return 'IC'

    def part_type(self):
        return 'Integrated Circuit'

    def pins_per_side(self):
        return int(self.pins/2)

    def center(self):
        return self.extent().scale(0.5)

    def width(self):
        return 4 + PITCH * (self.pins_per_side()-1)

    def height(self):
        return 3 * (PITCH - 1) -2

    def add_parts(self):
        self.add(Rectangle(self.width(), self.height(), fill='grey', stroke='grey'))
        self.add(Text(self.name,(self.center()+ Point(0, 2)), color='lightgrey', anchor='middle',size=4))
        for i in range(0, self.pins_per_side()):
            x = PITCH*i
            self.add(Rectangle(4, 2,fill='white').move_to(Point(x,-2.5)))
            self.add(Rectangle(4, 2,fill='white').move_to(Point(x,self.height()+1)))
            self.add(Text(self.labels[i], Point(x+3,self.height()-1),size=2, anchor='start').rotate(-90))
            self.add(Text(self.labels[self.pins-(i+1)], Point(x+3, 1),size=2,anchor='end').rotate(-90))
            self.add(Dimple(Point(0, self.center().y), 2))

    def extent(self):
        return Point(self.width(), self.height())

