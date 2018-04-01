import abc
import math
from xml.etree.ElementTree import Element, ElementTree

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

    def format(self):
        return '%s %s' % (str(self.x),str(self.y))



class Drawable:
    __metaclass__ = abc.ABCMeta

    def __init__(self, start):
        self.start = start

    @abc.abstractmethod
    def element(self):
        pass

    def move_to(self, point):
        self.start = point
        return self


class CompositeItem(Drawable):
    __metaclass__ = abc.ABCMeta

    def __init__(self,start=Point(0,0)):
        Drawable.__init__(self, start)
        self._children = []

    def add(self, item):
        self._children.append(item)

    def element(self):
        elm = self.container()
        for child in self._children:
            elm.append(child.element())
        return elm

    @abc.abstractmethod
    def container(self):
        pass

# TODO: replace PolygonalPath with Path;
# TODO: this will require an easy way of converting a sequence of points to a relative path (so move_to is easy)
# TODO: or letting move_to change path elements (probably better)

class PolygonalPath(Drawable):
    def __init__(self, start, *points, **attributes):
        Drawable.__init__(self, start)
        last = start
        self.points = []
        # Oh for a first difference operator :)
        for point in points:
            self.points.append(point-last)
            last = point
        self._attributes = attributes
        self.closed = True # can set to false if open path required

    def element(self):
        p = Element('path',**self._attributes)
        d = 'M %s' % self.start.format()
        d += ' '.join(['l %s' % point.format() for point in self.points]) # lowercase l means move is relative
        if self.closed:
            d += ' Z'
        p.set('d',d)
        return p


class Path(Drawable):
    def __init__(self, start, *segments, **attributes):
        Drawable.__init__(self, start)
        self.segments = segments
        self.closed = True # can set to false if open path required
        self._attributes = attributes

    def element(self):
        p = Element('path',**self._attributes)
        d = 'M %s ' % self.start.format()
        d += ' '.join([segment.specification() for segment in self.segments])
        if self.closed:
            d += ' Z'
        p.set('d', d)
        if 'width' in self._attributes:
            p.set('stroke-width', self._attributes['width'])
        return p

class PathSegment():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def specification(self):
        pass


class RelativeVector(PathSegment):
    def __init__(self, x, y):
        self.point = Point(x,y)

    def specification(self):
        return 'l %s ' % self.point.format()

def vector(x, y):
    return RelativeVector(x,y)


class Arc(PathSegment):
    def __init__(self, x, y, xrot, large_arc, sweep, endx, endy):
        self._spec = (x, y, xrot, large_arc, sweep, endx, endy)

    def specification(self):
        return 'a %f %f, %f, %d, %d, %f %f' % self._spec


def arc(x, y, xrot, large_arc, sweep, endx, endy):
    return Arc(x, y, xrot, large_arc, sweep, endx, endy)


class Transform():
    """Represents an atomic svg transformation - a translation, rotation or scaling"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def text(self):
        pass


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
    def __init__(self, svg_id=None):
        CompositeItem.__init__(self)
        self.svg_id = svg_id
        self.angle = 0
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
        Drawable.move_to(self, point)
        self.transformations.append(Translation(point))
        return self


class Rectangle(Drawable):
    def __init__(self, width, height, stroke_width=1, stroke='black',rounded=False, **attributes):
        Drawable.__init__(self, Point(0,0))
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self.stroke = stroke
        self.rounded = rounded
        self._attributes = attributes

    def element(self):
        rect = Element('rect', x=str(self.start.x), y=str(self.start.y), width=str(self.width),
                          height=str(self.height), style='stroke-width:%d;stroke:%s' % (self.stroke_width, self.stroke),
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