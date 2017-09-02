from breadboarder.breadboard import Breadboard
from breadboarder.components import Wire, Button, Resistor
from breadboarder.dil import atMega328, pcf8574
from breadboarder.drawing import Drawing, write


def test_dil():
    drawing = Drawing()
    breadboard = Breadboard()
    drawing.add(breadboard)
    breadboard.connect(atMega328(), 'f10')
    breadboard.connect(pcf8574(), 'f1')
    breadboard.connect(Wire('red'),'g1','TP1')
    breadboard.connect(Wire('black'),'a8','BM6')
    breadboard.connect(Wire('blue'),'g3','g10')
    breadboard.connect(Wire('green'),'h2','h11')
    breadboard.connect(Wire('lightgrey'),'d1','BM1')
    breadboard.connect(Wire('lightgrey'),'d2','BM2')
    breadboard.connect(Wire('lightgrey'),'d3','BM3')
    breadboard.connect(Button(), 'd8')
    breadboard.connect(Resistor('330K'), 'g17','g22')
    svg = drawing.svg()
    write(svg, 'svg/dil.svg')

test_dil()
