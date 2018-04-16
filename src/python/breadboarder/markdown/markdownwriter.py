from io import StringIO


class MarkdownWriter():
    def __init__(self):
        self.contents = StringIO()

    def add_heading(self, text, level=1):
        self.nl(2)
        for i in range(level):
            self.contents.write('#')
        self.contents.write(' ')
        self.contents.write(text)
        self.nl(2)

    def add_para(self, *lines):
        self.nl(2)
        self.contents.writelines(lines)
        self.nl(2)

    def add_image(self, caption, location):
        self.nl(2)
        self.contents.write('![%s](%s)' % (caption, location))
        self.nl(2)

    def add_step(self, line):
        self.contents.write('1. %s\n' % line)

    def nl(self, count=1):
        for i in range(count):
            self.contents.write('\n')

    def markdown(self):
        self.contents.flush()
        return self.contents.getvalue()
