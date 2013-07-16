import should_be.all
import unittest

class TestSequenceMixin(unittest.TestCase):
    def setUp(self):
        self.lst = [1, 2, 3]

    def test_should_have_same_items_as(self):
        self.assertRaises(AssertionError,
                          self.lst.should_have_same_items_as,
                          [1, 2])

        self.assertRaises(AssertionError,
                          self.lst.should_have_same_items_as,
                          [1, 3, 2, 4])

        self.assertRaises(AssertionError,
                          self.lst.should_have_same_items_as,
                          [1, 4, 2])
        
        self.lst.should_have_same_items_as([3,1,2])

    def test_list_should_be(self):
        self.assertRaisesRegexp(AssertionError, r'lengths', 
                                self.lst.should_be, [1])

        self.assertRaisesRegexp(AssertionError, r'item', 
                                self.lst.should_be, [1, 3, 4])

        self.lst.should_be([1, 2, 3])

    def test_list_should_be_falls_back(self):
        self.assertRaises(AssertionError, self.lst.should_be, 1)
