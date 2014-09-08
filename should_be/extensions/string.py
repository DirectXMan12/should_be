from should_be.core import BaseMixin
import re


class StringMixin(BaseMixin):
    try:
        target_class = basestring
    except NameError:
        target_class = str

    def should_match(self, target):
        msg = '{txt} should have matched {re}, but was {self} instead'
        self.should_follow(re.match(target, self), msg, re=target)

    def shouldnt_match(self, target):
        msg = '{txt} should not have matched {re}, but did anyway'
        self.should_follow(re.match(target, self) is None, msg, re=target)

    # explicitly override this so it has precedence over sequence
    # and quotes around values
    def should_be(self, target):
        msg = '{txt} should have been "{val}", but was "{self}"'
        self.should_follow(self == target, msg, val=target)
