"""Raspberry Pi Pico boards with soldered headers, plugged into a breadboard.

A Pico straddles the centre channel, USB end to the left: pins 1-20 run left to
right along the row its pin 1 goes in, and pins 40-21 run left to right along
the row five letters on (c and h, say), seven rows apart as on the real board.

pico['GP15'] (or pico[20]) is the breadboard socket that pin sits in, so wires
connect to the Pico's pins by name.
"""
import re
from typing import List, Union

from breadboarder.core.port import Port
from breadboarder.core.project import Component
from breadboarder.core.units import PITCH
from svg.core import Circle, Rectangle, Text
from svg.point import Point

MM = 90 / 25.4
BOARD_LENGTH = 51 * MM
BOARD_WIDTH = 21 * MM
PINS_PER_SIDE = 20
BOARD_COLOR = '#1e7a3c'
SILK = 'white'

# Pin names from the Pico datasheets, pin 1 to pin 40. Pico, Pico W, Pico 2 and
# Pico 2 W share the pinout. The ground next to ADC_VREF is AGND; the others are
# GND, and pico['GND'] means pin 38, beside VSYS.
PIN_NAMES = ['GP0', 'GP1', 'GND', 'GP2', 'GP3', 'GP4', 'GP5', 'GND', 'GP6', 'GP7',
             'GP8', 'GP9', 'GND', 'GP10', 'GP11', 'GP12', 'GP13', 'GND', 'GP14', 'GP15',
             'GP16', 'GP17', 'GND', 'GP18', 'GP19', 'GP20', 'GP21', 'GND', 'GP22', 'RUN',
             'GP26', 'GP27', 'AGND', 'GP28', 'ADC_VREF', '3V3', '3V3_EN', 'GND', 'VSYS', 'VBUS']
DEFAULT_GND = 38
SOCKET_NAME = re.compile(r'([a-e])(\d+)')


class PicoPin:
    """A Pico pin, where it sits in a breadboard socket: wires connect to it like a socket."""

    def __init__(self, pico: 'Pico', number: int, socket: Port) -> None:
        self.pico = pico
        self.number = number
        self.socket = socket
        self.host = socket.host
        self.portname = socket.portname
        self.port_type = socket.port_type
        self.label = PIN_NAMES[number - 1]

    def location(self) -> Point:
        return self.socket.location()

    def describe_location(self) -> str:
        return '%s (%s %s)' % (self.socket.describe_location(), self.pico.id(), self.label)

    def description(self) -> str:
        return self.socket.description()


class Pico(Component):
    model = 'Pico'
    chip = 'RP2040'
    wireless = False

    def __init__(self, port: Port) -> None:
        Component.__init__(self, [port])
        self.sockets = self._find_sockets(port)
        self.span = (self.sockets[39].relative_location - self.sockets[0].relative_location).y
        self.add_parts()
        self.move_to(port.location())

    @staticmethod
    def _find_sockets(port: Port) -> List[Port]:
        """The sockets that pins 1 to 40 go in."""
        match = SOCKET_NAME.fullmatch(port.portname)
        if match is None:
            raise ValueError('Pin 1 of a Pico must go in a socket in rows a to e, not %s'
                             % port.portname)
        row, column = match.group(1), int(match.group(2))
        other_row = chr(ord(row) + 5)
        names = ([row + str(column + i) for i in range(PINS_PER_SIDE)] +
                 [other_row + str(column + PINS_PER_SIDE - 1 - i) for i in range(PINS_PER_SIDE)])
        try:
            return [port.host[name] for name in names]
        except KeyError:
            raise ValueError('A Pico needs 20 columns of sockets from %s' % port.portname)

    def __getitem__(self, pin: Union[int, str]) -> PicoPin:
        if isinstance(pin, int):
            number = pin
        elif pin == 'GND':
            number = DEFAULT_GND
        else:
            number = PIN_NAMES.index(pin) + 1
        return PicoPin(self, number, self.sockets[number - 1])

    def description(self) -> str:
        return 'Raspberry Pi %s' % self.model

    def full_description(self) -> str:
        return '%s: %s with soldered headers' % (self.id(), self.description())

    def id_prefix(self) -> str:
        return 'PICO'

    def part_type(self) -> str:
        return self.description()

    def instruction(self) -> str:
        return 'Insert the %s (%s), USB end to the left, with pin 1 (GP0) in %s' % (
            self.description(), self.id(), self.connected_ports[0].describe_location())

    # Drawing, with pin 1 at the origin and pin 40 at (0, span); span is negative
    # on a breadboard drawn with row j at the top.
    def add_parts(self) -> None:
        middle = self.span / 2
        overhang = (BOARD_LENGTH - (PINS_PER_SIDE - 1) * PITCH) / 2
        left = -overhang
        self.add(Rectangle(BOARD_LENGTH, BOARD_WIDTH, fill=BOARD_COLOR, stroke='#0f4d24',
                           rounded=True).move_to(Point(left, middle - BOARD_WIDTH / 2)))
        self._add_usb(left, middle)
        self._add_chips(middle)
        self._add_debug_pads(left + BOARD_LENGTH, middle)
        if self.wireless:
            self._add_wireless_module(left + BOARD_LENGTH, middle)
        else:
            self._add_name(Point((PINS_PER_SIDE - 1) * PITCH / 2 + 9 * MM, middle), SILK)
        self._add_pins()

    def _add_usb(self, left: float, middle: float) -> None:
        self.add(Rectangle(6 * MM, 8 * MM, fill='silver', stroke='grey')
                 .move_to(Point(left - 1.3 * MM, middle - 4 * MM)))
        self.add(Rectangle(3.5 * MM, 3.5 * MM, fill='white', stroke='grey', rounded=True)
                 .set_center(left + 10.5 * MM, middle + 2.5 * MM))  # BOOTSEL
        self.add(Rectangle(1.5 * MM, 1 * MM, fill='#9f9', stroke='none')
                 .set_center(left + 7 * MM, middle - 3 * MM))  # LED

    def _add_chips(self, middle: float) -> None:
        centre_x = (PINS_PER_SIDE - 1) * PITCH / 2
        chip = Rectangle(7 * MM, 7 * MM, fill='#222', stroke='#555').set_center(centre_x, middle)
        self.add(chip)
        self.add(Text(self.chip, Point(centre_x, middle + 1.5), color='lightgrey', size=4,
                      anchor='middle'))
        self.add(Rectangle(5 * MM, 6 * MM, fill='#222', stroke='#555')
                 .set_center(centre_x - 9 * MM, middle))  # flash

    def _add_name(self, centre: Point, color: str) -> None:
        self.add(Text('Raspberry Pi', centre + Point(0, -2), color=color,
                      size=4, anchor='middle', font_weight='bold'))
        self.add(Text(self.model, centre + Point(0, 4), color=color,
                      size=5, anchor='middle', font_weight='bold'))

    def _add_debug_pads(self, right: float, middle: float) -> None:
        x = right - (8 * MM if self.wireless else 1.6 * MM)
        for i in (-1, 0, 1):
            self.add(Circle(Point(0, 0), 2.5, fill='gold').move_center_to(Point(x, middle + i * PITCH)))
        self.add(Text('DEBUG', Point(x - 4, middle), color=SILK, size=2.5,
                      anchor='middle').rotate(-90))

    def _add_wireless_module(self, right: float, middle: float) -> None:
        self.add(Rectangle(10 * MM, 10 * MM, fill='#c8c8c8', stroke='grey')
                 .move_to(Point(right - 21 * MM, middle - 5 * MM)))
        self._add_name(Point(right - 16 * MM, middle), '#333')
        self.add(Rectangle(5 * MM, 18 * MM, fill='#14602e', stroke='none')
                 .move_to(Point(right - 5.5 * MM, middle - 9 * MM)))  # antenna keep-out
        self.add(Text('ANT', Point(right - 3 * MM, middle + 1), color=SILK, size=3,
                      anchor='middle'))

    def _add_pins(self) -> None:
        for i in range(PINS_PER_SIDE):
            x = i * PITCH
            for number, y, label_y in [(i + 1, 0, -4), (40 - i, self.span, self.span + 6)]:
                self.add(Circle(Point(0, 0), 2.6, fill='gold').move_center_to(Point(x, y)))
                self.add(Circle(Point(0, 0), 1.2, fill='#333').move_center_to(Point(x, y)))
                anchor = 'start' if y == 0 else 'end'
                self.add(Text(PIN_NAMES[number - 1], Point(x + 1, label_y), color=SILK, size=2.6,
                              anchor=anchor).rotate(-90))


class PicoW(Pico):
    model = 'Pico W'
    wireless = True


class Pico2(Pico):
    model = 'Pico 2'
    chip = 'RP2350'


class Pico2W(Pico):
    model = 'Pico 2 W'
    chip = 'RP2350'
    wireless = True
