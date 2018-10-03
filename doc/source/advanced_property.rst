.. AdvancedProperty

API: AdvancedProperty
========================

.. py:module:: advanced_descriptors
.. py:currentmodule:: advanced_descriptors


.. py:class:: AdvancedProperty(property)

    Advanced property main entry point.

    .. versionadded:: 2.1.0 Inherit property

    .. py:method:: __init__(fget=None, fset=None, fdel=None, fcget=None, )

        :param fget: normal getter.
        :type fget: ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``
        :param fset: normal setter.
        :type fset: ``typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]``
        :param fdel: normal deleter.
        :type fdel: ``typing.Optional[typing.Callable[[typing.Any, ], None]]``
        :param fcget: class getter. Used as normal, if normal is None.
        :type fcget: ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``

    .. note:: doc argument is not supported due to class wide getter usage.

    .. py:method:: getter(fget)

        Descriptor to change the getter on a property.

        :param fget: new normal getter.
        :type fget: ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``
        :rtype: ``AdvancedProperty``

    .. py:method:: setter(fset)

        Descriptor to change the setter on a property.

        :param fset: new setter.
        :type fset: ``typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]``
        :rtype: ``AdvancedProperty``

    .. py:method:: deleter(fdel)

        Descriptor to change the deleter on a property.

        :param fdel: New deleter.
        :type fdel: ``typing.Optional[typing.Callable[[typing.Any, ], None]]``
        :rtype: ``AdvancedProperty``

    .. py:method:: cgetter(fcget)

        Descriptor to change the class wide getter on a property.

        :param fcget: new class-wide getter.
        :type fcget: ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``
        :rtype: ``AdvancedProperty``

    .. py:attribute:: fget

        ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``
        Getter instance.

    .. py:attribute:: fset

        ``typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]``
        Setter instance.

    .. py:attribute:: fdel

        ``typing.Optional[typing.Callable[[typing.Any, ], None]]``
        Deleter instance.

    .. py:attribute:: fcget

        ``typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]``
        Class wide getter instance.
