#! /usr/bin/env python3

from breadboarder.examples import *
from breadboarder.tests.helpers.svg_writer import write_svg

write_svg(dil(), 'dil.svg')
write_svg(wire(), 'wire.svg')
write_svg(two_hosts(), 'two-hosts.svg')
write_svg(two_hosts_wired(), 'two-hosts-wired.svg')
write_svg(shrimp(), 'shrimp.svg')
