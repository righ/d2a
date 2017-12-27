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
    'table',
]

setup(
    name='djangomodel2alchemymap',
    version='0.0.0',
    install_requires=['Django', 'SQLAlchemy'],
    description='it converts a django model to a sqlalchemy mapping or table',
    long_description=open('./README.rst', 'r').read(),
    classifiers=classifiers,
    keywords=', '.join(keywords),
    author='righ',
    author_email="righ.m9@gmail.com,crohaco@beproud.jp",
    packages=find_packages(exclude=['tests']),
)
