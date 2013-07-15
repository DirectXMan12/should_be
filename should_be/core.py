from forbiddenfruit import curse
from forbiddenfruit import reverse as reverse_the_curse
import inspect
import abc
import re
from types import FunctionType, CodeType


def findObjectName(mname=None):
    stack = inspect.stack()

    if mname is None:
        if 'should' not in stack[2][3]:
            # go up a level if we've wrapped this method
            mname = stack[3][3]
        else:
            mname = stack[2][3]


    for frame in stack:
        frame_info = inspect.getframeinfo(frame[0])
        code = frame_info.code_context
        if code is not None:
            code = code[0]
            if ('.'+mname) in code:
                trimmed = code.strip()
                idx = trimmed.index('.'+mname)
                return trimmed[0:idx]

    return None

def methodsToAvoid(subclasses):
    res = []
    for cls in subclasses:
        res.extend([n for n, o
                    in cls.__dict__.items()
                    if inspect.ismethod(o) or inspect.isfunction(o)])
    return res

# actually copy the method contents so that
# we can have a different name
def alias_method(new_name, f):
    fr = inspect.currentframe().f_back # the current class

    # duplicate the code with the new name
    oc = f.func_code
    new_code = CodeType(oc.co_argcount, oc.co_nlocals, oc.co_stacksize,
                        oc.co_flags, oc.co_code, oc.co_consts,
                        oc.co_names, oc.co_varnames, oc.co_filename,
                        new_name, oc.co_firstlineno, oc.co_lnotab,
                        oc.co_freevars, oc.co_cellvars)

    # duplicate the function with the new name and add it to the class
    fr.f_locals[new_name] = FunctionType(new_code, f.func_globals, new_name,
                                         f.func_defaults, f.func_closure)

class BaseMixin(object):

    target_class = object

    @staticmethod
    def mix_method(target, method_name, method, method_type=None):
        # print 'Mixing {0} into {1}'.format(method_name, target)

        if method_type == 'static':
            method = staticmethod(method)
        elif method_type == 'class':
            method = classmethod(method)

        if method_name in target.__dict__:
            reverse_the_curse(target, method_name)

        if method_type is None and hasattr(method, '__func__'):
            curse(target, method_name, method.__func__)
        else:
            curse(target, method_name, method)



    @classmethod
    def __mixin__(cls, target, method_type=None, avoid_list=[]):
        methods = inspect.getmembers(cls, inspect.ismethod)
        for method_name, method in methods:
            if (method_name not in dir(BaseMixin)
                or (method_name == 'should_follow'
                    and 'should_follow' not in dir(target))):
                if method_name not in avoid_list:
                    cls.mix_method(target, method_name, method, method_type)

    @classmethod
    def mix(cls, target=None):
        if target is None:
            target = cls.target_class

        cls.__mixin__(target)
        attr_name = '_should_be_{0}.{1}'
        attr_name = attr_name.format(cls.__module__,
                                     cls.__name__)
        cls.mix_method(target, attr_name, lambda: cls)

        def submix(target_cls):
            try:
                if issubclass(target_cls.__metaclass__, abc.ABCMeta):
                    # print 'submixing {0}'.format(target_cls)
                    for impl_cls in target_cls._abc_registry:
                        if 'UserDict' in str(impl_cls):
                            pass # for some reason this class segfaults
                        else:
                            attr_name = '_should_be_{0}.{1}'
                            attr_name = attr_name.format(cls.__module__,
                                                         cls.__name__)

                            if attr_name not in dir(impl_cls):
                                subclasses = target.__subclasses__()
                                mta = methodsToAvoid(subclasses)
                                cls.__mixin__(impl_cls,
                                              avoid_list=mta)
                                cls.mix_method(impl_cls, attr_name, lambda: target_cls)

                    for subcls in target_cls.__subclasses__():
                        submix(subcls)
            except AttributeError:
                pass

        submix(target)


    def should_follow(self, assertion, msg=None, **kwargs):
        if msg is None:
            # TODO(sross): figure out what the assertion was
            msg = '{txt} failed to follow an assertion'

        if not assertion:
            obj_name = findObjectName()

            if obj_name is None:
                obj_name = '(unknown)'

            raise AssertionError(msg.format(txt=obj_name,
                                            self=self,
                                            **kwargs))


class ObjectMixin(BaseMixin):
    def should_be(self, target, method_name=None):
        msg = '{txt} should have been {val}, but was {self}'
        self.should_follow(self == target, msg, val=target)

    def shouldnt_be(self, target):
        msg = '{txt} should not have been {val}, but was anyway'
        self.should_follow(self != target, msg, val=target)

    def should_be_exactly(self, target):
        msg = '{txt} should have been exactly {val}, but was {self}'
        self.should_follow(self is target, msg, val=target)

    def shouldnt_be_exactly(self, target):
        msg = '{txt} should not have been exactly {val}, but was anyway'
        self.should_follow(self is not target, msg, val=target)

    def should_be_none(self):
        msg = '{txt} should have been {val}, but was {self}'
        self.should_follow(self is None, msg, val=None)

    def shouldnt_be_none(self):
        msg = '{txt} should not have been {val}, but was anyway'
        self.should_follow(self is not None, msg, val=None)

    def should_be_in(self, target):
        msg = '{txt} should have been in {val}, but was not'
        self.should_follow(self in target, msg, val=target)

    def shouldnt_be_in(self, target):
        msg = '{txt} should not have been in {val}, but was anyway'
        self.should_follow(self not in target, msg, val=target)

    def should_be_a(self, target):
        msg = '{txt} should have been a {val}, but was a {self_class}'
        if inspect.isclass(target):
            self.should_follow(isinstance(self, target), msg,
                               val=target, self_class=type(self))
        else:
            # treat target as a string
            str_target = str(target)
            if '.' in str_target:
                self_name = type(self).__module__ + '.' + type(self).__name__
                self.should_follow(self_name == str_target, msg,
                                   val=str_target, self_class=type(self))

            else:
                self.should_follow(type(self).__name__ == str_target, msg,
                                   val=str_target, self_class=type(self))



    def shouldnt_be_a(self, target):
        msg = '{txt} should not have been a {val}, but was anyway'
        if inspect.isclass(target):
            self.should_follow(not isinstance(self, target), msg, val=target)
        else:
            # treat target as a string
            str_target = str(target)
            if '.' in str_target:
                self_name = type(self).__module__ + '.' + type(self).__name__
                self.should_follow(self_name != str_target, msg,
                                   val=str_target)

            else:
                self.should_follow(type(self).__name__ != str_target, msg,
                                   val=str_target)

    def should_be_truthy(self):
        msg = '{txt} should have been truthy, but was {self}'
        self.should_follow(bool(self) is True, msg, val=True)

    alias_method('should_be_true', should_be_truthy)

    def should_be_falsy(self):
        msg = '{txt} should not have falsy, but was anyway'
        self.should_follow(bool(self) is False, msg, val=False)

    alias_method('should_be_false', should_be_falsy)

    def should_raise(self, target, *args, **kwargs):
        if not hasattr(self, '__call__'):
            msg_not_callable = "{txt} ({self}) should have been callable, but was not"
            self.should_follow(False, msg_not_callable)

        msg = "{txt}({args}, {kwargs}) should have raise {val}, but did not"

        try:
            self(*args, **kwargs)
        except target:
            pass
        else:
            kwa = ', '.join('{0}={1}'.format(k,v) for k, v in kwargs.items())
            self.should_follow(False, msg,
                               val=target,
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)

    def should_raise_with_message(self, target, tmsg, *args, **kwargs):
        if not hasattr(self, '__call__'):
            msg_not_callable = "{txt} ({self}) should have been callable, but was not"
            self.should_follow(False, msg_not_callable)

        try:
            self(*args, **kwargs)
        except target, ex:
            msg = ("{txt}({args}, {kwargs}) should have raised {val} "
                   "with a message matching {re}, but had a message of "
                   "{act_msg} instead")
            kwa = ', '.join('{0}={1}'.format(k,v) for k, v in kwargs.items())
            self.should_follow(re.match(tmsg, ex.message), msg,
                               val=target,
                               re=tmsg,
                               act_msg=ex.message,
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)
        else:
            msg = "{txt}({args}, {kwargs}) should have raised {val}, but did not"
            kwa = ', '.join('{0}={1}'.format(k,v) for k, v in kwargs.items())
            self.should_follow(False, msg,
                               val=target,
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)

class NoneTypeMixin(BaseMixin):
    target_class = type(None)

    _already_loaded = False
    # this works around None methods being 'unbound'

    @classmethod
    def _load_methods(cls):
        # python doesn't close in loops, grumble...
        def factory(method_name, method):
            def new_method(*args, **kwargs):
                method.__func__(None, *args, **kwargs)

            return new_method

        methods = inspect.getmembers(ObjectMixin, inspect.ismethod)
        for method_name, method in methods:
            if (method_name not in dir(BaseMixin) or method_name == 'should_follow'):
                new_method = factory(method_name, method)
                setattr(NoneTypeMixin, method_name, staticmethod(new_method))

    @classmethod
    def __mixin__(cls, target):
        if not cls._already_loaded:
            cls._load_methods()

        methods = [(meth_name, meth) for (meth_name, meth)
                   in NoneTypeMixin.__dict__.items()
                   if isinstance(meth, staticmethod)]

        for method_name, method in methods:
            if (method_name not in dir(BaseMixin)
                or method_name == 'should_follow'):
                cls.mix_method(target, method_name, method,
                               method_type='keep')
