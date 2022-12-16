#!/usr/bin/env python

#    Copyright 2016 - 2022 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at

#         http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Property with class-wide getter."""

from __future__ import annotations

# Standard Library
import typing

if typing.TYPE_CHECKING:
    # Standard Library
    from collections.abc import Callable

__all__ = ("AdvancedProperty",)

_OwnerClassT = typing.TypeVar("_OwnerClassT")
_ReturnT = typing.TypeVar("_ReturnT")
_ClassReturnT = typing.TypeVar("_ClassReturnT")


class AdvancedProperty(property, typing.Generic[_OwnerClassT, _ReturnT, _ClassReturnT]):
    """Property with class-wide getter.

    This property allows implementation of read-only getter for classes
    in additional to normal set of getter/setter/deleter on instance.
    Implements almost full @property interface,
    except __doc__ due to class-wide nature.

    .. versionadded:: 2.1.0 Inherit property

    .. note:: If class-wide setter/deleter required: use normal property in metaclass.

    Usage examples:

    >>> class LikeNormalProperty:
    ...     def __init__(self):
    ...         self.val = 42
    ...     @AdvancedProperty
    ...     def prop(self):
    ...         return self.val
    ...     @prop.setter
    ...     def prop(self, new_val):
    ...         self.val = new_val
    ...     @prop.deleter
    ...     def prop(self):
    ...         self.val = 0

    >>> test_instance = LikeNormalProperty()

    >>> test_instance.prop
    42

    >>> test_instance.prop=43
    >>> test_instance.prop
    43

    >>> del test_instance.prop
    >>> test_instance.prop
    0

    # But access from class is restricted instead of normal property return.
    >>> LikeNormalProperty.prop
    Traceback (most recent call last):
    ...
    AttributeError

    >>> class ExtendedProperty:
    ...     def __init__(self):
    ...         self.val = 21
    ...     @AdvancedProperty
    ...     def prop(self):
    ...         return self.val
    ...     @prop.setter
    ...     def prop(self, new_val):
    ...         self.val = new_val
    ...     @prop.deleter
    ...     def prop(self):
    ...         self.val = -1
    ...     @prop.cgetter
    ...     def prop(cls):
    ...         return 'self.val'

    >>> test_instance = ExtendedProperty()

    >>> test_instance.prop
    21

    >>> test_instance.prop=20
    >>> test_instance.prop
    20

    >>> del test_instance.prop
    >>> test_instance.prop
    -1

    # Class getter is set and differs from normal getter
    >>> ExtendedProperty.prop
    'self.val'

    >>> class ClassProperty:
    ...     def _getter(cls):
    ...         return cls
    ...     prop = AdvancedProperty(fcget=_getter)  # special case


    >>> ClassProperty.prop is ClassProperty
    True

    >>> ClassProperty().prop is ClassProperty  # class wide property is used
    True
    """

    def __init__(
        self,
        fget: Callable[[_OwnerClassT], _ReturnT] | None = None,
        fset: Callable[[_OwnerClassT, _ReturnT], None] | None = None,
        fdel: Callable[[_OwnerClassT], None] | None = None,
        fcget: Callable[[type[_OwnerClassT]], _ClassReturnT] | None = None,
    ) -> None:
        """Advanced property main entry point.

        :param fget: normal getter.
        :type fget: Callable[[typing.Any, ], typing.Any] | None
        :param fset: normal setter.
        :type fset: Callable[[typing.Any, typing.Any], None] | None
        :param fdel: normal deleter.
        :type fdel: Callable[[typing.Any, ], None] | None
        :param fcget: class getter. Used as normal, if normal is None.
        :type fcget: Callable[[typing.Any, ], typing.Any] | None

        .. note:: doc argument is not supported due to class wide getter usage.
        """
        super().__init__(fget=fget, fset=fset, fdel=fdel)

        self.__fcget: Callable[[type[_OwnerClassT]], _ClassReturnT] | None = fcget

    @typing.overload
    def __get__(self, instance: None, owner: type[_OwnerClassT]) -> _ClassReturnT:
        """Class method."""

    @typing.overload
    def __get__(self, instance: _OwnerClassT, owner: type[_OwnerClassT] | None = None) -> _ReturnT:
        """Normal method."""

    def __get__(
        self,
        instance: _OwnerClassT | None,
        owner: type[_OwnerClassT] | None = None,
    ) -> _ClassReturnT | _ReturnT:
        """Get descriptor.

        :param instance: Owner class instance. Filled only if instance created, else None.
        :type instance: owner | None
        :param owner: Owner class for property.
        :return: getter call result if getter presents
        :rtype: typing.Any
        :raises AttributeError: Getter is not available
        """
        if owner is not None and (instance is None or self.fget is None):
            if self.__fcget is None:
                raise AttributeError()
            return self.__fcget(owner)
        return super().__get__(instance, owner)  # type: ignore[no-any-return]

    @property
    def fcget(self) -> Callable[[type[_OwnerClassT]], _ClassReturnT] | None:
        """Class wide getter instance.

        :return: Class wide getter instance
        :rtype: Callable[[typing.Any, ], typing.Any] | None
        """
        return self.__fcget

    def cgetter(
        self,
        fcget: Callable[[type[_OwnerClassT]], _ClassReturnT] | None,
    ) -> AdvancedProperty[_OwnerClassT, _ReturnT, _ClassReturnT]:
        """Descriptor to change the class wide getter on a property.

        :param fcget: new class-wide getter.
        :type fcget: Callable[[typing.Any, ], typing.Any] | None
        :return: AdvancedProperty
        :rtype: AdvancedProperty
        """
        self.__fcget = fcget
        return self


if __name__ == "__main__":  # pragma: no cover
    # Standard Library
    import doctest

    doctest.testmod(verbose=True)
