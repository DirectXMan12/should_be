from should_be.core import BaseMixin
from should_be.extensions.container import ContainerMixin
from should_be.extensions.iterable import IterableMixin
from collections import Mapping


class MappingMixin(BaseMixin):
    target_class = Mapping

    def should_include_values(self, target):
        ContainerMixin.should_include(self.items(), target.items())

    def should_be_part_of_values(self, target):
        IterableMixin.should_be_part_of(self.items(), target.items())

    # TODO(sross): should we override should_be_empty to show items?
