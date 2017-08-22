from unittest import TestCase
from xml.etree.ElementTree import Element, tostring
from bs4 import BeautifulSoup

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


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        drawing.add(Breadboard())
        svg = drawing.svg()
        svg_root = self.check_svg_tag(svg)
        self.check_breadboard(svg_root)

    def check_svg_tag(self, svg):
        # self.assertTrue('<svg' in svg)
        soup = BeautifulSoup(svg,'xml')
        svg_tags = soup.find_all('svg')
        self.assertEqual(1, len(svg_tags))
        svg_root = svg_tags[0]
        self.assertEqual('480',svg_root['height'])
        self.assertEqual('640',svg_root['width'])
        return svg_root

    def check_breadboard(self, svg_root):
        bb = svg_root.find('g', id='breadboard')
        self.assertTrue(bb is not None)