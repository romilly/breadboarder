from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import LED, RgbLed
from breadboarder.core.project import Project


class RgbLedTests(TestCase):
    def setUp(self) -> None:
        self.breadboard = Breadboard()

    def test_instruction_names_pin_1_and_the_long_common_leg(self) -> None:
        led = RgbLed(self.breadboard['a10'])
        Project().add(self.breadboard, led)
        assert_that(led.instruction(),
                    equal_to('Insert the Common-cathode RGB LED (RGB1) with pin 1 (R) in BB1 socket a10'
                             ' and pin 2 (GND, the long leg) in BB1 socket a11'))

    def test_is_numbered_apart_from_plain_leds(self) -> None:
        rgb = RgbLed(self.breadboard['a10'])
        plain = LED('red', self.breadboard['b20'], self.breadboard['b21'])
        Project().add(self.breadboard, rgb, plain)
        assert_that([rgb.id(), plain.id()], equal_to(['RGB1', 'LED1']))
