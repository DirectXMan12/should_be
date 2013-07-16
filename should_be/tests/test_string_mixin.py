import should_be.all  # noqa
import unittest


class TestStringShoulds(unittest.TestCase):
    def test_should_match(self):
        self.assertRaises(AssertionError, 'abc'.should_match, r'd.c')
        'abc'.should_match(r'a.c')

    def test_shouldnt_match(self):
        self.assertRaises(AssertionError, 'abc'.shouldnt_match, r'a.c')
        'abc'.shouldnt_match(r'd.c')
