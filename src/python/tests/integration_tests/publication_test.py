from unittest import TestCase
from hamcrest import assert_that, contains_string

from breadboarder.author.builder import book_maker
from breadboarder.author.pubwriters import MockPubWriter
from breadboarder.core.project import Note, Project


class BookMakerTest(TestCase):
    def test_publishes_text_and_images(self):
        file_writer = MockPubWriter('manuscript','test')
        bm = book_maker(file_writer)
        project = Project()
        project.add(
                 Note('Note 1'),
                 Note('Note 2'),
                 Note('Note 3'))
        bm.publish(project)
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 1\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 2\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 3\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('\n![Figure 1](images/figure1.svg)'))
        assert_that('manuscript/images/figure1.svg' in file_writer)
        assert_that(file_writer['manuscript/images/figure1.svg'], contains_string('<svg xmlns'))

