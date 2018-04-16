from collections import defaultdict


class BillOfMaterials():
    def __init__(self):
        self.parts = defaultdict(list)

    def add(self, part):
        part_type = part.part_type()
        listed = self.parts[part_type]
        listed.append(part)
        self.parts[part_type] = listed
        part.set_id('%s-%d)' %(part.id_prefix(), len(listed)))

    def write_md(self, writer):
        keys = sorted(list(self.parts.keys()))
        writer.add_heading('BOM', 2)
        for key in keys:
            writer.add_heading(key+'s', 3)
            writer.add_para(', '.join([item.description() for item in self.parts[key]]))
