from xml.etree.ElementTree import register_namespace, tostring, XML

from breadboarder.svg.svg import CompositeItem


class Project(CompositeItem):
    def __init__(self, width=640, height=480, view_box=None):
        CompositeItem.__init__(self)
        self.width = width
        self.height = height
        self.view_box = view_box

    def container(self):
        register_namespace("","http://www.w3.org/2000/svg")
        if self.view_box:
            vb = ' viewBox="%d %d %d %d"' % self.view_box
        else:
            vb = ''
        xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' % (
        self.width, self.height, vb))
        return xml

    def tostring(self):
        return tostring(self.element())

