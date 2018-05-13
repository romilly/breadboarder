class MarkdownFormatter(object):
    def __init__(self, writer):
        self.writer = writer

    def heading(self, text, level=1):
        self.nl(2)
        for i in range(level):
            self.writer.write('#')
        self.writer.write(' ')
        self.writer.write(text)
        self.nl(2)

    def para(self, *lines):
        self.nl(2)
        self.writer.writelines(lines)
        self.nl(2)

    def image(self, caption, location):
        self.nl(2)
        self.writer.write('![%s](%s)' % (caption, location))
        self.nl(2)

    def step(self, instruction):
        self.writer.write('1. %s\n' % instruction)

    def nl(self, count=1):
        for i in range(count):
            self.writer.write('\n')

