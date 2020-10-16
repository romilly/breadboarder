from abc import ABC, abstractmethod


class FigureNamer(ABC):

    @abstractmethod
    def reset(self):
        pass


    @abstractmethod
    def source_path(self):
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

    def source_path(self):
        return 'resources/images/figure%d.svg' % self.count

    def path(self):
        return 'resources/images/figure%d.png' % self.count

