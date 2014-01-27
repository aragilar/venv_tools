# -*- coding: utf-8 -*-
"""
venv_tools
~~~~~~~~~~

A bunch of tools for using venvs (and virtualenvs) from python.

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
import os
import os.path
import sys
import tempfile
import shutil
import warnings

import venv_tools.utils as utils

BIN_DIR = "Scripts" if sys.platform == 'win32' else "bin"
__version__ = "0.1"

class Venv(object):
    """

    """
    def __init__(self, env_dir, venv_builder=None, **kwargs):
        self.env_dir = env_dir
        self._venv_builder = venv_builder
        self._kwargs = kwargs

    def __enter__(self):
        self._old_venv = os.environ.get("VIRTUAL_ENV", None)
        if self._old_venv is not None:
            warn_str = "Inside virtualenv {virtualenv}.".format(virtualenv=self._old_venv)
            warnings.warn(warn_str)
        self._old_path = os.environ["PATH"]
        self._python_home = os.environ.get("PYTHONHOME", None)
        if self._venv_builder:
            venv = self._venv_builder(**self._kwargs)
            venv.create(self.env_dir)
        utils.pathprepend(os.path.join(self.env_dir, BIN_DIR), "PATH")
        if self._python_home is not None:
            os.environ.pop("PYTHONHOME")
        os.environ["VIRTUAL_ENV"] = self.env_dir
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ["PATH"] = self._old_path
        if self._python_home is not None:
            os.environ["PYTHONHOME"] = self._python_home
        os.environ.pop("VIRTUAL_ENV")
        if self._old_venv is not None:
            os.environ["VIRTUAL_ENV"] = self._old_venv

class TemporaryVenv(object):
    """
    """
    def __init__(
            self,
            venv_builder=None,
            use_virtualenv=False,
            path_to_python_exe=None,
            **kwargs
            ):
        self._kwargs = kwargs
        self._venv_builder = (venv_builder or
            utils.get_default_venv_builder(use_virtualenv, path_to_python_exe))
        self._path_to_python_exe = path_to_python_exe
        self._kwargs["clear"] = True # needed for venv which wants to create dir

    def __enter__(self):
        self.env_dir = tempfile.mkdtemp()
        if self._path_to_python_exe:
            self._kwargs["path_to_python_exe"] = self._path_to_python_exe
        venv = self._venv_builder(**self._kwargs)
        venv.create(self.env_dir)
        self._opened_venv = Venv(self.env_dir)
        self._opened_venv.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._opened_venv.__exit__(exc_type, exc_value, traceback)
        shutil.rmtree(self.env_dir)

__all__ = [Venv, TemporaryVenv]
