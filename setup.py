#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="guolei-py3-wisharetec",
    version="2.3.1",
    description="慧享(绿城)科技 API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guolei19850528/guolei_py3_wisharetec",
    author="guolei",
    author_email="174000902@qq.com",
    license="MIT",
    keywors=["慧享科技", "绿城", "wisharetec"],
    packages=setuptools.find_packages('./'),
    install_requires=[
        "guolei-py3-requests",
        "requests",
        "diskcache",
        "redis",
        "addict",
        "retrying",
        "jsonschema",
    ],
    python_requires=">=3.0",
    zip_safe=False
)
