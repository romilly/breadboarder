from breadboarder.core.breadboard import Breadboard
from breadboarder.core.dil import atMega328, pcf8574
from breadboarder.core.project import Project, write

from breadboarder.core.components import Wire, Button, Resistor, Crystal


def test_dil():
    project = Project()
    breadboard = Breadboard()
    project.add(breadboard)
    breadboard.connect(atMega328(), 'f10')
    breadboard.connect(pcf8574(), 'f1')
    project.add(Wire('red',breadboard['g1'],breadboard['TP1']))
    project.add(Wire('black',breadboard['a8'],breadboard['BM6']))
    project.add(Wire('blue',breadboard['g3'],breadboard['g10']))
    project.add(Wire('green',breadboard['h2'],breadboard['h11']))
    project.add(Wire('lightgrey',breadboard['d1'],breadboard['BM1']))
    project.add(Wire('lightgrey',breadboard['d2'],breadboard['BM2']))
    project.add(Wire('lightgrey',breadboard['d3'],breadboard['BM3']))
    project.add(Button(breadboard['d8']))
    breadboard.connect(Resistor('330k'), 'g17','g22')
    breadboard.connect(Resistor('2R7'), 'g25','a25')
    breadboard.connect(Resistor('1M2'), 'g27','a30')
    breadboard.connect(Crystal('16Mz'), 'g24','a29')
    svg = project.svg()
    write(svg, 'svg/dil.svg')

test_dil()
