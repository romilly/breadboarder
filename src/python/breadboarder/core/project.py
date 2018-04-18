from breadboarder.author.bom import BillOfMaterials
from breadboarder.author.illustrations import SVGBuilder
from breadboarder.author.instructions import InstructionsBuilder
from breadboarder.svg.svg import GroupedDrawable, Drawable
from abc import ABCMeta, abstractmethod


class Part(Drawable):
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

    @abstractmethod
    def lab_instruction(self):
        pass

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

    def lab_instruction(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)

    def part_type(self):
        raise NotImplementedError(SHOULD_HAVE_IMPLEMENTED % self)


class Project():
    def __init__(self):
        self._parts = []

    def add(self,*parts):
        for part in parts:
            self._parts.append(part)
        return self

    def parts(self):
        return self._parts

    def welcome(self, visitor):
        visitor.start()
        visitor.visit_project(self)
        for part in self.parts():
            visitor.visit_part(part)
        visitor.end()

    def build_bom(self):
        bom = BillOfMaterials()
        self.welcome(bom)
        return bom

    def build_instructions(self):
        builder = InstructionsBuilder()
        self.welcome(builder)
        return builder.instructions()

    def build_svg(self):
        svb = SVGBuilder()
        self.welcome(svb)
        return svb.svg().decode('UTF-8')




