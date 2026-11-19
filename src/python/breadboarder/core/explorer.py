from typing import List, Optional, Tuple
from xml.etree.ElementTree import Element, SubElement

from breadboarder.core.host import Host
from breadboarder.core.port import Port, SocketGroup
from breadboarder.core.units import PITCH
from svg.core import Circle, Drawable, Rectangle, Text
from svg.path import Path, arc, vector
from svg.point import Point

# All positions are in SVG units (90 per inch) from the board's top-left corner,
# measured from photos of a real board using the breadboard pitch as a ruler.
BOARD_WIDTH = 283.5   # about 80mm
BOARD_HEIGHT = 354.0  # about 100mm
BOARD_COLOR = '#1f3a7a'
LABEL_COLOR = 'white'
# The printed artwork: a sky running from deep blue through sunset to navy, by height
SKY_GRADIENT_ID = 'explorer-sky'
SKY_STOPS = [(0.0, '#1d3f8f'), (0.30, '#34509c'), (0.42, '#e0686a'), (0.52, '#f6c453'),
             (0.60, '#f09a4a'), (0.68, '#2c3778'), (1.0, '#1d2a66')]
# Mountain outlines as (x, y) points across the board, back range then front range
BACK_MOUNTAINS = [(0, 228), (40, 214), (75, 222), (110, 200), (140, 214), (175, 196),
                  (201, 179), (225, 200), (255, 190), (283.5, 205), (283.5, 240), (0, 240)]
FRONT_MOUNTAINS = [(0, 232), (30, 224), (60, 229), (95, 214), (125, 226), (165, 218),
                   (200, 226), (235, 214), (283.5, 222), (283.5, 240), (0, 240)]
GRILLE_CENTER = Point(145, 196)
GRILLE_SLOT_HEIGHT = 18.0
# (distance from centre, arc radius) for each slot pair: curved inside, flatter outside
GRILLE_SLOTS = [(9.0, 10.0), (20.0, 16.0), (31.0, 30.0)]

GPIO_LEFT = ['GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5']
GPIO_RIGHT = ['ADC0', 'ADC1', 'ADC2', '3V3', 'GND1', 'GND2']
GPIO_RIGHT_PRINTED = ['ADC0', 'ADC1', 'ADC2', '3V3', 'GND', 'GND']
MINI_BB_TOP_ROWS = 'jihgf'
MINI_BB_BOTTOM_ROWS = 'edcba'
MINI_BB_COLUMNS = 17
MINI_BB_CHANNEL = 3 * PITCH  # from row f down to row e, across the centre channel
RIGHT_PADS = ['PAD_3V3', 'PAD_ADC3', 'PAD_GND', 'PAD_ADC4', 'PAD_ADC5']  # top to bottom
RIGHT_PADS_PRINTED = ['3.3V', 'ADC3', 'GND', 'ADC4', 'ADC5']
RIGHT_PAD_SPACING = 3.5 * PITCH
PAD_RADIUS = 9.0

# Socket j1, the top-left socket of the mini breadboard
MINI_BB_ORIGIN = Point(6 * PITCH, 26 * PITCH)
GPIO_ORIGIN = MINI_BB_ORIGIN + Point((MINI_BB_COLUMNS - 1 + 4) * PITCH, 5 * PITCH)
RIGHT_PADS_ORIGIN = MINI_BB_ORIGIN + Point(24 * PITCH, -4.5 * PITCH)
LEFT_PAD_CENTER = MINI_BB_ORIGIN + Point(-4 * PITCH, 3.5 * PITCH)

LCD_TOP_LEFT = Point(31, 21)
LCD_SIZE = Point(221, 160)
SERVO_ORIGIN = Point(220, 230)  # servo 1 SIG pin
SERVO_ROWS = 4
LEFT_BUTTONS = [('A', 54.5), ('B', 101), ('C', 150.5)]   # label, centre y
RIGHT_BUTTONS = [('X', 51), ('Y', 95), ('Z', 142)]
BUTTON_SIZE = 18


class _LinearGradient(Drawable):
    """A vertical SVG gradient, referenced by fill='url(#id)'."""

    def __init__(self, gradient_id: str, stops: List[Tuple[float, str]]) -> None:
        self.gradient_id = gradient_id
        self.stops = stops

    def element(self) -> Element:
        defs = Element('defs')
        gradient = SubElement(defs, 'linearGradient', id=self.gradient_id,
                              x1='0', y1='0', x2='0', y2='1')
        for offset, color in self.stops:
            SubElement(gradient, 'stop', {'offset': str(offset), 'stop-color': color})
        return defs


def _outline(points: List[Tuple[float, float]], fill: str) -> Path:
    start = Point(*points[0])
    steps = [vector(x - px, y - py) for (px, py), (x, y) in zip(points, points[1:])]
    return Path(start, True, *steps, fill=fill, stroke='none')


class Explorer(Host):
    def description(self) -> str:
        return 'Pimoroni Explorer (RP2350)'

    def id_prefix(self) -> str:
        return 'EXP-'

    def part_type(self) -> str:
        return 'Pimoroni Explorer'

    def add_components(self) -> None:
        self._add_board()
        self._add_screen()
        self._add_buttons()
        self._add_connectors()
        self._add_servo_header()
        self._add_mini_breadboard()
        self._add_gpio_header()
        self._add_croc_clip_pads()

    def _add_board(self) -> None:
        self.add(_LinearGradient(SKY_GRADIENT_ID, SKY_STOPS))
        self.add(Rectangle(BOARD_WIDTH, BOARD_HEIGHT, stroke=BOARD_COLOR, rounded=True,
                           fill='url(#%s)' % SKY_GRADIENT_ID))
        self.add(_outline(BACK_MOUNTAINS, '#7a4a8a'))
        self.add(_outline(FRONT_MOUNTAINS, '#b8504f'))
        self.add(Text('Explorer', Point(31, 16), color=LABEL_COLOR, size=10, font_weight='bold'))
        self.add(Text('by PIMORONI', Point(252, 16), color=LABEL_COLOR, size=7.5,
                      anchor='end', font_weight='bold'))
        # lanyard slot, cut through the board
        self.add(Rectangle(53, 11, stroke='#ccc', fill='white', rounded=True)
                 .move_to(Point(112, 7)))

    def _add_screen(self) -> None:
        self.add(Rectangle(LCD_SIZE.x, LCD_SIZE.y, stroke='grey', fill='black')
                 .move_to(LCD_TOP_LEFT))
        self.add(Text('SCREEN', LCD_TOP_LEFT + Point(10, LCD_SIZE.y + 8),
                      color=LABEL_COLOR, size=4))
        self._add_speaker_grille()

    def _add_speaker_grille(self) -> None:
        # curved slots, ((( ))), all the same height
        for offset, radius in GRILLE_SLOTS:
            for side, sweep in [(-1, 0), (1, 1)]:  # '(' bulges left, ')' bulges right
                start = GRILLE_CENTER + Point(side * offset, -GRILLE_SLOT_HEIGHT / 2)
                self.add(Path(start, False, arc(radius, radius, 0, 0, sweep, 0, GRILLE_SLOT_HEIGHT),
                              fill='none', stroke='#222', **{'stroke-width': '3',
                                                             'stroke-linecap': 'round'}))

    def _add_buttons(self) -> None:
        for buttons, x in [(LEFT_BUTTONS, 10), (RIGHT_BUTTONS, 273.5)]:
            for label, y in buttons:
                self.add(Rectangle(BUTTON_SIZE, BUTTON_SIZE, stroke='grey', fill='#333')
                         .set_center(x, y))
                self.add(Text(label, Point(x, y + BUTTON_SIZE), color=LABEL_COLOR,
                              size=7, anchor='middle', font_weight='bold'))

    def _add_connectors(self) -> None:
        for top_left in [Point(8, 192), Point(8, 233)]:  # Qw/ST
            self.add(Rectangle(20, 22, stroke='grey', fill='white').move_to(top_left))
        self.add(Text('QW/ST I2C', Point(4, 229), color=LABEL_COLOR, size=3))
        self.add(Rectangle(26, 22, stroke='grey', fill='silver').move_to(Point(0, 304)))
        self.add(Text('USB-C', Point(14, 337), color=LABEL_COLOR, size=4, anchor='middle'))

    def _add_servo_header(self) -> None:
        self.add(Text('SERVOS', SERVO_ORIGIN + Point(PITCH, -12), color=LABEL_COLOR,
                      size=4, anchor='middle'))
        for column, label in enumerate(['SIG', '5V', 'GND']):
            self.add(Text(label, SERVO_ORIGIN + Point(column * PITCH, -5), color=LABEL_COLOR,
                          size=2, anchor='middle'))
        for row in range(SERVO_ROWS):
            self.add(Text(str(row + 1), SERVO_ORIGIN + Point(-6, row * PITCH + 1.5),
                          color=LABEL_COLOR, size=3, anchor='end'))
            for column in range(3):
                self.add(Rectangle(3, 3, stroke='gold', fill='gold')
                         .set_center(SERVO_ORIGIN.x + column * PITCH, SERVO_ORIGIN.y + row * PITCH))

    def _add_mini_breadboard(self) -> None:
        bottom_half_drop = (len(MINI_BB_TOP_ROWS) - 1) * PITCH + MINI_BB_CHANNEL
        width = (MINI_BB_COLUMNS - 1) * PITCH + 10
        height = bottom_half_drop + (len(MINI_BB_BOTTOM_ROWS) - 1) * PITCH + 14
        self.add(Rectangle(width, height, stroke='black', fill='#3a3a3a')
                 .move_to(MINI_BB_ORIGIN - Point(5, 7)))
        self.add(Rectangle(width - 30, 3, stroke='black', fill='black')
                 .move_to(MINI_BB_ORIGIN + Point(10, bottom_half_drop - 0.5 * MINI_BB_CHANNEL - 1.5)))
        for half, rows in enumerate([MINI_BB_TOP_ROWS, MINI_BB_BOTTOM_ROWS]):
            self.add(SocketGroup(MINI_BB_ORIGIN + Point(0, half * bottom_half_drop),
                                 len(rows), MINI_BB_COLUMNS, rows, self))

    def _add_gpio_header(self) -> None:
        self.add(Rectangle(2 * PITCH + 2, len(GPIO_LEFT) * PITCH + 2, stroke='black', fill='#3a3a3a')
                 .move_to(GPIO_ORIGIN - Point(5.5, 5.5)))
        self.add(Text('GPIO', GPIO_ORIGIN + Point(0.5 * PITCH, -9), color=LABEL_COLOR,
                      size=5, anchor='middle'))
        for column, (labels, printed, anchor, dx) in enumerate([
                (GPIO_LEFT, GPIO_LEFT, 'end', -7),
                (GPIO_RIGHT, GPIO_RIGHT_PRINTED, 'start', 7)]):
            origin = GPIO_ORIGIN + Point(PITCH * column, 0)
            for row, text in enumerate(printed):
                self.add(Text(text, origin + Point(dx, row * PITCH + 1.5), color=LABEL_COLOR,
                              size=3.5, anchor=anchor))
            self.add(SocketGroup(origin, len(labels), 1, labels, self, start_number=-1))

    def _add_croc_clip_pads(self) -> None:
        for index, (name, printed) in enumerate(zip(RIGHT_PADS, RIGHT_PADS_PRINTED)):
            self._add_pad(name, printed, RIGHT_PADS_ORIGIN + Point(0, index * RIGHT_PAD_SPACING),
                          edge_x=BOARD_WIDTH)
        self._add_pad('PAD_GND_L', 'GND', LEFT_PAD_CENTER, edge_x=0, label='GND (left)')

    def _add_pad(self, name: str, printed: str, center: Point, edge_x: float,
                 label: Optional[str] = None) -> None:
        """label names the pad in instructions; it defaults to the printed text."""
        # copper runs the full height of the ring out to the nearest board edge
        left = min(center.x, edge_x)
        self.add(Rectangle(abs(edge_x - center.x), 2 * PAD_RADIUS, stroke='gold', stroke_width=0,
                           fill='gold').move_to(Point(left, center.y - PAD_RADIUS)))
        self.add(Circle(Point(0, 0), PAD_RADIUS, fill='gold').move_center_to(center))
        self.add(Circle(Point(0, 0), PAD_RADIUS / 2, fill='#222').move_center_to(center))
        self.add(Text(printed, center + Point(0, PAD_RADIUS + 6), color=LABEL_COLOR,
                      size=4, anchor='middle', font_weight='bold'))
        self.add_port(Port(self, center, name, port_type='pad',
                           label=printed if label is None else label))
