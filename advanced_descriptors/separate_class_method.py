#!/usr/bin/env python

#    Copyright 2017 - 2022 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Separate class and instance methods with the same name."""

from __future__ import annotations

# Standard Library
import functools
import typing

if typing.TYPE_CHECKING:
    # Standard Library
    from collections.abc import Callable

__all__ = ("SeparateClassMethod",)

_MethodReturnT = typing.TypeVar("_MethodReturnT")
_ClassMethodReturnT = typing.TypeVar("_ClassMethodReturnT")


class SeparateClassMethod(typing.Generic[_MethodReturnT, _ClassMethodReturnT]):
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
        self,
        imeth: Callable[..., _MethodReturnT] | None = None,
        cmeth: Callable[..., _ClassMethodReturnT] | None = None,
    ) -> None:
        """Separate class method and instance methods.

        :param imeth: Instance method
        :type imeth: Callable[..., _MethodReturnT] | None
        :param cmeth: Class method
        :type cmeth: Callable[..., _ClassMethodReturnT] | None
        """
        self.__instance_method: Callable[..., _MethodReturnT] | None = imeth
        self.__class_method: Callable[..., _ClassMethodReturnT] | None = cmeth
        self.__owner: type | None = None
        self.__name: str = ""

    def __set_name__(self, owner: type | None, name: str) -> None:
        """Set __name__ and __objclass__ property."""
        self.__owner = owner
        self.__name = name

    @typing.overload
    def __get__(self, instance: None, owner: typing.Any) -> Callable[..., _ClassMethodReturnT]:
        """Class method."""

    @typing.overload
    def __get__(self, instance: typing.Any, owner: typing.Any) -> Callable[..., _MethodReturnT]:
        """Normal method."""

    def __get__(
        self,
        instance: typing.Any | None,
        owner: typing.Any,
    ) -> Callable[..., _MethodReturnT | _ClassMethodReturnT]:
        """Get descriptor.

        :return: class method or instance method depends on call behavior
        :rtype: Callable
        :raises AttributeError: Not implemented getter for class method and called class context.
        """
        if instance is None or self.__instance_method is None:
            if self.__class_method is None:
                raise AttributeError()

            @functools.wraps(self.__class_method)
            def class_method(*args: typing.Any, **kwargs: typing.Any) -> _ClassMethodReturnT:
                """Bound class method.

                :return: bound class method result
                :rtype: typing.Any
                """
                return self.__class_method(owner, *args, **kwargs)  # type: ignore[misc]

            return class_method

        @functools.wraps(self.__instance_method)
        def instance_method(*args: typing.Any, **kwargs: typing.Any) -> _MethodReturnT:
            """Bound instance method.

            :return: bound instance method result
            :rtype: typing.Any
            """
            return self.__instance_method(instance, *args, **kwargs)  # type: ignore[misc]

        return instance_method

    @property
    def __objclass__(self) -> type | None:  # pragma: no cover
        """Read-only owner.

        :return: property owner class
        :rtype: type | None
        """
        return self.__owner

    @property
    def __name__(self) -> str:  # pragma: no cover
        """Read-only name.

        :return: attribute name (may be overridden)
        :rtype: str
        """
        return self.__name

    def instance_method(
        self,
        imeth: Callable[..., _MethodReturnT] | None,
    ) -> SeparateClassMethod[_MethodReturnT, _ClassMethodReturnT]:
        """Descriptor to change instance method.

        :param imeth: New instance method.
        :type imeth: Callable[..., _MethodReturnT] | None
        :return: SeparateClassMethod
        :rtype: SeparateClassMethod[_MethodReturnT, _ClassMethodReturnT]
        """
        self.__instance_method = imeth
        return self

    def class_method(
        self,
        cmeth: Callable[..., _ClassMethodReturnT] | None,
    ) -> SeparateClassMethod[_MethodReturnT, _ClassMethodReturnT]:
        """Descriptor to change class method.

        :param cmeth: New class method.
        :type cmeth: Callable[..., _ClassMethodReturnT] | None
        :return: SeparateClassMethod
        :rtype: SeparateClassMethod[_MethodReturnT, _ClassMethodReturnT]
        """
        self.__class_method = cmeth
        return self

    @property
    def imeth(self) -> Callable[..., _MethodReturnT] | None:
        """Instance method instance.

        :rtype: Callable[..., _MethodReturnT] | None
        """
        return self.__instance_method

    @property
    def cmeth(self) -> Callable[..., _ClassMethodReturnT] | None:
        """Class method instance.

        :rtype: Callable[..., _ClassMethodReturnT] | None
        """
        return self.__class_method


if __name__ == "__main__":  # pragma: no cover
    # Standard Library
    import doctest

    doctest.testmod(verbose=True)
