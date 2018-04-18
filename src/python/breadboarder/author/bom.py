from collections import defaultdict

from breadboarder.author.visitor import ProjectVisitor
from breadboarder.markdown.markdownwriter import MarkdownWriter


class BillOfMaterials(ProjectVisitor):
    def __init__(self):
        ProjectVisitor.__init__(self)
        self.parts = defaultdict(list)

    def visit_project(self, project):
        pass

    def visit_part(self, part):
        part_type = part.part_type()
        listed = self[part_type]
        listed.append(part)
        self[part_type] = listed
        part.set_id('%s%s' %(part.id_prefix(), len(listed)))

    def sorted_keys(self):
        return sorted(list(self.parts.keys()))

    def __getitem__(self, part_type):
        return self.parts[part_type]

    def __setitem__(self, part_type, listed):
        self.parts[part_type] = listed

    def markdown(self, writer):
        bw = BomWriter()
        bw.markdown(self, writer)


class BomWriter():
    def __init__(self):
        pass

    def markdown(self, bom, writer):
        keys = bom.sorted_keys()
        writer.add_heading('Bill of Materials', 2)
        for key in keys:
            items = bom[key]
            writer.add_heading(key+('s' if len(items) > 1 else ''), 3)
            writer.add_para(', '.join([item.full_description() for item in bom[key]]))
        return writer.markdown()

