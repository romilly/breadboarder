from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Drawing, write


def test_breadboard():
    drawing = Drawing()
    drawing.add(Breadboard())
    svg = drawing.svg()
    write(svg, 'svg/foo.svg')

test_breadboard()
