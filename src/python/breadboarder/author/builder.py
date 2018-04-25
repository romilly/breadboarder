from breadboarder.author.book_maker import StepSpreader, BookMaker
from breadboarder.author.illustrator import SVGWriter, DefaultFigureNamer
from breadboarder.markdown.markdownformatter import MarkdownFormatter
from tests.unit_tests.bookmaker_test import InstructionWriter


def book_maker(file_writer):
    formatter = MarkdownFormatter(file_writer)
    iw = InstructionWriter(formatter)
    pw = SVGWriter(file_writer, formatter, DefaultFigureNamer())
    sp = StepSpreader(iw, pw)
    bm = BookMaker(sp)
    return bm