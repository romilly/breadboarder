import math


def angle(start, end):
    x , y = (end-start).cartesian_coords()
    return math.degrees(math.atan2(y, x))