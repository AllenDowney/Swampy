#!/usr/bin/env python

from distutils.core import setup
import sys

if sys.version_info < (3,):
    package_dir = {'swampy': 'python2'}
else:
    package_dir = {'swampy': 'python3'}


setup(name='swampy',
      version='3.0.1',
      description='Companion code for Think Python/Python for Software Design',
      license='GNU GPL 3.0',
      author='Allen Downey',
      author_email='downey@allendowney.com',
      url='http://allendowney.com/swampy',
      packages=['swampy'],
      package_dir=package_dir,
      #package_data={'swampy': ['*.html']},
      data_files=[('swampy', ['python3/danger.gif', 'python3/words.txt'])],
     )
