from xml.etree.ElementTree import Element

from breadboarder.drawing import CompositeItem, Rectangle, horizontal_line, Text, Point



class SocketGroup(CompositeItem):
    def __init__(self, center, rows, cols, id='sockets'):
        CompositeItem.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                self.add(self.socket().center(center.x + Breadboard.PITCH * i, center.y + Breadboard.PITCH * j))

    def socket(self):
        return Rectangle(self.socket_size, self.socket_size, fill='black')

    def container(self):
        return Element('g', id=self.id)


class LineOffset(Point):
    pass



# TODO: add breadboard_config
# TODO: use group/move to locate things

# Breadboard measurements documented in docs/BREADBOARD_LAYOUT.md


class Breadboard(CompositeItem):
    PITCH = 0.1*90 # 0.1", 90 DPI
    def __init__(self):
        CompositeItem.__init__(self)
        self.width = 291.7
        self.height = 192.2
        self.inset = 19.08
        self.columns = 30
        self.power_socket_group_count = 5
        self.gap_from_left_to_body_sockets = 15.2
        self.drop_to_top_numeric_labels = 90 * 0.469
        self.drop_to_top_body_sockets = 47.4
        self.drop_to_lower_body_sockets = 108
        self.drop_to_lower_numeric_labels = 90 * 1.66
        self.drop_to_top_power_group = 5
        self.drop_to_lower_power_group = 1.81 * 90
        self.drop_from_line_to_power_sockets = 8.06
        self.gap_between_power_lines = 24.4
        self.gap_to_left_of_power_line = 10
        self.offset_from_line_start_to_text = Point(-8, 1)
        self.inset_to_letters = 8
        self.add_components()

    def add_components(self):
        self.add(Rectangle(self.width, self.height, fill='none'))
        self.add_power_group(self.drop_to_top_power_group)
        self.add_numeric_labels(self.drop_to_top_numeric_labels, self.columns, 'start')
        self.add_body_sockets(Point(self.gap_from_left_to_body_sockets, self.drop_to_top_body_sockets))
        self.add_body_sockets(Point(self.gap_from_left_to_body_sockets, self.drop_to_lower_body_sockets))
        self.add_numeric_labels(self.drop_to_lower_numeric_labels, self.columns, 'end')
        self.add_power_group(self.drop_to_lower_power_group)
        self.add_alpha_labels(self.drop_to_top_body_sockets + 2,'jihgf')
        self.add_alpha_labels(self.drop_to_lower_body_sockets + 2,'edcba')

    def add_power_group(self, vertical_location):
        EM_DASH = u'\u2014'
        self.add_power_line(vertical_location, EM_DASH, 'blue')
        self.add_power_sockets(vertical_location + self.drop_from_line_to_power_sockets)
        self.add_power_line(vertical_location + self.gap_between_power_lines, '+', 'red')

    def add_power_line(self, vertical_location, text, color):
        line_offset = LineOffset(self.gap_to_left_of_power_line, vertical_location)
        self.add(horizontal_line(line_offset, self.width - 2 * line_offset.x, color=color))
        self.add(Text(text, line_offset + self.offset_from_line_start_to_text, color=color, anchor='middle', size=7).rotate(90))
        self.add(Text(text, self.offset_from_line_start_to_text + line_offset + Point(self.width - 8, -1),
                      color=color, anchor='middle', size=7).rotate(90))

    def add_power_sockets(self, top_centre):
        for group in range(self.power_socket_group_count):
            self.add(SocketGroup(Point(self.inset + 53.5* group, top_centre), 2, 5))

    def add_body_sockets(self, center):
        self.add(SocketGroup(center, 5, self.columns))

    def container(self):
        return Element('g', id='breadboard')

    def add_numeric_labels(self, vertical_location, count, anchor):
        for i in range(count):
            self.add(Text(str(i+1), Point(self.inset - 1 + self.PITCH * i, vertical_location), anchor=anchor, size=6).rotate(-90))

    def add_alpha_labels(self, drop_to_letters, letters):
        for i in range(len(letters)):
            self.add(Text(letters[i], Point(self.inset_to_letters, drop_to_letters + self.PITCH*i), size=6 ).rotate(-90))