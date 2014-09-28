import os
import sys
import shutil
import tempfile
import subprocess

if sys.version_info[:2] < (2,7):
    import unittest2 as unittest
else:
    import unittest

from venv_tools import Venv, TemporaryVenv
from venv_tools._utils import is_venv

VENV_PYTHON_TEST_CODE = "from __future__ import print_function; import sys; print(sys.prefix)"
DEVNULL = open(os.devnull, "w")

def pyvenv_exists():
    try:
        subprocess.call(["pyvenv"], stdout=DEVNULL, stderr=DEVNULL)
    except OSError:
        return False
    else:
        return True

class TestNonExistance(unittest.TestCase):
    def setUp(self):
        self.empty_folder = tempfile.mkdtemp()

    def test_is_venv_fail(self):
        self.assertFalse(is_venv(self.empty_folder))

    def test_Venv_fail(self):
        self.assertRaises(RuntimeError,Venv(self.empty_folder).__enter__)

    def tearDown(self):
        shutil.rmtree(self.empty_folder)

class TestVirtualenvActivation(unittest.TestCase):
    def setUp(self):
        self.virtualenv = tempfile.mkdtemp()
        subprocess.call(
                ["virtualenv", self.virtualenv],
                stdout=DEVNULL, stderr=DEVNULL
        )

    def test_no_pythonhome(self):
        with Venv(self.virtualenv):
            with self.assertRaises(KeyError):
                os.environ["PYTHONHOME"]

    def test_correct_virtualenv(self):
        with Venv(self.virtualenv):
            self.assertEqual(os.environ["VIRTUAL_ENV"], self.virtualenv)

    def test_path_added(self):
        with Venv(self.virtualenv):
            self.assertTrue(os.environ["PATH"].find(self.virtualenv) > -1)

    def test_python_actually_found(self):
        with Venv(self.virtualenv):
            internal_prefix = subprocess.check_output([
                "python", "-c", VENV_PYTHON_TEST_CODE
            ]).strip()
            self.assertEqual(internal_prefix.decode("utf8"), self.virtualenv)

    def tearDown(self):
        shutil.rmtree(self.virtualenv)

@unittest.skipIf(not pyvenv_exists(), "Skipping pyvenv")
class TestVenvActivation(unittest.TestCase):
    def setUp(self):
        self.venv = tempfile.mkdtemp()
        subprocess.call(
                ["pyvenv", self.venv],
                stdout=DEVNULL, stderr=DEVNULL
        )

    def test_no_pythonhome(self):
        with Venv(self.venv):
            with self.assertRaises(KeyError):
                os.environ["PYTHONHOME"]

    def test_correct_venv(self):
        with Venv(self.venv):
            self.assertEqual(os.environ["VIRTUAL_ENV"], self.venv)

    def test_path_added(self):
        with Venv(self.venv):
            self.assertTrue(os.environ["PATH"].find(self.venv) > -1)

    def test_python_actually_found(self):
        with Venv(self.venv):
            internal_prefix = subprocess.check_output([
                "python", "-c", VENV_PYTHON_TEST_CODE
            ]).strip()
            self.assertEqual(internal_prefix.decode("utf8"), self.venv)

    def tearDown(self):
        shutil.rmtree(self.venv)

class TestTemporaryVenv(unittest.TestCase):
    def test_default_via_is_venv(self):
        with TemporaryVenv() as envdir:
            self.assertTrue(is_venv(envdir))
