from forbiddenfruit import curse
import inspect

from should_be import core

def isMixin(obj):
    return inspect.isclass(obj) and issubclass(obj, core.BaseMixin) and obj != core.BaseMixin

core_mixins = inspect.getmembers(core, isMixin)
print 'Core Mixins were: {0}'.format(', '.join(m[0] for m in core_mixins))

try:
    _builtin_loaded_mixins
except NameError:
    _builtin_loaded_mixins = {}

for mixin_name, mixin_class in core_mixins:
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
