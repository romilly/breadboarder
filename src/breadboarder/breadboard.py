from xml.etree.ElementTree import Element

from breadboarder.drawing import CompositeItem, Rectangle, hline, Text

H_LINE_OFFSET = 14
V_LINE_OFFSET = 4
V_LINE_SPACING = 24.4
LEFT_POWER_SOCKET_H_OFFSET = 19.08
LEFT_POWER_SOCKET_V_OFFSET = 12.06
BODY_SOCKET_V_OFFSET = 47.4
BODY_SOCKET_V_2ND_OFFSET = 82.17
H_TEXT_OFFSET = 10
BODY_SOCKET_H_OFFSET = 15.2
GRID_SPACING = 9


class SocketGroup(CompositeItem):
    def __init__(self, x, y, rows, cols, id='sockets'):
        CompositeItem.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                self.add(Rectangle(self.socket_size, self.socket_size, fill='black').
                         center(x + GRID_SPACING * i,
                                y + GRID_SPACING * j))

    def container(self):
        return Element('g', id=self.id)


class Point():
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)


class LineOffset(Point):
    pass


class CharOffset(Point):
    pass


class Breadboard(CompositeItem):
    def __init__(self, width = 291.7, height= 192.2):
        CompositeItem.__init__(self)
        self.width = width
        self.height = height
        self.add(Rectangle(self.width, self.height, fill='none'))
        self.add_top_power()
        self.add_body_sockets(BODY_SOCKET_V_OFFSET)
        self.add_body_sockets(self.height - BODY_SOCKET_V_2ND_OFFSET)
        self.add_bottom_power()

    def add_bottom_power(self):
        self.add_power_sockets(self.height - (LEFT_POWER_SOCKET_V_OFFSET + GRID_SPACING))
        self.add_power_line(LineOffset(H_TEXT_OFFSET, self.height - (V_LINE_OFFSET + V_LINE_SPACING)), CharOffset(0, 0), '_', 'blue')
        self.add_power_line(LineOffset(10, self.height - V_LINE_OFFSET), CharOffset(-8, -6),'+', 'red')

    def add_top_power(self):
        self.add_power_line(LineOffset(H_TEXT_OFFSET, V_LINE_OFFSET), CharOffset(0, 0), '_', 'blue')
        self.add_power_line(LineOffset(10, V_LINE_OFFSET + V_LINE_SPACING), CharOffset(-8, -6), '+', 'red')
        self.add_power_sockets(LEFT_POWER_SOCKET_V_OFFSET)

    def add_power_line(self, line_offset, char_offset, text, color):
        self.add(hline(line_offset.x, line_offset.y, self.width - 2 * line_offset.x , color=color))
        self.add(Text(text, (line_offset+char_offset).x, (line_offset+char_offset).y, color=color, align='middle', size=10).rotate(90))
        self.add(Text(text, char_offset.x + self.width + 5 - line_offset.x, char_offset.y+ line_offset.y,
                      color=color, align='middle', size=10).rotate(90))

    def add_power_sockets(self, top_centre):
        for group in range(5):
            self.add(SocketGroup(LEFT_POWER_SOCKET_H_OFFSET + 53.5* group, top_centre, 2, 5))

    def add_body_sockets(self, top_centre):
        self.add(SocketGroup(BODY_SOCKET_H_OFFSET, top_centre, 5, 30))

    def container(self):
        return Element('g', id='breadboard')