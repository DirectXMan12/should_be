#!/usr/bin/env python2.7
import setuptools
from setuptools import setup
from setuptools import Extension

setup(
    name='ShouldBe',
    version='0.1.0',
    author='Solly Ross',
    author_email='sross@redhat.com',
    packages=['should_be', 'should_be.tests'],
    description='Python Assertion Helpers inspired by Shouldly',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    install_requires=[
        'forbiddenfruit'
    ]
)

