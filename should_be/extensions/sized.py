from should_be.core import BaseMixin, alias_method
from collections import Sized


class SizedMixin(BaseMixin):
    target_class = Sized

    def should_be_size(self, target):
        msg = '{txt} should have been size {val}, but was size {self_size}'
        self.should_follow(len(self) == target, msg,
                           val=target,
                           self_size=len(self))

    alias_method('should_have_len', should_be_size)
    alias_method('should_have_length', should_be_size)

    def should_be_size_of(self, target):
        msg = ('{txt} should have been the size of {val} ({val_size}), '
                'but was size {self_size}')
        self.should_follow(len(self) == len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    alias_method('should_match_size_of', should_be_size_of)
    alias_method('should_match_len_of', should_be_size_of)
    alias_method('should_match_length_of', should_be_size_of)

    def should_be_at_least_size(self, target):
        msg = ('{txt} should have been at least size {val}, but '
               'was size {self_size}')
        self.should_follow(len(self) >= target, msg,
                           val=target,
                           self_size=len(self))

    alias_method('should_be_at_least_len', should_be_at_least_size)
    alias_method('should_be_at_least_length', should_be_at_least_size)

    def should_be_at_most_size(self, target):
        msg = ('{txt} should have been at most size {val}, but '
               'was size {self_size}')
        self.should_follow(len(self) <= target, msg,
                           val=target,
                           self_size=len(self))

    alias_method('should_be_at_most_len', should_be_at_most_size)
    alias_method('should_be_at_most_length', should_be_at_most_size)

    def should_be_at_least_size_of(self, target):
        msg = ('{txt} should have been at least the size of {val} ({val_size})'
                ', but was size {self_size}')
        self.should_follow(len(self) >= len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    alias_method('should_be_at_least_len_of', should_be_at_least_size_of)
    alias_method('should_be_at_least_length_of', should_be_at_least_size_of)

    def should_be_at_most_size_of(self, target):
        msg = ('{txt} should have been at most the size of {val} ({val_size})'
                ', but was size {self_size}')
        self.should_follow(len(self) <= len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    alias_method('should_be_at_most_len_of', should_be_at_most_size_of)
    alias_method('should_be_at_most_length_of', should_be_at_most_size_of)

    def should_be_bigger_than(self, target):
        if isinstance(target, Sized):
            # we have a sized object
            msg = ('{txt} should have been bigger than {val} ({val_size}), '
                   'but was size {self_size}')
            self.should_follow(len(self) > len(target), msg,
                               val=target,
                               val_size=len(target),
                               self_size=len(self))

        else:
            # have a number
            msg = ('{txt} should have had size greater than {val}, but '
                   'was size {self_size}')
            self.should_follow(len(self) > target, msg,
                               val=target,
                               self_size=len(self))

    alias_method('should_be_longer_than', should_be_bigger_than)

    def should_be_smaller_than(self, target):
        if isinstance(target, Sized):
            # we have a sized object
            msg = ('{txt} should have been smaller than {val} ({val_size}), '
                   'but was size {self_size}')
            self.should_follow(len(self) < len(target), msg,
                               val=target,
                               val_size=len(target),
                               self_size=len(self))

        else:
            # have a number
            msg = ('{txt} should have had size less than {val}, but '
                   'was size {self_size}')
            self.should_follow(len(self) < target, msg,
                               val=target,
                               self_size=len(self))

    alias_method('should_be_shorter_than', should_be_smaller_than)

    def should_be_empty(self):
        msg = '{txt} should have been empty, but had size {val}'
        self.should_follow(len(self) == 0, msg, val=len(self))

    def shouldnt_be_empty(self):
        msg = '{txt} should not have been empty, but was anyway'
        self.should_follow(len(self) > 0, msg)
