# coding=UTF-8
from collections import defaultdict
from unittest import TestCase
from xml.etree.ElementTree import tostring

from bs4 import BeautifulSoup
from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Drawing


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        drawing.add(Breadboard())
        svg = drawing.tostring()
        svg_root = self.check_svg_root(svg)
        self.check_breadboard(svg_root)

    def check_svg_root(self, svg):
        soup = BeautifulSoup(svg,'xml')
        svg_tags = soup.find_all('svg')
        self.assertEqual(1, len(svg_tags))
        svg_root = svg_tags[0]
        self.assertEqual('480',svg_root['height'])
        self.assertEqual('640',svg_root['width'])
        return svg_root

    def check_breadboard(self, svg_root):
        bb = svg_root.find('g', id='breadboard')
        self.assertTrue(bb is not None,'drawing should contain breadboard group')

class BreadboardTest(TestCase):
    def test_breadboard_rendering(self):
        svg = tostring(Breadboard().svg())
        bb = BeautifulSoup(svg, 'xml')
        r = bb.find('rect')
        self.assertTrue(r is not None, 'breadboard should contain a rectangle')
        self.check_four_lines(bb)
        self.check_labels(bb)

    def check_four_lines(self, bb):
        lines = bb.find_all('line')
        self.assertEqual(4, len(lines),'should have 4 power lines')

    def check_labels(self, bb):
        labels = bb.find_all('text')
        ld = defaultdict(int)
        for label in labels:
            ld[label.text] += 1
        self.assertEqual(4, ld['+'])
        self.assertEqual(4, ld[u'—'])
        for letter in 'abcdefghij':
            self.assertEqual(2, ld[letter])
        for i in range(30):
            self.assertEqual(2, ld[str(i+1)])



