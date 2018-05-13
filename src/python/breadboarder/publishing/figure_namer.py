from abc import ABCMeta, abstractmethod

class FigureNamer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def path(self):
        pass

    @abstractmethod
    def caption(self):
        pass

    @abstractmethod
    def next(self):
        pass


class DefaultFigureNamer(FigureNamer):
    def next(self):
        self.count += 1

    def relative_path(self):
        pass

    def caption(self):
        return 'Figure %d' % self.count

    def __init__(self):
        self.count = 0

    def reset(self):
        self.count = 0

    def path(self):
        return 'images/figure%d.svg' % self.count

