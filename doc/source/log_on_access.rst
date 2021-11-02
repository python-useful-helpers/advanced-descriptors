.. AdvancedProperty

API: LogOnAccess
========================

.. py:module:: advanced_descriptors
.. py:currentmodule:: advanced_descriptors


.. py:class:: LogOnAccess(property)

    Property with logging on successful get/set/delete or failure.

    .. versionadded:: 2.1.0
    .. versionchanged:: 2.2.0 Re-use logger from instance, if possible.

    .. py:method:: __init__(fget=None, fset=None, fdel=None, doc=None, *, logger=None, log_object_repr=True, log_level=logging.DEBUG, exc_level=logging.DEBUG, log_success=True, log_failure=True, log_traceback=True, override_name=None)

        :param fget: normal getter.
        :type fget: ``typing.Callable[[_OwnerT], _ReturnT] | None``
        :param fset: normal setter.
        :type fset: ``typing.Callable[[_OwnerT, _ReturnT], None] | None``
        :param fdel: normal deleter.
        :type fdel: ``typing.Callable[[_OwnerT], None] | None``
        :param doc: docstring override
        :type doc: ``str | None``
        :param logger: logger instance or name to use as override
        :type logger: ``logging.Logger | str | None``
        :param log_object_repr: use `repr` over object to describe owner if True else owner class name and id
        :type log_object_repr: ``bool``
        :param log_level: log level for successful operations
        :type log_level: ``int``
        :param exc_level: log level for exceptions
        :type exc_level: ``int``
        :param log_success: log successful operations
        :type log_success: ``bool``
        :param log_failure: log exceptions
        :type log_failure: ``bool``
        :param log_traceback: Log traceback on exceptions
        :type log_traceback: ``bool``
        :param override_name: override property name if not None else use getter/setter/deleter name
        :type override_name: ``str | None``

    .. py:method:: getter(fget)

        Descriptor to change the getter on a property.

        :param fget: new normal getter.
        :type fget: ``typing.Callable[[_OwnerT], _ReturnT] | None``
        :rtype: ``AdvancedProperty``

    .. py:method:: setter(fset)

        Descriptor to change the setter on a property.

        :param fset: new setter.
        :type fset: ``typing.Callable[[_OwnerT, _ReturnT], None] | None``
        :rtype: ``AdvancedProperty``

    .. py:method:: deleter(fdel)

        Descriptor to change the deleter on a property.

        :param fdel: New deleter.
        :type fdel: ``typing.Callable[[_OwnerT], None] | None``
        :rtype: ``AdvancedProperty``

    .. py:attribute:: fget

        ``typing.Callable[[_OwnerT], _ReturnT] | None``
        Getter instance.

    .. py:attribute:: fset

        ``typing.Callable[[_OwnerT, _ReturnT], None] | None``
        Setter instance.

    .. py:attribute:: fdel

        ``typing.Callable[[_OwnerT], None] | None``
        Deleter instance.

    .. py:attribute:: logger

        ``typing.Optional[logging.Logger]``
        Logger instance to use as override.

    .. py:attribute:: log_object_repr

        ``bool``
        Use `repr` over object to describe owner if True else owner class name and id.

    .. py:attribute:: log_level

        ``int``
        Log level for successful operations.

    .. py:attribute:: exc_level

        ``int``
        Log level for exceptions.

    .. py:attribute:: log_success

        ``bool``
        Log successful operations.

    .. py:attribute:: log_failure

        ``bool``
        Log exceptions.

    .. py:attribute:: log_traceback

        ``bool``
        Log traceback on exceptions.

    .. py:attribute:: override_name

        ``str | None``
        Override property name if not None else use getter/setter/deleter name.
