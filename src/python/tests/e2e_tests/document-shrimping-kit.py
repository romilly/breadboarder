from unittest import TestCase
from hamcrest import assert_that, contains_string

from breadboarder.examples.shrimp_kit import shrimp_kit


class BomTester(TestCase):
    def setUp(self):
        self.project = shrimp_kit()

    def test_bom(self):
        md = self.project.md('shrimp','svg/shrimp-kit.svg')
        assert_that(md, contains_string('## Bill of Materials'))
        assert_that(md, contains_string('### Resistors'))
        assert_that(md, contains_string('R1 (10k 5%)'))

