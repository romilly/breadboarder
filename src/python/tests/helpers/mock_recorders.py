from io import StringIO

from breadboarder.author.recorders import TextRecorder, SVGRecorder


class MockTextRecorder(TextRecorder):
    def __init__(self):
        self._text = StringIO()

    def write(self, text):
        self._text.write(text)

    def contents(self):
        return self._text.getvalue()

    def close(self):
        self._text.close()


class MockSVGRecorder(SVGRecorder):
    def __init__(self):
        self._svg = {}

    def write_svg_file(self, svg, path):
        self._svg[path] = svg

    def __getitem__(self, path):
        return self._svg[path]

    def __contains__(self, path):
        return path in self._svg
