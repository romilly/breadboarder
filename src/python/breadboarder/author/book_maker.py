import os
from abc import abstractmethod, ABCMeta

from breadboarder.author.visitor import ProjectVisitor
from breadboarder.examples.shrimp_kit import shrimp_kit

# TODO: Try the idea below


class BookMaker(ProjectVisitor):
    """
    The bookmaker flows the project steps through a StepTaker
    """

    def end(self):
        self.step_taker.end()

    def __init__(self, step_taker):
        self.step_taker = step_taker

    def take(self, step):
        self.step_taker.take(step)

    def visit_project(self, project):
        pass

    def publish(self, project):
        project.welcome(self)


class StepTaker():
    __metaclass__ = ABCMeta

    @abstractmethod
    def take(self, step):
        pass

    @abstractmethod
    def end(self):
        pass


class StepSpreader(StepTaker):
    def __init__(self, *takers):
        self.takers = takers

    def take(self, step):
        for taker in self.takers:
            taker.take(step)

    def end(self):
        for taker in self.takers:
            taker.end()

