from unittest import TestCase

from hamcrest import assert_that, is_
from hamcrest.core.base_matcher import BaseMatcher

from breadboarder.components import Wire, Button, Resistor
from breadboarder.dil import atMega328
from breadboarder.drawing import Point


class WireTest(TestCase):
    def test_inserts_itself(self):
        wire = Wire()
        w = wire.connect((Point(1,2),Point(3,4)))
        self.assertEqual(wire.start.x, 1)
        self.assertEqual(wire.start.y, 2)
        self.assertEqual(wire.end().x, 3)
        self.assertEqual(wire.end().y, 4)
        self.assertEqual(w, wire,'check self is returned')


class ButtonTest(TestCase):
    def test_inserts_itself(self):
        button = Button()
        b = button.connect((Point(1,3),))
        self.assertEqual(button.start.x, 1)
        self.assertEqual(button.start.y, 3)
        self.assertEqual(b, button,'check self is returned')


class DilTest(TestCase):
    def test_inserts_itself(self):
        dil = atMega328()
        d = dil.connect((Point(2,5),))
        self.assertEqual(dil.start.x, 0)
        self.assertEqual(dil.start.y, 6)
        self.assertEqual(d, dil,'check self is returned')


class PointMatcher(BaseMatcher):
    def __init__(self, point):
        self.expected_point = point

    def _matches(self, item):
        if isinstance(self.expected_point, Point) and isinstance(item, Point):
            return self.expected_point.x == item.x and self.expected_point.y == item.y
        return False

    def describe_to(self, description):
        description.append(str(self.expected_point))


def is_located_at(point):
    return PointMatcher(point)


class ResistorTest(TestCase):
    def test_inserts_itself(self):
        resistor = Resistor('330K')
        r = resistor.connect((Point(1,2), Point(1,10)))
        assert_that(resistor.start, is_located_at(Point(1,2)))
        assert_that(resistor.end, is_located_at(Point(1,10)))
        assert_that(r, is_(resistor))






