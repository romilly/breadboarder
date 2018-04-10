from abc import abstractmethod, ABCMeta
from xml.etree.ElementTree import Element, ElementTree
from breadboarder.transformations.transform import Point, Rotation, Translation

PITCH = 0.1*90 # 0.1", 90 DPI


def to_cms(distance):
    return distance * PITCH / 0.254


def cms(*distances):
    if len(distances) == 1:
        return to_cms(distances[0])
    return [to_cms(distance) for distance in distances]


def to_ins(distance):
    return distance * PITCH * 10


def ins(*distances):
    if len(distances) == 1:
        return to_ins(distances[0])
    return [to_ins(distance) for distance in distances]


class Drawable:
    __metaclass__ = ABCMeta

    def __init__(self, start):
        self.start = start

    @abstractmethod
    def element(self):
        pass

    def move_to(self, point):
        self.start = point
        return self


class CompositeItem(Drawable):
    __metaclass__ = ABCMeta

    def __init__(self, start=Point(0,0)):
        Drawable.__init__(self, start)
        self._children = []

    def add(self, item):
        self._children.append(item)

    def element(self):
        elm = self.container()
        for child in self._children:
            elm.append(child.element())
        return elm

    @abstractmethod
    def container(self):
        pass


class GroupedDrawable(CompositeItem):
    def __init__(self, svg_id=None):
        CompositeItem.__init__(self)
        self.svg_id = svg_id
        self.transformations = []

    def transformation(self):
        return ' '.join([t.text() for t in self.transformations])

    def container(self):
            group = Element('g')
            if len(self.transformations) > 0:
                group.set('transform',self.transformation())
            if self.svg_id is not None:
                group.set('id',self.svg_id)
            return group

    def rotate(self, theta, origin=Point(0,0)):
        self.transformations.append(Rotation(theta, origin))
        return self

    def move_to(self, point):
        Drawable.move_to(self, point)
        self.transformations.append(Translation(point))
        return self


class Rectangle(Drawable):
    def __init__(self, width, height, stroke_width=1, stroke='black', stroke_dasharray=None,rounded=False, **attributes):
        Drawable.__init__(self, Point(0,0))
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.stroke_dasharray = stroke_dasharray
        self.stroke = stroke
        self.rounded = rounded
        self._attributes = attributes

    def element(self):
        style = 'stroke-width:%d;stroke:%s;' % (self.stroke_width, self.stroke)
        if self.stroke_dasharray:
            style += 'stroke-dasharray: %s;' % self.stroke_dasharray
        rect = Element('rect', x=str(self.start.x), y=str(self.start.y), width=str(self.width),
                       height=str(self.height), style=style,
                       **self._attributes)
        if self.rounded:
            rect.set('rx', '4')
            rect.set('ry', '4')
        return rect

    def set_center(self, x, y):
        self.move_to(Point(x-0.5*self.width, y-0.5*self.height))
        return self

    def center(self):
        return self.start + Point(self.width, self.height).scale(0.5)

    def set_fill(self, color):
        self._attributes['fill'] = color


class Line(Drawable):
    def __init__(self, start, end, color='black', stroke_width=1, linecap='butt', stroke_dasharray=None, **attributes):
        Drawable.__init__(self, start)
        self.vector = end-start
        self.color = color
        self.stroke_width = stroke_width
        self.linecap = linecap
        self._attributes = attributes
        self.stroke_dasharray = stroke_dasharray

    def set_end(self, point):
        self.vector = point-self.start

    def end(self):
        return self.start + self.vector

    def element(self):
        style = 'stroke:%s;stroke-width:%d;stroke-linecap:%s;' % (self.color, self.stroke_width, self.linecap)
        if self.stroke_dasharray:
            style += 'stroke-dasharray: %s;' % self.stroke_dasharray
        return Element('line', x1=str(self.start.x), y1=str(self.start.y), x2=str(self.end().x), y2=str(self.end().y),
                       style=style, **self._attributes)


def horizontal_line(start, length, color='black', stroke_width=1, linecap='butt'):
    return Line(start, start+Point(length,0), color=color, stroke_width=stroke_width, linecap=linecap)


class Text(Drawable):
    def __init__(self, text, start, color='black', anchor='start', size=8, **attributes):
        Drawable.__init__(self, start)
        self.text = text
        self.color = color
        self.anchor = anchor
        self.size = size
        self._attributes = attributes
        self.angle = 0

    def element(self):
        text = Element('text', x=str(self.start.x), y=str(self.start.y),
            style= 'fill:%s;text-anchor:%s;font-size: %dpt' % (self.color, self.anchor, self.size))
        text.text = self.text
        if self.angle != 0:
            text.set('transform','rotate(%d,%d,%d)' % (self.angle, self.start.x, self.start.y))
        return text

    def rotate(self, angle):
        self.angle  = angle
        return self

# TODO: add circles to ends of wires (?)


class Circle(Drawable):
    def __init__(self, start, radius, **attributes):
        Drawable.__init__(self, start)
        self.radius = radius
        self._attributes = attributes

    def center(self):
        return self.start + Point(self.radius, self.radius)

    def element(self):
        return Element('circle', cx=str(self.center().x), cy=str(self.center().y), r=str(self.radius), **self._attributes)

    def move_center_to(self, point):
        self.move_to(point - Point(self.radius, self.radius))
        return self


def write(diagram, filename):
    ElementTree(diagram).write(filename, 'UTF-8')