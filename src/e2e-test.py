from breadboarder.breadboard import Breadboard
from breadboarder.drawing import Drawing, write, Wire


# TODO: add drawable class?



def test_breadboard():
    drawing = Drawing()
    breadboard = Breadboard()
    drawing.add(breadboard)
    breadboard.connect(Wire('red'), 'TP3','a10')
    svg = drawing.svg()
    write(svg, 'svg/foo.svg')

test_breadboard()
