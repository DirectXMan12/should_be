import should_be.all  # noqa
import unittest


class TestContainerMixin(unittest.TestCase):
    def setUp(self):
        self.lst = [1, 2, 3]

    def test_should_include_iter(self):
        err_msg = (r'[a-zA-Z0-9.]+ should have included \[.+?\]'
                   r', but did not have items .+')
        self.assertRaisesRegexp(AssertionError, err_msg,
                                self.lst.should_include, [4])

        self.lst.should_include([1, 2, 3])

    def test_should_include_item(self):
        err_msg = (r'[a-zA-Z0-9.]+ should have included .+?'
                   r', but did not')
        self.assertRaisesRegexp(AssertionError, err_msg,
                                self.lst.should_include, 4)

        self.lst.should_include(3)
