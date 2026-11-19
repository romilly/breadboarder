from breadboarder.core.project import Project
from breadboarder.core.explorer import Explorer
from breadboarder.core.components import LED, Resistor, Wire
from svg.point import Point

project = Project()
explorer = Explorer().move_to(Point(20, 20))
project.add(explorer,
            Wire('yellow', explorer['GP0'], explorer['e10']),
            Resistor('220R', '5%', explorer['c10'], explorer['c14']),
            LED('red', explorer['b14'], explorer['b15']),
            Wire('black', explorer['GND1'], explorer['a15']),
            Wire('red', explorer['PAD_3V3'], explorer['j1']))
