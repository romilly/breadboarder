from collections import OrderedDict

from breadboarder.author.visitor import ProjectVisitor
from breadboarder.markdown.markdownwriter import MarkdownWriter


class DefaultFigureNamer(object):
    def __init__(self):
        self.count = 0

    def next_name(self):
        self.count += 1
        return [text % self.count for text in['Figure %d','figure%d.md']]




class Instructions(object):
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def markdown(self, writer):
        for instruction in self.instructions:
            writer.add_step(instruction)



class InstructionsBuilder(ProjectVisitor):

    def __init__(self):
        ProjectVisitor.__init__(self)
        self._instructions = Instructions()

    def visit_project(self, project):
        pass

    def visit_part(self, part):
        self._instructions.add_instruction(part.lab_instruction())

    def instructions(self):
        return self._instructions









