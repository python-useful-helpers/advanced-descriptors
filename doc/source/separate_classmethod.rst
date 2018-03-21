.. SeparateClassMethod

API: SeparateClassMethod
========================

.. py:module:: advanced_descriptors
.. py:currentmodule:: advanced_descriptors


.. py:class:: SeparateClassMethod(imeth=None, cmeth=None, )

    Separate class method and instance methods.

    :param imeth: Instance method
    :type imeth: ``typing.Optional[typing.Callable[..., typing.Any]]``
    :param cmeth: Class method
    :type cmeth: ``typing.Optional[typing.Callable[..., typing.Any]]``

    .. py:method:: instance_method(imeth)

        Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: ``typing.Optional[typing.Callable[..., typing.Any]]``
        :rtype: ``SeparateClassMethod``

    .. py:method:: class_method(cmeth)

        Descriptor to change class method.

        :type cmeth: New class method.
        :type cmeth: ``typing.Optional[typing.Callable[..., typing.Any]]``
        :rtype: ``SeparateClassMethod``

    .. py:attribute:: imeth

        ``typing.Optional[typing.Callable[..., typing.Any]]``
        Instance method instance.

    .. py:attribute:: cmeth

        ``typing.Optional[typing.Callable[..., typing.Any]]``
        Class method instance.
