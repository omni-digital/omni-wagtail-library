#!/usr/bin/env python
from __future__ import unicode_literals
from omni_wagtail_library import __version__
from setuptools import setup, find_packages

setup(
      name='omni_wagtail_library',
      version=__version__,
      description='Library features for Wagtail',
      author='Omni Digital',
      author_email='dev@omni-digital.co.uk',
      url='https://github.com/omni-digital/omni-wagtail-library',
      download_url='https://github.com/omni-digital/omni-wagtail-library/tarball/0.1.0',
      packages=find_packages(exclude=['app']),
      license='MIT',
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5'
      ],
      include_package_data=True,
      keywords=['wagtail', 'django', 'mvc']
)
