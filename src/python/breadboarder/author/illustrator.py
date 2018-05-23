from xml.etree.ElementTree import register_namespace, XML, tostring


class Illustrator():
    def __init__(self, width=640, height=480, view_box= None):
        register_namespace("", "http://www.w3.org/2000/svg")
        if view_box:
            vb = ' viewBox="%d %d %d %d"' % view_box
        else:
            vb = ''
        self.xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' %
                       (width, height, vb))

    def take(self, step):
        if step.is_part():
            self.xml.append(step.element())

    def svg(self):
        return tostring(self.xml).decode('utf-8')


