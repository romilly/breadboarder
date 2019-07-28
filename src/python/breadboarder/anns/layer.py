from breadboarder.core.host import Host
from breadboarder.core.port import Port
from svg.point import Point
from svg.svg import Circle, Line


class Layer(Host):
    def __init__(self, width=100, nodes=5, fill='grey', diameter=10):
        Host.__init__(self)
        self.nodes = nodes
        self.fill = fill
        radius = diameter/2.0
        gap = diameter/3.0
        spacing = diameter + gap
        node_span = nodes*diameter + gap*(nodes-1)
        left_center =  radius + 0.5*(width-node_span)
        offset = Point(radius, radius)
        for i in range(self.nodes):
            centre = Point(left_center + i * spacing, 0.6 * radius)
            self.add(Circle(centre, radius, fill=self.fill))
            self.add_port(Port(self,centre+offset,str(i)))


class Network(Host):
    def __init__(self, *layers):
        Host.__init__(self)
        self.layers = layers
        for (one, two) in zip(layers[:-1],layers[1:]):
            self.link(one, two)
        for layer in layers:
            self.add(layer)

    def link(self, one: Layer, two: Layer):
        for port1 in one.ports():
            for port2 in two.ports():
                self.add(Line(port1.location(), port2.location()))



