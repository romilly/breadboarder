from breadboarder.author.visitor import ProjectVisitor


class InstructionWriter(ProjectVisitor):
    def end(self):
        pass

    def visit_project(self, project):
        self.figure_namer.reset()

    def __init__(self, writer,  editor, figure_namer):
        self.writer = writer
        self.editor = editor
        self.figure_namer = figure_namer

    def take(self, step):
        self.writer.step(step.instruction())
        if self.editor.wants_to_illustrate(step):
            self.illustrate()

    def illustrate(self):
        self.figure_namer.next()
        path = self.figure_namer.path()
        caption = self.figure_namer.caption()
        self.writer.image(caption, path)