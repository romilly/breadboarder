from svg.point import Point
from svg.svg import Circle, GroupedDrawable


class Layer(GroupedDrawable):
    def __init__(self, width, nodes=5, fill='grey'):
        self.nodes = nodes
        self.fill = fill
        GroupedDrawable.__init__(self)
        diameter = 0.6*width/self.nodes
        radius = diameter/2.0
        gap = diameter/3.0
        spacing = diameter + gap
        for i in range(self.nodes):
            left_center =  0.5*diameter + 0.1*width
            self.add(Circle(Point(left_center + i*spacing, 0.6*radius),radius,fill=self.fill))

