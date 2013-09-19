from should_be.core import BaseMixin


class Py3CompatMixin(BaseMixin):
    target_class = object

    def should_be_an_integer(self):
        msg = '{txt} should have been an integer, but was a {self_class}'
        try:
            self.should_follow(isinstance(self, int) or isinstance(self, long),
                               msg, self_class=type(self))
        except NameError:
            self.should_follow(isinstance(self, int), msg,
                               self_class=type(self))

    def should_be_a_unicode_string(self):
        msg = ('{txt} should have been a (unicode) string, '
               'but was a {self_class}')

        self.should_follow(isinstance(self, type(u'')), msg,
                           self_class=type(self))
