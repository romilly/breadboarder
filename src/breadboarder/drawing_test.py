from unittest import TestCase
from bs4 import BeautifulSoup

from breadboarder.drawing import Drawing, Breadboard


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        drawing.add(Breadboard())
        svg = drawing.svg()
        svg_root = self.check_svg_root(svg)
        self.check_breadboard(svg_root)

    def check_svg_root(self, svg):
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