import os

from breadboarder.author.illustrator import Illustrator
from svg.core import write


def write_svg(project, svg_file):
    illustrator = Illustrator()
    for step in project.steps():
        illustrator.take(step)
    write(illustrator.svg(), os.path.join('..', '..', 'svg', svg_file))
