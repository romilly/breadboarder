import os

from breadboarder.author.illustrator import Illustrator
from svg.svg import write


def write_svg(project, svg_file):
    illustrator = Illustrator()
    for step in project.steps():
        illustrator.take(step)
    write(illustrator.svg(), os.path.join('..', '..', 'svg', svg_file))
