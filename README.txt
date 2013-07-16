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

