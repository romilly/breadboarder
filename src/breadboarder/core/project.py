from xml.etree.ElementTree import Element, tostring, ElementTree

import math


class Point():
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        # Hademard (direct) product
        return Point(self.x*other.x, self.y*other.y)


    def v_flip(self):
        # flip about vertical axis
        return Point(-self.x, self.y)

    def scale(self, factor):
        return Point(self.x * factor, self.y * factor)

    def __str__(self):
        return 'a Point(%s,%s)' % (str(self.x),str(self.y))

    def cartesian_coordinates(self):
        return (self.x, self.y)

    def r(self):
        return math.sqrt(sum((self*self).cartesian_coordinates()))

    def theta(self):
        return math.degrees(math.atan2(self.y, self.x))


class Drawable():
    def __init__(self, start):
        self.start = start

    def svg(self):
        raise Exception('my SubClass should have implemented this method')

    def move_to(self, point):
        self.start = point
        return self

    def move_by(self, amount):
        self.start = self.start + amount


class CompositeItem(Drawable):
    def __init__(self,start=Point(0,0)):
        Drawable.__init__(self, start)
        self._children = []

    def add(self, item):
        self._children.append(item)

    def svg(self):
        svg = self.container()
        for child in self._children:
            svg.append(child.svg())
        return svg

    def container(self):
        raise Exception('My SubClass should have implemented this method')


class Project(CompositeItem):

    def container(self):
        return Element('svg', height='480', width='640')

    def tostring(self):
        return tostring(self.svg())


class Transform():
    """Represents an atomic svg transformation - a translation, rotation or scaling"""
    def text(self):
        raise Exception('my SubClass should have implemented this method')

class Translation(Transform):
    def __init__(self, vector):
        self.vector = vector

    def text(self):
        return 'translate(%f,%f)' % (self.vector.cartesian_coordinates())


class Rotation(Transform):
    def __init__(self, angle, origin=Point(0,0)):
        self.angle = angle
        self.origin = origin

    def text(self):
        return 'rotate(%f,%f,%f)' % (self.angle, self.origin.x, self.origin.y)


class GroupedDrawable(CompositeItem):
    def __init__(self, svg_id=None, origin=Point(0,0)):
        CompositeItem.__init__(self)
        self.svg_id = svg_id
        self.angle = 0
        self.origin = origin
        self.transformations = []

    def transformation(self):
        return ' '.join([t.text() for t in self.transformations])

    def container(self):
            group = Element('g', transform=self.transformation())
            if self.svg_id is not None:
                group.set('id',self.svg_id)
            return group

    def rotate(self, theta, origin=Point(0,0)):
        self.transformations.append(Rotation(theta, origin))
        return self

    def move_to(self, point):
        self.transformations.append(Translation(point))
        return self


class Rectangle(Drawable):
    def __init__(self, width, height, stroke_width=1, stroke='black',**attributes):
        Drawable.__init__(self, Point(0,0))
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.stroke = stroke
        self._attributes = attributes

    def svg(self):
        return Element('rect', x=str(self.start.x), y=str(self.start.y), width=str(self.width), height=str(self.height),
                       style= 'stroke-width:%d;stroke:%s' % (self.stroke_width,self.stroke), **self._attributes)

    def set_center(self, x, y):
        self.move_to(Point(x-0.5*self.width, y-0.5*self.height))
        return self

    def center(self):
        return self.start + Point(self.width, self.height).scale(0.5)


class Line(Drawable):
    def __init__(self, start, end, color='black', stroke_width=1, linecap='butt', **attributes):
        Drawable.__init__(self, start)
        self.vector = end-start
        self.color = color
        self.stroke_width = stroke_width
        self.linecap = linecap
        self._attributes = attributes

    def set_end(self, point):
        self.vector = point-self.start

    def end(self):
        return self.start + self.vector

    def svg(self):
        return Element('line', x1=str(self.start.x), y1=str(self.start.y), x2=str(self.end().x), y2=str(self.end().y),
                       style='stroke:%s;stroke-width:%d;stroke-linecap:%s' % (self.color, self.stroke_width, self.linecap), **self._attributes)


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

    def svg(self):
        text = Element('text', x=str(self.start.x), y=str(self.start.y),
            style= 'fill:%s;text-anchor:%s;font-size: %dpt' % (self.color, self.anchor, self.size))
        text.text = self.text
        if self.angle != 0:
            text.set('transform','rotate(%d,%d,%d)' % (self.angle, self.start.x, self.start.y))
        return text

    def rotate(self, angle):
        self.angle  = angle
        return self


class Circle(Drawable):
    def __init__(self, start, radius, color='green', **attributes):
        Drawable.__init__(self, start)
        self.radius = radius
        self.color = color
        self._attributes = attributes

    def svg(self):
        return Element('circle', cx=str(self.start.x), cy=str(self.start.y), r=str(self.radius), **self._attributes)


def write(diagram, filename):
    ElementTree(diagram).write(filename, 'UTF-8')
