from breadboarder.core.host import Host
from breadboarder.core.port import SocketGroup
from breadboarder.core.units import PITCH
from svg.point import Point

GPIO_LEFT = ['GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5']
GPIO_RIGHT = ['ADC0', 'ADC1', 'ADC2', '3V3', 'GND1', 'GND2']


class Explorer(Host):
    def description(self) -> str:
        return 'Pimoroni Explorer (RP2350)'

    def id_prefix(self) -> str:
        return 'EXP-'

    def part_type(self) -> str:
        return 'Pimoroni Explorer'

    def add_components(self) -> None:
        gpio_origin = Point(0, 0)
        for column, labels in enumerate([GPIO_LEFT, GPIO_RIGHT]):
            self.add(SocketGroup(gpio_origin + Point(PITCH * column, 0),
                                 len(labels), 1, labels, self, start_number=-1))
