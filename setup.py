"""
Setup
"""
from setuptools import setup, find_packages
from sectoralarmlib import VERSION

setup(
  name = 'sectoralarmlib',
  packages = find_packages(),
  version = VERSION,
  description = 'Library for Sector Alarm',
  long_description = 'Library for Sector Alarm',
  author = 'Per-Øyvind Bruun',
  author_email = 'per-oyvind.bruun@vitari.no',
  url = 'https://github.com/peroyvind/sectoralarmlib',
  keywords = ['sectoralarm'],
  classifiers = [ 'Programming Language :: Python :: 3.7',
                  'Programming Language :: Python :: 3.6',
                  'Programming Language :: Python :: 3.5'
                ],
  install_requires=[
          'requests'
  ],
)
