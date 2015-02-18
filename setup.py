#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from tecdoc import VERSION
import os


def _read(rel_path):
    with open(os.path.join(os.path.dirname(__file__), rel_path)) as fp:
        return fp.read()


setup(
    name='django-tecdoc',
    version=VERSION,

    description='Itegration django and tecdoc db',
    long_description=_read('README.md'),
    author='Victor Safronovich',
    author_email='vsafronovich@gmail.com',
    license='MIT',
    url='https://github.com/marazmiki/django-tecdoc',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    install_requires=file(
        os.path.join(
            os.path.dirname(__file__),
            'requirements.txt'
        )
    ).read(),
    include_package_data=True,
)
