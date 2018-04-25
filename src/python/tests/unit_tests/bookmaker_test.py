from unittest import TestCase

from hamcrest import assert_that, equal_to, string_contains_in_order, contains_string

from breadboarder.author.book_maker import BookMaker, StepTaker, StepSpreader
from breadboarder.author.recorders import MockPubWriter
from breadboarder.core.project import Note
from breadboarder.markdown.markdownformatter import MarkdownFormatter
from tests.helpers.test_projects import test_project

class MockStepTaker(StepTaker):
    def __init__(self):
        self.steps = []

    def take(self, step):
        self.steps.append(step)



class BookmakerTest(TestCase):
    def test_passes_on_project_steps(self):
        st = MockStepTaker()
        bm = BookMaker(st)
        bm.publish(test_project())
        assert_that(len(st.steps), equal_to(4))


class StepSpreaderTest(TestCase):
    def test_spreader_shares_the_goodness(self):
        st1 = MockStepTaker()
        st2 = MockStepTaker()
        ss = StepSpreader(st1, st2)
        anything = 43
        ss.take(anything)
        ss.take(anything)
        ss.take(anything)
        assert_that(len(st1.steps), equal_to(3))
        assert_that(len(st2.steps), equal_to(3))


class InstructionWriter(StepTaker):
    def __init__(self, writer):
        self.writer = writer

    def take(self, step):
        self.writer.step(step.instruction())


class InstructionWriterTest(TestCase):
    def test_writes_each_step_instruction(self):
        fw = MockPubWriter('manuscript','test')
        formatter = MarkdownFormatter(fw)
        iw = InstructionWriter(formatter)
        notes = [Note('Note 1'),
                 Note('Note 2'),
                 Note('Note 3')]
        for note in notes:
            iw.take(note)
        assert_that(fw['manuscript/test.md'], contains_string('Note 1\n'))
        assert_that(fw['manuscript/test.md'], contains_string('Note 2\n'))
        assert_that(fw['manuscript/test.md'], contains_string('Note 3\n'))
        assert_that('manuscript/images/figure1.svg' in fw)

