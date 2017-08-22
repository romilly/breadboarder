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
        text = Element('text', x=str(self.x), y=str(self.y), style= 'fill:%s;text-anchor:%s;font-size:%dpt' %
                                                                    (self.color, self.anchor, self.size))
        text.text = self.text
        if self.angle != 0:
            text.set('transform','rotate(%d,%d,%d)' % (self.angle, self.x, self.y))
        return text

    def rotate(self, angle):
        self.angle  = angle
        return self


BREADBOARD_WIDTH = 291.7
BREADBOARD_HEIGHT = 192.2
H_LINE_OFFSET = 14
V_LINE_OFFSET = 4
V_LINE_SPACING = 24.4
LEFT_POWER_SOCKET_H_OFFSET = 19.08
LEFT_POWER_SOCKET_V_OFFSET = 12.06
BODY_SOCKET_V_OFFSET = 47.4
BODY_SOCKET_V_2ND_OFFSET = 82.17

BODY_SOCKET_H_OFFSET = 15.2
GRID_SPACING = 9
SOCKET_SIZE = 2.88



class Breadboard(CompositeItem):
    def __init__(self):
        CompositeItem.__init__(self)
        self.add(Rectangle(BREADBOARD_WIDTH, BREADBOARD_HEIGHT, fill='none'))
        self.add(hline(H_LINE_OFFSET, V_LINE_OFFSET, BREADBOARD_WIDTH - 2 * H_LINE_OFFSET, color='blue'))
        self.add(Text('-',4, 4, color='blue', size=14).rotate(90))
        self.add(Text('-',BREADBOARD_WIDTH-14, 4, color='blue', size=14).rotate(90))
        self.add(hline(H_LINE_OFFSET, V_LINE_OFFSET+V_LINE_SPACING, BREADBOARD_WIDTH - 2 * H_LINE_OFFSET, color='red'))
        self.add_power_sockets(LEFT_POWER_SOCKET_V_OFFSET)
        self.add_body_sockets(BODY_SOCKET_V_OFFSET)
        self.add_body_sockets(BREADBOARD_HEIGHT-BODY_SOCKET_V_2ND_OFFSET)
        self.add_power_sockets(BREADBOARD_HEIGHT-(LEFT_POWER_SOCKET_V_OFFSET+GRID_SPACING))
        self.add(hline(H_LINE_OFFSET, BREADBOARD_HEIGHT-(V_LINE_OFFSET+V_LINE_SPACING), BREADBOARD_WIDTH - 2 * H_LINE_OFFSET, color='blue'))
        self.add(hline(H_LINE_OFFSET, BREADBOARD_HEIGHT-V_LINE_OFFSET, BREADBOARD_WIDTH - 2 * H_LINE_OFFSET, color='red'))

    def add_power_sockets(self, top_centre):
        for group in range(5):
            for i in range(5):
                for j in (0, 1):
                    self.add(Rectangle(SOCKET_SIZE, SOCKET_SIZE, fill='black').
                             center(LEFT_POWER_SOCKET_H_OFFSET + GRID_SPACING * i + 53.5 * group, top_centre + GRID_SPACING * j))

    def add_body_sockets(self, top_centre):
        for i in range(30):
            for j in range(5):
                    self.add(Rectangle(SOCKET_SIZE, SOCKET_SIZE, fill='black').
                             center(BODY_SOCKET_H_OFFSET + GRID_SPACING * i, top_centre + GRID_SPACING * j))

    def container(self):
        return Element('g', id='breadboard')


def write(diagram, filename):
    ElementTree(diagram).write(filename, 'UTF-8')
