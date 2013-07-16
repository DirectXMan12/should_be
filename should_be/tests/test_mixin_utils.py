from should_be import core as sc
import unittest


class TestMixin(sc.BaseMixin):
    target_class = object

    def should_cheese(self):
        self.should_follow(True)


class TestMixinUtils(unittest.TestCase):
    def test_default_mix(self):
        TestMixin.mix()
        (object()).should_cheese()

    def test_static_mix_method(self):
        sc.BaseMixin.mix_method(object, 'should_static', lambda: 3,
                                method_type='static')
        object.should_static()

    def test_class_mix_method(self):
        sc.BaseMixin.mix_method(object, 'should_class', lambda cls: str(cls),
                                method_type='class')
        object.should_class()
