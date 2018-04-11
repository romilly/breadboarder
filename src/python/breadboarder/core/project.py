from xml.etree.ElementTree import register_namespace, tostring, XML

from breadboarder.svg.svg import CompositeItem


class Project(CompositeItem):

    def container(self):
        register_namespace("","http://www.w3.org/2000/svg")
        return XML('<svg width="640" height="480" version="1.1" xmlns="http://www.w3.org/2000/svg"></svg>')

    def tostring(self):
        return tostring(self.element())

