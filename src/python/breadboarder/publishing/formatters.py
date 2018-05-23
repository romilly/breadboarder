from abc import abstractmethod, ABCMeta


class Formatter():
    __metaclass__ = ABCMeta

    @abstractmethod
    def heading(self, text, level=1):
        raise NotImplementedError()

    @abstractmethod
    def para(self, *lines):
        raise NotImplementedError()

    @abstractmethod
    def image(self, caption, location):
        raise NotImplementedError()

    @abstractmethod
    def step(self, instruction):
        raise NotImplementedError()


class NullFormatter(Formatter):

    def para(self, *lines):
        pass

    def image(self, caption, location):
        pass

    def step(self, instruction):
        pass

    def heading(self, text, level=1):
        pass


class MarkdownFormatter(Formatter):
    def __init__(self, writer):
        self.writer = writer

    def heading(self, text, level=1):
        self.newline(2)
        for i in range(level):
            self.writer.write('#')
        self.writer.write(' ')
        self.writer.write(text)
        self.newline(2)

    def para(self, *lines):
        self.newline(2)
        self.writer.writelines(lines)
        self.newline(2)

    def image(self, caption, location):
        self.newline(2)
        self.writer.write('![%s](%s)' % (caption, location))
        self.newline(2)

    def step(self, instruction):
        self.writer.write('1. %s\n' % instruction)

    def newline(self, count=1):
        for i in range(count):
            self.writer.write('\n')

