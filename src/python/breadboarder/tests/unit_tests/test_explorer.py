from unittest import TestCase

from hamcrest import assert_that, close_to, has_items

from breadboarder.core.explorer import Explorer
from breadboarder.core.units import PITCH
from svg.point import Point


class ExplorerTests(TestCase):
    def setUp(self) -> None:
        self.explorer = Explorer()

    def test_has_gpio_header_ports(self) -> None:
        assert_that(list(self.explorer.port_names()),
                    has_items('GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5',
                              'ADC0', 'ADC1', 'ADC2', '3V3', 'GND1', 'GND2'))

    def test_gpio_columns_run_down_the_board_one_pitch_apart(self) -> None:
        self.check_offset('GP0', 'GP5', Point(0, 5 * PITCH))
        self.check_offset('ADC0', 'GND2', Point(0, 5 * PITCH))

    def test_gpio_rows_pair_left_and_right_columns(self) -> None:
        self.check_offset('GP0', 'ADC0', Point(PITCH, 0))
        self.check_offset('GP3', '3V3', Point(PITCH, 0))

    def test_has_170_mini_breadboard_sockets_lettered_a_to_j(self) -> None:
        expected = [row + str(column) for row in 'abcdefghij' for column in range(1, 18)]
        assert_that(list(self.explorer.port_names()), has_items(*expected))

    def check_offset(self, from_port: str, to_port: str, expected: Point) -> None:
        offset = self.explorer[to_port].location() - self.explorer[from_port].location()
        assert_that(offset.x, close_to(expected.x, 1e-9))
        assert_that(offset.y, close_to(expected.y, 1e-9))
