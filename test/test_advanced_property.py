# pylint: skip-file

"""Tests for AdvancedProperty."""

# Standard Library
import unittest

# Package Implementation
import advanced_descriptors


class TestAdvancedProperty(unittest.TestCase):
    """Main tests for AdvancedProperty."""

    def test_01_normal_property(self):
        """Test work like normal property."""

        class Target:
            def __init__(tself):
                tself._value = 42

            @advanced_descriptors.AdvancedProperty
            def val(tself):
                return tself._value

            @val.setter
            def val(tself, value):
                tself._value = value

            @val.deleter
            def val(tself):
                tself._value = 0

        instance = Target()
        self.assertEqual(instance.val, 42)
        instance.val = 21
        self.assertEqual(instance.val, 21)
        del instance.val
        self.assertEqual(instance.val, 0)
        with self.assertRaises(AttributeError):
            getattr(Target, "val")  # noqa: B009

    def test_02_full(self):
        """Test all getters + setter + deleter implemented."""

        class Target:
            _value = 777

            def __init__(tself):
                tself._value = 42

            val = advanced_descriptors.AdvancedProperty()

            @val.getter
            def val(tself):
                return tself._value

            @val.setter
            def val(tself, value):
                tself._value = value

            @val.deleter
            def val(tself):
                tself._value = 0

            @val.cgetter
            def val(cls):
                return cls._value

        instance = Target()
        self.assertEqual(instance.val, 42)
        self.assertEqual(Target.val, 777)
        instance.val = 21
        self.assertEqual(instance.val, 21)
        del instance.val
        self.assertEqual(instance.val, 0)
        self.assertEqual(Target.val, 777)

    def test_03_class_wide_only(self):
        """Test class wide getter is implemented, while instance not."""

        class Target:
            getcls = advanced_descriptors.AdvancedProperty()

            @getcls.cgetter
            def getcls(cls):
                return cls

        self.assertIs(Target, Target.getcls)
        self.assertIs(Target, Target().getcls)

    def test_04_no_methods(self):
        """Test no any methods implemented."""

        class Target:
            prop = advanced_descriptors.AdvancedProperty()

        with self.assertRaises(AttributeError):
            getattr(Target, "prop")  # noqa: B009

        with self.assertRaises(AttributeError):
            getattr(Target(), "prop")  # noqa: B009

        with self.assertRaises(AttributeError):
            Target().prop = 1

        with self.assertRaises(AttributeError):
            del Target().prop

    def test_05_methods_access(self):
        """Test access to original methods."""

        def getter(inst):
            return inst._value

        def setter(inst, val):
            inst._value = val

        def deleter(inst):
            inst._value = 0

        def cgetter(cls):
            return cls._value

        class Target:
            _value = 777

            def __init__(self):
                self._value = 42

            val = advanced_descriptors.AdvancedProperty(fget=getter, fset=setter, fdel=deleter, fcget=cgetter)

        instance = Target()
        self.assertEqual(instance.val, 42)
        self.assertEqual(Target.val, 777)
        instance.val = 21
        self.assertEqual(instance.val, 21)
        del instance.val
        self.assertEqual(instance.val, 0)
        self.assertEqual(Target.val, 777)

        prop = Target.__dict__["val"]
        self.assertIs(prop.fget, getter)
        self.assertIs(prop.fset, setter)
        self.assertIs(prop.fdel, deleter)
        self.assertIs(prop.fcget, cgetter)
