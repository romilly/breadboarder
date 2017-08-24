from xml.etree.ElementTree import Element

from breadboarder.drawing import CompositeItem, Rectangle, horizontal_line, Text, Point

V_LINE_OFFSET = 4
V_LINE_SPACING = 24.4
LEFT_POWER_SOCKET_V_OFFSET = 12.06
H_TEXT_OFFSET = 10
GRID_SPACING = 9


class SocketGroup(CompositeItem):
    def __init__(self, center, rows, cols, id='sockets'):
        CompositeItem.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                self.add(Rectangle(self.socket_size, self.socket_size, fill='black').
                         center(center.x + GRID_SPACING * i,
                                center.y + GRID_SPACING * j))

    def container(self):
        return Element('g', id=self.id)


class LineOffset(Point):
    pass


class CharOffset(Point):
    pass


class Breadboard(CompositeItem):
    def __init__(self):
        CompositeItem.__init__(self)
        self.width = 291.7
        self.height = 192.2
        self.add(Rectangle(self.width, self.height, fill='none'))
        self.add_top_power()
        self.add_body_sockets(Point(15.2,47.4))
        self.add_body_sockets(Point(15.2,108))
        self.add_bottom_power()

    def add_bottom_power(self):
        self.add_power_line(self.height - (V_LINE_OFFSET + V_LINE_SPACING), u'\u2014', 'blue')
        self.add_power_line(self.height - V_LINE_OFFSET, '+', 'red')
        self.add_power_sockets(self.height - (LEFT_POWER_SOCKET_V_OFFSET + GRID_SPACING))

    def add_top_power(self):
        self.add_power_line(V_LINE_OFFSET, u'\u2014', 'blue')
        self.add_power_line(V_LINE_OFFSET + V_LINE_SPACING, '+', 'red')
        self.add_power_sockets(LEFT_POWER_SOCKET_V_OFFSET)

    def add_power_line(self, vertical_location, text, color):
        line_offset = LineOffset(10, vertical_location)
        char_offset = CharOffset(8,-3)
        self.add(horizontal_line(line_offset, self.width - 2 * line_offset.x, color=color))
        self.add(Text(text, line_offset+char_offset.v_flip(), color=color, align='middle', size=7).rotate(90))
        self.add(Text(text, char_offset.v_flip() + line_offset + Point(self.width - 8,-1),
                      color=color, align='middle', size=7).rotate(90))

    def add_power_sockets(self, top_centre):
        for group in range(5):
            self.add(SocketGroup(Point(19.08 + 53.5* group, top_centre), 2, 5))

    def add_body_sockets(self, center):
        self.add(SocketGroup(center, 5, 30))

    def container(self):
        return Element('g', id='breadboard')