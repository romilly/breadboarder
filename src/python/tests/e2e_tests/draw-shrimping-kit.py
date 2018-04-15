from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, Crystal, Resistor, DiskCapacitor, LED
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.dil import atMega328
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point, write


def draw_shrimp_kit():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90., Point(40,400)).move_to(Point(40,400))
    project.add(Wire('green',cp['GND'],breadboard['a10']))
    project.add(Wire('red',cp['5V'],breadboard['a9']))
    project.add(Wire('yellow',cp['TXD'],breadboard['a4']))
    project.add(Wire('orange',cp['RXD'],breadboard['a5']))
    project.add(Wire('brown',cp['DTR'],breadboard['a2']))
    project.add(cp)
    project.add(atMega328(breadboard['f3']))
    project.add(Wire('red',breadboard['d9'],breadboard['g11']))
    project.add(Wire('green',breadboard['d10'],breadboard['g9']))
    project.add(Crystal('16Mz', breadboard['a11'], breadboard['b12']))
    project.add(Resistor('10k', '5%', breadboard['b3'], breadboard['b9']))
    project.add(Resistor('1k', '5%', breadboard['j9'], breadboard['j17']))
    project.add(DiskCapacitor('1N4', breadboard['c2'], breadboard['c3']))
    project.add(LED('red',breadboard['g12'],breadboard['g17']))
    svg = project.element()
    print(project.md('shrimp','svg/shrimp-kit.svg'))
    write(svg, 'svg/shrimp-kit.svg')


draw_shrimp_kit()