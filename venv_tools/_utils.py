# -*- coding: utf-8 -*-
"""
venv_tools._utils
~~~~~~~~~~

Useful internal functions

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import sys
import os.path as pth

from ._venv_builders import VirtualenvBuilder

BIN_DIR = "Scripts" if sys.platform == 'win32' else "bin"
PYVENV_FILENAME = "pyvenv.cfg"
ACTIVATE_FILENAMES = [
    "activate",
    "activate.csh",
    "activate.fish",
    "activate_this.py",
    "activate.bat",
    "activate.ps1",
]

def pathremove(dir, path):
    """
    Remove `dir` from path `path`.
    e.g. to remove `/bin` from `$PATH`
    >>> pathremove('/bin', 'PATH')
    
    Based on http://hg.flowblok.id.au/dotfiles/src/85661d53e226dfe1e79b125942594a4275d8ed75/.shell/env_functions?at=flowblok
    """
    os.environ[path] = os.pathsep.join(
        p for p in os.environ[path].split(os.pathsep) if p != dir
    )

def pathprepend(dir, path):
    """
    Prepend `dir` ro path `path`.
    e.g. to prepend `/bin` to `$PATH`
    >>> pathprepend('/bin', 'PATH')
    
    Based on http://hg.flowblok.id.au/dotfiles/src/85661d53e226dfe1e79b125942594a4275d8ed75/.shell/env_functions?at=flowblok
    """
    pathremove(dir, path)
    os.environ[path] = dir + os.pathsep + os.environ[path]

def pathappend(dir, path):
    """
    Append `dir` to path `path`.
    e.g. to append `/bin` to `$PATH`
    >>> pathappend('/bin', 'PATH')
    
    Based on http://hg.flowblok.id.au/dotfiles/src/85661d53e226dfe1e79b125942594a4275d8ed75/.shell/env_functions?at=flowblok
    """
    pathremove(dir, path)
    os.environ[path] = os.environ[path] + os.pathsep + dir

def get_default_venv_builder(use_virtualenv, path_to_python_exe):
    """
    Given `use_virtualenv` and `path_to_python_exe`, returns a venv builder that
    will satisfy the requirements.
    """
    if path_to_python_exe:
        return VirtualenvBuilder
    elif use_virtualenv:
        return VirtualenvBuilder
    try:
        import venv
        if sys.version_info[0:2] == (3, 3):
            return VirtualenvBuilder
        return venv.EnvBuilder
    except ImportError as e:
        return VirtualenvBuilder

def is_virtualenv(path):
    """
    Checks whether `path` is a virtualenv.
    """
    if pth.exists(pth.join(path, BIN_DIR, "python")):
        # we might have a virtualenv (/usr would pass the above test)
        activate_exists = any(
                pth.exists(pth.join(path, BIN_DIR, f))
                    for f in ACTIVATE_FILENAMES
        )
        if activate_exists and not is_pep_405_venv(path):
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
                if key == "home": # home key required by PEP
                    return True
    return False

def is_venv(path):
    """
    Checks whether `path` is a virtualenv/venv.
    """
    return is_pep_405_venv(path) or is_virtualenv(path)
