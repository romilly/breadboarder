from unittest import TestCase

from hamcrest import assert_that, equal_to

from breadboarder.transformations.arrays import decode


class DecodeTest(TestCase):
    assert_that(decode([2, 2, 2], [1, 1, 1]), equal_to(7))
    # 68 <-> 1760 3 12 ⊥ 1 2 8
    assert_that(decode([1760, 3, 12], [1, 2, 8]), equal_to(68))
    # 2667 <-> 0 20 12 4 ⊥ 2 15 6 3
    assert_that(decode([0, 20, 12, 4], [2, 15, 6, 3]), equal_to(2667))
