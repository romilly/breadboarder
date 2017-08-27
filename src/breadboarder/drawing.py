from xml.etree.ElementTree import Element, tostring, ElementTree


class Point():
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)


    def v_flip(self):
        # flip about vertical axis
        return Point(-self.x, self.y)

    def scale(self, factor):
        return Point(self.x * factor, self.y * factor)


class Drawable():
    def __init__(self, start):
        self.start = start

    def svg(self):
        raise Exception('my subclass should have implemented this method')

    def move_to(self, point):
        self.start = point
        return self


class CompositeItem(Drawable):
    def __init__(self,start = Point(0,0)):
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
        raise Exception('My Subclass should have implemented this method')


class Drawing(CompositeItem):

    def container(self):
        return Element('svg', height='480', width='640')

    def tostring(self):
        return tostring(self.svg())


class GroupedDrawable(CompositeItem):
    def __init__(self, svg_id=None):
        CompositeItem.__init__(self)
        self.svg_id = svg_id

    def container(self):
            group = Element('g', transform='translate(%f,%f)' % (self.start.x, self.start.y))
            if self.svg_id is not None:
                group.set('id',self.svg_id)
            return group


class Rectangle(Drawable):
    def __init__(self, width, height, stroke_width=1,**attributes):
        Drawable.__init__(self, Point(0,0))
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self._attributes = attributes

    def svg(self):
        return Element('rect', x=str(self.start.x), y=str(self.start.y), width=str(self.width), height=str(self.height),
                       style= 'stroke-width:%d;stroke:black' % self.stroke_width,**self._attributes)

    def set_center(self, x, y):
        self.move_to(Point(x-0.5*self.width, y-0.5*self.height))
        return self

    def center(self):
        return self.start + Point(self.width, self.height).scale(0.5)


class Line(Drawable):
    def __init__(self, start, end, color='black', stroke_width=1,**attributes):
        Drawable.__init__(self, start)
        self.vector = end-start
        self.color = color
        self.stroke_width = stroke_width
        self._attributes = attributes

    def end(self, point):
        self.vector = point-self.start

    def svg(self):
        end = self.start + self.vector
        return Element('line', x1=str(self.start.x), y1=str(self.start.y), x2=str(end.x), y2=str(end.y),
                       style='stroke:%s;stroke-width:%d' % (self.color, self.stroke_width), **self._attributes)


def horizontal_line(start, length, color='black'):
    return Line(start, start+Point(length,0), color=color)


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


class Wire(Line):
    def __init__(self, color):
        Line.__init__(self, Point(0,0),Point(0,0), color, stroke_width=3)



def write(diagram, filename):
    ElementTree(diagram).write(filename, 'UTF-8')
