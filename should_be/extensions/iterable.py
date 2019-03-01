from should_be.core import BaseMixin
try:
    from collections.abc import Iterable
except ImportError:
    # python < 3.3
    from collections import Iterable


class IterableMixin(BaseMixin):
    target_class = Iterable

    def should_be_part_of(self, target):
        msg = ('{txt} should have been part of {val}, but had extra '
               'items {items}')

        extra_items = []
        for item in self:
            if item not in target:
                extra_items.append(item)

        self.should_follow(len(extra_items) == 0, msg,
                           val=target,
                           items=extra_items)

    def shouldnt_be_part_of(self, target):
        msg = '{txt} should not have been part of {val}, but was anyway'

        extra_items = []
        for item in self:
            if item not in target:
                extra_items.append(item)

        self.should_follow(len(extra_items) > 0, msg,
                           val=target,
                           items=extra_items)
