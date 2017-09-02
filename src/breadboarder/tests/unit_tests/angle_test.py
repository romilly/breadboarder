from unittest import TestCase

from hamcrest import assert_that, is_

from breadboarder.drawing import Point
from breadboarder.helpers.angles import angle


class AngleTest(TestCase):
    def test_calculates_angles(self):
        assert_that(angle(Point(0,0),Point(1,0)), is_(0))
        assert_that(angle(Point(0,0),Point(0,1)), is_(90))
        assert_that(angle(Point(0,0),Point(0,-1)), is_(-90))