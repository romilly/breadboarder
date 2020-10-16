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
    def take(self, instruction):
        raise NotImplementedError()

    @abstractmethod
    def new_page(self):
        raise NotImplementedError()


class NullFormatter(Formatter):
    def new_page(self):
        pass

    def para(self, *lines):
        pass

    def image(self, caption, location):
        pass

    def take(self, instruction):
        pass

    def heading(self, text, level=1):
        pass


class MarkdownFormatter(Formatter):
    def __init__(self, writer):
        self.writer = writer
        self.step_count = 1

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

    def take(self, step):
        if step.is_stage():
            return
        if step.is_new_page():
            self.new_page()
            return
        if step.is_note():
            self.writer.write('\nI> %s\n' % step.instruction())
        else:
            self.writer.write('\n%d: %s\n' % (self.step_count, step.instruction()))
            self.step_count += 1

    def new_page(self):
        self.writer.write('\n{pagebreak}\n')

    def newline(self, count=1):
        for i in range(count):
            self.writer.write('\n')

