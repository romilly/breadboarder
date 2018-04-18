from abc import ABCMeta, abstractmethod


class ProjectVisitor():
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def start(self):
        pass

    @abstractmethod
    def visit_project(self, project):
        pass

    @abstractmethod
    def visit_part(self, part):
        pass

    def end(self):
        pass
