import should_be.all  # noqa
import unittest


class TestIterableMixin(unittest.TestCase):
    def setUp(self):
        self.lst = [1, 2, 3]

    def test_should_be_part_of(self):
        self.assertRaises(AssertionError,
                          self.lst.should_be_part_of, [2, 3, 4])

        self.lst.should_be_part_of([1, 2, 3, 4])
