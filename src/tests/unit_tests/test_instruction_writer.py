from unittest import TestCase

from hamcrest import assert_that, contains_string

from breadboarder.author.pubwriters import MockPubWriter
from breadboarder.core.project import Note
from breadboarder.publishing.markdownformatter import MarkdownFormatter
from breadboarder.publishing.figure_namer import DefaultFigureNamer
from breadboarder.publishing.instruction_writer import InstructionWriter


class MockEditor(object):
    def wants_to_illustrate(self, step):
        return True

    def wants_illustration_at_end(self):
        return False


class InstructionWriterTest(TestCase):
    def test_writes_each_step_instruction(self):
        fw = MockPubWriter('manuscript','test')
        formatter = MarkdownFormatter(fw)
        iw = InstructionWriter(formatter, MockEditor(), DefaultFigureNamer())
        notes = [Note('Note 1'),
                 Note('Note 2'),
                 Note('Note 3')]
        for note in notes:
            iw.take(note)
        assert_that(fw['manuscript/test.md'], contains_string('Note 1\n'))
        assert_that(fw['manuscript/test.md'], contains_string('Note 2\n'))
        assert_that(fw['manuscript/test.md'], contains_string('Note 3\n'))
        assert_that(fw['manuscript/test.md'], contains_string('images/figure1.svg'))

