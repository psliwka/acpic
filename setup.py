#!/usr/bin/env python3

from setuptools import setup

setup(
    py_modules=["acpic"],
    setup_requires=["pbr>=5.8.1,<6"],
    pbr=True,
)
