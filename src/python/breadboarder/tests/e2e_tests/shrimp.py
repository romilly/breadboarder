from breadboarder.author.book_maker import make_book
from breadboarder.author.pubwriters import FileBasedPublicationWriter
from breadboarder.examples import shrimp_kit
from breadboarder.publishing.editor import Editor

shrimp = shrimp_kit.shrimp_kit()
file_writer = FileBasedPublicationWriter('manuscript', 'test')
make_book(shrimp, file_writer, options=Editor.PictureAtEnd)
