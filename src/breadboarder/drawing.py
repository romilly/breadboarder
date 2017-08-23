from xml.etree.ElementTree import Element, tostring, ElementTree



class CompositeItem():
    def __init__(self):
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


class Rectangle(object):
    def __init__(self, width, height, stroke_width=1,**attributes):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.stroke_width = stroke_width
        self._attributes = attributes

    def at(self, x ,y):
        self.x = x
        self.y = y
        return self

    def svg(self):
        return Element('rect', x=str(self.x), y=str(self.y), width=str(self.width), height=str(self.height),
                       style= 'stroke-width:%d;stroke:black' % self.stroke_width,**self._attributes)

    def center(self, x, y):
        self.x = x-0.5*self.width
        self.y = y-0.5*self.height
        return self


class Line():
    def __init__(self, x1, x2, y1, y2, color='black', **attributes):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color
        self._attributes = attributes

    def svg(self):
        return Element('line', x1=str(self.x1), y1=str(self.y1), x2=str(self.x2), y2=str(self.y2),
                       style='stroke:%s' % self.color, **self._attributes)


def hline(x, y, length, color='black'):
    return Line(x, x+length, y, y, color=color)


class Text():
    def __init__(self, text, x, y, color='black', anchor='start', size=8, **attributes):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.anchor = anchor
        self.size = size
        self._attributes = attributes
        self.angle = 0

    def svg(self):
        text = Element('text', x=str(self.x), y=str(self.y), style= 'fill:%s;text-anchor:%s;font-size: %dpt' %
                                                                    (self.color, self.anchor, self.size))
        text.text = self.text
        if self.angle != 0:
            text.set('transform','rotate(%d,%d,%d)' % (self.angle, self.x, self.y))
        return text

    def rotate(self, angle):
        self.angle  = angle
        return self




def write(diagram, filename):
    ElementTree(diagram).write(filename, 'UTF-8')
