#!/usr/bin/env python

#    Copyright 2017-2018 Alexey Stepanov aka penguinolog
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
import typing

__all__ = ("SeparateClassMethod",)


class SeparateClassMethod:
    """Separate class method and instance methods with the same name.

    Usage examples:

    >>> class WithNormalMethod:  # no wrapper should be used
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

    >>> class WithSeparateMethod:
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

    >>> class WithClassMethod:  # @classmethod should be used
    ...     def _func(cls):
    ...         return cls
    ...     meth = SeparateClassMethod(cmeth=_func)

    >>> WithClassMethod.meth() is WithClassMethod
    True

    >>> WithClassMethod().meth() is WithClassMethod
    True
    """

    __slots__ = ("__instance_method", "__class_method", "__owner", "__name")

    def __init__(
        self, imeth: typing.Optional[typing.Callable] = None, cmeth: typing.Optional[typing.Callable] = None
    ) -> None:
        """Separate class method and instance methods.

        :param imeth: Instance method
        :type imeth: typing.Optional[typing.Callable]
        :param cmeth: Class method
        :type cmeth: typing.Optional[typing.Callable]
        """
        self.__instance_method = imeth
        self.__class_method = cmeth
        self.__owner = None
        self.__name = ""

    def __set_name__(self, owner: typing.Any, name: str) -> None:
        """Set __name__ and __objclass__ property."""
        self.__owner = owner
        self.__name = name

    def __get__(self, instance: typing.Optional[typing.Any], owner: typing.Any) -> typing.Callable:
        """Get descriptor.

        :return: class method or instance method depends on call behavior
        :rtype: typing.Callable
        :raises AttributeError: Not implemented getter for class method and called class context.
        """
        if instance is None or self.__instance_method is None:
            if self.__class_method is None:
                raise AttributeError()

            @functools.wraps(self.__class_method)
            def class_method(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
                """Bound class method."""
                return self.__class_method(owner, *args, **kwargs)  # type: ignore

            return class_method

        @functools.wraps(self.__instance_method)
        def instance_method(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            """Bound instance method."""
            return self.__instance_method(instance, *args, **kwargs)  # type: ignore

        return instance_method

    @property
    def __objclass__(self) -> typing.Any:  # pragma: no cover
        """Read-only owner."""
        return self.__owner

    @property
    def __name__(self) -> str:  # pragma: no cover
        """Read-only name."""
        return self.__name

    def instance_method(self, imeth: typing.Optional[typing.Callable]) -> "SeparateClassMethod":
        """Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: typing.Optional[typing.Callable]
        :return: SeparateClassMethod
        :rtype: SeparateClassMethod
        """
        self.__instance_method = imeth
        return self

    def class_method(self, cmeth: typing.Optional[typing.Callable]) -> "SeparateClassMethod":
        """Descriptor to change class method.

        :param cmeth: New class method.
        :type cmeth: typing.Optional[typing.Callable]
        :return: SeparateClassMethod
        :rtype: SeparateClassMethod
        """
        self.__class_method = cmeth
        return self

    @property
    def imeth(self) -> typing.Optional[typing.Callable]:
        """Instance method instance.

        :rtype: typing.Optional[typing.Callable]
        """
        return self.__instance_method

    @property
    def cmeth(self) -> typing.Optional[typing.Callable]:
        """Class method instance.

        :rtype: typing.Optional[typing.Callable]
        """
        return self.__class_method


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod(verbose=True)
