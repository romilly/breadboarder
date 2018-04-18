import os

from breadboarder.examples.shrimp_kit import shrimp_kit
from breadboarder.markdown.markdownwriter import MarkdownWriter
from breadboarder.svg.svg import write


class BookMaker():
    def __init__(self):
        pass

    def publish(self, project, title, filename, directory='manuscript'):
        writer = MarkdownWriter()
        writer.add_heading(title)
        project.build_bom().markdown(writer)
        project.build_instructions().markdown(writer)
        svg = project.build_svg()
        writer.add_image(title, self.svg_file(directory, filename))
        write(svg, self.svg_file(directory, filename))
        write(writer.markdown(), self.md_file(directory, filename))

    def svg_file(self, directory, filename):
        return os.path.join(directory, 'images', filename + '.svg')

    def md_file(self, directory, filename):
        return os.path.join(directory, filename + '.md')

BookMaker().publish(shrimp_kit(),'Making the shrimp', 'shrimping')

