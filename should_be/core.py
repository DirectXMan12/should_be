from forbiddenfruit import curse
from forbiddenfruit import reverse as reverse_the_curse
import inspect
import abc
import re
from types import FunctionType, CodeType


# this whole bit does unspeakable things,
# but so does the rest of this library.
# if there's an issue with extension methods
# not appearing, check here.
def getRegisteredABCsPurePython(cls):
    return cls._abc_registry


if not hasattr(abc, 'ABC'):
    getRegisteredABCs = getRegisteredABCsPurePython
else:
    # detect python 3.7 C abc issues
    class _ABCTester(abc.ABC):
        pass

    if hasattr(_ABCTester, '_abc_registry'):
        # python <= 3.6, python 3.7 pure-Python ABCs
        getRegisteredABCs = getRegisteredABCsPurePython
    else:
        # python 3.7 C abcs
        def getRegisteredABCs(cls):
            import _abc
            dump = _abc._get_dump(cls)
            for cls_ref in dump[0]:
                # dereference the weakref,
                # since this is a normal set of weakrefs,
                # not a weak set
                yield cls_ref()


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


def buildFunction(baseFunc, code=None, glbls=None,
                  name=None, defaults=None,
                  kwdefaults=None, closure=None,
                  annotations=None, doc=None, dct=None):

    resf = None

    def _f():
        pass

    if hasattr(_f, 'func_code'):
        # Python 2.x
        resf = FunctionType(code or baseFunc.func_code,
                            glbls or baseFunc.func_globals,
                            name or baseFunc.func_name,
                            defaults or baseFunc.func_defaults,
                            closure or baseFunc.func_closure)
        resf.func_dict = dct or baseFunc.func_dict
        resf.func_doc = doc or baseFunc.func_doc

    else:
        # Python 3.x
        resf = FunctionType(code or baseFunc.__code__,
                            glbls or baseFunc.__globals__,
                            name or baseFunc.__name__,
                            defaults or baseFunc.__defaults__,
                            closure or baseFunc.__closure__)
        resf.__kwdefaults__ = kwdefaults or baseFunc.__kwdefaults__
        resf.__annotations__ = annotations or baseFunc.__annotations__
        resf.__dict__ = dct or baseFunc.__dict__
        resf.__doc__ = doc or baseFunc.__doc__

    return resf


def buildCode(baseCode, argcount=None, kwonlyargcount=None,
              nlocals=None, stacksize=None, flags=None,
              code=None, consts=None, names=None,
              varnames=None, filename=None, name=None,
              firstlineno=None, lnotab=None, freevars=None,
              cellvars=None):

    resc = None

    def _f():
        pass

    if hasattr(_f, 'func_code'):
        # Python 2.x
        resc = CodeType(argcount or baseCode.co_argcount,
                        nlocals or baseCode.co_nlocals,
                        stacksize or baseCode.co_stacksize,
                        flags or baseCode.co_flags,
                        code or baseCode.co_code,
                        consts or baseCode.co_consts,
                        names or baseCode.co_names,
                        varnames or baseCode.co_varnames,
                        filename or baseCode.co_filename,
                        name or baseCode.co_name,
                        firstlineno or baseCode.co_firstlineno,
                        lnotab or baseCode.co_lnotab,
                        freevars or baseCode.co_freevars,
                        cellvars or baseCode.co_cellvars)
    else:
        # Python 3.x
        resc = CodeType(argcount or baseCode.co_argcount,
                        kwonlyargcount or baseCode.co_kwonlyargcount,
                        nlocals or baseCode.co_nlocals,
                        stacksize or baseCode.co_stacksize,
                        flags or baseCode.co_flags,
                        code or baseCode.co_code,
                        consts or baseCode.co_consts,
                        names or baseCode.co_names,
                        varnames or baseCode.co_varnames,
                        filename or baseCode.co_filename,
                        name or baseCode.co_name,
                        firstlineno or baseCode.co_firstlineno,
                        lnotab or baseCode.co_lnotab,
                        freevars or baseCode.co_freevars,
                        cellvars or baseCode.co_cellvars)

    return resc


def getFunctionCode(func):
    try:
        return func.func_code
    except AttributeError:
        return func.__code__


# actually copy the method contents so that
# we can have a different name
def alias_method(new_name, f):
    fr = inspect.currentframe().f_back  # the current class

    # duplicate the code with the new name
    oc = getFunctionCode(f)
    new_code = buildCode(oc, name=new_name)

    # duplicate the function with the new name and add it to the class
    fr.f_locals[new_name] = buildFunction(f, name=new_name, code=new_code)


class BaseMixin(object):

    target_class = object

    @staticmethod
    def mix_method(target, method_name, method, method_type=None):
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
        # methods = inspect.getmembers(cls, inspect.ismethod)
        methods = [(method_name, method) for method_name, method
                   in cls.__dict__.items()
                   if inspect.isfunction(method)]
        try:
            methods.append(('should_follow', cls.should_follow.__func__))
        except AttributeError:
            methods.append(('should_follow', cls.should_follow))

        for method_name, method in methods:
            in_base = method_name in BaseMixin.__dict__
            is_should_follow = method_name == 'should_follow'
            sf_in_target = 'should_follow' in dir(target)
            if not in_base or (is_should_follow and not sf_in_target):
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
            if issubclass(type(target_cls), abc.ABCMeta):
                # print 'submixing {0}'.format(target_cls)
                for impl_cls in getRegisteredABCs(target_cls):
                    if 'UserDict' in str(impl_cls):
                        pass  # for some reason this class segfaults
                    else:
                        attr_name = '_should_be_{0}.{1}'
                        attr_name = attr_name.format(cls.__module__,
                                                     cls.__name__)

                        if attr_name not in dir(impl_cls):
                            subclasses = target.__subclasses__()
                            mta = methodsToAvoid(subclasses)
                            cls.__mixin__(impl_cls,
                                          avoid_list=mta)
                            cls.mix_method(impl_cls, attr_name,
                                           lambda: target_cls)

                for subcls in target_cls.__subclasses__():
                    submix(subcls)

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
            msg_not_callable = ("{txt} ({self}) should have "
                                "been callable, but was not")
            self.should_follow(False, msg_not_callable)

        msg = "{txt}({args}, {kwargs}) should have raise {val}, but did not"

        try:
            self(*args, **kwargs)
        except target:
            pass
        else:
            kwa = ', '.join('{0}={1}'.format(k, v) for k, v in kwargs.items())
            self.should_follow(False, msg,
                               val=target,
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)

    def should_raise_with_message(self, target, tmsg, *args, **kwargs):
        if not hasattr(self, '__call__'):
            msg_not_callable = ("{txt} ({self}) should have "
                                "been callable, but was not")
            self.should_follow(False, msg_not_callable)

        try:
            self(*args, **kwargs)
        except target as ex:
            msg = ("{txt}({args}, {kwargs}) should have raised {val} "
                   "with a message matching /{re}/, but had a message of "
                   "'{act_msg}' instead")
            kwa = ', '.join('{0}={1}'.format(k, v) for k, v in kwargs.items())
            self.should_follow(re.match(tmsg, str(ex)), msg,
                               val=target.__name__,
                               re=tmsg,
                               act_msg=str(ex),
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)
        else:
            msg = ("{txt}({args}, {kwargs}) should have raised "
                   "{val}, but did not")
            kwa = ', '.join('{0}={1}'.format(k, v) for k, v in kwargs.items())
            self.should_follow(False, msg,
                               val=target.__name__,
                               args=', '.join(repr(a) for a in args),
                               kwargs=kwa)


class NoneTypeMixin(BaseMixin):
    target_class = type(None)
    source_class = ObjectMixin

    _already_loaded = False
    # this works around None methods being 'unbound'

    @classmethod
    def _load_methods(cls, src=ObjectMixin):
        # python doesn't close in loops, grumble...
        def factory(method_name, method):
            if hasattr(method, '__func__'):
                # Python 2.x
                def new_method(*args, **kwargs):
                    method.__func__(None, *args, **kwargs)

                return new_method
            else:
                # Python 3.x
                def new_method(*args, **kwargs):
                    method(None, *args, **kwargs)

                return new_method

        methods = [(method_name, method) for method_name, method
                   in src.__dict__.items()
                   if inspect.isfunction(method)]
        try:
            methods.append(('should_follow', cls.should_follow.__func__))
        except AttributeError:
            methods.append(('should_follow', cls.should_follow))

        for method_name, method in methods:
            new_method = factory(method_name, method)
            setattr(cls, method_name, staticmethod(new_method))

    @classmethod
    def __mixin__(cls, target):
        if not cls._already_loaded:
            cls._load_methods(src=cls.source_class)

        methods = [(meth_name, meth) for (meth_name, meth)
                   in cls.__dict__.items()
                   if isinstance(meth, staticmethod)]

        for method_name, method in methods:
            if (method_name not in dir(BaseMixin)
                    or method_name == 'should_follow'):

                cls.mix_method(target, method_name, method,
                               method_type='keep')
