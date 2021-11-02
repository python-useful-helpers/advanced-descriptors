# pylint: skip-file

"""Tests for SeparateClassMethod."""

# Standard Library
import unittest

# Package Implementation
import advanced_descriptors


class TestSeparateClassMethod(unittest.TestCase):
    """Main tests for SeparateClassMethod."""

    def test_01_instance_method(self):
        """Test instance method support with decorating in-place."""

        class Target(object):
            def __init__(tself):
                tself.value = 42

            @advanced_descriptors.SeparateClassMethod
            def getval(tself):
                return tself.value

        instance = Target()
        self.assertEqual(instance.getval(), 42)
        with self.assertRaises(AttributeError):
            Target.getval()

    def test_02_alt_instance_method(self):
        """Test instance method support with late bind."""

        class Target(object):
            def __init__(tself):
                tself.value = 42

            getval = advanced_descriptors.SeparateClassMethod()

            @getval.instance_method
            def getval(tself):
                return tself.value

        instance = Target()
        self.assertEqual(instance.getval(), 42)
        with self.assertRaises(AttributeError):
            Target.getval()

    def test_03_class_method(self):
        """Test class method support."""

        class Target(object):
            getcls = advanced_descriptors.SeparateClassMethod()

            @getcls.class_method
            def getcls(cls):
                return cls

        self.assertIs(Target, Target.getcls())
        self.assertIs(Target, Target().getcls())

    def test_04_both(self):
        """Test coexistency of class method and instance method."""

        class Target(object):
            value = 1

            def __init__(tself):
                tself.value = 2

            @advanced_descriptors.SeparateClassMethod
            def getval(tself):
                return tself.value

            @getval.class_method
            def getval(cls):
                return cls.value

        instance = Target()
        self.assertEqual(instance.getval(), 2)
        self.assertEqual(Target.getval(), 1)

    def test_05_functions_access(self):
        """Test possibility to get original functions from decorator object."""

        def imeth(instance):
            return instance.value

        def cmeth(owner):
            return owner.value

        class Target(object):
            value = 1

            def __init__(tself):
                tself.value = 2

            getval = advanced_descriptors.SeparateClassMethod(imeth, cmeth)

        instance = Target()
        self.assertEqual(instance.getval(), 2)
        self.assertEqual(Target.getval(), 1)
        descr = Target.__dict__["getval"]
        self.assertIs(descr.imeth, imeth)
        self.assertIs(descr.cmeth, cmeth)
