from unittest import TestCase

from hamcrest import assert_that, is_

from breadboarder.components import Wire, Button, Resistor
from breadboarder.dil import atMega328
from breadboarder.drawing import Point
from breadboarder.helpers.test_helpers import is_located_at


class WireTest(TestCase):
    def test_inserts_itself(self):
        wire = Wire()
        w = wire.connect((Point(1,2),Point(3,4)))
        assert_that(wire.start, is_located_at(Point(1,2)))
        assert_that(wire.end(), is_located_at(Point(3,4)))
        self.assertEqual(w, wire,'check self is returned')


class ButtonTest(TestCase):
    def test_inserts_itself(self):
        button = Button()
        b = button.connect((Point(1,3),))
        assert_that(button.start, is_located_at(Point(1,3)))
        self.assertEqual(b, button,'check self is returned')


class DilTest(TestCase):
    def test_inserts_itself(self):
        dil = atMega328()
        d = dil.connect((Point(2,5),))
        assert_that(dil.start, is_located_at(Point(0,6)),'dil should be offset for visual fidelity')
        self.assertEqual(d, dil,'check self is returned')


class ResistorTest(TestCase):
    def test_inserts_itself(self):
        resistor = Resistor('330K')
        r = resistor.connect((Point(1,2), Point(1,10)))
        assert_that(resistor.start, is_located_at(Point(1,2)))
        assert_that(resistor.end, is_located_at(Point(1,10)))
        assert_that(r, is_(resistor))





