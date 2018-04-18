from abc import ABCMeta, abstractmethod

from breadboarder.core.project import Part
from breadboarder.svg.svg import GroupedDrawable


class Host(GroupedDrawable, Part):
    __metaclass__ = ABCMeta

    def lab_instruction(self):
        return 'Take a %s (%s)' % (self.description(),self.id())

    def __init__(self):
        GroupedDrawable.__init__(self)
        self.ports = {}
        self.add_components()

    @abstractmethod
    def add_components(self):
        pass

    def add_port(self, port):
        self.ports[port.portname] = port

    def __getitem__(self, item):
        return self.ports[item]

    def describe_port_location(self, port_name):
        return self.id()+' '+self[port_name].description()