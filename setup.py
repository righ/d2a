#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Topic :: Software Development',
]
keywords = [
    'django',
    'sqlalchemy',
    'model',
    'mapping',
    'decralation',
    'table',
    'expression',
    'orm',
]

setup(
    name='d2a',
    version='1.0.1',
    description='It converts django models to a sqlalchemy orm/expression objects.',
    long_description=open('./README.rst', 'r').read(),
    classifiers=classifiers,
    keywords=', '.join(keywords),
    author='righ',
    author_email="righ.m9@gmail.com,crohaco@beproud.jp",
    packages=find_packages(exclude=['tests', 'projects_*']),
)

