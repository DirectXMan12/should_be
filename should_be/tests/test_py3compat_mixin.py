import should_be.all  # noqa
import unittest
import sys


class TestPy3CompatMixins(unittest.TestCase):
    def test_should_be_an_integer(self):
        self.assertRaises(AssertionError, (1.23).should_be_an_integer)
        (3).should_be_an_integer()
        (sys.maxsize + 1).should_be_an_integer()

    def test_should_be_a_unicode_string(self):
        if sys.version_info.major >= 3:
            self.assertRaises(AssertionError,
                              b'abc'.should_be_a_unicode_string)
        else:
            self.assertRaises(AssertionError, 'abc'.should_be_a_unicode_string)

        u'abc'.should_be_a_unicode_string()
