from breadboarder.author.bom import BomWriter, BillOfMaterials
from breadboarder.svg.svg import GroupedDrawable, Drawable
from abc import ABCMeta, abstractmethod

class Step(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def instruction(self):
        pass

    def is_part(self):
        return False


class Part(Drawable, Step):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._id = ''

    @abstractmethod
    def id_prefix(self):
        pass

    @abstractmethod
    def part_type(self):
        pass

    def set_id(self, id):
        self._id = id

    def id(self):
        return self._id

    @abstractmethod
    def description(self):
        pass

    def is_part(self):
        return True

    def full_description(self):
        return self.description()

SHOULD_HAVE_IMPLEMENTED = '%s - My subclass shold have implemented this method'


class Component(GroupedDrawable, Part):
    __metaclass__ = ABCMeta

    def __init__(self, connected_ports):
        GroupedDrawable.__init__(self)
        Part.__init__(self)
        self.connected_ports = connected_ports

    def id_prefix(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)

    def description(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)

    def instruction(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)

    def part_type(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)


class Project():
    def __init__(self):
        self._steps = []
        self._bom = BillOfMaterials()

    def bom(self):
        return self._bom

    def add(self,*steps):
        for step in steps:
            self._steps.append(step)
            if step.is_part():
                self._bom.add(step)
        return self

    def welcome(self, visitor):
        visitor.start()
        visitor.visit_project(self)
        for step in self.steps():
            visitor.take(step)
        visitor.end()

    def steps(self):
        return self._steps

class Note(Step):
    def __init__(self, text):
        self.text = text

    def instruction(self):
        return self.text





