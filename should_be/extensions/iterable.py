from should_be.core import BaseMixin, alias_method
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
