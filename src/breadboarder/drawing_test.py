from unittest import TestCase
from xml.etree.ElementTree import Element, tostring
from bs4 import BeautifulSoup

class Drawing(object):
    def __init__(self):
        self._svg = Element('svg', height='480', width='640')

    def svg(self):
        return tostring(self._svg)


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        svg = drawing.svg()
        self.check_svg_tag(svg)

    def check_svg_tag(self, svg):
        # self.assertTrue('<svg' in svg)
        soup = BeautifulSoup(svg,'xml')
        svg_tags = soup.find_all('svg')
        self.assertEqual(1, len(svg_tags))
        svg_root = svg_tags[0]
        self.assertEqual('480',svg_root['height'])
        self.assertEqual('640',svg_root['width'])