import operator
from copy import copy
from functools import reduce
from itertools import cycle, accumulate

from more_itertools import take

def decode(radices, values):
    result = 0
    rv = zip(radices, values)
    for (r, v) in rv:
        result = v + result * r
    return result


class Array():
    def __init__(self, shape, elements):
        self._shape = shape
        self._elements = elements

    @classmethod
    def cv(cls, item_list):
        return Array([len(item_list),1], item_list)

    def reshape(self, new_shape):
        count = reduce(operator.add, new_shape)
        elements = take(count,cycle(self._elements))
        return Array(new_shape, elements)

    def idx(self, idx_):
        return decode(self._shape, idx_)

    def __getitem__(self, idx_):
        return self._elements[self.idx(idx_)]

    def __setitem__(self, idx_, value):
        self._elements[self.idx(idx_)] = value

    def transpose(self):
        # flips last two dimensions
        # scalars and vectors are returned unchanged
        if len(self._shape) < 2:
            return Array(copy(self._shape), copy(self._elements))
        elements = len(self._elements)*[0]
        new_shape = self._shape[:-2]+self._shape[-1:]+[self._shape[-2]]
        idx = 0
        for j in range(self._shape[-2]):
            for i in range(self._shape[-1]):
                elements[idx] = self[i,j]
        return Array(new_shape, elements)

    def str(self):
        # TODO: implement something more like APL's output
        return '%s⍴%s' % (self._shape, self._elements)
