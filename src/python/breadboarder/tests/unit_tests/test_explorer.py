from unittest import TestCase

from hamcrest import assert_that, has_items

from breadboarder.core.explorer import Explorer


class ExplorerTests(TestCase):
    def setUp(self) -> None:
        self.explorer = Explorer()

    def test_has_gpio_header_ports(self) -> None:
        assert_that(list(self.explorer.port_names()),
                    has_items('GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5',
                              'ADC0', 'ADC1', 'ADC2', '3V3', 'GND1', 'GND2'))
