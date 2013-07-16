import should_be.all  # noqa
import unittest


class TestSetMixin(unittest.TestCase):
    def setUp(self):
        self.st = {1, 2, 3}

    def test_set_should_be(self):
        self.assertRaisesRegexp(AssertionError,
                                'extra',
                                self.st.should_be,
                                {1, 2})

        self.assertRaisesRegexp(AssertionError,
                                r'did not have',
                                self.st.should_be,
                                {1, 3, 2, 4})

        self.assertRaisesRegexp(AssertionError,
                                r'differed in',
                                self.st.should_be,
                                {1, 4, 2})

        self.st.should_be({1, 2, 3})

    def test_set_should_be_fall_back(self):
        self.assertRaises(AssertionError, self.st.should_be, 3)
