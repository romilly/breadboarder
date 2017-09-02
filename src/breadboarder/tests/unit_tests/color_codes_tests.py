from unittest import TestCase

from decimal import Decimal
from hamcrest import assert_that, is_

from breadboarder.helpers.color_codes import ColorCode


class ColorCodeTest(TestCase):
    def setUp(self):
        self.cc = ColorCode()

    def test_converts_string_to_value(self):
        assert_that(self.cc.parse('2R7'), is_(Decimal('2.7')))
        assert_that(self.cc.parse('27R'),is_(27))
        assert_that(self.cc.parse('820R'),is_(820))
        assert_that(self.cc.parse('2k7'),is_(2700))
        assert_that(self.cc.parse('27k'),is_(27000))
        assert_that(self.cc.parse('100k'),is_(100000))
        assert_that(self.cc.parse('1M'),is_(1000000))
        assert_that(self.cc.parse('1M2'),is_(1200000))

    def tests_converts_value_to_color_code(self):
        assert_that(self.cc.bands_for(Decimal('2.7')),is_(['red','violet','gold']))
