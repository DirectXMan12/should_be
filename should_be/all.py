from forbiddenfruit import curse
import inspect
import pkgutil
from importlib import import_module

from should_be import core
from should_be import extensions

def isMixin(obj):
    return inspect.isclass(obj) and issubclass(obj, core.BaseMixin) and obj != core.BaseMixin

default_mixins = []

# first get core mixings
default_mixins.extend(inspect.getmembers(core, isMixin))

# then get extensions
for _, ext_mod, ispkg in pkgutil.walk_packages(extensions.__path__):
    if not ispkg:
        mod = import_module(extensions.__name__ + '.' + ext_mod)
        default_mixins.extend(inspect.getmembers(mod, isMixin))

# print 'Default Mixins were: {0}'.format(', '.join(m[0] for m in default_mixins))

try:
    _builtin_loaded_mixins
except NameError:
    _builtin_loaded_mixins = {}

for mixin_name, mixin_class in default_mixins:
    target_class = mixin_class.target_class
    try:
        if not hasattr(target_class, '_should_be_loaded_mixins'):
                target_class._should_be_loaded_mixins = []

        if mixin_class not in target_class._should_be_loaded_mixins:
            mixin_class.mix(target_class)
    except TypeError:
        # we have a builtin
        try:
            _builtin_loaded_mixins[target_class]
        except KeyError:
            _builtin_loaded_mixins[target_class] = []

        if mixin_class not in _builtin_loaded_mixins[target_class]:
            mixin_class.mix(target_class)
