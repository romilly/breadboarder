from xml.etree.ElementTree import Element, tostring

from breadboarder.svg.svg import CompositeItem


class Project(CompositeItem):

    def container(self):
        return Element('svg', height='480', width='640')

    def tostring(self):
        return tostring(self.element())

