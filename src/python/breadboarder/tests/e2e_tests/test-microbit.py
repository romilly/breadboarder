from breadboarder.core.microbit import Microbit
from breadboarder.core.project import Project
from breadboarder.core.svg import write


def test_microbit():
    p = Project()
    p.add(Microbit())
    svg = p.element()
    write(svg, 'svg/microbit.svg')


test_microbit()