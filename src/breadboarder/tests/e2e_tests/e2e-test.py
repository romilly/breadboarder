from breadboarder.core.breadboard import Breadboard
from breadboarder.core.drawing import Drawing, write

from breadboarder.core.components import Wire


def test_breadboard():
    drawing = Drawing()
    breadboard = Breadboard()
    drawing.add(breadboard)
    breadboard.connect(Wire('red'), 'TP3','a10')
    svg = drawing.svg()
    write(svg, 'svg/foo.svg')

test_breadboard()
