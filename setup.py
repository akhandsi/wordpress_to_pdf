#!/usr/bin/env python

import re
import ast
from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

# get version information from __init__.py
with open('scripts/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# set up dependencies and cli command 'print'
setup(
    name="wordpress_to_pdf",
    version='0.1',
    py_modules=['start'],
    install_requires=[],
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        wordpressPrint=scripts.start:main
    ''',
)
