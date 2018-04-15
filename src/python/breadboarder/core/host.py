from abc import ABCMeta, abstractmethod

from breadboarder.core.project import Part
from breadboarder.svg.svg import GroupedDrawable


class Host(GroupedDrawable, Part):
    __metaclass__ = ABCMeta

    def lab_instruction(self):
        return None

    def __init__(self, svg_id):
        GroupedDrawable.__init__(self, svg_id)
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
        return self.description()+' '+port_name