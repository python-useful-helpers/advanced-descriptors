# pylint: skip-file

"""Tests for LogOnAccess descriptor."""

# Standard Library
import io
import logging
import unittest

# Package Implementation
import advanced_descriptors


class TestLogOnAccess(unittest.TestCase):
    """Main tests for LogOnAccess descriptor."""

    def setUp(self):
        """Initialize specific logger for tests."""
        self.stream = io.StringIO()
        logging.getLogger().handlers.clear()
        logging.basicConfig(level=logging.DEBUG, stream=self.stream)

    def tearDown(self):
        """Close test logger."""
        logging.getLogger().handlers.clear()
        self.stream.close()

    def test_01_positive(self):
        """Test positive scenario."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                return self.val

            @ok.setter
            def ok(self, val):
                self.val = val

            @ok.deleter
            def ok(self):
                self.val = ""

        target = Target()
        self.assertEqual(target.ok, "ok")
        self.assertEqual(self.stream.getvalue(), "DEBUG:advanced_descriptors.log_on_access:Target(val=ok).ok -> 'ok'\n")

        self.stream.seek(0)
        self.stream.truncate()

        target.ok = "OK"
        self.assertEqual(self.stream.getvalue(), "DEBUG:advanced_descriptors.log_on_access:Target(val=ok).ok = 'OK'\n")

        self.assertEqual(target.ok, "OK")

        self.stream.seek(0)
        self.stream.truncate()

        del target.ok
        self.assertEqual(self.stream.getvalue(), "DEBUG:advanced_descriptors.log_on_access:del Target(val=OK).ok\n")

    def test_02_positive_properties(self):
        """Test positive scenario with non standard settings."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                return self.val

            ok.log_level = logging.INFO
            ok.log_object_repr = False
            ok.override_name = "override"

        target = Target()

        self.assertEqual(target.ok, "ok")
        self.assertEqual(
            self.stream.getvalue(),
            f"INFO:advanced_descriptors.log_on_access:<Target() at 0x{id(target):X}>.override -> 'ok'\n",
        )

    def test_03_positive_no_log(self):
        """Test log_success flag."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                return self.val

            ok.log_success = False

        target = Target()

        self.assertEqual(target.ok, "ok")
        self.assertEqual(self.stream.getvalue(), "")

    def test_04_negative(self):
        """Test basic negative scenario."""

        class Target:
            def __repr__(self):
                return f"{self.__class__.__name__}()"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                raise AttributeError()

            @ok.setter
            def ok(self, val):
                raise ValueError(val)

            @ok.deleter
            def ok(self):
                raise RuntimeError()

        target = Target()

        with self.assertRaises(AttributeError):
            self.assertIsNone(target.ok)

        self.assertEqual(
            self.stream.getvalue().splitlines()[0], "DEBUG:advanced_descriptors.log_on_access:Failed: Target().ok"
        )
        self.assertEqual(self.stream.getvalue().splitlines()[1], "Traceback (most recent call last):")

        self.stream.seek(0)
        self.stream.truncate()

        with self.assertRaises(ValueError):
            target.ok = "ok"

        self.assertEqual(
            self.stream.getvalue().splitlines()[0],
            "DEBUG:advanced_descriptors.log_on_access:Failed: Target().ok = 'ok'",
        )

        self.stream.seek(0)
        self.stream.truncate()

        with self.assertRaises(RuntimeError):
            del target.ok

        self.assertEqual(
            self.stream.getvalue().splitlines()[0], "DEBUG:advanced_descriptors.log_on_access:Target(): Failed: del ok"
        )

    def test_05_negative_properties(self):
        """Test negative scenario with non standard settings."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                raise AttributeError()

            ok.exc_level = logging.ERROR
            ok.log_traceback = False
            ok.log_object_repr = False
            ok.override_name = "override"

        target = Target()

        with self.assertRaises(AttributeError):
            self.assertIsNone(target.ok)

        self.assertEqual(
            self.stream.getvalue().splitlines()[0],
            f"ERROR:advanced_descriptors.log_on_access:Failed: <Target() at 0x{id(target):X}>.override",
        )
        self.assertEqual(len(self.stream.getvalue().splitlines()), 1)

    def test_06_negative_no_log(self):
        """Test log_failure flag."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                raise AttributeError()

            ok.log_failure = False

        target = Target()

        with self.assertRaises(AttributeError):
            self.assertIsNone(target.ok)

        self.assertEqual(self.stream.getvalue(), "")

    def test_07_property_mimic(self):
        """Test property API not broken."""

        class Target:
            def __repr__(self):
                return f"{self.__class__.__name__}()"

            empty = advanced_descriptors.LogOnAccess(doc="empty_property")

        target = Target()

        with self.assertRaises(AttributeError):
            self.assertIsNone(target.empty)

        with self.assertRaises(AttributeError):
            target.empty = None

        with self.assertRaises(AttributeError):
            del target.empty

        self.assertEqual(self.stream.getvalue(), "")

    def test_08_logger(self):
        """Test with logger enforced."""

        class Target:
            on_init_set = advanced_descriptors.LogOnAccess(
                logger=logging.getLogger("on_init_set"), fget=lambda self: "on_init_set"
            )
            on_init_name = advanced_descriptors.LogOnAccess(logger="on_init_name", fget=lambda self: "on_init_name")

            @advanced_descriptors.LogOnAccess
            def prop_set(self):
                return "prop_set"

            prop_set.logger = logging.getLogger("prop_set")

            @advanced_descriptors.LogOnAccess
            def prop_name(self):
                return "prop_name"

            prop_name.logger = "prop_name"

            def __repr__(self):
                return f"{self.__class__.__name__}()"

        target = Target()

        getattr(target, "on_init_set")  # noqa: B009
        self.assertEqual(self.stream.getvalue(), "DEBUG:on_init_set:Target().on_init_set -> 'on_init_set'\n")

        self.stream.seek(0)
        self.stream.truncate()

        getattr(target, "on_init_name")  # noqa: B009
        self.assertEqual(self.stream.getvalue(), "DEBUG:on_init_name:Target().on_init_name -> 'on_init_name'\n")

        self.stream.seek(0)
        self.stream.truncate()

        getattr(target, "prop_set")  # noqa: B009
        self.assertEqual(self.stream.getvalue(), "DEBUG:prop_set:Target().prop_set -> 'prop_set'\n")

        self.stream.seek(0)
        self.stream.truncate()

        getattr(target, "prop_name")  # noqa: B009
        self.assertEqual(self.stream.getvalue(), "DEBUG:prop_name:Target().prop_name -> 'prop_name'\n")

    def test_09_logger_implemented(self):
        """Test with logger attribute available in target instance."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val
                self.logger = logging.getLogger(self.__class__.__name__)

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                return self.val

            @ok.setter
            def ok(self, val):
                self.val = val

            @ok.deleter
            def ok(self):
                self.val = ""

        target = Target()
        self.assertEqual(target.ok, "ok")
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:Target(val=ok).ok -> 'ok'\n")

        self.stream.seek(0)
        self.stream.truncate()

        target.ok = "OK"
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:Target(val=ok).ok = 'OK'\n")

        self.assertEqual(target.ok, "OK")

        self.stream.seek(0)
        self.stream.truncate()

        del target.ok
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:del Target(val=OK).ok\n")

    def test_10_log_implemented(self):
        """Test with log attribute available in target instance."""

        class Target:
            def __init__(self, val="ok"):
                self.val = val
                self.log = logging.getLogger(self.__class__.__name__)

            def __repr__(self):
                return f"{self.__class__.__name__}(val={self.val})"

            @advanced_descriptors.LogOnAccess
            def ok(self):
                return self.val

            @ok.setter
            def ok(self, val):
                self.val = val

            @ok.deleter
            def ok(self):
                self.val = ""

        target = Target()
        self.assertEqual(target.ok, "ok")
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:Target(val=ok).ok -> 'ok'\n")

        self.stream.seek(0)
        self.stream.truncate()

        target.ok = "OK"
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:Target(val=ok).ok = 'OK'\n")

        self.assertEqual(target.ok, "OK")

        self.stream.seek(0)
        self.stream.truncate()

        del target.ok
        self.assertEqual(self.stream.getvalue(), "DEBUG:Target:del Target(val=OK).ok\n")
