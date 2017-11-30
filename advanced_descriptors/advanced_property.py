#!/usr/bin/env python

#    Copyright 2016 - 2017 Alexey Stepanov aka penguinolog
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

try:  # pragma: no cover
    import typing
    GetterType = typing.Optional[
        typing.Callable[[typing.Any, ], typing.Any]
    ]
    SetterType = typing.Optional[
        typing.Callable[[typing.Any, typing.Any], None]
    ]
    DeleterType = typing.Optional[
        typing.Callable[[typing.Any, ], None]
    ]
except ImportError:  # pragma: no cover
    typing = None
    GetterType = None
    SetterType = None
    DeleterType = None

__all__ = (
    'AdvancedProperty',
)


class AdvancedProperty(object):
    """Property with class-wide getter.

    This property allows implementation of read-only getter for classes
    in additional to normal set of getter/setter/deleter on instance.
    Implements almost full @property interface,
    except __doc__ due to class-wide nature.

    .. note:

        If class-wide setter/deleter required:
        use normal property in metaclass.

    Usage examples:

    >>> class LikeNormalProperty(object):
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

    >>> class ExtendedProperty(object):
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

    >>> class ClassProperty(object):
    ...     def _getter(cls):
    ...         return cls
    ...     prop = AdvancedProperty(fcget=_getter)  # special case


    >>> ClassProperty.prop is ClassProperty
    True

    >>> ClassProperty().prop is ClassProperty  # class wide property is used
    True
    """

    __slots__ = (
        '__fget',
        '__fset',
        '__fdel',
        '__fcget',
    )

    def __init__(
            self,
            fget=None,  # type: GetterType
            fset=None,  # type: SetterType
            fdel=None,  # type: DeleterType
            fcget=None,  # type: GetterType
    ):
        """Advanced property main entry point.

        :param fget: normal getter.
        :type fget:
            typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        :param fset: normal setter.
        :type fset:
            typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]
        :param fdel: normal deleter.
        :type fdel:
            typing.Optional[typing.Callable[[typing.Any, ], None]]
        :param fcget: class getter. Used as normal, if normal is None.
        :type fcget:
            typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]

        .. note: doc argument is not supported due to class wide getter usage.
        """
        self.__fget = fget
        self.__fset = fset
        self.__fdel = fdel

        self.__fcget = fcget

    def __get__(self, instance, owner):  # type: (...) -> typing.Any
        """Get descriptor.

        :param instance:
            Owner class instance. Filled only if instance created, else None.
        :type instance: typing.Optional[owner]
        :param owner: Owner class for property.
        :return: getter call result if getter presents
        :rtype: typing.Any
        :raises AttributeError: Getter is not available
        """
        if instance is None or self.__fget is None:
            if self.__fcget is None:
                raise AttributeError()
            return self.__fcget(owner)
        return self.__fget(instance)

    def __set__(self, instance, value):  # type: (...) -> None
        """Set descriptor.

        :param instance:
            Owner class instance. Filled only if instance created, else None.
        :type instance: typing.Optional
        :param value: Value for setter
        :raises AttributeError: Setter is not available
        """
        if self.__fset is None:
            raise AttributeError()
        return self.__fset(instance, value)

    def __delete__(self, instance):  # type: (...) -> None
        """Delete descriptor.

        :param instance:
            Owner class instance. Filled only if instance created, else None.
        :type instance: typing.Optional
        :raises AttributeError: Deleter is not available
        """
        if self.__fdel is None:
            raise AttributeError()
        return self.__fdel(instance)

    @property
    def fget(self):  # type: (AdvancedProperty) -> GetterType
        """Getter instance.

        :rtype: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        """
        return self.__fget

    @property
    def fset(self):  # type: (AdvancedProperty) -> SetterType
        """Setter instance.

        :rtype:
            typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]
        """
        return self.__fset

    @property
    def fdel(self):  # type: (AdvancedProperty) -> DeleterType
        """Deleter instance.

        :rtype: typing.Optional[typing.Callable[[typing.Any, ], None]]
        """
        return self.__fdel

    @property
    def fcget(self):  # type: (AdvancedProperty) -> GetterType
        """Class wide getter instance.

        :rtype: typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        """
        return self.__fcget

    def getter(
            self,
            fget  # type: GetterType
    ):  # type: (...) -> None
        """Descriptor to change the getter on a property.

        :param fget: new normal getter.
        :type fget:
            typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        :rtype: GetterType
        """
        self.__fget = fget
        return self

    def setter(
            self,
            fset  # type: SetterType
    ):  # type: (...) -> AdvancedProperty
        """Descriptor to change the setter on a property.

        :param fset: new setter.
        :type fset:
            typing.Optional[typing.Callable[[typing.Any, typing.Any], None]]
        :rtype: GetterType
        """
        self.__fset = fset
        return self

    def deleter(
            self,
            fdel  # type: DeleterType
    ):  # type: (...) -> AdvancedProperty
        """Descriptor to change the deleter on a property.

        :param fdel: New deleter.
        :type fdel: typing.Optional[typing.Callable[[typing.Any, ], None]]
        :rtype: GetterType
        """
        self.__fdel = fdel
        return self

    def cgetter(
            self,
            fcget  # type: GetterType
    ):  # type: (...) -> AdvancedProperty
        """Descriptor to change the class wide getter on a property.

        :param fcget: new class-wide getter.
        :type fcget:
            typing.Optional[typing.Callable[[typing.Any, ], typing.Any]]
        :rtype: GetterType
        """
        self.__fcget = fcget
        return self


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod(verbose=True)
