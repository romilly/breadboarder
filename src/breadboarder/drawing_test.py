from unittest import TestCase
from xml.etree.ElementTree import Element, tostring


class Drawing(object):
    def __init__(self):
        self._svg = Element('svg')

    def svg(self):
        return tostring(self._svg)


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        svg = drawing.svg()
        self.check_svg_tag(svg)

    def check_svg_tag(self, svg):
        self.assertTrue('<svg' in svg)