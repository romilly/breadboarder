from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Potentiometer, RotaryPotentiometer
from breadboarder.core.project import Project


class RotaryPotentiometerTests(TestCase):
    def setUp(self) -> None:
        self.breadboard = Breadboard()

    def test_instruction_names_pin_1(self) -> None:
        pot = RotaryPotentiometer('10K', self.breadboard['j15'])
        Project().add(self.breadboard, pot)
        assert_that(pot.instruction(),
                    equal_to('Insert the 10K Rotary potentiometer (VR1) with pin 1 in BB1 socket j15'))

    def test_is_numbered_apart_from_trimmer_potentiometers(self) -> None:
        trimmer = Potentiometer('10k', self.breadboard['a5'])
        rotary = RotaryPotentiometer('10K', self.breadboard['j15'])
        Project().add(self.breadboard, trimmer, rotary)
        assert_that([trimmer.id(), rotary.id()], equal_to(['VR1', 'VR2']))
