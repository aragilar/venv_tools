import setuptools

import os
import re

## Utility funcs from https://github.com/pypa/sampleproject/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))
# Read the version number from a source file.
# Code taken from pip's setup.py
def find_version(*file_paths):
    import codecs
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
with open('README.rst') as f:
    long_description = f.read()

deps = ["requests"]

try:
    import venv
except ImportError:
    deps.append("virtualenv")

setuptools.setup(
    name="venv_tools",
    version=find_version("venv_tools", "__init__.py"),
    packages = ["venv_tools"],
    install_requires = deps,
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "A bunch of tools for using venvs (and virtualenvs) from python.",
    long_description = long_description,
    license = "BSD",
    keywords = "virtualenv venv",
    url = "http://venv_tools.rtfd.org",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    extras_require = {
        "virtualenv": ["virtualenv"]
    }
)
