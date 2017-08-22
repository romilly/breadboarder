from xml.etree.ElementTree import Element, tostring


class Drawing(object):
    def __init__(self):
        self._children = []

    def svg(self):
        svg = Element('svg', height='480', width='640')
        for child in self._children:
            svg.append(child.svg())
        return tostring(svg)

    def add(self, item):
        self._children.append(item)


class Breadboard(object):
    def svg(self):
        return Element('g',id='breadboard')

