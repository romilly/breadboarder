from breadboarder.core.breadboard import SocketGroup, Breadboard
from breadboarder.svg.svg import GroupedDrawable, Rectangle, Text, PITCH
from breadboarder.transformations.transform import Point


class CP2102(GroupedDrawable):
    def __init__(self):
        GroupedDrawable.__init__(self, svg_id='CP2102')
        self.ports = {}
        self.width = 90*2.135
        self.height = 90*0.675
        self.usb_width = 90*0.741
        self.usb_height = 90*0.483
        self.pin_width = 25
        self.pin_height = 2
        self.board_width = 90*1.30
        self.board_offset = 20
        self.labels = ['DTR', 'RXD', 'TXD', '5V', 'CTS', 'GND']
        self.add(Rectangle(self.board_width, self.height, fill='black')
                 .move_to(Point(self.board_offset, 0)))
        self.add(Rectangle(self.usb_width, self.usb_height, fill='silver', stroke='silver')
                 .move_to(Point(0, 0.5*(self.height-self.usb_height))))
        self.add(Text('CP2102',Point(self.usb_width + 5, 10),color='white'))
        for pin_index, label in enumerate(self.labels):
            self.add(Text(label, Point(self.board_offset+self.board_width-10,6 + PITCH*pin_index),
                          color='white',size=3, anchor='end'))
            self.add(Rectangle(self.pin_width, self.pin_height, fill='gold', stroke='none')
                     .move_to(Point(self.board_offset+self.board_width-6, 4+PITCH*pin_index)))
        self.add(SocketGroup(Point(self.board_offset+self.board_width-6+self.pin_width, 5),
                             6,1,self.labels, self, fill='none'))

    def add_port(self, port, label):
        self.ports[label] = port