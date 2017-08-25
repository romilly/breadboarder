from xml.etree.ElementTree import Element

from breadboarder.drawing import CompositeItem, Rectangle, horizontal_line, Text, Point

GRID_SPACING = 9


class SocketGroup(CompositeItem):
    def __init__(self, center, rows, cols, id='sockets'):
        CompositeItem.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                self.add(self.socket().center(center.x + GRID_SPACING * i, center.y + GRID_SPACING * j))

    def socket(self):
        return Rectangle(self.socket_size, self.socket_size, fill='black')

    def container(self):
        return Element('g', id=self.id)


class LineOffset(Point):
    pass


class CharOffset(Point):
    pass


# TODO: add breadboard_config
# TODO: use group/move to locate things


class Breadboard(CompositeItem):
    def __init__(self):
        CompositeItem.__init__(self)
        self.width = 291.7
        self.height = 192.2
        self.inset = 19.08
        self.add(Rectangle(self.width, self.height, fill='none'))
        self.add_power_group(5)
        gap_from_left_to_body_sockets = 15.2
        self.add_numeric_labels(90*0.469, 30, 'start')
        self.add_body_sockets(Point(gap_from_left_to_body_sockets,47.4))
        self.add_body_sockets(Point(gap_from_left_to_body_sockets,108))
        self.add_numeric_labels(90*1.66, 30, 'end')
        self.add_power_group(1.81*90)

    def add_power_group(self, vertical_location):
        self.add_power_line(vertical_location, u'\u2014', 'blue')
        self.add_power_sockets(vertical_location + 8.06)
        self.add_power_line(vertical_location + 24.4, '+', 'red')

    def add_power_line(self, vertical_location, text, color):
        line_offset = LineOffset(10, vertical_location)
        char_offset = CharOffset(8, 1)
        self.add(horizontal_line(line_offset, self.width - 2 * line_offset.x, color=color))
        self.add(Text(text, line_offset+char_offset.v_flip(), color=color, anchor='middle', size=7).rotate(90))
        self.add(Text(text, char_offset.v_flip() + line_offset + Point(self.width - 8,-1),
                      color=color, anchor='middle', size=7).rotate(90))

    def add_power_sockets(self, top_centre):
        for group in range(5):
            self.add(SocketGroup(Point(self.inset + 53.5* group, top_centre), 2, 5))

    def add_body_sockets(self, center):
        self.add(SocketGroup(center, 5, 30))

    def container(self):
        return Element('g', id='breadboard')

    def add_numeric_labels(self, vertical_location, count, anchor):
        for i in range(count):
            self.add(Text(str(i+1), Point(self.inset-1+GRID_SPACING*i, vertical_location), anchor=anchor, size=6).rotate(-90))