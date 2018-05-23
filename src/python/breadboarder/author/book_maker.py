from breadboarder.publishing.editor import Editor
from breadboarder.publishing.figure_namer import DefaultFigureNamer


#   TODO: move figure_namer into editor?
def make_book(project, file_writer, figure_namer= None, pictures=None):
    figure_namer = figure_namer if figure_namer else DefaultFigureNamer()
    editor = Editor(file_writer, figure_namer, pictures)
    project.welcome(editor)

