from breadboarder.core.port import SocketGroup
from breadboarder.core.host import Host
from breadboarder.core.units import PITCH
from svg.svg import Rectangle, Text
from svg.transform import Point


class FtdiFriend(Host):
    def description(self):
        return 'FTDI Friend UART'

    def __init__(self):
        self.width = 90 * 3.0
        self.height = 90 * 0.675
        self.usb_width = 90 * 0.75
        self.usb_height = 90 * 0.483
        self.chip_width = 90 * 0.3
        self.chip_height = 90 * 0.15
        self.chip_offset = 80
        self.pin_width = 25
        self.pin_height = 2
        self.board_width = 90 * 1.60
        self.board_offset = 20
        self.labels = ['CTS', 'RTS', 'RXD', 'TXD', 'GND', 'VCC']
        Host.__init__(self)

    def id_prefix(self):
        return 'FTDI-'

    def part_type(self):
        return 'FTDI Friend'

    def add_components(self):
        self.add(Rectangle(self.board_width, self.height, fill='blue')
                 .move_to(Point(self.board_offset, 0)))
        self.add(Rectangle(self.usb_width, self.usb_height, fill='silver', stroke='silver')
                 .move_to(Point(-0.5 * self.usb_width, 0.5 * (self.height - self.usb_height))))
        self.add(Rectangle(self.chip_width, self.chip_height, fill='black')
                 .move_by(Point(self.chip_offset, 0.5 * (self.height - self.chip_height))))
        self.add(Text('FT232', Point(self.usb_width * 0.5 + 10, 10), color='white', anchor='middle').rotate(-90).move_by(Point(10, 20)))
        for pin_index, label in enumerate(self.labels):
            self.add(Text(label, Point(self.board_offset + self.board_width - 10, 6 + PITCH * pin_index),
                          color='white', size=4).rotate(180).move_by(Point(0, -2)))
            self.add(Rectangle(self.pin_width, self.pin_height, fill='gold', stroke='none')
                     .move_to(Point(self.board_offset + self.board_width - 6, 4 + PITCH * pin_index)))
        self.add(SocketGroup(Point(self.board_offset + self.board_width - 6 + self.pin_width, 5),
                             6, 1, self.labels, self, start_number=-1, fill='none', port_type='pin'))
