from hamcrest.core.base_matcher import BaseMatcher

from breadboarder.core.project import Point


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




class RectangleMatcher(BaseMatcher):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def _matches(self, item):
        rectangles = item.find_all('rect')
        for rect in rectangles:
            if (self.x == float(rect['x']) and
                self.y == float(rect['y']) and
                self.width == float(rect['width']) and
                self.height == float(rect['height'])):
                    return True
        return False

    def describe_to(self, description):
        description.append('A rectangle(x=%s,y=%s,width=%s,height=%s)' % tuple([str(arg) for arg in [self.x, self.y, self.width, self.height]]))


def contains_svg_rectangle(x, y, width, height):
    return RectangleMatcher(x, y, width, height)

