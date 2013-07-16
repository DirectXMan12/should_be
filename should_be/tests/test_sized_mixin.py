import should_be.all
import unittest

class TestSizedMixin(unittest.TestCase):
    def setUp(self):
        self.lst = [1, 2, 3]

    def test_should_be_size(self):
        self.assertRaises(AssertionError, self.lst.should_be_size, 4)
        self.lst.should_be_size(3)

    def test_should_be_size_of(self):
        self.assertRaises(AssertionError, self.lst.should_be_size_of, [1, 2])
        self.lst.should_be_size_of([1, 2, 4])

    def test_should_be_at_least_size(self):
        self.assertRaises(AssertionError, self.lst.should_be_at_least_size, 4)
        self.lst.should_be_at_least_size(2)
        self.lst.should_be_at_least_size(3)

    def test_should_be_at_least_size_of(self):
        self.assertRaises(AssertionError, self.lst.should_be_at_least_size_of,
                          [1, 2, 3, 4])
        self.lst.should_be_at_least_size_of([1, 2])
        self.lst.should_be_at_least_size_of([1, 2, 4])

    def test_should_be_at_most_size(self):
        self.assertRaises(AssertionError, self.lst.should_be_at_most_size, 2)
        self.lst.should_be_at_most_size(3)
        self.lst.should_be_at_most_size(4)

    def test_should_be_at_most_size_of(self):
        self.assertRaises(AssertionError, self.lst.should_be_at_most_size_of,
                          [1, 2])
        self.lst.should_be_at_most_size_of([1, 2, 4])
        self.lst.should_be_at_most_size_of([1, 2, 4, 5])

    def test_should_be_bigger_than_num(self):
        self.assertRaises(AssertionError, self.lst.should_be_bigger_than, 3)
        self.lst.should_be_bigger_than(2)

    def test_should_be_bigger_than_sized(self):
        self.assertRaises(AssertionError, self.lst.should_be_bigger_than,
                          [1, 2, 3])
        self.lst.should_be_bigger_than([1, 2])

    def test_should_be_smaller_than_num(self):
        self.assertRaises(AssertionError, self.lst.should_be_smaller_than, 3)
        self.lst.should_be_smaller_than(4)

    def test_should_be_smaller_than_sized(self):
        self.assertRaises(AssertionError, self.lst.should_be_smaller_than,
                          [1, 2, 3])
        self.lst.should_be_smaller_than([1, 2, 3, 4])

    def test_should_be_empty(self):
        self.assertRaises(AssertionError, self.lst.should_be_empty)
        [].should_be_empty()

    def test_shouldnt_be_empty(self):
        self.assertRaises(AssertionError, [].shouldnt_be_empty)
        self.lst.shouldnt_be_empty()
