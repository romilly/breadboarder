from xml.etree.ElementTree import Element

from breadboarder.drawing import CompositeItem, Rectangle, horizontal_line, Text, Point


class SocketGroup(CompositeItem):
    def __init__(self, center, rows, cols, alpha_labels, parent, start_number=1, id='sockets'):
        CompositeItem.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                socket = self.socket().set_center(center.x + Breadboard.PITCH * i, center.y + Breadboard.PITCH * j)
                parent.add_connector(socket, alpha_labels[j]+str(i+start_number))
                self.add(socket)

    def socket(self):
        rectangle = Rectangle(self.socket_size, self.socket_size, fill='black')
        return rectangle

    def container(self):
        return Element('g', id=self.id)


class LineOffset(Point):
    pass


# TODO: document Breadboard measurements in docs/BREADBOARD_LAYOUT.md


class Breadboard(CompositeItem):
    PITCH = 0.1*90 # 0.1", 90 DPI
    def __init__(self):
        CompositeItem.__init__(self)
        self.connectors = {}
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
        self.inset_to_left_letters = 8
        self.inset_to_right_letters = 90 * 3.18
        self.add_components()

    def add_connector(self, connector, key):
        self.connectors[key] = connector

    def add_components(self):
        self.add(Rectangle(self.width, self.height, fill='none'))
        self.add_power_group(self.drop_to_top_power_group,'T')
        self.add_numeric_labels(self.drop_to_top_numeric_labels, self.columns, 'start')
        self.add_body_sockets(Point(self.gap_from_left_to_body_sockets, self.drop_to_top_body_sockets), 'jihgf')
        self.add_body_sockets(Point(self.gap_from_left_to_body_sockets, self.drop_to_lower_body_sockets), 'edcba')
        self.add_numeric_labels(self.drop_to_lower_numeric_labels, self.columns, 'end')
        self.add_power_group(self.drop_to_lower_power_group,'B')

    def add_power_group(self, vertical_location, prefix):
        EM_DASH = u'\u2014'
        self.add_power_line(vertical_location, EM_DASH, 'blue')
        self.add_power_sockets(vertical_location + self.drop_from_line_to_power_sockets, prefix)
        self.add_power_line(vertical_location + self.gap_between_power_lines, '+', 'red')

    def add_power_line(self, vertical_location, text, color):
        line_offset = LineOffset(self.gap_to_left_of_power_line, vertical_location)
        self.add(horizontal_line(line_offset, self.width - 2 * line_offset.x, color=color))
        self.add(Text(text, line_offset + self.offset_from_line_start_to_text, color=color, anchor='middle', size=7).rotate(90))
        self.add(Text(text, self.offset_from_line_start_to_text + line_offset + Point(self.width - 8, -1),
                      color=color, anchor='middle', size=7).rotate(90))

    def add_power_sockets(self, top_centre, prefix):
        for group in range(self.power_socket_group_count):
            self.inter_power_group_spacing = 53.5
            self.add(SocketGroup(Point(self.inset + self.inter_power_group_spacing * group, top_centre), 2, 5, (prefix+'M',prefix+'P'), self))

    def add_body_sockets(self, center, alpha_labels):
        self.add_alpha_labels(Point(self.inset_to_left_letters, center.y + 2), alpha_labels)
        self.add(SocketGroup(center, 5, self.columns, alpha_labels, self))
        self.add_alpha_labels(Point(self.inset_to_right_letters, center.y + 2), alpha_labels)

    def container(self):
        return Element('g', id='breadboard')

    def add_numeric_labels(self, vertical_location, count, anchor):
        for i in range(count):
            self.add(Text(str(i+1), Point(self.inset - 1 + self.PITCH * i, vertical_location), anchor=anchor, color='grey', size=6).rotate(-90))

    def add_alpha_labels(self, offset_to_letters, letters):
        for i in range(len(letters)):
            self.add(Text(letters[i], offset_to_letters +Point(0,self.PITCH*i), color='grey', size=6 ).rotate(-90))

    def connect(self, component, start, end):
        component.start = self.connectors[start].center()
        component.end = self.connectors[end].center()
        self.add(component)
