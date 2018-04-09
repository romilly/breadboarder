import operator
from copy import copy
from functools import reduce
from itertools import cycle
from more_itertools import take


def decode(radices, values):
    result = 0
    rv = zip(radices, values)
    for (r, v) in rv:
        result = v + result * r
    return result



def cv(item_list):
        return Array([len(item_list),1], item_list)

def scalar(value):
        return(Array([],[value]))

class Array():
    def __init__(self, shape, elements):
        self._shape = shape
        self._elements = elements

    def shape(self):
        return Array([len(self._shape)], copy(self._shape))

    def reshape(self, new_shape):
        if isinstance(new_shape, Array):
            new_shape = new_shape._elements
        count = reduce(operator.mul, new_shape, 1) # 1 is identity for multiply
        elements = take(count,cycle(self._elements))
        return Array(new_shape, elements)

    def idx(self, idx_):
        return decode(self._shape, idx_)

    def __getitem__(self, idx_):
        return self._elements[self.idx(idx_)]

    def __setitem__(self, idx_, value):
        self._elements[self.idx(idx_)] = value

    def dot(self, array):
        # TODO: one day handle scalar args
        if not isinstance(array, Array):
            raise Exception('domain error')
        if self._shape[-1] != array._shape[0]:
            raise Exception('length error')
        leading_count = reduce(operator.mul, self._shape[:-1], 1)
        trailing_count = reduce(operator.mul, array._shape[1:], 1)
        l = self._shape[-1]
        elements = (leading_count*trailing_count*[0])
        index = 0
        for i in range(0, leading_count):
            for j in range(0, trailing_count):
                for k in range(l):
                    first = i * l + k
                    last = j + trailing_count * k
                    elements[index] += self._elements[first] * array._elements[last]
                index += 1
        return Array(self._shape[:-1]+array._shape[1:], elements)


    def __str__(self):
        # TODO: implement something more like APL's output
        return '%s⍴%s' % (self._shape, self._elements)
