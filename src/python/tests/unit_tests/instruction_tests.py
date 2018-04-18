from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.core.components import Resistor, DiskCapacitor, Crystal
from breadboarder.core.host import Host
from breadboarder.core.port import Port
from breadboarder.svg.point import Point


class MockBoard(Host):
    def add_components(self):
        pass

    def id_prefix(self):
        return 'HOST'

    def part_type(self):
        return 'Mock Host'

    def description(self):
        return 'Board'

    def __init__(self):
        Host.__init__(self)


class InstructionTests(TestCase):
    def setUp(self):
        host = MockBoard()
        anywhere = Point(0,0)
        self.p1 = Port(host, anywhere, 'p1')
        self.p2 = Port(host, anywhere, 'p2')

    def test_resistor(self):
        r = Resistor('100k', '5%', self.p1, self.p2)
        r.set_id('R1')
        self.check_instruction(r, 'Resistor R1: 100k 5% (Black Brown Blue Gold)')

    def test_capacitor(self):
        c = DiskCapacitor('1n4',self.p1, self.p2)
        c.set_id('C1')
        self.check_instruction(c, 'Capacitor C1: (1n4)')

    def test_crystal(self):
        xtal = Crystal('16MHz', self.p1, self.p2)
        xtal.set_id('X1')
        self.check_instruction(xtal, 'Crystal X1: (16MHz)')

    def check_instruction(self, r, desc):
        assert_that(r.lab_instruction(),
                    equal_to('Connect a %s from Board p1 to Board p2' % desc))
