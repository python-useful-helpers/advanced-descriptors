Advanced descriptors
====================

.. image:: https://travis-ci.com/python-useful-helpers/advanced-descriptors.svg?branch=master
    :target: https://travis-ci.com/python-useful-helpers/advanced-descriptors
.. image:: https://dev.azure.com/python-useful-helpers/advanced-descriptors/_apis/build/status/python-useful-helpers.advanced-descriptors?branchName=master
    :alt: Azure DevOps builds
    :target: https://dev.azure.com/python-useful-helpers/advanced-descriptors/_build?definitionId=2
.. image:: https://coveralls.io/repos/github/python-useful-helpers/advanced-descriptors/badge.svg?branch=master
    :target: https://coveralls.io/github/python-useful-helpers/advanced-descriptors?branch=master
.. image:: https://readthedocs.org/projects/advanced-descriptors/badge/?version=latest
    :target: http://advanced-descriptors.readthedocs.io/
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/advanced-descriptors.svg
    :target: https://pypi.python.org/pypi/advanced-descriptors
.. image:: https://img.shields.io/pypi/pyversions/advanced-descriptors.svg
    :target: https://pypi.python.org/pypi/advanced-descriptors
.. image:: https://img.shields.io/pypi/status/advanced-descriptors.svg
    :target: https://pypi.python.org/pypi/advanced-descriptors
.. image:: https://img.shields.io/github/license/python-useful-helpers/advanced-descriptors.svg
    :target: https://raw.githubusercontent.com/python-useful-helpers/advanced-descriptors/master/LICENSE
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

This package includes helpers for special cases:

* `SeparateClassMethod` - allow to have classmethod and normal method both with the same name.

* `AdvancedProperty` - property with possibility to set class wide getter.

* `LogOnAccess` - property with logging on successful get/set/delete or failure.

SeparateClassMethod
-------------------

This descriptor can be set using standard decorator syntax.
Create instance with arguments:

.. code-block:: python

  def imeth(instance):
      return instance.value

  def cmeth(owner):
      return owner.value

  class Target(object):
      value = 1

      def __init__(self):
          self.value = 2
      getval = advanced_descriptors.SeparateClassMethod(
          imeth, cmeth
      )

Create instance wrapping as decorator:

.. code-block:: python

  class Target(object):
      value = 1

      def __init__(self):
          self.value = 2

      @advanced_descriptors.SeparateClassMethod
      def getval(self):
          return self.value

      @getval.class_method
      def getval(cls):
          return cls.value

Cases with method only and classmethod only is useless:
method as-is and `@classmethod` should be used in corresponding cases.

.. note::

  classmethod receives class as argument. IDE's don't know about custom descriptors and substitutes `self` by default.

AdvancedProperty
----------------

This descriptor should be used in cases, when in addition to normal property API, class getter is required.
If class-wide setter and deleter also required - you should use standard propery in metaclass.

Usage examples:

1. In addition to normal property API:

  .. code-block:: python

    class Target(object):
        _value = 777

        def __init__(self):
            self._value = 42

        @advanced_descriptors.AdvancedProperty
        def val(self):
            return self._value

        @val.setter
        def val(self, value):
            self._value = value

        @val.deleter
        def val(self):
            self._value = 0

        @val.cgetter
        def val(cls):
            return cls._value

2. Use class-wide getter for instance too:

  .. code-block:: python

    class Target(object):
        _value = 1

        val = advanced_descriptors.AdvancedProperty()

        @val.cgetter
            def val(cls):
                return cls._value

.. note::

  class-wide getter receives class as argument. IDE's don't know about custom descriptors and substitutes `self` by default.

LogOnAccess
-----------

This special case of property is useful in cases, where a lot of properties should be logged by similar way without writing a lot of code.

Basic API is conform with `property`, but in addition it is possible to customize logger, log levels and log conditions.

Usage examples:

1. Simple usage.
   All by default.
   logger is re-used from instance if available with names `logger` or `log` else used internal `advanced_descriptors.log_on_access` logger:

  .. code-block:: python

    import logging

    class Target(object):

        def init(self, val='ok')
            self.val = val
            self.logger = logging.get_logger(self.__class__.__name__)  # Single for class, follow subclassing

        def __repr__(self):
            return "{cls}(val={self.val})".format(cls=self.__class__.__name__, self=self)

        @advanced_descriptors.LogOnAccess
        def ok(self):
            return self.val

        @ok.setter
        def ok(self, val):
            self.val = val

        @ok.deleter
        def ok(self):
            self.val = ""

2. Use with global logger for class:

  .. code-block:: python

    class Target(object):

      def init(self, val='ok')
          self.val = val

      def __repr__(self):
          return "{cls}(val={self.val})".format(cls=self.__class__.__name__, self=self)

      @advanced_descriptors.LogOnAccess
      def ok(self):
          return self.val

      @ok.setter
      def ok(self, val):
          self.val = val

      @ok.deleter
      def ok(self):
          self.val = ""

      ok.logger = 'test_logger'
      ok.log_level = logging.INFO
      ok.exc_level = logging.ERROR
      ok.log_object_repr = True  # As by default
      ok.log_success = True  # As by default
      ok.log_failure = True  # As by default
      ok.log_traceback = True  # As by default
      ok.override_name = None  # As by default: use original name

Testing
=======
The main test mechanism for the package `advanced-descriptors` is using `tox`.
Available environments can be collected via `tox -l`

CI systems
==========
For code checking several CI systems is used in parallel:

1. `Travis CI: <https://travis-ci.com/python-useful-helpers/advanced-descriptors>`_ is used for checking: PEP8, pylint, bandit, installation possibility and unit tests. Also it's publishes coverage on coveralls.

2. `coveralls: <https://coveralls.io/github/python-useful-helpers/advanced-descriptors>`_ is used for coverage display.

3. `Azure CI: <https://dev.azure.com/python-useful-helpers/advanced-descriptors/_build?definitionId=2>`_ is used for functional tests on Windows.

CD system
=========
`Travis CI: <https://travis-ci.com/python-useful-helpers/advanced-descriptors>`_ is used for package delivery on PyPI.
