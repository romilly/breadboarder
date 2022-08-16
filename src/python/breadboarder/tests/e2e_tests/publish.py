import os.path
from unittest import TestCase
from hamcrest import assert_that, contains_string

from breadboarder.author.book_maker import make_book
from breadboarder.author.pubwriters import MockPublicationWriter, FileBasedPublicationWriter
from breadboarder.core.breadboard import Breadboard
from breadboarder.core.project import Note, Project
from breadboarder.publishing.editor import Editor
from svg.point import Point


class BookMakerTest(TestCase):
    def test_publishes_text_and_images(self):
        file_writer = FileBasedPublicationWriter('manuscript', 'test')
        project = Project()
        breadboard = Breadboard().move_to(Point(20, 20))
        project.add(breadboard)
        project.add(
                 Note('Note 1'),
                 Note('Note 2'),
                 Note('Note 3'))
        make_book(project, file_writer, options=Editor.PicturePerStep)
        assert_that(os.path.exists('manuscript/resources/images/figure1.png'))
        # assert_that(file_writer['manuscript/images/figure1.svg'], contains_string('<svg xmlns'))

