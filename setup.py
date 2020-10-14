#!/usr/bin/python3

from setuptools import setup, find_packages


setup(name='ddgparser',
      version='1.0.0',
      description='A DuckDuckGo parser',
      long_description='A small Python parser for DuckDuckGo.',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Development Status :: 5 - Production/Stable'
      ],
      keywords='duckduckgo parser',
      url='https://github.com/arisuchr/ddg-parser',
      author='Arisu Wonderland',
      author_email='arisuchr@protonmail.ch',
      license='GNU General Public License v3 or later (GPLv3+)',
      packages=find_packages(),
      install_requires=[
          'lxml',
          'requests'
      ],
      python_requires='>=3.6')
