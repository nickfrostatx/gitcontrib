# -*- coding: utf-8 -*-

from setuptools import setup
import re

version = ''
with open('gitcontrib.py', 'r') as f:
    version = re.search(r'__version__\s*=\s*\'([\d.]+)\'', f.read()).group(1)

with open('README.md') as f:
    readme = f.read()

with open('HISTORY.md') as f:
    history = f.read()

setup(
    name='gitcontrib',
    version=version,
    author='Nick Frost, Max Zinkus, & Nick Gonella',
    author_email='nickfrostatx@gmail.com',
    url='https://github.com/nickfrostatx/gitcontrib',
    description='Compare the activity of different git contributors.',
    long_description=readme + '\n\n' + history,
    py_modules=['gitcontrib'],
    install_requires=[],
    extras_require={
        'testing': [
            'pytest',
            'pytest-cov',
            'pytest-pep8',
            'pytest-pep257',
        ],
    },
    entry_points={
        'console_scripts': 'git-contrib=gitcontrib:main',
    },
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
)
