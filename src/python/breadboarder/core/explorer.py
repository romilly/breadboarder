from breadboarder.core.host import Host
from breadboarder.core.port import SocketGroup
from breadboarder.core.units import PITCH
from svg.point import Point

GPIO_LEFT = ['GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5']
GPIO_RIGHT = ['ADC0', 'ADC1', 'ADC2', '3V3', 'GND1', 'GND2']
MINI_BB_TOP_ROWS = 'jihgf'
MINI_BB_BOTTOM_ROWS = 'edcba'
MINI_BB_COLUMNS = 17
MINI_BB_CHANNEL = 3 * PITCH  # from row f down to row e, across the centre channel
RIGHT_PADS = ['PAD_3V3', 'PAD_ADC3', 'PAD_GND', 'PAD_ADC4', 'PAD_ADC5']  # top to bottom
RIGHT_PAD_SPACING = 3.5 * PITCH

# Top-left socket of each feature, relative to the board; estimated from photos.
MINI_BB_ORIGIN = Point(0, 0)
GPIO_ORIGIN = MINI_BB_ORIGIN + Point((MINI_BB_COLUMNS - 1 + 4) * PITCH, 6 * PITCH)
RIGHT_PADS_ORIGIN = MINI_BB_ORIGIN + Point(24 * PITCH, -4.5 * PITCH)
LEFT_PAD_CENTER = MINI_BB_ORIGIN + Point(-4 * PITCH, 3.5 * PITCH)


class Explorer(Host):
    def description(self) -> str:
        return 'Pimoroni Explorer (RP2350)'

    def id_prefix(self) -> str:
        return 'EXP-'

    def part_type(self) -> str:
        return 'Pimoroni Explorer'

    def add_components(self) -> None:
        self._add_mini_breadboard()
        self._add_gpio_header()
        self._add_croc_clip_pads()

    def _add_mini_breadboard(self) -> None:
        bottom_half_drop = (len(MINI_BB_TOP_ROWS) - 1) * PITCH + MINI_BB_CHANNEL
        for half, rows in enumerate([MINI_BB_TOP_ROWS, MINI_BB_BOTTOM_ROWS]):
            self.add(SocketGroup(MINI_BB_ORIGIN + Point(0, half * bottom_half_drop),
                                 len(rows), MINI_BB_COLUMNS, rows, self))

    def _add_gpio_header(self) -> None:
        for column, labels in enumerate([GPIO_LEFT, GPIO_RIGHT]):
            self.add(SocketGroup(GPIO_ORIGIN + Point(PITCH * column, 0),
                                 len(labels), 1, labels, self, start_number=-1))

    def _add_croc_clip_pads(self) -> None:
        for index, name in enumerate(RIGHT_PADS):
            self._add_pad(name, RIGHT_PADS_ORIGIN + Point(0, index * RIGHT_PAD_SPACING))
        self._add_pad('PAD_GND_L', LEFT_PAD_CENTER)

    def _add_pad(self, name: str, center: Point) -> None:
        self.add(SocketGroup(center, 1, 1, [name], self, start_number=-1))
