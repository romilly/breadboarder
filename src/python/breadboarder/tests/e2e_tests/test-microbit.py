from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.core.microbitfront import MicrobitFront
from breadboarder.core.project import Project
from breadboarder.core.svg import write

FILE_NAME = 'microbit-front.svg'
MICROBIT_FRONT_SVG = 'svg/%s' % FILE_NAME


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
        expected = read('test-data/%s' % FILE_NAME)
        assert_that(op, equal_to(expected))



