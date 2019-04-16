Advanced descriptors
====================

.. image:: https://travis-ci.com/python-useful-helpers/advanced-descriptors.svg?branch=master
    :target: https://travis-ci.com/python-useful-helpers/advanced-descriptors
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

Testing
=======
The main test mechanism for the package `advanced-descriptors` is using `tox`.
Available environments can be collected via `tox -l`

CI systems
==========
For code checking several CI systems is used in parallel:

1. `Travis CI: <https://travis-ci.com/python-useful-helpers/advanced-descriptors>`_ is used for checking: PEP8, pylint, bandit, installation possibility and unit tests. Also it's publishes coverage on coveralls.

2. `coveralls: <https://coveralls.io/github/python-useful-helpers/advanced-descriptors>`_ is used for coverage display.

CD system
=========
`Travis CI: <https://travis-ci.com/python-useful-helpers/advanced-descriptors>`_ is used for package delivery on PyPI.
