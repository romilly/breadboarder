from breadboarder.anns.layer import Layer, Network
from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, Button, Resistor, Diode, Crystal, DiskCapacitor, atMega328, pcf8574, LED
from breadboarder.core.cp2102 import CP2102
from breadboarder.core.project import Project
from svg.svg import Point


def dil():
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
    return project


def two_hosts():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90, Point(40, 400)).move_to(Point(40,400))
    project.add(cp)
    return project


def shrimp():
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


def wire():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(Wire('red', breadboard['g1'], breadboard['TP1']))
    return project


def two_hosts_wired():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    cp = CP2102().rotate(-90., Point(40,400)).move_to(Point(40,400))
    project.add(cp)
    project.add(Wire('red',cp['5V'],breadboard['a1']))
    return project


def network():
    project = Project()
    l1 = Layer(nodes=3, fill='red')
    l2 = Layer()
    l2.move_to(Point(0, 25))
    l3 = Layer()
    l3.move_to(Point(0, 50))
    l4 = Layer(nodes=2, fill='green')
    l4.move_to(Point(0, 75))
    network = Network(l1,l2,l3,l4)
    project.add(network)
    return project

def bar():
    project = Project()
    breadboard = Breadboard().move_to(Point(20, 20))
    project.add(breadboard)
    project.add(Wire('green', breadboard['g1'], breadboard['TP1']))
    return project




