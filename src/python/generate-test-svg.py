#! /usr/bin/env python3

import sys
# TODO: ugh! below, temporary fix until I put svg on PyPi
sys.path.insert(0,'/home/romilly/git/active/svg/src')
from breadboarder.examples import *
from breadboarder.tests.helpers.svg_writer import write_svg

write_svg(dil(), 'dil.svg')
write_svg(wire(), 'wire.svg')
write_svg(two_hosts(), 'two-hosts.svg')
write_svg(two_hosts_wired(), 'two-hosts-wired.svg')
write_svg(shrimp(), 'shrimp.svg')
# write_svg(network(), 'network.svg')
write_svg(bar(), 'bar.svg')
