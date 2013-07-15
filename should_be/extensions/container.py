from should_be.core import BaseMixin, alias_method
from collections import Container


class ContainerMixin(BaseMixin):
    target_class = Container

    def should_include(self, target):
        if isinstance(target, Iterable):
            msg = ('{txt} should have included {val}, but did not have '
                  'items {items}')

            missing_items = []
            for item in target:
                if item not in self:
                    missing_items.append(item)

            self.should_follow(len(missing_items) == 0, msg,
                               val=target,
                               items=missing_items)
        else:
            msg = '{txt} should have included {val}, but did not'
            self.should_follow(target in self, msg,
                               val=target)
