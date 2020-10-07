from breadboarder.author.illustrator import ContentPage
from breadboarder.publishing.formatters import MarkdownFormatter
from breadboarder.publishing.figure_namer import DefaultFigureNamer
from unit_tests.test_instruction_writer import InstructionWriter


def book_maker(file_writer):
    formatter = MarkdownFormatter(file_writer)
    iw = InstructionWriter(formatter)
    pw = ContentPage(file_writer, formatter, DefaultFigureNamer())
    sp = StepSpreader(iw, pw)
    bm = BookMaker(sp)
    return bm