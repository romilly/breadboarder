from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.core.microbit import MicrobitFront, MicrobitBack
from breadboarder.core.project import Project
from breadboarder.core.svg import write

EXPECTED_FRONT_FILE_NAME = 'microbit-front.svg'
MICROBIT_FRONT_SVG = 'svg/%s' % EXPECTED_FRONT_FILE_NAME

EXPECTED_BACK_FILE_NAME = 'microbit-back.svg'
MICROBIT_BACK_SVG = 'svg/%s' % EXPECTED_BACK_FILE_NAME


def read(filename):
    try:
        with open(filename) as f:
            return f.read()
    except:
        raise Exception("can't open %s" % filename)


class MicrobitFrontTest(TestCase):
    def test_writes_correct_file_contents(self):
        p = Project()
        p.add(MicrobitFront())
        svg = p.element()
        write(svg, MICROBIT_FRONT_SVG)
        op = read(MICROBIT_FRONT_SVG)
        expected = read('test-data/%s' % EXPECTED_FRONT_FILE_NAME)
        assert_that(op, equal_to(expected))


class MicrobitBackTest(TestCase):
       def test_writes_correct_file_contents(self):
        p = Project()
        p.add(MicrobitBack())
        svg = p.element()
        write(svg, MICROBIT_BACK_SVG)
        op = read(MICROBIT_BACK_SVG)
        # expected = read('test-data/%s' % EXPECTED_BACK_FILE_NAME)
        # assert_that(op, equal_to(expected))





