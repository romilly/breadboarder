from unittest import TestCase
from xml.etree.ElementTree import tostring

from breadboarder.core.breadboard import Port, Breadboard
from breadboarder.core.dil import atMega328
from breadboarder.core.project import Point
from bs4 import BeautifulSoup
from hamcrest import assert_that, is_

from breadboarder.core.components import Wire, Button, Resistor
from breadboarder.helpers.test_helpers import is_located_at, contains_svg_rectangle


class WireTest(TestCase):
    def test_inserts_itself(self):
        wire = Wire('black', Port(MockHost(), Point(1,2),'one'), Port(MockHost(), Point(3,4), 'two'))
        assert_that(wire.start, is_located_at(Point(1,2)))
        assert_that(wire.end(), is_located_at(Point(3,4)))


class MockHost():
    def __init__(self):
        self.origin = Point(0,0)


class ButtonTest(TestCase):
    def test_inserts_itself(self):
        button = Button(Port(MockHost(), Point(1,3), 'doesnotmatter'))
        assert_that(button.start, is_located_at(Point(1,3)))


class DilTest(TestCase):
    def test_inserts_itself(self):
        dil = atMega328()
        d = dil.connect((Point(2,5),))
        assert_that(dil.start, is_located_at(Point(0,6)),'dil should be offset for visual fidelity')
        self.assertEqual(d, dil,'check self is returned')


class ResistorTest(TestCase):
    def setUp(self):
        self.resistor = Resistor('330k')

    def test_inserts_itself(self):
        r = self.resistor.connect((Point(1,2), Point(1,10)))
        assert_that(r, is_(self.resistor), 'check self is returned')
        assert_that(r.start, is_located_at(Point(1,2)))
        assert_that(r.end, is_located_at(Point(1,10)))

    def test_aligns_itself(self):
        r = self.resistor.connect((Point(0,1), Point(40, 1)))
        svg = tostring(r.svg())
        soup = BeautifulSoup(svg, 'xml')
        assert_that(soup, contains_svg_rectangle(0, 0, 27, 9)) # relative to resistor body start








