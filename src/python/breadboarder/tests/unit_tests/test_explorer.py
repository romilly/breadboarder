from unittest import TestCase

from hamcrest import (assert_that, close_to, equal_to, greater_than, greater_than_or_equal_to,
                      has_items, less_than_or_equal_to)

from breadboarder.core.components import Wire
from breadboarder.core.explorer import BOARD_HEIGHT, BOARD_WIDTH, Explorer
from breadboarder.core.project import Project
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

    def test_mini_breadboard_columns_are_one_pitch_apart(self) -> None:
        self.check_offset('a1', 'a17', Point(16 * PITCH, 0))
        self.check_offset('j1', 'j17', Point(16 * PITCH, 0))

    def test_mini_breadboard_rows_run_j_to_f_then_e_to_a_down_the_board(self) -> None:
        self.check_offset('j1', 'f1', Point(0, 4 * PITCH))
        self.check_offset('e1', 'a1', Point(0, 4 * PITCH))

    def test_mini_breadboard_halves_are_separated_by_a_centre_channel(self) -> None:
        self.check_offset('f1', 'e1', Point(0, 3 * PITCH))

    def test_gpio_header_is_right_of_the_mini_breadboard(self) -> None:
        gp0 = self.explorer['GP0'].location()
        assert_that(gp0.x - self.explorer['a17'].location().x, greater_than(PITCH))

    def test_right_croc_clip_pads_run_down_the_right_edge_in_printed_order(self) -> None:
        names = ['PAD_3V3', 'PAD_ADC3', 'PAD_GND', 'PAD_ADC4', 'PAD_ADC5']
        pads = [self.explorer[name].location() for name in names]
        right_of_gpio = greater_than(self.explorer['ADC0'].location().x)
        for pad in pads:
            assert_that(pad.x, close_to(pads[0].x, 1e-9))
            assert_that(pad.x, right_of_gpio)
        for upper, lower in zip(pads, pads[1:]):
            assert_that(lower.y, greater_than(upper.y))

    def test_left_croc_clip_pad_is_left_of_the_mini_breadboard(self) -> None:
        assert_that(self.explorer['a1'].location().x,
                    greater_than(self.explorer['PAD_GND_L'].location().x))

    def test_instructions_name_the_explorer_and_its_sockets(self) -> None:
        wire = Wire('red', self.explorer['3V3'], self.explorer['a1'])
        Project().add(self.explorer, wire)
        assert_that(self.explorer.instruction(),
                    equal_to('Take a Pimoroni Explorer (RP2350) (EXP-1)'))
        assert_that(wire.instruction(),
                    equal_to('Connect a Red Jumper Wire (M-M) from EXP-1 socket 3V3 to EXP-1 socket a1'))

    def test_ports_move_with_the_explorer(self) -> None:
        before = self.explorer['a1'].location()
        self.explorer.move_to(Point(100, 50))
        self.check_offset_from(before, 'a1', Point(100, 50))

    def test_ports_turn_with_the_explorer(self) -> None:
        self.explorer.rotate(90)
        # on screen (y down), rotate(90) turns "down the board" into "to the left"
        self.check_offset('GP0', 'GP5', Point(-5 * PITCH, 0))
        self.check_offset('a1', 'a17', Point(0, 16 * PITCH))

    def test_every_port_lies_on_the_board(self) -> None:
        for port in self.explorer.ports():
            location = port.location()
            assert_that(location.x, greater_than_or_equal_to(0), port.portname)
            assert_that(location.x, less_than_or_equal_to(BOARD_WIDTH), port.portname)
            assert_that(location.y, greater_than_or_equal_to(0), port.portname)
            assert_that(location.y, less_than_or_equal_to(BOARD_HEIGHT), port.portname)

    def test_drawing_shows_the_labels_printed_on_the_board(self) -> None:
        texts = list(self.explorer.element().itertext())
        assert_that(texts, has_items('Explorer',
                                     'GP0', 'GP1', 'GP2', 'GP3', 'GP4', 'GP5',
                                     'ADC0', 'ADC1', 'ADC2', '3V3', 'GND',
                                     '3.3V', 'ADC3', 'ADC4', 'ADC5'))

    def check_offset_from(self, start: Point, to_port: str, expected: Point) -> None:
        offset = self.explorer[to_port].location() - start
        assert_that(offset.x, close_to(expected.x, 1e-9))
        assert_that(offset.y, close_to(expected.y, 1e-9))

    def check_offset(self, from_port: str, to_port: str, expected: Point) -> None:
        self.check_offset_from(self.explorer[from_port].location(), to_port, expected)
