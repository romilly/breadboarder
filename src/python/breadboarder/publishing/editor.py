from breadboarder.author.pubwriters import PublicationWriter
from breadboarder.publishing.figure_namer import DefaultFigureNamer
from breadboarder.publishing.formatters import NullFormatter
from breadboarder.author.illustrator import Illustrator
from breadboarder.author.visitor import ProjectVisitor
from breadboarder.publishing.formatters import MarkdownFormatter


class Editor(ProjectVisitor):
    PicturePerStep = 1
    PicturePerStage = 2
    PictureAtEnd = 3
    NoText = 4

    def __init__(self, file_writer: PublicationWriter, figure_namer=None, options=None):
        self.file_writer = file_writer
        self.formatter = NullFormatter() if options == self.NoText else MarkdownFormatter(self.file_writer)
        self.figure_namer = figure_namer if figure_namer else DefaultFigureNamer()
        self.illustrator = Illustrator()
        self.options = options

    def visit_project(self, project):
        self.file_writer.open()

    def take(self, step):
        self.formatter.take(step)
        self.illustrator.take(step)
        if self.options == self.PicturePerStep:
            self.add_picture()
        if self.options == self.PicturePerStage and step.is_stage():
            self.add_picture()

    def add_picture(self):
        self.figure_namer.next()
        path = self.figure_namer.path()
        source_path = self.figure_namer.source_path()
        self.formatter.image(self.figure_namer.caption(), path)
        self.file_writer.write(self.illustrator.svg(), source_path)
        self.file_writer.convert_to_png(source_path, path)
        self.formatter.new_page()


    def end(self):
        if self.options == self.PictureAtEnd or self.options == self.NoText:
            self.add_picture()


