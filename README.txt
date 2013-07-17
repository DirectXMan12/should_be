========
ShouldBe
========

---------------------------------------------
Python Assertion Helpers Inspired by Shouldly
---------------------------------------------

Requirements
============

- forbiddenfruit
- a version of python with which forbidden fruit will work
  (must implement the CTypes/CPython Python API)
- Python 2.7 or 3.3
  (it may work with other versions, such as other 3.x versions,
  but it has not been tested with these versions)

Assertions
==========

See ASSERTIONS.rst

Example
=======

::

    >>> import should_be.all
    >>> class Cheese(object):
    ...     crackers = 3
    ...
    >>> swiss = Cheese()
    >>> swiss.crackers.should_be(4)
    AssertionError: swiss.crackers should have been 4, but was 3


.. note::

   Because of the way the Python REPL shows stack traces, if the 'should_be'
   assertion is typed in a line on the REPL, '(unknown)' will show instead
   of 'swiss.crackers'.  This is not an issue when the 'should_be' statement
   is in a file instead.

Installation
============

The easy way

.. code-block:: bash

   $ sudo pip install https://github.com/DirectXMan12/should_be.git#egg=ShouldBe

The slightly-less-easy way

.. code-block:: bash

   $ git clone https://github.com/DirectXMan12/should_be.git
   $ cd should_be
   $ ./setup.py build
   $ sudo ./setup.py install

Extending
=========

Writing your own assertions is fairly easy.  There are two core parts of
ShouldBe: `BaseMixin` and `should_follow`.

All assertions should be placed in classes that inherit from `BaseMixin`.
`BaseMixin` provides the basic utilities for extending built-in objects
with your assertions.

The class which holds your assertions should have a class variable called
`target_class`.  This is the class on which your assertions will be run.
By default, this is set to `object`.  If you wish to have your assertions
run on `object`, there are a few additional considerations to make (see
warning below).

Then, assertions should be defined as instance methods.  Each method should call
`self.should_follow` one or more times.  Think of `should_follow` as `assertTrue`
on steroids.  It has the following signature:
`should_follow(self, assertion, msg=None, **kwargs)`.  Obviously, assertion is
an expression which, when `False`, causes `should_follow` to raise an `AssertionError`.
So far, pretty normal.  `msg` is where things get interesting.  `msg` should be
a new-style Python format string which contains only named substitutions.  By
default, `should_follow` will pass the `txt` and `self` keys to the `format` method,
in addition to any keyword arguments passed to `should_follow`.  `self` is, obviously,
the current object.  `txt` is the code that represents the current object.  For instance,
if we wrote `(3).should_be(4)`, `txt` would be '(3)'.  If we wrote
`cheese.variety.should_be('cheddar')`, `txt` would be 'cheese.variety'.

Once all of your assertions are written, you can simply write
`MyAssertionMixin.mix()` to load your assertions.  A `setuptools`
hook is on the way for autoloading custom assertion mixins
with `import should_be.all`.

.. warning::

   When you extend object, you need to also create the proper mixins for
   `NoneType`, since `None` doesn't have instance methods per-se (since
   `self` gets set to `None`, the Python interpreter complains).  Thankfully,
   this is fairly easy.  Simply create a class which inherits from `NoneTypeMixin`,
   and set the class variable `source_class` to the name of your `object` assertions
   class.  You can then simply run `MyNoneTypeMixin.mix()`, and your methods will
   be automatically retrieved and converted from your `object` mixin class.
