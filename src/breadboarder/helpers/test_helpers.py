from hamcrest.core.base_matcher import BaseMatcher

from breadboarder.drawing import Point


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