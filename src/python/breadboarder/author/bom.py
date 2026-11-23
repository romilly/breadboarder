from collections import defaultdict


class BillOfMaterials():
    def __init__(self):
        self.parts = defaultdict(list)
        self.prefix_counts = defaultdict(int)

    def add(self, part):
        part_type = part.part_type()
        listed = self[part_type]
        listed.append(part)
        self[part_type] = listed
        # number by prefix, not by type, so types that share a prefix never share an ID
        prefix = part.id_prefix()
        self.prefix_counts[prefix] += 1
        part.set_id('%s%s' % (prefix, self.prefix_counts[prefix]))

    def sorted_keys(self):
        return sorted(list(self.parts.keys()))

    def __getitem__(self, part_type):
        return self.parts[part_type]

    def __setitem__(self, part_type, listed):
        self.parts[part_type] = listed

class BomWriter():
    def __init__(self, writer):
        self.writer = writer

    def markdown(self, bom):
        keys = bom.sorted_keys()
        self.writer.add_heading('Bill of Materials', 2)
        for key in keys:
            items = bom[key]
            self.writer.add_heading(key+('s' if len(items) > 1 else ''), 3)
            self.writer.add_para(', '.join([item.full_description() for item in bom[key]]))
        return self.writer.markdown()

