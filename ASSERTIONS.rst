==========
Assertions
==========

All assertions and their parameters are listed here,
organized by target class.  Assertions with a parameter
list mentioned take 1 parameter (a pair of empty parentheses
will be noted if an assertion takes no parameters).  Assertions
with no specific documentation (just a name) do exactly
what they sound like.  '/' denotes an opposite,
while ',' denotes an alias.  Some objects override
methods from object mixin, but those are not explicitly
listed in the object sections.

Object
======

should_be / shouldnt_be
    assert that self is equal/not equal to target

should_be_exactly / shouldnt_be_exactly 
    assert that self :code:`is`/:code:`is not` target

should_be_none / shouldnt_be_none : ()

should_be_in / shouldnt_be_in

should_be_a / shouldnt_be_a
    assert that self is/is not an instance of target

should_be_truthy, should_be_true : ()
    assert that the boolean representation of self is true

should_be_falsy, should_be_false : ()
    assert thta the boolean representation of self is false

should_raise : `(target, *args, **kwargs)`
    assert that self, when called with `args` and `kwargs`,
    raises the target exception

should_raise_with_message : `(target, tmsg, *args, **kwargs)`
    like should_raise, but also checks that the exception's
    string representation (message) matches the given regular
    expression

NoneType
========

Same as object

Sequence
========

should_have_same_items_as
    assert that the items in self are the same as those
    in target, no matter the order

Basestring/String
=================

should_match / shouldnt_match
    assert that self matches/does not match the given regular expression

Sized
=====

should_be_size, should_have_len, should_have_length
    assert that the size of self is target

should_be_size_of, should_match_size_of, should_match_len_of, should_match_length_of
    assert that self has the same size as target

should_be_at_least_size, should_be_at_least_len, should_be_at_least_length

should_be_at_most_size, should_be_at_most_len, should_be_at_most_length

should_be_at_least_size_of, should_be_at_least_len_of, should_be_at_least_length_of

should_be_at_most_size_of, should_be_at_most_len_of, should_be_at_most_length_of

should_be_bigger_than
    if target is a Sized, assert that the size of self is larger than that of
    target.  Otherwise, assert that the size of self is greater than target

should_be_smaller_than

should_be_empty / shouldnt_be_empty : ()

Number (Real)
=============

should_be_roughly / shouldnt_be_roughly : (target, places=None, delta=None)
    assert that self is/is not within `places` or `delta` of target (do not
    specify both `places` and `delta`, only one, the other, or neither, which
    is the same as :code:`places=7`)

should_be_above, should_be_greater_than, should_be_more_than

should_be_below, should_be_less_than

should_be_at_or_above, should_be_greater_than_or_equal_to, should_be_at_least

should_be_at_or_below, should_be_less_than_or_equal_to, should_be_at_most

Mapping
=======

(this has a couple undocumented assertions that are subject
to change in the near future)

Iterable
========

should_be_part_of / shouldnt_be_part_of
    asserts that self is/is not a part of target (in any order and
    not necessarily contiguous)

Container
=========

should_include / shouldnt_include
    if target is Iterable, assert that self does/does not include
    the items of target (in any order, not neccesarily contiguously),
    otherwise, assert that target is/is not in self

