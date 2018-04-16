from breadboarder.examples.shrimp_kit import shrimp_kit
from breadboarder.svg.svg import write


def draw_shrimp_kit():
    project = shrimp_kit()
    svg = project.element()
    write(svg, 'svg/shrimp-kit.svg')


draw_shrimp_kit()