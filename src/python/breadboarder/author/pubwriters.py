import os
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from io import StringIO


class PublicationWriter():
    __metaclass__ = ABCMeta

    def __init__(self, root_path, title):
        self.root_path = root_path
        self.title = title


    @abstractmethod
    def write(self, text, path):
        pass

    def path_to_document(self):
        return os.path.join(self.root_path, '%s.md' % self.title)

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def open(self):
        pass

    def find_path(self, filename):
        if filename:
            path = os.path.join(self.root_path, filename)
        else:
            path = self.path_to_document()
        return path


class FileBasedPublicationWriter(PublicationWriter):
    def __init__(self, root_path, title):
        PublicationWriter.__init__(self, root_path, title)
        self.doc = None

    def open(self):
        self.doc = open(self.path_to_document(),'w')

    def close(self):
        self.doc.close()

    def write(self, text, filename=None):
        if filename is None:
            self.doc.write(text)
            return
        with open(self.find_path(filename), 'w') as f:
            f.write(text)



class MockPublicationWriter(PublicationWriter):
    def __init__(self, root_path, title):
        PublicationWriter.__init__(self, root_path, title)
        self.store = defaultdict(StringIO)

    def __getitem__(self, path):
        return self.store[path].getvalue()

    def paths(self):
        return self.store.keys()

    def __contains__(self, path):
        return path in self.store

    def write(self, text, filename=None):
        self.store[self.find_path(filename)].write(text)


    def close(self):
        for path in self.paths():
            self.store[path].close()

