#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup function for the package."""

from setuptools import setup

setup(
  name='gbj_config',
  version='1.0.0',
  description='Python package for module config.',
  long_description='Module for processing INI configuration files.',
  classifiers=[
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Topic :: System :: Monitoring',
  ],
  keywords='utils',
  url='http://github.com/mrkalePythonLib/gbj_config',
  author='Libor Gabaj',
  author_email='libor.gabaj@gmail.com',
  license='MIT',
  packages=['gbj_config'],
  install_requires=[],
  include_package_data=True,
  zip_safe=False
)
