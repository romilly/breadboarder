from unittest import TestCase

from hamcrest import assert_that, close_to, contains_string, equal_to, has_items

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire
from breadboarder.core.pico import Pico, Pico2, Pico2W, PicoW
from breadboarder.core.project import Project
from breadboarder.core.units import PITCH
from svg.point import Point


class PicoTests(TestCase):
    def setUp(self) -> None:
        self.breadboard = Breadboard()
        self.pico = Pico(self.breadboard['c5'])

    def test_pins_1_to_20_run_along_the_pin_1_row(self) -> None:
        self.assert_in_socket('GP0', 'c5')
        self.assert_in_socket(3, 'c7')
        self.assert_in_socket('GP15', 'c24')

    def test_pins_21_to_40_run_back_along_the_row_five_letters_on(self) -> None:
        self.assert_in_socket('GP16', 'h24')
        self.assert_in_socket('VBUS', 'h5')
        self.assert_in_socket(40, 'h5')
        self.assert_in_socket('3V3', 'h9')

    def test_gnd_means_pin_38_and_agnd_pin_33(self) -> None:
        self.assert_in_socket('GND', 'h7')
        self.assert_in_socket('AGND', 'h12')

    def test_instruction_names_the_model_and_where_pin_1_goes(self) -> None:
        Project().add(self.breadboard, self.pico)
        assert_that(self.pico.instruction(),
                    equal_to('Insert the Raspberry Pi Pico (PICO1), USB end to the left, '
                             'with pin 1 (GP0) in BB1 socket c5'))

    def test_wires_to_pico_pins_name_the_socket_and_the_pin(self) -> None:
        wire = Wire('red', self.pico['3V3'], self.breadboard['TP1'])
        Project().add(self.breadboard, self.pico, wire)
        assert_that(wire.instruction(),
                    equal_to('Connect a Red Jumper Wire (M-M) from BB1 socket h9 (PICO1 3V3) '
                             'to BB1 socket TP1'))

    def test_models_differ_in_name_and_chip(self) -> None:
        port = self.breadboard['c5']
        names = [(cls(port).description(), cls(port).chip) for cls in (Pico, PicoW, Pico2, Pico2W)]
        assert_that(names, equal_to([('Raspberry Pi Pico', 'RP2040'),
                                     ('Raspberry Pi Pico W', 'RP2040'),
                                     ('Raspberry Pi Pico 2', 'RP2350'),
                                     ('Raspberry Pi Pico 2 W', 'RP2350')]))

    def test_drawing_shows_model_chip_and_pin_names(self) -> None:
        texts = list(Pico2W(self.breadboard['c5']).element().itertext())
        assert_that(texts, has_items('Pico 2 W', 'RP2350', 'GP0', 'VBUS', 'GND'))

    def test_pin_1_must_be_in_rows_a_to_e(self) -> None:
        with self.assertRaises(ValueError):
            Pico(self.breadboard['h5'])

    def test_needs_twenty_columns(self) -> None:
        with self.assertRaises(ValueError) as raised:
            Pico(self.breadboard['c12'])
        assert_that(str(raised.exception), contains_string('20'))

    def assert_in_socket(self, pin, socket: str) -> None:
        actual = self.pico[pin].location()
        expected = self.breadboard[socket].location()
        assert_that(actual.x, close_to(expected.x, 1e-9))
        assert_that(actual.y, close_to(expected.y, 1e-9))
