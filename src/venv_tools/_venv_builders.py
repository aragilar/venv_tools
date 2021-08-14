# -*- coding: utf-8 -*-
"""
venv_tools._venv_builders
~~~~~~~~~~

EnvBuilder replacement classes for where EnvBuilder isn't available.

:copyright: (c) 2014 by James Tocknell.
:license: BSD, see LICENSE for more details.
"""
import sys
import shlex
import subprocess
import logging

log = logging.getLogger(__name__)

VIRTUALENV_COMMAND = "virtualenv {options} {env_dir}"


class VirtualenvBuilder(object):
    # pylint: disable=missing-docstring
    def __init__(
        self, system_site_packages=False, clear=False, with_pip=False,
        path_to_python_exe=None, **kwargs
    ):
        self.system_site_packages = system_site_packages
        self.clear = clear
        self.kwargs = kwargs
        self.with_pip = with_pip
        self.path_to_python_exe = path_to_python_exe or sys.executable

    def create(self, env_dir):
        # pylint: disable=missing-docstring
        options = ""
        options += " --python {python} ".format(python=self.path_to_python_exe)
        if self.system_site_packages:
            options += " --system-site-packages "
        if self.clear:
            options += " --clear "
        if not self.with_pip:
            options += " --no-setuptools --no-pip "
        log.debug("virtualenv options: {}".format(options))
        subprocess.check_output(
            shlex.split(VIRTUALENV_COMMAND.format(
                options=options, env_dir=env_dir
            )), stderr=subprocess.STDOUT
        )
