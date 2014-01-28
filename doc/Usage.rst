Usage
=====
:py:mod:`venv_tools` contains two context managers,
:py:class:`venv_tools.Venv`
and
:py:class:`venv_tools.TemporaryVenv`,
which are designed to work together:

.. code-block :: python

    with TemporaryVenv() as env_dir, Venv(env_dir):
        call(["pip", "install", "-r", "requirements.txt"])
        call(["python", "-m", "profile", "project"])

Or, if you already have a venv:

.. code-block :: python

    with Venv(env_dir):
        call(["pip", "install", "-r", "requirements.txt"])
        call(["python", "-m", "profile", "project"])

Because :py:mod:`venv_tools`
wraps around the `venv.EnvBuilder` API
in Python 3.3 and above,
it's possible to use more featureful subclasses,
such as the example given
`here <http://docs.python.org/3.3/library/venv.html#an-example-of-extending-envbuilder>`_.
In fact, for Python 3.3,
the default `venv_builder` is
a subclass of `venv.EnvBuilder`
which includes the option
`get_pip`.
This has the advantage that
if you're using Python 3.3 or above,
and you have a set of
packages you keep installing inside your venv,
you don't need to copy the same code around,
you can just create a subclass.

