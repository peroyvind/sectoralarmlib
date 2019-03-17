#from distutils.core import setup
from setuptools import setup
setup(
  name = 'sectoralarmlib',
  packages = ['sectoralarmlib'], # this must be the same as the name above
  version = '0.3',
  description = 'Library for Sector Alarm',
  author = 'Per-Øyvind Bruun',
  author_email = 'per-oyvind.bruun@vitari.no',
  url = 'https://github.com/peroyvind/sectoralarmlib',
  download_url = 'https://github.com/peroyvind/sectoralarmlib/tarball/0.1',
  keywords = ['sectoralarm'], 
  classifiers = [],
  install_requires=[
          'requests'
  ]
)
