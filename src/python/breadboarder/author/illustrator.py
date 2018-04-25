from xml.etree.ElementTree import register_namespace, XML, tostring
from abc import ABCMeta, abstractmethod

from breadboarder.author.book_maker import StepTaker


class SVGWriter(StepTaker):
    def __init__(self, file_writer, formatter, figure_namer, width=640, height=480, view_box= None, opacity=1.0):
        self.file_writer = file_writer
        self.figure_namer = figure_namer
        self.formatter = formatter
        self.opacity = opacity
        register_namespace("", "http://www.w3.org/2000/svg")
        if view_box:
            vb = ' viewBox="%d %d %d %d"' % view_box
        else:
            vb = ''
        self.xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' % (
        width, height, vb))

    def fade_parts(self):
        if self.opacity < 1.0:
            for element in self.xml:
                element.set_attribute('opacity', self.opacity)

    def take(self, step):
        if step.is_part():
            self.xml.append(step.element())

    def end(self):
        (caption, path) = self.figure_namer.next_name()
        self.file_writer.write(tostring(self.xml).decode('utf-8'), path)
        self.formatter.image(caption, path)


class FigureNamer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def next_name(self):
        pass


class DefaultFigureNamer(FigureNamer):
    def __init__(self):
        self.count = 0

    def next_name(self):
        self.count += 1
        return [text % self.count for text in['Figure %d','images/figure%d.svg']]

