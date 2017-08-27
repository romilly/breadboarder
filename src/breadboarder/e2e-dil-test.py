from breadboarder.breadboard import Breadboard
from breadboarder.dil import atMega328
from breadboarder.drawing import Drawing, write


def test_dil():
    drawing = Drawing()
    breadboard = Breadboard()
    drawing.add(breadboard)
    breadboard.insert(atMega328(), 'f10')
    svg = drawing.svg()
    write(svg, 'svg/dil.svg')

test_dil()
