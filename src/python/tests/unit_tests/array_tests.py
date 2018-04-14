from unittest import TestCase

from hamcrest import assert_that, equal_to
from hamcrest.core.base_matcher import BaseMatcher

from breadboarder.transformations.arrays import decode, Array, scalar, identity, cv


class DecodeTest(TestCase):
    def test_decode(self):
        assert_that(decode([2, 2, 2], [1, 1, 1]), equal_to(7))
        # 68 <-> 1760 3 12 ⊥ 1 2 8
        assert_that(decode([1760, 3, 12], [1, 2, 8]), equal_to(68))
        # 2667 <-> 0 20 12 4 ⊥ 2 15 6 3
        assert_that(decode([0, 20, 12, 4], [2, 15, 6, 3]), equal_to(2667))


class ArrayMatcher(BaseMatcher):
    def __init__(self, array):
        self._array = array

    def matches(self, item):
        if not isinstance(item, Array):
            return False
        if item._shape != self._array._shape:
            return False
        if item._elements != self._array._elements:
            return False
        return True

    def describe_to(self, description):
        description.append('An array %s' % self._array)


def equal_to_array(array):
    return ArrayMatcher(array)


class ArrayTest(TestCase):
    def setUp(self):
        self.a = Array([2,3],[1,2,3,4,5,6])
        self.b = Array([3], [2, 3, 5])

    def test_shape(self):
        assert_that(self.a.shape(), equal_to_array(Array([2],[2,3])))

    def test_reshape(self):
        assert_that(self.a.reshape([1, 3]), equal_to_array(Array([1, 3],[1, 2, 3])))
        assert_that(self.a.reshape([2, 3]), equal_to_array(Array([2, 3],[1, 2, 3, 4, 5, 6])))
        assert_that(self.a.reshape([3, 3]), equal_to_array(Array([3, 3],[1, 2, 3, 4, 5, 6, 1, 2, 3])))
        assert_that(self.a.reshape([3]), equal_to_array(Array([3],[1, 2, 3])))
        assert_that(self.a.reshape([0]), equal_to_array(Array([0],[])))
        assert_that(self.a.reshape([0, 3]), equal_to_array(Array([0, 3],[])))
        assert_that(self.a.reshape([3, 0]), equal_to_array(Array([3, 0],[])))
        assert_that(self.a.reshape([]), equal_to_array(scalar(1)))

    def test_dot_checks_array_argument(self):
        try:
            self.a.dot([2, 3])
        except:
            # expected
            return
        self.fail('should have raised a domain error')

    def test_dot_checks_conformability(self):
        try:
            self.a.dot(self.a)
        except:
            # expected
            return
        self.fail('should have raised a length error')

    def test_dot_multiplies_matrix_with_vector(self):
        v = self.a.dot(self.b)
        assert_that(v, equal_to_array(Array([2],[23,53])))

    def test_dot_multiples_matrices(self):
        c = Array([4, 3],[10, 7, 1, 2, 1, 8, 10, 4, 2, 6, 5, 5])
        d = Array([3, 2],[5, 3, 8, 8, 6, 7])
        assert_that(c.dot(d), equal_to_array(Array([4,2],[112, 93, 66, 70, 94, 76, 100, 93])))

    def test_dot_multiplies_tensor_by_matrix(self):
        # not really needed, but I want to be sure I got it right!
        # The values look random cos they are :)
        c = Array([4, 3],[10, 7, 1, 2, 1, 8, 10, 4, 2, 6, 5, 5])
        e = Array([2, 3, 4],[10, 1, 3, 2, 10, 4, 9, 6, 3, 7, 2, 4, 6, 4, 9, 7, 6, 9, 2, 6, 8, 7, 8, 1])
        assert_that(e.dot(c), equal_to_array(Array([2, 3, 3],[144, 93, 34, 234, 140, 90, 88, 56, 83, 200, 117,
                                                       91, 134, 89, 112, 180, 100, 85])))

    def test_identity_returns_identity_matrix(self):
        i3 = identity(3)
        assert_that(i3.dot(i3), equal_to_array(i3))
        assert_that(i3.dot(cv(1,2,3)), equal_to_array(cv(1,2,3)))





