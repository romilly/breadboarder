from breadboarder.author.illustrator import Illustrator
from breadboarder.markdown.markdownformatter import MarkdownFormatter
from breadboarder.publishing.figure_namer import DefaultFigureNamer
from unit_tests.test_instruction_writer import InstructionWriter

#   TODO: move figure_namer into editor?
def make_book(project, editor, file_writer):
    figure_namer = DefaultFigureNamer()
    iw = InstructionWriter(MarkdownFormatter(file_writer), editor, figure_namer)
    pw = Illustrator(file_writer, editor, figure_namer)
    project.publish(iw, pw)

