from abc import ABCMeta, abstractmethod


class ProjectVisitor():
    __metaclass__ = ABCMeta

    def start(self):
        pass

    @abstractmethod
    def visit_project(self, project):
        pass

    @abstractmethod
    def take(self, step):
        pass

    @abstractmethod
    def end(self):
        pass
