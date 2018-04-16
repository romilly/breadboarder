from _elementtree import Element

from breadboarder.svg.svg import GroupedDrawable, PITCH, Rectangle


class Port():
    # the socket or pin belonging to a host that a component can be connected to
    def __init__(self, host, relative_location, portname):
        self.host = host
        self.portname = portname
        self.relative_location = relative_location

    def location(self):
        return self.host.location_of(self.relative_location)

    def describe_location(self):
        return self.host.describe_port_location(self.portname)


class SocketGroup(GroupedDrawable):
    def __init__(self, center, rows, cols, alpha_labels, host, start_number=1, id='sockets', fill='black'):
        GroupedDrawable.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                socket = self.socket(fill).set_center(center.x + PITCH * i, center.y + PITCH * j)
                label = alpha_labels[j] + self.numeric_label(i, start_number)
                host.add_port(Port(host, socket.center(), label))
                self.add(socket)

    def numeric_label(self, i, start_number):
        return '' if start_number == -1 else str(i + start_number)

    def socket(self, fill):
        rectangle = Rectangle(self.socket_size, self.socket_size, fill=fill, stroke=fill)
        return rectangle

    def container(self):
        return Element('g', id=self.id)
