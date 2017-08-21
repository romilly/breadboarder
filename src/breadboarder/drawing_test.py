from unittest import TestCase


class Drawing(object):
    def svg(self):
        pass


class DrawingTest(TestCase):
    def test_builds_svg(self):
        drawing = Drawing()
        svg = drawing.svg()
        self.assertTrue('<svg' in svg)