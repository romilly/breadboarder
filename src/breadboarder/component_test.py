from unittest import TestCase

from breadboarder.components import Wire, Button
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


