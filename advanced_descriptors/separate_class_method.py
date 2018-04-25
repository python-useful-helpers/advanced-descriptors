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

import six

try:  # pragma: no cover
    import typing  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    # noinspection PyRedeclaration
    typing = None

__all__ = (
    'SeparateClassMethod',
)


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
            imeth=None,  # type: typing.Optional[typing.Callable[..., typing.Any]]
            cmeth=None,  # type: typing.Optional[typing.Callable[..., typing.Any]]
    ):  # type: (...) -> None
        """Separate class method and instance methods.

        :param imeth: Instance method
        :type imeth: typing.Optional[typing.Callable[..., typing.Any]]
        :param cmeth: Class method
        :type cmeth: typing.Optional[typing.Callable[..., typing.Any]]
        """
        self.__instance_method = imeth
        self.__class_method = cmeth

    def __get__(
        self,
        instance,  # type: typing.Optional[object]
        owner  # type: typing.Type[object]
    ):  # type: (...) -> typing.Callable[..., typing.Any]
        """Get descriptor.

        :rtype: typing.Callable[..., typing.Any]
        :raises: AttributeError
        """
        if instance is None or self.__instance_method is None:
            if self.__class_method is None:
                raise AttributeError()

            @six.wraps(self.__class_method)
            def class_method(*args, **kwargs):
                """Bound class method."""
                return self.__class_method(owner, *args, **kwargs)

            return class_method

        @six.wraps(self.__instance_method)
        def instance_method(*args, **kwargs):
            """Bound instance method."""
            return self.__instance_method(instance, *args, **kwargs)

        return instance_method

    def instance_method(
            self,
            imeth  # type: typing.Optional[typing.Callable[..., typing.Any]]
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
            cmeth  # type: typing.Optional[typing.Callable[..., typing.Any]]
    ):  # type: (...) -> SeparateClassMethod
        """Descriptor to change class method.

        :type cmeth: New class method.
        :type cmeth: typing.Optional[typing.Callable[..., typing.Any]]
        :rtype: SeparateClassMethod
        """
        self.__class_method = cmeth
        return self

    @property
    def imeth(self):  # type: () -> typing.Optional[typing.Callable[..., typing.Any]]
        """Instance method instance.

        :rtype: typing.Optional[typing.Callable[..., typing.Any]]
        """
        return self.__instance_method

    @property
    def cmeth(self):  # type: () -> typing.Optional[typing.Callable[..., typing.Any]]
        """Class method instance.

        :rtype: typing.Optional[typing.Callable[..., typing.Any]]
        """
        return self.__class_method


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod(verbose=True)
