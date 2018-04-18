from xml.etree.ElementTree import register_namespace, XML, ElementTree, tostring

from breadboarder.author.visitor import ProjectVisitor


class SVGBuilder(ProjectVisitor):
    def __init__(self, width=640, height=480, view_box= None):
        ProjectVisitor.__init__(self)
        register_namespace("", "http://www.w3.org/2000/svg")
        if view_box:
            vb = ' viewBox="%d %d %d %d"' % view_box
        else:
            vb = ''
        self.xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' % (
        width, height, vb))

    def visit_project(self, project):
        pass

    def visit_part(self, part):
        self.xml.append(part.element())

    def svg(self):
        return tostring(self.xml)

