"""Draw a Pimoroni Explorer with an LED circuit on its mini breadboard.

Writes svg/explorer.svg relative to the current directory."""
from breadboarder.author.illustrator import Illustrator
from breadboarder.core.components import LED, Resistor, Wire
from breadboarder.core.explorer import Explorer
from breadboarder.core.project import Project
from svg.core import write
from svg.point import Point


def draw_explorer() -> None:
    project = Project()
    explorer = Explorer().move_to(Point(20, 20))
    project.add(explorer,
                Wire('yellow', explorer['GP0'], explorer['e10']),
                Resistor('220R', '5%', explorer['c10'], explorer['c14']),
                LED('red', explorer['b14'], explorer['b15']),
                Wire('black', explorer['GND1'], explorer['a15']))
    illustrator = Illustrator(330, 400)
    for step in project.steps():
        illustrator.take(step)
    write(illustrator.svg(), 'svg/explorer.svg')


draw_explorer()
