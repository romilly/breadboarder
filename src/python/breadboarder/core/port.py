from _elementtree import Element

from breadboarder.core.units import PITCH
from svg.svg import GroupedDrawable, Rectangle


class Port():
    # the socket or pin belonging to a host that a component can be connected to
    def __init__(self, host, relative_location, portname, port_type='socket'):
        self.host = host
        self.portname = portname
        self.relative_location = relative_location
        self.port_type = port_type

    def location(self):
        return self.host.location_of(self.relative_location)

    def describe_location(self):
        return self.host.describe_port_location(self.portname)

    def description(self):
        return '%s %s' % (self.port_type, self.portname)


class SocketGroup(GroupedDrawable):
    # TODO: remove fill as this is determined by port_type
    def __init__(self, center, rows, cols, alpha_labels, host, start_number=1,
                 id='sockets', fill='black', port_type='socket'):
        GroupedDrawable.__init__(self)
        self.socket_size = 2.88
        self.id = id
        for i in range(cols):
            for j in range(rows):
                socket = self.socket(fill).set_center(center.x + PITCH * i, center.y + PITCH * j)
                label = alpha_labels[j] + self.numeric_label(i, start_number)
                host.add_port(Port(host, socket.center(), label, port_type=port_type))
                self.add(socket)

    # TODO: use None, not -1, as flag
    def numeric_label(self, i, start_number):
        return '' if start_number == -1 else str(i + start_number)

    def socket(self, fill):
        rectangle = Rectangle(self.socket_size, self.socket_size, fill=fill, stroke=fill)
        return rectangle

    def container(self):
        return Element('g', id=self.id)
