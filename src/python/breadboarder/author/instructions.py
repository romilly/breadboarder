from abc import ABCMeta, abstractmethod

# TODO: move to correct module
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










