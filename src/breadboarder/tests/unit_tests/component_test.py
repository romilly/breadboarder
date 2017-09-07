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

def test_port(x, y):
    return Port(MockHost(), Point(x,y), 'whocares?')


class DilTest(TestCase):
    def test_inserts_itself(self):
        dil = atMega328(test_port(2, 5))
        assert_that(dil.transformations[0].vector, is_located_at(Point(0,6)),'dil should be offset for visual fidelity')


class ResistorTest(TestCase):
    def test_inserts_itself(self):
        r = Resistor('330k', '5%', test_port(1,2), test_port(1,10))
        assert_that(r.start, is_located_at(Point(1,2)))
        assert_that(r.end, is_located_at(Point(1,10)))

    def test_aligns_itself(self):
        r = Resistor('2M7','1%', test_port(0,1), test_port(40, 1))
        svg = tostring(r.svg())
        soup = BeautifulSoup(svg, 'xml')
        assert_that(soup, contains_svg_rectangle(0, 0, 27, 9)) # relative to resistor body start








