#!/usr/bin/env python

from setuptools import setup

setup(
    setup_requires=['pbr'],
    package_dir={'': 'src'},
    py_moculdes=['icingapy'],
    pbr=True,
)