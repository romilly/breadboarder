from collections import defaultdict
from xml.etree.ElementTree import register_namespace, tostring, XML
from breadboarder.svg.svg import CompositeItem
from abc import ABCMeta, abstractmethod

class Part():
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


class Project(CompositeItem):
    def __init__(self, width=640, height=480, view_box=None):
        CompositeItem.__init__(self)
        self.width = width
        self.height = height
        self.view_box = view_box
        self.bom = BillOfMaterials()

    def container(self):
        register_namespace("","http://www.w3.org/2000/svg")
        if self.view_box:
            vb = ' viewBox="%d %d %d %d"' % self.view_box
        else:
            vb = ''
        xml = XML('<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg"%s></svg>' % (
        self.width, self.height, vb))
        return xml

    def tostring(self):
        return tostring(self.element())

    def add(self, item):
        CompositeItem.add(self,item)
        self.bom.add(item)

    def bom_md(self):
        return self.bom.md()


class BillOfMaterials():
    def __init__(self):
        self.parts = defaultdict(list)

    def add(self, part):
        part_type = part.part_type()
        listed = self.parts[part_type]
        listed.append(part)
        self.parts[part_type] = listed
        part.set_id('%s-%d)' %(part.id_prefix(), len(listed)))

    def md(self):
        keys = self.parts.keys()
        sorted(keys)
        result = ''
        for key in keys:
            result += ('\n'+key+'s\n\n')
            for item in self.parts[key]:
                result += item.description()+'\n'
        return result



