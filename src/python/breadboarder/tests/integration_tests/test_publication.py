from unittest import TestCase
from hamcrest import assert_that, contains_string

from breadboarder.author.book_maker import make_book
from breadboarder.author.pubwriters import MockPublicationWriter
from breadboarder.core.project import Note, Project
from breadboarder.publishing.editor import Editor


class BookMakerTest(TestCase):
    def test_publishes_text_and_images(self):
        file_writer = MockPublicationWriter('manuscript', 'test')
        project = Project()
        project.add(
                 Note('Note 1'),
                 Note('Note 2'),
                 Note('Note 3'))
        make_book(project, file_writer, options=Editor.PicturePerStep)
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 1\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 2\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('Note 3\n'))
        assert_that(file_writer['manuscript/test.md'], contains_string('\n![Figure 1](resources/images/figure1.png)'))
        # assert_that('manuscript/resources/images/figure1.png' in file_writer)

