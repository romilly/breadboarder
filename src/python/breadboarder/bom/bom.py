from collections import defaultdict

from breadboarder.markdown.markdownwriter import MarkdownWriter


class BillOfMaterials():
    def __init__(self):
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


class BomWriter():
    def __init__(self, bom):
        self._bom = bom

    def markdown(self):
        writer = MarkdownWriter()
        keys = self._bom.sorted_keys()
        writer.add_heading('Bill of Materials', 2)
        for key in keys:
            items = self._bom[key]
            writer.add_heading(key+('s' if len(items) > 1 else ''), 3)
            writer.add_para(', '.join([item.description() for item in self._bom[key]]))
        return writer.markdown()

