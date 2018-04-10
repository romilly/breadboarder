import math
from abc import ABCMeta, abstractmethod

from breadboarder.svg.point import Point


class Transform():
    """Represents an atomic svg transformation - a translation, rotation or scaling"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def text(self):
        pass

    @abstractmethod
    def as_matrix(self):
        pass


    def offset(self):
        return 0


class Translation(Transform):
    def __init__(self, vector):
        self.vector = vector

    def text(self):
        return 'translate(%f,%f)' % (self.vector.cartesian_coordinates())

    def as_matrix(self):
        return

    def offset(self):
        return self.vector


class Rotation(Transform):
    def __init__(self, angle, origin=Point(0, 0)):
        self.angle = angle
        self.origin = origin

    def text(self):
        return 'rotate(%f,%f,%f)' % (self.angle, self.origin.x, self.origin.y)