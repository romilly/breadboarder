from breadboarder.core.port import SocketGroup
from breadboarder.core.host import Host
from breadboarder.svg.svg import Rectangle, Text, PITCH
from breadboarder.transformations.transform import Point


class CP2102(Host):
    def description(self):
        return 'CP2102 UART'

    def __init__(self):
        Host.__init__(self, svg_id='CP2102')

    def id_prefix(self):
        return 'CP2102'

    def part_type(self):
        return 'CP2102'

    def add_components(self):
        self.width = 90 * 2.135
        self.height = 90 * 0.675
        self.usb_width = 90 * 0.741
        self.usb_height = 90 * 0.483
        self.pin_width = 25
        self.pin_height = 2
        self.board_width = 90 * 1.30
        self.board_offset = 20
        self.labels = ['DTR', 'RXD', 'TXD', '5V', 'CTS', 'GND']
        self.add(Rectangle(self.board_width, self.height, fill='black')
                 .move_to(Point(self.board_offset, 0)))
        self.add(Rectangle(self.usb_width, self.usb_height, fill='silver', stroke='silver')
                 .move_to(Point(0, 0.5 * (self.height - self.usb_height))))
        self.add(Text('CP2102', Point(self.usb_width + 5, 10), color='white'))
        for pin_index, label in enumerate(self.labels):
            self.add(Text(label, Point(self.board_offset + self.board_width - 10, 6 + PITCH * pin_index),
                          color='white', size=3, anchor='end'))
            self.add(Rectangle(self.pin_width, self.pin_height, fill='gold', stroke='none')
                     .move_to(Point(self.board_offset + self.board_width - 6, 4 + PITCH * pin_index)))
        self.add(SocketGroup(Point(self.board_offset + self.board_width - 6 + self.pin_width, 5),
                             6, 1, self.labels, self, start_number=-1, fill='none'))
