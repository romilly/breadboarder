from _elementtree import Element
from abc import ABCMeta, abstractmethod

from breadboarder.svg.point import Point
from breadboarder.svg.svg import cms, Drawable, SimpleItem


def v(x, y):  # for brevity, which is the soul of wit
    return vector(*cms(x, y))


def point(x, y):
    return Point(*cms(x, y))


def sv(x, y):
    return v(x*0.025, y*0.025)


def up(y):
    return sv(0, -y)


def down(y):
    return sv(0, y)


def left(x):
    return sv(-x,0)


def right(x):
    return sv(x,0)


def up_left(x, y=None):
    y = x if not y else y
    return sv(-x,-y)


def up_right(x, y=None):
    y = x if not y else y
    return sv(x, -y)


def down_left(x, y=None):
    y = x if not y else y
    return sv(-x,y)


def down_right(x, y=None):
    y = x if not y else y
    return sv(x,y)


class Path(SimpleItem):
    def __init__(self, start, *segments, **attributes):
        SimpleItem.__init__(self, start)
        self.segments = segments
        self.closed = True # can set to false if open path required
        self._attributes = attributes

    def element(self):
        p = Element('path',**self._attributes)
        d = 'M %s ' % self.top_left.format()
        d += ' '.join([segment.specification() for segment in self.segments])
        if self.closed:
            d += ' Z'
        p.set('d', d)
        if 'width' in self._attributes:
            p.set('stroke-width', self._attributes['width'])
        return p

class PathSegment():
    __metaclass__ = ABCMeta

    @abstractmethod
    def specification(self):
        pass


class RelativeVector(PathSegment):
    def __init__(self, x, y):
        self.point = Point(x,y)

    def specification(self):
        return 'l %s ' % self.point.format()

    def scale(self,scale):
        self.point= self.point.scale(scale)
        return self


def vector(x, y):
    return RelativeVector(x,y)


class Arc(PathSegment):
    def __init__(self, x, y, xrot, large_arc, sweep, endx, endy):
        self._spec = (x, y, xrot, large_arc, sweep, endx, endy)

    def specification(self):
        return 'a %f %f, %f, %d, %d, %f %f' % self._spec


def arc(x, y, xrot, large_arc, sweep, endx, endy):
    return Arc(x, y, xrot, large_arc, sweep, endx, endy)

