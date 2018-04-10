from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, Button, Resistor, Diode, Crystal, DiskCapacitor
from breadboarder.core.dil import atMega328, pcf8574
from breadboarder.core.project import Project



# TODO: add image-based testing
from breadboarder.svg.svg import Point, write


def test_dil():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(atMega328(breadboard['f10']))
    project.add(pcf8574(breadboard['f1']))
    project.add(Wire('red',breadboard['g1'],breadboard['TP1']))
    project.add(Wire('black',breadboard['a8'],breadboard['BM6']))
    project.add(Wire('blue',breadboard['g3'],breadboard['g10']))
    project.add(Wire('green',breadboard['h2'],breadboard['h11']))
    project.add(Wire('lightgrey',breadboard['d1'],breadboard['BM1']))
    project.add(Wire('lightgrey',breadboard['d2'],breadboard['BM2']))
    project.add(Wire('lightgrey',breadboard['d3'],breadboard['BM3']))
    project.add(Button(breadboard['d8']))
    project.add(Resistor('330k', '5%', breadboard['g17'],breadboard['g22']))
    project.add(Resistor('2R7', '5%', breadboard['g25'],breadboard['a25']))
    project.add(Resistor('1M2', '5%', breadboard['g27'],breadboard['a30']))
    project.add(Crystal('16Mz', breadboard['g24'],breadboard['a29']))
    project.add(Diode('1N4001', breadboard['d24'],breadboard['f24']))
    project.add(DiskCapacitor('1N5', breadboard['a13'],breadboard['a18']))
    svg = project.element()
    write(svg, 'svg/dil.svg')

test_dil()
