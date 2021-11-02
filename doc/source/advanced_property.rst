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
        :type fget: ``typing.Callable[[_OwnerClassT], _ReturnT] | None``
        :param fset: normal setter.
        :type fset: ``typing.Callable[[_OwnerClassT, _ReturnT], None] | None``
        :param fdel: normal deleter.
        :type fdel: ``typing.Callable[[_OwnerClassT], None] | None``
        :param fcget: class getter. Used as normal, if normal is None.
        :type fcget: ``typing.Callable[[type[_OwnerClassT]], _ClassReturnT] | None``

    .. note:: doc argument is not supported due to class wide getter usage.

    .. py:method:: getter(fget)

        Descriptor to change the getter on a property.

        :param fget: new normal getter.
        :type fget: ``typing.Callable[[_OwnerClassT], _ReturnT] | None``
        :rtype: ``AdvancedProperty``

    .. py:method:: setter(fset)

        Descriptor to change the setter on a property.

        :param fset: new setter.
        :type fset: ``typing.Callable[[_OwnerClassT, _ReturnT], None] | None``
        :rtype: ``AdvancedProperty``

    .. py:method:: deleter(fdel)

        Descriptor to change the deleter on a property.

        :param fdel: New deleter.
        :type fdel: ``typing.Callable[[_OwnerClassT], None] | None``
        :rtype: ``AdvancedProperty``

    .. py:method:: cgetter(fcget)

        Descriptor to change the class wide getter on a property.

        :param fcget: new class-wide getter.
        :type fcget: ``typing.Callable[[type[_OwnerClassT]], _ClassReturnT] | None``
        :rtype: ``AdvancedProperty``

    .. py:attribute:: fget

        ``typing.Callable[[_OwnerClassT], _ReturnT] | None``
        Getter instance.

    .. py:attribute:: fset

        ``typing.Callable[[_OwnerClassT, _ReturnT], None] | None``
        Setter instance.

    .. py:attribute:: fdel

        ``typing.Callable[[_OwnerClassT], None] | None``
        Deleter instance.

    .. py:attribute:: fcget

        ``typing.Callable[[type[_OwnerClassT]], _ClassReturnT] | None``
        Class wide getter instance.
