from unittest import TestCase

import math
from hamcrest import assert_that, is_

from breadboarder.drawing import Point


def angle(start, end):
    x , y = (end-start).cartesian_coords()
    return math.degrees(math.atan2(y, x))


class AngleTest(TestCase):
    def test_calculates_angles(self):
        assert_that(angle(Point(0,0),Point(1,0)), is_(0))
        assert_that(angle(Point(0,0),Point(0,1)), is_(90))
        assert_that(angle(Point(0,0),Point(0,-1)), is_(-90))