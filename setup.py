#from distutils.core import setup
from setuptools import setup
setup(
  name = 'sectoralarmlib',
  packages = ['sectoralarmlib'], # this must be the same as the name above
  version = '0.5',
  description = 'Library for Sector Alarm',
  author = 'Per-Øyvind Bruun',
  author_email = 'per-oyvind.bruun@vitari.no',
  url = 'https://github.com/peroyvind/sectoralarmlib',
  keywords = ['sectoralarm'], 
  classifiers = [ 'Programming Language :: Python :: 3.6' ],
  install_requires=[
          'requests'
  ],
  
)
