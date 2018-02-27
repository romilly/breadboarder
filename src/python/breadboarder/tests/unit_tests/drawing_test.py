# coding=UTF-8
from collections import defaultdict
from unittest import TestCase
from xml.etree.ElementTree import tostring

from breadboarder.core.project import Project
from bs4 import BeautifulSoup

from breadboarder.core.breadboard import Breadboard


class DrawingTest(TestCase):
    def test_builds_svg(self):
        project = Project()
        project.add(Breadboard())
        svg = project.tostring()
        soup = BeautifulSoup(svg,'xml')
        svg_tags = soup.find_all('svg')
        self.assertEqual(1, len(svg_tags))
        svg_root = svg_tags[0]
        self.assertEqual('480',svg_root['height'])
        self.assertEqual('640',svg_root['width'])
        bb = svg_root.find('g', id='breadboard')
        self.assertTrue(bb is not None,'project should contain breadboard group')


class BreadboardTest(TestCase):
    def setUp(self):
        self.bb = Breadboard()

    def test_breadboard_rendering(self):
        bb_svg = self.bb.element()
        svg = tostring(bb_svg)
        soup = BeautifulSoup(svg, 'xml')
        self.assertTrue(soup.find('rect') is not None, 'breadboard should contain a rectangle')
        self.check_four_lines(soup)
        self.check_labels(soup)

    def check_four_lines(self, soup):
        lines = soup.find_all('line')
        self.assertEqual(4, len(lines),'should have 4 power lines')

    def check_labels(self, soup):
        labels = soup.find_all('text')
        ld = defaultdict(int)
        for label in labels:
            ld[label.text] += 1
        self.assertEqual(4, ld['+'])
        self.assertEqual(4, ld[u'—'])
        for letter in 'abcdefghij':
            self.assertEqual(2, ld[letter])
        for i in range(30):
            self.assertEqual(2, ld[str(i+1)])

    def test_breadboard_connectors(self):
        c = Breadboard().ports
        for i in range(1,26):
            self.assertTrue(('TP%d' % i) in c) # Top Plus power connectors
            self.assertTrue(('TM%d' % i) in c) # Top Minus power connectors
            self.assertTrue(('BP%d' % i) in c) # Bottom Plus power connectors
            self.assertTrue(('BM%d' % i) in c) # Bottom Minus power connectors
        for letter in 'abcdefghij':
            for index in range(0, 30):
                self.assertTrue(('%s%d' % (letter, i+1)) in c) # body connectors





