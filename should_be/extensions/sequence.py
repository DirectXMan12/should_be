from should_be.core import BaseMixin, alias_method
from collections import Sequence, Counter


class SequenceMixin(BaseMixin):
    target_class = Sequence

    def should_have_same_items_as(self, target):
        msg_smaller = ('{txt} should have been {val}, but did not have '
                       'the items {items}')
        msg_bigger = ('{txt} should have been {val}, but had the extra '
                       'items {items}')
        msg_diff = ('{txt} should have been {val}, but differed in items '
                    '{i1} and {i2}')

        fst = Counter(self)
        snd = Counter(target)

        we_had = fst - snd
        they_had = snd - fst

        if we_had != Counter() and they_had != Counter():
            self.should_follow(fst == snd, msg_diff,
                               val=target,
                               i1=we_had.keys(),
                               i2=they_had.keys())

        self.should_follow(we_had == {}, msg_bigger,
                           val=target,
                           items=list(we_had.elements()))

        self.should_follow(they_had == {}, msg_smaller,
                           val=target,
                           items=list(they_had.elements()))

    def should_be(self, target):
        if self == target:
            return

        try:
            len_msg = ('{txt} should have been {val}, but they had '
                       ' different lengths ({l1} vs {l2})')
            self.should_follow(len(self) == len(target), len_msg,
                               val=target,
                               l1=len(self),
                               l2=len(target))
            item_msg = ('{txt} should have been {val}, but they differed '
                        ' at item {ind} ({i1} vs {i2})')
            for i in xrange(len(self)):
                self.should_follow(self[i] == target[i], item_msg,
                                   val=target,
                                   ind=i,
                                   i1=self[i],
                                   i2=target[i])
        except (TypeError, NotImplementedError):
            ObjectMixin.should_be(self, target)
