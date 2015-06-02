#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
dice
-----

dice is an test tool for adexchange.

"""

import ast
import os
import os.path
import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
data_dir = 'dice/res'
data = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]

with open('dice/__init__.py', 'rb') as f:
        version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))
        setup(
            name='dice',
            version=version,
            url='http://git.adleida.com/paxp/',
            author='adleida',
            author_email='noreply@adleida.com',
            description='dice is an test tool for adexchange.',
            long_description=__doc__,
            packages=['dice', 'dice.ext'],
            package_data={'dice': data},
            include_package_data=True,
            zip_safe=False,
            platforms='any',
            entry_points='''
                [console_scripts]
                dice=dice.dice:main
            ''',
            install_requires=[
                'Flask>=0.10.1',
                'Flask-RESTful',
                'requests',
                'PyYAML>=3.11',
                'fake-factory>=0.5.0',
                'apitools',
                'rstr'
            ],
        )
