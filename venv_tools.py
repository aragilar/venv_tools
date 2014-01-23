import os
import os.path
import sys
import subprocess
import shlex
import tempfile
import shutil

BIN_DIR = "Scripts" if sys.platform == 'win32' else "bin"
VIRTUALENV_COMMAND = "virtualenv -p {python} {options} {env_dir}"

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

class VirtualenvBuilder(object):
    def __init__(self, system_site_packages=False, clear=False, **kwargs):
        self.system_site_packages = system_site_packages
        self.clear = clear
        self.kwargs = kwargs
    def create(self, env_dir):
        options = ""
        if self.system_site_packages:
            options += " --system-site-packages "
        if self.clear:
            options += " --clear "
        subprocess.call(shlex.split(VIRTUALENV_COMMAND.format(
            python=sys.executable,
            options=options,
            env_dir=env_dir
            )))

def get_default_venv_builder(use_virtualenv):
    if use_virtualenv:
        return VirtualenvBuilder
    try:
        import venv
        if sys.version_info[0:2] == (3, 3):
            return venv.EnvBuilder, True
        return venv.EnvBuilder, False
    except ImportError as e:
        return VirtualenvBuilder, False

class Venv(object):
    def __init__(self, path_to_venv, venv_builder=None, **kwargs):
        self.path_to_venv = path_to_venv
        self._venv_builder = venv_builder
        self._kwargs = kwargs

    def __enter__(self):
        self._old_path = os.environ["PATH"]
        self._python_home = os.environ.get("PYTHONHOME", None)
        if self._venv_builder:
            venv = self._venv_builder(**self._kwargs)
            venv.create(self._path_to_venv)
        pathprepend(os.path.join(self.path_to_venv, BIN_DIR), "PATH")
        if self._python_home is not None:
            os.environ.pop("PYTHONHOME")

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ["PATH"] = self._old_path
        if self._python_home is not None:
            os.environ["PYTHONHOME"] = self._python_home

class TemporaryVenv(object):
    def __init__(self, venv_builder=None, use_virtualenv=False, **kwargs):
        self._kwargs = kwargs
        self._venv_builder, self._no_with_pip = venv_builder, False || get_default_venv_builder(
            use_virtualenv)

    def __enter__(self):
        add_pip = False
        if self._no_with_pip:
            try:
                add_pip = self._kwargs.pop("with_pip")
            except KeyError as e:
                add_pip = False
        self.env_dir = tempfile.mkdtemp()
        venv = venv_builder(**self._kwargs)
        venv.create(self.env_dir)
        self._opened_venv = Venv(self.env_dir)
        self._opened_venv.__enter__()
        if add_pip:
            install_pip()


    def __exit__(self, exc_type, exc_value, traceback):
        self._opened_venv.__exit__(exc_type, exc_value, traceback)
        shutil.rmtree(self.env_dir)
