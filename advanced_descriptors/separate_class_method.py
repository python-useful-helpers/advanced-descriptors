#!/usr/bin/env python

#    Copyright 2017 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Separate class and instance methods with the same name."""

import functools

try:  # pragma: no cover
    import typing
    TargetFunctionType = typing.Optional[typing.Callable[..., typing.Any]]
except ImportError:  # pragma: no cover
    typing = None
    TargetFunctionType = None

__all__ = (
    'SeparateClassMethod',
)

_WRAPPER_ASSIGNMENTS = (
    '__module__',
    '__name__',
    '__qualname__',
    '__doc__',
    '__annotations__'
)
_WRAPPER_UPDATES = ('__dict__',)


def _update_wrapper(wrapper,
                    wrapped,
                    assigned=_WRAPPER_ASSIGNMENTS,
                    updated=_WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function.

    wrapper is the function to be updated
    wrapped is the original function
    assigned is a tuple naming the attributes assigned directly
    from the wrapped function to the wrapper function (defaults to
    functools.WRAPPER_ASSIGNMENTS)
    updated is a tuple naming the attributes of the wrapper that
    are updated with the corresponding attribute from the wrapped
    function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper


def _wraps(wrapped,
           assigned=_WRAPPER_ASSIGNMENTS,
           updated=_WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function.

    Returns a decorator that invokes update_wrapper() with the decorated
    function as the wrapper argument and the arguments to wraps() as the
    remaining arguments. Default arguments are as for update_wrapper().
    This is a convenience function to simplify applying partial() to
    update_wrapper().
    """
    return functools.partial(
        _update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)


class SeparateClassMethod(object):
    """Separate class method and instance methods with the same name.

    Usage examples:

    >>> class WithNormalMethod(object):  # no wrapper should be used
    ...     def __init__(self):
    ...         self.val=42
    ...     @SeparateClassMethod
    ...     def set_val(self, new_val):
    ...         self.val=new_val

    >>> tst_obj = WithNormalMethod()
    >>> tst_obj.val
    42

    >>> tst_obj.set_val(21)
    >>> tst_obj.val
    21

    >>> WithNormalMethod.set_val()  # It's not defined
    Traceback (most recent call last):
    ...
    AttributeError

    >>> class WithSeparateMethod(object):
    ...     val = 33
    ...     def __init__(self):
    ...         self.val=42
    ...     @SeparateClassMethod
    ...     def set_val(self, new_val):
    ...         self.val=new_val
    ...     @set_val.class_method
    ...     def set_val(cls, new_val):
    ...         cls.val=new_val

    >>> tst_obj = WithSeparateMethod()
    >>> WithSeparateMethod.val
    33

    >>> tst_obj.val
    42

    >>> tst_obj.set_val(21)  # normal method
    >>> tst_obj.val
    21

    >>> WithSeparateMethod.val
    33

    >>> WithSeparateMethod.set_val(44)  # class method (not instance)
    >>> tst_obj.val
    21
    >>> WithSeparateMethod.val
    44

    >>> class WithClassMethod(object):  # @classmethod should be used
    ...     def _func(cls):
    ...         return cls
    ...     meth = SeparateClassMethod(cmeth=_func)

    >>> WithClassMethod.meth() is WithClassMethod
    True

    >>> WithClassMethod().meth() is WithClassMethod
    True
    """

    __slots__ = (
        '__instance_method',
        '__class_method',
    )

    def __init__(
            self,
            imeth=None,  # type: TargetFunctionType
            cmeth=None,  # type: TargetFunctionType
    ):
        """Separate class method and instance methods.

        :param imeth: Instance method
        :type imeth: typing.Optional[typing.Callable[..., typing.Any]]
        :param cmeth: Class method
        :type cmeth: typing.Optional[typing.Callable[..., typing.Any]]
        """
        self.__instance_method = imeth
        self.__class_method = cmeth

    def __get__(self, instance, owner):  # type: (...) -> TargetFunctionType
        """Get descriptor.

        :rtype: typing.Callable[..., typing.Any]
        :raises: AttributeError
        """
        if instance is None or self.__instance_method is None:
            if self.__class_method is None:
                raise AttributeError()

            @_wraps(self.__class_method)
            def class_method(*args, **kwargs):
                """Bound class method."""
                return self.__class_method(owner, *args, **kwargs)

            return class_method

        @_wraps(self.__class_method)
        def instance_method(*args, **kwargs):
            """Bound instance method."""
            return self.__instance_method(instance, *args, **kwargs)

        return instance_method

    def instance_method(
            self,
            imeth  # type: TargetFunctionType
    ):  # type: (...) -> SeparateClassMethod
        """Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: typing.Optional[typing.Callable[..., typing.Any]]
        :rtype: SeparateClassMethod
        """
        self.__instance_method = imeth
        return self

    def class_method(
            self,
            cmeth  # type: TargetFunctionType
    ):  # type: (...) -> SeparateClassMethod
        """Descriptor to change class method.

        :type cmeth: New class method.
        :type cmeth: typing.Optional[typing.Callable[..., typing.Any]]
        :rtype: SeparateClassMethod
        """
        self.__class_method = cmeth
        return self

    @property
    def imeth(self):  # type: (SeparateClassMethod) -> TargetFunctionType
        """Instance method instance.

        :rtype: typing.Optional[typing.Callable[..., typing.Any]]
        """
        return self.__instance_method

    @property
    def cmeth(self):  # type: (SeparateClassMethod) -> TargetFunctionType
        """Class method instance.

        :rtype: typing.Optional[typing.Callable[..., typing.Any]]
        """
        return self.__class_method


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod(verbose=True)
