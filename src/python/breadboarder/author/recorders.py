import os
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from io import StringIO


class PubWriter():
    """
    Abstract class which builds up multiple strings, each associated with a file path.

    It should be closed when each string is complete.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def write(self, text, path):
        pass

    @classmethod
    def path_to_document(self, root_path, title):
        return os.path.join(root_path, '%s.md' % title)

    @abstractmethod
    def close(self):
        pass


class MockPubWriter(PubWriter):
    def __init__(self, root_path, title):
        self.root_path = root_path
        self.title = title
        self.store = defaultdict(StringIO)

    def __getitem__(self, path):
        return self.store[path].getvalue()

    def paths(self):
        return self.store.keys()

    def __contains__(self, path):
        return path in self.store

    def write(self, text, filename=None):
        if filename:
            path = os.path.join(self.root_path, filename)
        else:
            path = self.path_to_document(self.root_path, self.title)
        self.store[path].write(text)

    def close(self):
        for path in self.paths():
            self.store[path].close()

