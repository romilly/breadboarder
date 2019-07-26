from breadboarder.examples import *
from src.tests.helpers.svg_writer import write_svg

write_svg(dil(), 'dil.svg')
write_svg(wire(), 'wire.svg')
write_svg(two_hosts(), 'two-hosts.svg')
write_svg(shrimp(), 'shrimp.svg')
