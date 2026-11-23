from unittest import TestCase
from hamcrest import assert_that, equal_to
from svg.point import Point

from breadboarder.core.components import Resistor, DiskCapacitor, Crystal, Potentiometer, Wire
from breadboarder.core.project import Project
from breadboarder.core.host import Host
from breadboarder.core.port import Port


class MockBoard(Host):
    def add_components(self):
        pass

    def id_prefix(self):
        return 'HOST'

    def part_type(self):
        return 'Mock Host'

    def description(self):
        return 'Board'

    def __init__(self, id,):
        Host.__init__(self)
        self.set_id(id)


class InstructionTests(TestCase):
    def setUp(self):
        host = MockBoard('bb')
        anywhere = Point(0,0)
        self.p1 = Port(host, anywhere, 'p1')
        self.p2 = Port(host, anywhere, 'p2')
        host.add_port(self.p1)
        host.add_port(self.p2)

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

    def test_wire_to_a_pad_is_a_croc_clip_lead_named_by_the_pad_label(self):
        pad = Port(self.p1.host, Point(0, 0), 'PAD_X', port_type='pad', label='X')
        self.p1.host.add_port(pad)
        assert_that(Wire('red', pad, self.p2).instruction(),
                    equal_to('Connect a Red Croc-clip Lead (Clip-M) from bb pad X to bb socket p2'))

    def test_potentiometer_is_inserted_by_pin_1(self):
        pot = Potentiometer('10k', self.p1)
        Project().add(pot)
        assert_that(pot.instruction(),
                    equal_to('Insert the 10k Potentiometer (VR1) with pin 1 in bb socket p1'))

    def check_instruction(self, component, desc):
        assert_that(component.instruction(),
                    equal_to('Connect a %s from bb socket p1 to bb socket p2' % desc))
