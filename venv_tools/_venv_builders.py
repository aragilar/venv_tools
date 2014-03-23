# -*- coding: utf-8 -*-
"""
venv_tools._venv_builders
~~~~~~~~~~

EnvBuilder replacement classes for where EnvBuilder isn't available.

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, print_function

import os
import sys
import shlex
import subprocess
import tempfile

import requests

VIRTUALENV_COMMAND = "virtualenv {options} {env_dir}"
PIP_URL = "https://raw.github.com/pypa/pip/master/contrib/get-pip.py"
PIP_FILE = "get_pip.py"
PIP_ERROR = "get_pip.py failed: Error {error_code}\n{error_output}"

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

try:
    import venv

    class VenvBuilderWithPip(venv.EnvBuilder):
        def __init__(self, system_site_packages=False, clear=False, symlinks=False, upgrade=False, with_pip=False):
            super().__init__(
                    system_site_packages=system_site_packages,
                    clear=clear,
                    symlinks=symlinks,
                    upgrade=upgrade
                )
            self.with_pip = with_pip
        def post_setup(self, context):
            if self.with_pip:
                with tempfile.TemporaryDirectory() as t:
                    with open(PIP_FILE, "wb") as f:
                        r = requests.get(PIP_URL)
                        r.raise_for_status() # dunno what state this leaves the venv in...
                        f.write(r.content)
                    try:
                        subprocess.check_output(
                            [context.env_exe, os.path.join(t, PIP_FILE)],
                            stderr=subprocess.STDOUT
                            )
                    except subprocess.CalledProcessError as e:
                        print(PIP_ERROR.format(
                            error_code=e.returncode,
                            error_output=e.output
                            ))
except ImportError as e:
    pass
