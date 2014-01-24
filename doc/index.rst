
Welcome to venv_tools's documentation!
======================================
:py:mod:`venv_tools` is a collection of
`BSD Licenced`_ utilities for
using venvs from Python.

.. _BSD Licenced: https://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29

.. code-block :: python

    with venv_tools.TemporaryVenv(path_to_venv):
        subprocess.call(["pip", "install", "-r", "requirements.txt"])
        subprocess.call(["python", "-m", "profile", "project"])

Contents:

.. toctree::
   :maxdepth: 2

   Usage
   API





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

