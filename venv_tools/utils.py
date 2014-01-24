import os
import sys
import venv_tools.venv_builders as venv_builders

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

def get_default_venv_builder(use_virtualenv):
    if use_virtualenv:
        return venv_builders.VirtualenvBuilder
    try:
        import venv
        if sys.version_info[0:2] == (3, 3):
            return venv_builders.VenvBuilderWithPip
        return venv.EnvBuilder
    except ImportError as e:
        return venv_builders.VirtualenvBuilder
