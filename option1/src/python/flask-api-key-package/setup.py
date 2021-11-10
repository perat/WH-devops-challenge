# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

setup(
    name='flask-api-key',
    version='0.1.0',
    description='Sample package for flask with API Key check',
    author='Taras Perebeynosov',
    author_email='taras.perebeynosov@gmail.com',
    url='https://github.com/perat/WH-devops-challenge',
    packages=find_packages(exclude=('tests', 'docs'))
)
