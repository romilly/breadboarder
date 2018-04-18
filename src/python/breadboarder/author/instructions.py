from collections import OrderedDict

from breadboarder.author.visitor import ProjectVisitor
from breadboarder.markdown.markdownwriter import MarkdownWriter
from breadboarder.svg.svg import SVGDocument


class DefaultFigureNamer(object):
    def __init__(self):
        self.count = 0

    def next_name(self):
        self.count += 1
        return [text % self.count for text in['Figure %d','figure%d.md']]




class Instructions(object):
    def __init__(self):
        self.writer = MarkdownWriter()
        self.images = OrderedDict()
        self.document = SVGDocument()

    def add_instruction(self, instruction):
        self.writer.add_step(instruction)

    def add_image_element(self, element):
        self.document.add(element)

    def markdown(self):
        return self.writer.markdown()


class InstructionsBuilder(ProjectVisitor):

    def __init__(self):
        ProjectVisitor.__init__(self)
        self._instructions = Instructions()

    def visit_project(self, project):
        pass

    def visit_part(self, part):
        self._instructions.add_instruction(part.lab_instruction())
        self._instructions.add_image_element(part.element())

    def instructions(self):
        return self._instructions









