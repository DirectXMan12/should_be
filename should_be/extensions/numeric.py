from should_be.core import BaseMixin, alias_method
import numbers


class NumberMixin(BaseMixin):
    target_class = numbers.Real

    def should_be_roughly(self, target, places=None, delta=None):
        if self == target:
            return

        if delta is not None and places is not None:
            raise TypeError('specify delta or places, not both')

        if delta is not None:
            msg = ("{txt} should have been within {delta} of {val},"
                   " but was {self}, which is {actual_delta} from {val}")
            self.should_follow(abs(self - target) <= delta,
                               msg,
                               delta=delta,
                               actual_delta=abs(self - target),
                               val=target)
        else:
            if places is None:
                places = 7

            msg = ("{txt} should have been equal to {val} within {places}"
                   " places, but was {self}")
            self.should_follow(round(abs(self - target), places) == 0,
                               msg,
                               places=places,
                               val=target)

    def shouldnt_be_roughly(self, target, delta=None, places=None):
        if delta is not None and places is not None:
            raise TypeError('specify delta or places, not both')

        if delta is not None:
            msg = ("{txt} should not have been within {delta} of {val},"
                   " but was {self}, which is {actual_delta} from {val}")
            expr = self != target and abs(self - target) > delta
            self.should_follow(expr,
                               msg,
                               delta=delta,
                               actual_delta=abs(self - target),
                               val=target)
        else:
            if places is None:
                places = 7

            msg = ("{txt} should not have been equal to {val} within {places}"
                   " places, but was {self}")
            expr = self != target and round(abs(self - target), places) != 0
            self.should_follow(expr,
                               msg,
                               places=places,
                               val=target)

    def should_be_above(self, target):
        msg = '{txt} should have been greater than {val}, but was {self}'
        self.should_follow(self > target, msg, val=target)

    alias_method('should_be_greater_than', should_be_above)
    alias_method('should_be_more_than', should_be_above)

    def should_be_below(self, target):
        msg = '{txt} should have been less than {val}, but was {self}'
        self.should_follow(self < target, msg, val=target)

    alias_method('should_be_less_than', should_be_below)

    def should_be_at_or_above(self, target):
        msg = ('{txt} should have been greater than or equal '
               'to {val}, but was {self}')
        self.should_follow(self >= target, msg, val=target)

    alias_method('should_be_greater_than_or_equal_to', should_be_at_or_above)
    alias_method('should_be_at_least', should_be_at_or_above)

    def should_be_at_or_below(self, target):
        msg = ('{txt} should have been less than or equal '
               'to {val}, but was {self}')
        self.should_follow(self <= target, msg, val=target)

    alias_method('should_be_less_than_or_equal_to', should_be_at_or_below)
    alias_method('should_be_at_most', should_be_at_or_below)
