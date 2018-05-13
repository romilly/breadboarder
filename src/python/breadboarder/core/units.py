PITCH = 0.1*90 # 0.1", 90 DPI


def to_cms(distance):
    return distance * PITCH / 0.254


def cms(*distances):
    if len(distances) == 1:
        return to_cms(distances[0])
    return [to_cms(distance) for distance in distances]


def to_ins(distance):
    return distance * PITCH * 10


def ins(*distances):
    if len(distances) == 1:
        return to_ins(distances[0])
    return [to_ins(distance) for distance in distances]

def v(x, y):  # for brevity, which is the soul of wit
    return vector(*cms(x, y))


def point(x, y):
    return Point(*cms(x, y))


def sv(x, y):
    return v(x*0.025, y*0.025)


def up(y):
    return sv(0, -y)


def down(y):
    return sv(0, y)


def left(x):
    return sv(-x,0)


def right(x):
    return sv(x,0)


def up_left(x, y=None):
    y = x if not y else y
    return sv(-x,-y)


def up_right(x, y=None):
    y = x if not y else y
    return sv(x, -y)


def down_left(x, y=None):
    y = x if not y else y
    return sv(-x,y)


def down_right(x, y=None):
    y = x if not y else y
    return sv(x,y)


