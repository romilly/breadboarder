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

# Top-left socket of each feature, relative to the board; estimated from photos.
MINI_BB_ORIGIN = Point(0, 0)
GPIO_ORIGIN = MINI_BB_ORIGIN + Point((MINI_BB_COLUMNS - 1 + 4) * PITCH, 6 * PITCH)


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

    def _add_mini_breadboard(self) -> None:
        bottom_half_drop = (len(MINI_BB_TOP_ROWS) - 1) * PITCH + MINI_BB_CHANNEL
        for half, rows in enumerate([MINI_BB_TOP_ROWS, MINI_BB_BOTTOM_ROWS]):
            self.add(SocketGroup(MINI_BB_ORIGIN + Point(0, half * bottom_half_drop),
                                 len(rows), MINI_BB_COLUMNS, rows, self))

    def _add_gpio_header(self) -> None:
        for column, labels in enumerate([GPIO_LEFT, GPIO_RIGHT]):
            self.add(SocketGroup(GPIO_ORIGIN + Point(PITCH * column, 0),
                                 len(labels), 1, labels, self, start_number=-1))
