from should_be.core import BaseMixin, alias_method
import re


class StringMixin(BaseMixin):
    target_class = basestring

    def should_match(self, target):
        msg = '{txt} should have matched {re}, but was {self} instead'
        self.should_follow(re.match(target, self), msg, re=target)

    def shouldnt_match(self, target):
        msg = '{txt} should not have matched {re}, but did anyway'
        self.should_follow(re.match(target, self) is None, msg, re=target)
