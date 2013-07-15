from should_be.core import BaseMixin, alias_method
from collections import Set


class SetMixin(BaseMixin):
    target_class = Set

    def should_be(self, target):
        msg_smaller = ('{txt} should have been {val}, but did not have '
                       'the items {items}')
        msg_bigger = ('{txt} should have been {val}, but had the extra '
                       'items {items}')
        msg_diff = ('{txt} should have been {val}, but differed in items '
                    '{i1} and {i2}')

        try:
            we_had = self.difference(target)
            they_had = target.differnce(self)

            if (we_had != {} and they_had != {}):
                self.should_follow(they_had == they_had == {}, msg_diff,
                                   val=target,
                                   i1=we_had,
                                   i2=they_had)

            self.should_follow(we_had == {}, msg_bigger,
                               val=target,
                               items=we_had)

            self.should_follow(they_had == {}, msg_smaller,
                               val=target,
                               items=they_had)
        except TypeError:
            ObjectMixin.should_be(self, target)



