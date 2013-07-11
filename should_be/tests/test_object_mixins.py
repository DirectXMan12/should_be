import should_be.all
import unittest

class TestBasicShoulds(unittest.TestCase):
    def test_should_be(self):
        self.assertRaises(AssertionError, (3).should_be, 4)
        (3).should_be(3)

    def test_shouldnt_be(self):
        self.assertRaises(AssertionError, (3).shouldnt_be, 3)
        (3).shouldnt_be(4)

    def test_should_be_exactly(self):
        self.assertRaises(AssertionError, (3).should_be_exactly, 4)
        (3).should_be_exactly(3)

    def test_should_be_exactly(self):
        self.assertRaises(AssertionError, (3).shouldnt_be_exactly, 3)
        (3).shouldnt_be_exactly(4)

    def test_should_be_none(self):
        self.assertRaises(AssertionError, (3).should_be_none)
        None.should_be_none()

    def test_should_be_none(self):
        self.assertRaises(AssertionError, None.shouldnt_be_none)
        (3).shouldnt_be_none()

    def test_should_be_in(self):
        self.assertRaises(AssertionError, 'a'.should_be_in, ['b'])
        'a'.should_be_in(['a','b'])

    def test_shouldnt_be_in(self):
        self.assertRaises(AssertionError, 'a'.shouldnt_be_in, ['a'])
        'a'.shouldnt_be_in(['b'])

    def test_should_be_a(self):
        self.assertRaises(AssertionError, 'a'.should_be_a, int)
        'a'.should_be_a(str)

    def test_shouldnt_be_a(self):
        self.assertRaises(AssertionError, 'a'.shouldnt_be_a, str)
        'a'.shouldnt_be_a(int)

    def test_should_be_true(self):
        self.assertRaises(AssertionError, False.should_be_true)
        True.should_be_true()

    def test_should_be_false(self):
        self.assertRaises(AssertionError, True.should_be_false)
        False.should_be_false()

class TestShouldRaises(unittest.TestCase):
    def test_should_raise_basic(self):
        self.assertRaises(AssertionError, (lambda x: 3).should_raise, Exception, 1)
        (lambda: 1/0).should_raise(Exception)

    def test_should_raises_not_callable(self):
        self.assertRaises(AssertionError, (3).should_raise, Exception)
        self.assertRaises(AssertionError, (3).should_raise_with_message, Exception, 'a')

    def test_should_raise_with_message(self):
        self.assertRaises(AssertionError, (lambda x: x/2).should_raise_with_message, Exception, 'a', 1)
        (lambda x: x/0).should_raise_with_message(ZeroDivisionError, 'integer division or modulo by zero', 1)
