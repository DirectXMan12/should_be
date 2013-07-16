import inspect
import pkgutil
from importlib import import_module

from should_be import core
from should_be import extensions

__all__ = ['default_mixins', 'loaded_mixins']


def isMixin(obj):
    return (inspect.isclass(obj)
            and issubclass(obj, core.BaseMixin)
            and obj != core.BaseMixin)

default_mixins = []

# first get core mixings
default_mixins.extend(inspect.getmembers(core, isMixin))

# then get extensions
for _, ext_mod, ispkg in pkgutil.walk_packages(extensions.__path__):
    if not ispkg:
        mod = import_module(extensions.__name__ + '.' + ext_mod)
        default_mixins.extend(inspect.getmembers(mod, isMixin))

try:
    loaded_mixins
except NameError:
    loaded_mixins = {}

for mixin_name, mixin_class in default_mixins:
    target_class = mixin_class.target_class

    try:
        loaded_mixins[target_class]
    except KeyError:
        loaded_mixins[target_class] = []

    if mixin_class not in loaded_mixins[target_class]:
        mixin_class.mix(target_class)
        loaded_mixins[target_class].append(mixin_class)
