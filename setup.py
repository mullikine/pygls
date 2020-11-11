#!/usr/bin/env python
import sys
from setuptools import find_packages, setup
import versioneer
import sys

README = open('README.rst', 'r').read()

install_requires = [
        'configparser; python_version<"3.0"',
        'future>=0.14.0; python_version<"3"',
        'backports.functools_lru_cache; python_version<"3.2"',
        'jedi>=0.17.2,<0.18.0',
        'python-jsonrpc-server>=0.4.0',
        'pluggy',
        'ujson<=2.0.3 ; platform_system!="Windows" and python_version<"3.0"',
        'ujson>=3.0.0 ; python_version>"3"']

setup(
    name='glossary-language-server',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Glossary Language Server for the Language Server Protocol',

    long_description=README,

    # The project's main homepage.
    url='https://github.com/mullikine/glossary-language-server',

    author='mullikine',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'test', 'test.*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[test]
    extras_require={
        'all': [
            'autopep8',
            'flake8>=3.8.0',
            'mccabe>=0.6.0,<0.7.0',
            'pycodestyle>=2.6.0,<2.7.0',
            'pydocstyle>=2.0.0',
            'pyflakes>=2.2.0,<2.3.0',
            # pylint >= 2.5.0 is required for working through stdin and only
            # available with python3
            'pylint>=2.5.0' if sys.version_info.major >= 3 else 'pylint',
            'rope>=0.10.5',
            'yapf',
        ],
        'autopep8': ['autopep8'],
        'flake8': ['flake8>=3.8.0'],
        'mccabe': ['mccabe>=0.6.0,<0.7.0'],
        'pycodestyle': ['pycodestyle>=2.6.0,<2.7.0'],
        'pydocstyle': ['pydocstyle>=2.0.0'],
        'pyflakes': ['pyflakes>=2.2.0,<2.3.0'],
        'pylint': [
            'pylint>=2.5.0' if sys.version_info.major >= 3 else 'pylint'],
        'rope': ['rope>0.10.5'],
        'yapf': ['yapf'],
        'test': ['versioneer',
                 'pylint>=2.5.0' if sys.version_info.major >= 3 else 'pylint',
                 'pytest', 'mock', 'pytest-cov', 'coverage', 'numpy', 'pandas',
                 'matplotlib', 'pyqt5;python_version>="3"', 'flaky'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pygls = pygls.__main__:main',
        ],
        'pygls': [
            'autopep8 = pygls.plugins.autopep8_format',
            'folding = pygls.plugins.folding',
            'flake8 = pygls.plugins.flake8_lint',
            'jedi_completion = pygls.plugins.jedi_completion',
            'jedi_definition = pygls.plugins.definition',
            'jedi_hover = pygls.plugins.hover',
            'jedi_highlight = pygls.plugins.highlight',
            'jedi_references = pygls.plugins.references',
            'jedi_rename = pygls.plugins.jedi_rename',
            'jedi_signature_help = pygls.plugins.signature',
            'jedi_symbols = pygls.plugins.symbols',
            'mccabe = pygls.plugins.mccabe_lint',
            'preload = pygls.plugins.preload_imports',
            'pycodestyle = pygls.plugins.pycodestyle_lint',
            'pydocstyle = pygls.plugins.pydocstyle_lint',
            'pyflakes = pygls.plugins.pyflakes_lint',
            'pylint = pygls.plugins.pylint_lint',
            'rope_completion = pygls.plugins.rope_completion',
            'rope_rename = pygls.plugins.rope_rename',
            'yapf = pygls.plugins.yapf_format'
        ]
    },
)
