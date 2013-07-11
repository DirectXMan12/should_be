from forbiddenfruit import curse
from collections import Sequence, Mapping, Container, Iterable, Counter, Set, Sized
import inspect
import numbers
import re
import abc


def findObjectName(mname=None):
    stack = inspect.stack()

    if mname is None:
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

class BaseMixin(object):

    target_class = object

    @staticmethod
    def mix_method(target, method_name, method, method_type=None):
        print 'Mixing {0} into {1}'.format(method_name, target)

        if method_type == 'static':
            method = staticmethod(method)
        elif method_type == 'class':
            method = classmethod(method)

        if method_type is None and hasattr(method, '__func__'):
            curse(target, method_name, method.__func__)
        else:
            curse(target, method_name, method)
         

    @classmethod
    def __mixin__(cls, target, method_type=None):
        methods = inspect.getmembers(cls, inspect.ismethod)
        for method_name, method in methods:
            if (method_name not in dir(BaseMixin)
                or method_name == 'should_follow'):
                cls.mix_method(target, method_name, method, method_type)
                        
        

    @classmethod
    def mix(cls, target=None):
        if target is None:
            target = cls.target_class

        cls.__mixin__(target)

        def submix(target_cls):
            try:
                if issubclass(target_cls.__metaclass__, abc.ABCMeta):
                    print 'submixing {0}'.format(target_cls)
                    for impl_cls in target_cls._abc_registry:
                        if 'UserDict' in str(impl_cls):
                            pass # for some reason this class segfaults
                        else:
                            attr_name = '_should_be_{0}.{1}'
                            attr_name = attr_name.format(cls.__module__,
                                                         cls.__name__)

                            if attr_name not in dir(impl_cls):
                                cls.__mixin__(impl_cls)
                                cls.mix_method(target, attr_name, lambda x: True)

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
        self.should_follow(isinstance(self, target), msg,
                           val=target, self_class=type(self))

    def shouldnt_be_a(self, target):
        msg = '{txt} should not have been a {val}, but was anyway'
        self.should_follow(not isinstance(self, target), msg, val=target)

    def should_be_truthy(self):
        msg = '{txt} should have been truthy, but was {self}'
        self.should_follow(bool(self) is True, msg, val=True)

    should_be_true = should_be_truthy

    def should_be_falsy(self):
        msg = '{txt} should not have falsy, but was anyway'
        self.should_follow(bool(self) is False, msg, val=False)
    
    should_be_false = should_be_falsy

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


class NumberMixin(BaseMixin):
    target_class = numbers.Real

    def should_be_roughly(self, target, places=None, delta=None):
        if self == target:
            return

        if delta is not None and places is not None:
            raise TypeError('specify delta or places, not both')

        if delta is not None:
            msg = ("{txt} should have been within {delta} of {val},"
                   " but was {self}, which is {actual_delta} from {val}") 
            self.should_follow(abs(self - target) <= delta,
                               msg,
                               delta=delta,
                               actual_delta=abs(self - target),
                               val=target)
        else:
            if places is None:
                places = 7

            msg = ("{txt} should have been equal to {val} within {places}"
                   " places, but was {self}")
            self.should_follow(round(abs(self - target), places) == 0,
                               msg,
                               places=places,
                               val=target)

    def shouldnt_be_roughly(self, target, delta=None, places=None):
        if delta is not None and places is not None:
            raise TypeError('specify delta or places, not both')

        if delta is not None:
            msg = ("{txt} should not have been within {delta} of {val},"
                   " but was {self}, which is {actual_delta} from {val}") 
            expr = self != target and abs(self - target) > delta
            self.should_follow(expr,
                               msg,
                               delta=delta,
                               actual_delta=abs(self - target),
                               val=target)
        else:
            if places is None:
                places = 7

            msg = ("{txt} should not have been equal to {val} within {places}"
                   " places, but was {self}")
            expr = self != target and round(abs(self - target), places) != 0
            self.should_follow(expr,
                               msg,
                               places=places,
                               val=target)

    def should_be_above(self, target):
        msg = '{txt} should have been greater than {val}, but was {self}'
        self.should_follow(self > target, msg, val=target)

    should_be_greater_than = should_be_above
    should_be_more_than = should_be_above

    def should_be_below(self, target):
        msg = '{txt} should have been less than {val}, but was {self}'
        self.should_follow(self < target)

    should_be_less_than = should_be_below

    def should_be_at_or_above(self, target):
        msg = ('{txt} should have been greater than or equal '
               'to {val}, but was {self}')
        self.should_follow(self >= target, msg, val=target)
    
    should_be_greater_than_or_equal_to = should_be_at_or_above

    def should_be_at_or_below(self, target):
        msg = ('{txt} should have been less than or equal '
               'to {val}, but was {self}')
        self.should_follow(self <= target, msg, val=target)
         
    should_be_less_than_or_equal_to = should_be_at_or_below

class StringMixin(BaseMixin):
    target_class = basestring

    def should_match(self, target):
        msg = '{txt} should have matched {re}, but was {self} instead'
        self.should_follow(re.match(target, self), msg, re=target)

    def shouldnt_match(self, target):
        msg = '{txt} should not have matched {re}, but did anyway'
        self.should_follow(re.match(target, self) is None, msg, re=target)

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
            self.should_follow(len(self) == len(target), msg,
                               val=target,
                               l1=len(self),
                               l2=len(target))
            item_msg = ('{txt} should have been {val}, but they differed '
                        ' at item {ind} ({i1} vs {i2})')
            for i in xrange(len(self)):
                self.should_follow(self[i] == target[i], msg,
                                   val=target,
                                   i1=self[i],
                                   i2=target[i])
        except (TypeError, NotImplementedError):
            ObjectMixin.should_be(self, target)

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
        
class ContainerMixin(BaseMixin):
    target_class = Container

    def should_include(self, target):
        msg = ('{txt} should have included {val}, but did not have '
              'items {items}')
        
        missing_items = []
        for item in target:
            if item not in self:
                missing_items.append(item)

        self.should_follow(len(missing_items) == 0, msg,
                           val=target,
                           items=missing_items)

class SizedMixin(BaseMixin):
    target_class = Sized

    def should_be_size(self, target):
        msg = '{txt} should have been size {val}, but was size {self_size}'
        self.should_follow(len(self) == target, msg,
                           val=target,
                           self_size=len(self))

    should_have_len = should_be_size
    should_have_length = should_be_size

    def should_be_size_of(self, target):
        msg = ('{txt} should have been the size of {val} ({val_size}), '
                'but was size {self_size}')
        self.should_follow(len(self) == len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    should_match_size_of = should_be_size_of
    should_match_len_of = should_be_size_of
    should_match_length_of = should_be_size_of

    def should_be_at_least_size(self, target):
        msg = ('{txt} should have been at least size {val}, but '
               'was size {self_size}')
        self.should_follow(len(self) >= target, msg,
                           val=target,
                           self_size=len(self))

    should_be_at_least_len = should_be_at_least_size
    should_be_at_least_length = should_be_at_least_size

    def should_be_at_most_size(self, target):
        msg = ('{txt} should have been at most size {val}, but '
               'was size {self_size}')
        self.should_follow(len(self) <= target, msg,
                           val=target,
                           self_size=len(self))

    should_be_at_most_len = should_be_at_most_size
    should_be_at_most_length = should_be_at_most_size

    def should_be_at_least_size_of(self, target):
        msg = ('{txt} should have been at least the size of {val} ({val_size})'
                ', but was size {self_size}')
        self.should_follow(len(self) >= len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    should_be_at_least_len_of = should_be_at_least_size_of
    should_be_at_least_length_of = should_be_at_least_size_of

    def should_be_at_most_size_of(self, target):
        msg = ('{txt} should have been at most the size of {val} ({val_size})'
                ', but was size {self_size}')
        self.should_follow(len(self) <= len(target), msg,
                           val=target,
                           val_size=len(target),
                           self_size=len(self))

    should_be_at_most_len_of = should_be_at_most_size_of
    should_be_at_most_length_of = should_be_at_most_size_of

    def should_be_bigger_than(self, target):
        if isinstance(target, Sized):
            # we have a sized object
            msg = ('{txt} should have been bigger than {val} ({val_size}), '
                   'but was size {self_size}')
            self.should_follow(len(self) > len(target), msg,
                               val=target,
                               val_size=len(target),
                               self_size=len(self))

        else:
            # have a number 
            msg = ('{txt} should have had size greater than {val}, but '
                   'was size {self_size}')
            self.should_follow(len(self) > target, msg,
                               val=target,
                               self_size=len(self))

    should_be_longer_than = should_be_bigger_than

    def should_be_smaller_than(self, target):
        if isinstance(target, Sized):
            # we have a sized object
            msg = ('{txt} should have been smaller than {val} ({val_size}), '
                   'but was size {self_size}')
            self.should_follow(len(self) < len(target), msg,
                               val=target,
                               val_size=len(target),
                               self_size=len(self))

        else:
            # have a number 
            msg = ('{txt} should have had size less than {val}, but '
                   'was size {self_size}')
            self.should_follow(len(self) < target, msg,
                               val=target,
                               self_size=len(self))

    should_be_shorter_than = should_be_smaller_than
    

class MappingMixin(BaseMixin):
    target_class = Mapping

    def should_include_values(self, target):
        ContainerMixin.should_include(self.items(), target.items())

    def should_be_part_of_values(self, target):
        IterableMixin.should_be_part_of(self.items(), target.items())

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
