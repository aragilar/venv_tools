# -*- coding: utf-8 -*-
"""
venv_tools._utils
~~~~~~~~~~

Useful internal functions

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
from logging import getLogger
import os
import os.path as pth
import subprocess
import sys

from ._venv_builders import VirtualenvBuilder

BIN_DIR = "Scripts" if sys.platform == 'win32' else "bin"
PYTHON_FILENAME = "python.exe" if sys.platform == 'win32' else "python"
PYVENV_FILENAME = "pyvenv.cfg"
ACTIVATE_FILENAMES = (
    "activate",
    "activate.csh",
    "activate.fish",
    "activate_this.py",
    "activate.bat",
    "activate.ps1",
)

log = getLogger(__name__)


def pathremove(dirname, path):
    """
    Remove `dirname` from path `path`.
    e.g. to remove `/bin` from `$PATH`
    >>> pathremove('/bin', 'PATH')

    Based on shell function by Peter Ward
    """
    os.environ[path] = os.pathsep.join(
        p for p in os.environ[path].split(os.pathsep) if p != dirname
    )


def pathprepend(dirname, path):
    """
    Prepend `dirname` ro path `path`.
    e.g. to prepend `/bin` to `$PATH`
    >>> pathprepend('/bin', 'PATH')

    Based on shell function by Peter Ward
    """
    pathremove(dirname, path)
    os.environ[path] = dirname + os.pathsep + os.environ[path]


def pathappend(dirname, path):
    """
    Append `dirname` to path `path`.
    e.g. to append `/bin` to `$PATH`
    >>> pathappend('/bin', 'PATH')

    Based on shell function by Peter Ward
    """
    pathremove(dirname, path)
    os.environ[path] = os.environ[path] + os.pathsep + dirname


def get_default_venv_builder(use_virtualenv, path_to_python_exe):
    """
    Given `use_virtualenv` and `path_to_python_exe`, returns a venv builder
    that will satisfy the requirements.
    """
    if path_to_python_exe:
        return VirtualenvBuilder
    if use_virtualenv:
        return VirtualenvBuilder
    try:
        import venv  # pylint: disable=import-outside-toplevel
        if sys.version_info[0:2] == (3, 3):
            return VirtualenvBuilder
        return venv.EnvBuilder
    except ImportError:
        return VirtualenvBuilder


def is_virtualenv(path):
    """
    Checks whether `path` is a virtualenv.

    This function is somewhat redundant now that virtualenv uses venv
    """
    if pth.exists(pth.join(path, BIN_DIR, "python")):
        # we might have a virtualenv (/usr would pass the above test)
        activate_exists = any(
            pth.exists(pth.join(path, BIN_DIR, f))
            for f in ACTIVATE_FILENAMES
        )
        if activate_exists:
            return True
    return False


def is_pep_405_venv(path):
    """
    Checks whether `path` is a PEP 405 venv.
    """
    if pth.exists(pth.join(path, PYVENV_FILENAME)):
        # we have a PEP 405 venv (probably)
        with open(pth.join(path, PYVENV_FILENAME)) as f:
            for line in f:
                key = line.split("=")[0].strip()
                if key == "home":  # home key required by PEP
                    return True
    return False


def is_venv(path):
    """
    Checks whether `path` is a virtualenv/venv.
    """
    return is_pep_405_venv(path) or is_virtualenv(path)


def abspath_python_exe(python_exe):
    """
    Discover absolute path to python executable given by `python_exe`.
    """
    if python_exe is None:
        return sys.executable
    full_path = pth.abspath(python_exe)
    if is_executable(full_path):
        return full_path
    try:
        return abspath_path_executable(python_exe)
    except FileNotFoundError:
        return RuntimeError("Cannot find " + python_exe)


def is_executable(path):
    """
    Check whether `path` is an executable file.
    """
    return pth.isfile(path) and os.access(path, os.X_OK)


def abspath_path_executable(executable):
    """
    Discover absolute path of executable `executable` on system path.
    """
    for path in os.environ["PATH"].split(os.pathsep):
        full_path = pth.join(path, executable)
        if is_executable(full_path):
            return full_path
    raise FileNotFoundError(executable + " is not on current path")


def run_python_with_args(
    *, python_exe, args=None, module=None, code=None, script=None,
    input=None,  # pylint: disable=redefined-builtin
    stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=None
):
    """
    Wrapper around subprocess.run for calling python interpreter.
    """
    if sum(1 for kw in (module, code, script) if kw is not None) != 1:
        raise RuntimeError(
            "One of module, code or script should be provided."
        )

    cmd_list = [python_exe]
    if module is not None:
        cmd_list.extend(['-m', module])
    if code is not None:
        cmd_list.extend(['-c', code])
    if script is not None:
        cmd_list.append(script)

    if args is not None:
        cmd_list.extend(args)

    log.debug("Running command %s", cmd_list)

    return subprocess.run(
        cmd_list, input=input, stdin=stdin, stdout=stdout, stderr=stderr,
        timeout=timeout, shell=False, universal_newlines=True, check=True
    )
