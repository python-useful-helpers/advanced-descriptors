.. SeparateClassMethod

API: SeparateClassMethod
========================

.. py:module:: advanced_descriptors
.. py:currentmodule:: advanced_descriptors


.. py:class:: SeparateClassMethod

    Separate class method and instance methods.

    .. py:method:: __init__(imeth=None, cmeth=None, )

        :param imeth: Instance method
        :type imeth: ``Callable[..., _MethodReturnT] | None``
        :param cmeth: Class method
        :type cmeth: ``Callable[..., _ClassMethodReturnT] | None``

    .. py:method:: instance_method(imeth)

        Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: ``Callable[..., _MethodReturnT] | None``
        :rtype: ``SeparateClassMethod``

    .. py:method:: class_method(cmeth)

        Descriptor to change class method.

        :type cmeth: New class method.
        :type cmeth: ``Callable[..., _ClassMethodReturnT] | None``
        :rtype: ``SeparateClassMethod``

    .. py:attribute:: imeth

        ``Callable[..., _MethodReturnT] | None``
        Instance method instance.

    .. py:attribute:: cmeth

        ``Callable[..., _ClassMethodReturnT] | None``
        Class method instance.
