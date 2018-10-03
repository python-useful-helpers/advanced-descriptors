#!/usr/bin/env python

#    Copyright 2016 - 2018 Alexey Stepanov aka penguinolog
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

"""Property with class-wide getter."""

import typing

__all__ = ("AdvancedProperty",)


class AdvancedProperty(property):
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
        fget: typing.Optional[typing.Callable[[typing.Any], typing.Any]] = None,
        fset: typing.Optional[typing.Callable[[typing.Any, typing.Any], None]] = None,
        fdel: typing.Optional[typing.Callable[[typing.Any], None]] = None,
        fcget: typing.Optional[typing.Callable[[typing.Any], typing.Any]] = None,
    ) -> None:
        """Advanced property main entry point.

        :param fget: normal getter.
        :type fget: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        :param fset: normal setter.
        :type fset: typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]
        :param fdel: normal deleter.
        :type fdel: typing.Optional[typing.Callable[[typing.Any, ], None]]
        :param fcget: class getter. Used as normal, if normal is None.
        :type fcget: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]

        .. note:: doc argument is not supported due to class wide getter usage.
        """
        super(AdvancedProperty, self).__init__(fget=fget, fset=fset, fdel=fdel)

        self.__fcget = fcget

    def __get__(self, instance: typing.Any, owner: typing.Any = None) -> typing.Any:
        """Get descriptor.

        :param instance: Owner class instance. Filled only if instance created, else None.
        :type instance: typing.Optional[owner]
        :param owner: Owner class for property.
        :return: getter call result if getter presents
        :rtype: typing.Any
        :raises AttributeError: Getter is not available
        """
        if owner is not None and (instance is None or self.fget is None):
            if self.__fcget is None:
                raise AttributeError()
            return self.__fcget(owner)
        return super(AdvancedProperty, self).__get__(instance, owner)

    @property
    def fcget(self) -> typing.Optional[typing.Callable[[typing.Any], typing.Any]]:
        """Class wide getter instance.

        :return: Class wide getter instance
        :rtype: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        """
        return self.__fcget

    def cgetter(self, fcget: typing.Optional[typing.Callable[[typing.Any], typing.Any]]) -> "AdvancedProperty":
        """Descriptor to change the class wide getter on a property.

        :param fcget: new class-wide getter.
        :type fcget: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        :return: AdvancedProperty
        :rtype: AdvancedProperty
        """
        self.__fcget = fcget
        return self


if __name__ == "__main__":  # pragma: no cover
    import doctest

    doctest.testmod(verbose=True)
