.. SeparateClassMethod

API: SeparateClassMethod
========================

.. py:module:: advanced_descriptors
.. py:currentmodule:: advanced_descriptors


.. py:class:: SeparateClassMethod

    Separate class method and instance methods.

    .. py:method:: __init__(imeth=None, cmeth=None, )

        :param imeth: Instance method
        :type imeth: ``typing.Optional[typing.Callable]``
        :param cmeth: Class method
        :type cmeth: ``typing.Optional[typing.Callable]``

    .. py:method:: instance_method(imeth)

        Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: ``typing.Optional[typing.Callable]``
        :rtype: ``SeparateClassMethod``

    .. py:method:: class_method(cmeth)

        Descriptor to change class method.

        :type cmeth: New class method.
        :type cmeth: ``typing.Optional[typing.Callable]``
        :rtype: ``SeparateClassMethod``

    .. py:attribute:: imeth

        ``typing.Optional[typing.Callable]``
        Instance method instance.

    .. py:attribute:: cmeth

        ``typing.Optional[typing.Callable]``
        Class method instance.
