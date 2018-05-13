from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire
from breadboarder.core.project import Project
from breadboarder.svg.svg import Point, write

from unittest import TestCase
from hamcrest import assert_that, equal_to


FILE_NAME = 'bb-wire.svg'
EXPECTED_FILE = 'test-data/%s' % FILE_NAME
ACTUAL_FILE = 'svg/%s' % FILE_NAME


def read(filename):
    try:
        with open(filename) as f:
            return f.read()
    except:
        raise Exception("can't open %s" % filename)


class BreadboardWireTest(TestCase):
    def test_writes_correct_file_contents(self):
        project = Project()
        breadboard = Breadboard().move_to(Point(20, 20))
        project.add(breadboard)
        project.add(Wire('red', breadboard['g1'], breadboard['TP1']))
        svg = project.element()
        write(svg, ACTUAL_FILE)
        op = read(ACTUAL_FILE)
        expected = read(EXPECTED_FILE)
        assert_that(op, equal_to(expected))
