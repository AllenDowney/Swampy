#!/usr/bin/env python

from distutils.core import setup

setup(name='swampy',
      version='2.0.1',
      description='Companion code for Think Python/Python for Software Design',
      license='GNU GPL 3.0',
      author='Allen Downey',
      author_email='downey@allendowney.com',
      url='http://allendowney.com/swampy',
      packages=['swampy', 'swampy.sync_code'],
      package_dir={'swampy': 'python2'},
      package_data={'swampy': ['*.html']},
      data_files=[('swampy', ['danger.gif', 'words.txt'])],
     )
