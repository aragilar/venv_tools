# -*- coding: utf-8 -*-
"""
venv_tools
~~~~~~~~~~

A bunch of tools for using venvs (and virtualenvs) from python.

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import os.path
import sys
import tempfile
import shutil
import warnings

from ._utils import pathprepend, get_default_venv_builder, is_venv, BIN_DIR

__version__ = "0.1"

class Venv(object):
    """
    Context manager around activating and deactivating a venv.

    `Venv` sets a number of environment variables which are equivalent to
    running `bin/activate`. It can create a venv if `venv_builder` is given.

    .. warning::
        Creating or activating a venv inside a venv can be "interesting", with
        the results varying between different python versions (and different
        venv tools). The safest method appears to be using virtualenv, however
        this should not be relied upon. A warning will be raised if it is
        detected that this is running inside a venv.

    :param str env_dir: The absolute path to the venv.
    :param venv_builder: An object which creates a venv. It must define a method
        `create` which takes one argument, `env_dir`, and creates a venv at that
        path. Any additional keywords passed to `Venv` will be passed to the
        object.

    :type venv_builder: `venv.EnvBuilder or similar`
    """
    def __init__(self, env_dir, venv_builder=None, **kwargs):

        self.env_dir = env_dir
        self._venv_builder = venv_builder
        self._kwargs = kwargs

    def __enter__(self):
        if not is_venv(self.env_dir):
            raise RuntimeError(
                    "{} is not a venv/virtualenv.".format(self.env_dir))
        self._old_venv = os.environ.get("VIRTUAL_ENV", None)
        if self._old_venv is not None:
            warn_str = "Inside virtualenv {virtualenv}.".format(virtualenv=self._old_venv)
            warnings.warn(warn_str)
        self._old_path = os.environ["PATH"]
        self._python_home = os.environ.get("PYTHONHOME", None)
        if self._venv_builder:
            venv = self._venv_builder(**self._kwargs)
            venv.create(self.env_dir)
        pathprepend(os.path.join(self.env_dir, BIN_DIR), "PATH")
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
    Context manager around creating a temporary venv.

    `TemporaryVenv` handles the creation and removal of a temporary venv. By
    default it will try to use the venv tools in the standard library, and fall
    back to using `virtualenv <http://www.virtualenv.org/>`_.

    .. note::
        The tool used to create the venv depends on the arguments given.
        `venv_builder` overrules `use_virtualenv` which overrules the defaults.
        If `path_to_python_exe` is given, then it is passed to the venv builder,
        which is chosen as above with the addition that the default will be a
        tool that supports using a specific python executable (most likely
        virtualenv).

    .. note::
        If you plan on using pip, you need the argument `with_pip`, as both
        `EnvBuilder` in the standard library, and the virtualenv builder
        included in `venv_tools` (to try to present a similar interface to
        `EnvBuilder`) default to not installing pip.

    .. warning::
        Creating or activating a venv inside a venv can be "interesting", with
        the results varying between different python versions (and different
        venv tools). The safest method appears to be using virtualenv, however
        this should not be relied upon. A warning will be raised if it is
        detected that this is running inside a venv.

    :param str path_to_python_exe: The absolute path to the python executable.
    :param bool use_virtualenv: Use virtualenv instead of the default to create
        the venv.
    :param venv_builder: An object which creates a venv. It must define a method
        `create` which takes one argument, `env_dir`, and creates a venv at that
        path. Any additional keywords passed to `Venv` will be passed to the
        object.

    :type venv_builder: `venv.EnvBuilder or similar`
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
            get_default_venv_builder(use_virtualenv, path_to_python_exe))
        self._path_to_python_exe = path_to_python_exe
        self._kwargs["clear"] = True # needed for venv which wants to create dir

    def __enter__(self):
        self.env_dir = tempfile.mkdtemp()
        if self._path_to_python_exe:
            self._kwargs["path_to_python_exe"] = self._path_to_python_exe
        venv = self._venv_builder(**self._kwargs)
        venv.create(self.env_dir)
        return self.env_dir

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.env_dir)

