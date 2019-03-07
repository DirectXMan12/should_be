#!/usr/bin/env python2.7
from setuptools import setup

setup(
    name='shouldbe',
    version='0.1.1',
    author='Solly Ross',
    author_email='sross@redhat.com',
    packages=['should_be', 'should_be.tests', 'should_be.extensions'],
    description='Python Assertion Helpers inspired by Shouldly',
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    url="https://github.com/directxman12/should_be",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'forbiddenfruit'
    ],
    tests_require=[
        'nose'
    ],
    keywords=['testing', 'assertions'],
)
