import math


class Point():
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        # Hademard (direct) product
        return Point(self.x*other.x, self.y*other.y)


    def v_flip(self):
        # flip about vertical axis
        return Point(-self.x, self.y)

    def scale(self, factor):
        return Point(self.x * factor, self.y * factor)

    def __str__(self):
        return 'a Point(%s,%s)' % (str(self.x),str(self.y))

    def cartesian_coordinates(self):
        return (self.x, self.y)

    def r(self):
        return math.sqrt(sum((self*self).cartesian_coordinates()))

    def theta(self):
        return math.degrees(math.atan2(self.y, self.x))

    def format(self):
        return '%s %s' % (str(self.x),str(self.y))


