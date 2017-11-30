import unittest

import advanced_descriptors


class TestAdvancedProperty(unittest.TestCase):
    def test_01_normal_property(self):
        class Target(object):
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
            getattr(Target, 'val')

    def test_02_full(self):
        class Target(object):
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
        class Target(object):
            getcls = advanced_descriptors.AdvancedProperty()

            @getcls.cgetter
            def getcls(cls):
                return cls

        self.assertIs(Target, Target.getcls)
        self.assertIs(Target, Target().getcls)

    def test_04_no_methods(self):
        class Target(object):
            prop = advanced_descriptors.AdvancedProperty()

        with self.assertRaises(AttributeError):
            getattr(Target, 'prop')

        with self.assertRaises(AttributeError):
            getattr(Target(), 'prop')

        with self.assertRaises(AttributeError):
            Target().prop = 1

        with self.assertRaises(AttributeError):
            del Target().prop

    def test_05_methods_access(self):
        def getter(inst):
            return inst._value

        def setter(inst, val):
            inst._value = val

        def deleter(inst):
            inst._value = 0

        def cgetter(cls):
            return cls._value

        class Target(object):
            _value = 777

            def __init__(self):
                self._value = 42

            val = advanced_descriptors.AdvancedProperty(
                fget=getter,
                fset=setter,
                fdel=deleter,
                fcget=cgetter
            )

        instance = Target()
        self.assertEqual(instance.val, 42)
        self.assertEqual(Target.val, 777)
        instance.val = 21
        self.assertEqual(instance.val, 21)
        del instance.val
        self.assertEqual(instance.val, 0)
        self.assertEqual(Target.val, 777)

        prop = Target.__dict__['val']
        self.assertIs(prop.fget, getter)
        self.assertIs(prop.fset, setter)
        self.assertIs(prop.fdel, deleter)
        self.assertIs(prop.fcget, cgetter)
