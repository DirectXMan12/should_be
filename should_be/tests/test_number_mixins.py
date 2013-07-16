import should_be.all  # noqa
import unittest


class TestNumberShoulds(unittest.TestCase):
    def test_basic_should_be_roughtly(self):
        self.assertRaises(AssertionError, (3).should_be_roughly, 3.01)
        (3).should_be_roughly(3.00000000001)

    def test_should_be_roughly_equals_returns(self):
        # for coverage
        (3).should_be_roughly(3)

    def test_should_be_roughly_places(self):
        self.assertRaises(AssertionError, (3).should_be_roughly,
                          3.01, places=3)
        (3).should_be_roughly(3.01, places=1)

    def test_should_be_roughly_delta(self):
        self.assertRaises(AssertionError, (30).should_be_roughly,
                          41, delta=10)
        (30).should_be_roughly(31, delta=10)

    def test_should_be_roughly_with_both_params_raises_error(self):
        self.assertRaises(TypeError, (30).should_be_roughly,
                          31, delta=10, places=3)

    def test_basic_shouldnt_be_roughtly(self):
        self.assertRaises(AssertionError, (3).shouldnt_be_roughly,
                          3.00000000001)
        (3).shouldnt_be_roughly(3.01)

    def test_shouldnt_be_roughly_places(self):
        self.assertRaises(AssertionError, (3).shouldnt_be_roughly,
                          3.01, places=1)
        (3).shouldnt_be_roughly(3.1, places=1)

    def test_shouldnt_be_roughly_delta(self):
        self.assertRaises(AssertionError, (30).shouldnt_be_roughly,
                          31, delta=10)
        (30).shouldnt_be_roughly(41, delta=10)

    def test_shouldnt_be_roughly_with_both_params_raises_error(self):
        self.assertRaises(TypeError, (30).shouldnt_be_roughly,
                          31, delta=10, places=3)

    def test_should_be_above(self):
        self.assertRaises(AssertionError, (30).should_be_above, 40)
        self.assertRaises(AssertionError, (30).should_be_at_or_above, 40)

        (30).should_be_above(20)
        (30).should_be_at_or_above(30)

    def test_should_be_below(self):
        self.assertRaises(AssertionError, (30).should_be_below, 20)
        self.assertRaises(AssertionError, (30).should_be_at_or_below, 20)

        (30).should_be_below(40)
        (30).should_be_at_or_below(30)
