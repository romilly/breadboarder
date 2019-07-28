from abc import ABCMeta, abstractmethod

from breadboarder.core.project import Part
from svg.svg import GroupedDrawable


class Host(GroupedDrawable, Part):
    __metaclass__ = ABCMeta

    def instruction(self):
        return 'Take a %s (%s)' % (self.description(),self.id())

    def __init__(self):
        GroupedDrawable.__init__(self)
        self._ports = {}
        self.add_components()

    @abstractmethod
    def add_components(self):
        pass

    def add_port(self, port):
        self._ports[port.portname] = port

    def port_names(self):
        return self._ports.keys()

    def ports(self):
        return self._ports.values()

    def __getitem__(self, item):
        return self._ports[item]

    def describe_port_location(self, port_name):
        return self.id()+' '+self[port_name].description()