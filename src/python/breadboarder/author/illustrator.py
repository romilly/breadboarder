from xml.etree.ElementTree import register_namespace, XML, tostring

from breadboarder.author.visitor import ProjectVisitor


class Illustrator(ProjectVisitor):
    def __init__(self, file_writer, editor, figure_namer, width=640, height=480, view_box= None):
        self.file_writer = file_writer
        self.figure_namer = figure_namer
        self.editor = editor
        register_namespace("", "http://www.w3.org/2000/svg")
        if view_box:
            vb = ' viewBox="%d %d %d %d"' % view_box
        else:
            vb = ''
        self.xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' %
                       (width, height, vb))

    def visit_project(self, project):
        self.figure_namer.reset()

    def take(self, step):
        if step.is_part():
            self.xml.append(step.element())
        if self.editor.wants_to_illustrate(step):
            self.illustrate()

    def end(self):
        if self.editor.wants_illustration_at_end():
            self.illustrate()

    def illustrate(self):
        self.figure_namer.next()
        path = self.figure_namer.path()
        self.file_writer.write(tostring(self.xml).decode('utf-8'), path)


