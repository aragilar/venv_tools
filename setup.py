import setuptools

import versioneer

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name="venv_tools",
    version = versioneer.get_version(),
    packages = setuptools.find_packages(),
    install_requires = ["virtualenv"],
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "A bunch of tools for using venvs (and virtualenvs) from python.",
    long_description = long_description,
    license = "BSD",
    keywords = "virtualenv venv",
    url = "https://venv-tools.readthedocs.io/",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass=versioneer.get_cmdclass(),
)
