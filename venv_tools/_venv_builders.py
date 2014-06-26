# -*- coding: utf-8 -*-
"""
venv_tools._venv_builders
~~~~~~~~~~

EnvBuilder replacement classes for where EnvBuilder isn't available.

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import sys
import shlex
import subprocess
import tempfile

VIRTUALENV_COMMAND = "virtualenv {options} {env_dir}"

class VirtualenvBuilder(object):
    def __init__(self, system_site_packages=False, clear=False, with_pip=False, **kwargs):
        self.system_site_packages = system_site_packages
        self.clear = clear
        self.kwargs = kwargs
        self.with_pip = with_pip
    def create(self, env_dir):
        options = ""
        if self.system_site_packages:
            options += " --system-site-packages "
        if self.clear:
            options += " --clear "
        if sys.executable:
            options += " --python {python} ".format(python=sys.executable)
        if not self.with_pip:
            options += " --no-setuptools --no-pip "
        subprocess.check_output(shlex.split(VIRTUALENV_COMMAND.format(
            options=options,
            env_dir=env_dir
            )),
            stderr=subprocess.STDOUT
            )
