
"""
def button(left, right, y, label):
    width = right - left
    swidth = 12
    radius = 2
    wlength = (width - swidth)/2
    sleft = left + wlength
    sright = sleft + swidth
    mid = (sleft + sright)/ 2
    twire = wire(sleft, y+4, sright, y+4)
    vwire = wire(mid, y, mid, y+4)
    lwire = wire(left, y+10, sleft, y+10)
    lcirc = circle(sleft+radius, y+10, radius, style='stroke:black;fill:none')
    rwire = wire(sright, y+10, right, y+10)
    rcirc = circle(sright-radius, y+10, radius, style='stroke:black;fill:none')
    txt = text(right+2, y+6, label)
    return group(twire, vwire, lwire, lcirc, rwire, rcirc, txt, style='font-size:4pt')
"""
from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Point, GroupedDrawable, Rectangle


class Button(GroupedDrawable):
    def __init__(self):
        GroupedDrawable.__init__(self, Point(0,0))
        width = Breadboard.PITCH * 3
        height = Breadboard.PITCH * 3 - 6
        self.add(Rectangle(width, height))
