from unittest import TestCase
from hamcrest import assert_that, contains_string

from breadboarder.author.bom import BomWriter
from breadboarder.author.instructions import InstructionsBuilder
from breadboarder.examples.shrimp_kit import shrimp_kit



class DocsTester(TestCase):
    def setUp(self):
        self.project = shrimp_kit()

    def test_bom(self):
        md = BomWriter().markdown(self.project.build_bom())
        assert_that(md, contains_string('## Bill of Materials'))
        assert_that(md, contains_string('### Resistors'))
        assert_that(md, contains_string('### CP2102\n'))
        assert_that(md, contains_string('R1: 10k 5% (Black Brown Yellow Gold)'))
        # TODO: add M-M to wire description
        assert_that(md, contains_string('Red Jumper Wire'))

    def test_instructions(self):
        builder = InstructionsBuilder()
        self.project.build_bom()
        self.project.welcome(builder)
        md = builder.instructions().markdown()
        print(md)
        assert_that(md, contains_string('Breadboard'))
        assert_that(md, contains_string('Red Jumper Wire'))
        # svgs =



