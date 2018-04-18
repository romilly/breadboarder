from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, Crystal, Resistor, DiskCapacitor, LED, atMega328
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point


def shrimp_kit():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90., Point(40,400)).move_to(Point(40,400))
    project.add(cp,
                Wire('green',cp['GND'],breadboard['a10']),
                Wire('red',cp['5V'],breadboard['a9']),
                Wire('yellow',cp['TXD'],breadboard['a4']),
                Wire('orange',cp['RXD'],breadboard['a5']),
                Wire('brown',cp['DTR'],breadboard['a2']),
                atMega328(breadboard['f3']),
                Wire('red',breadboard['d9'],breadboard['g11']),
                Wire('green',breadboard['d10'],breadboard['g9']),
                Crystal('16Mz', breadboard['a11'], breadboard['b12']),
                Resistor('10k', '5%', breadboard['b3'], breadboard['b9']),
                Resistor('1k', '5%', breadboard['j9'], breadboard['j17']),
                DiskCapacitor('1N4', breadboard['c2'], breadboard['c3']),
                LED('red',breadboard['g12'],breadboard['g17']))
    return project
