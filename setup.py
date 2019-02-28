#!/usr/bin/env python
from __future__ import unicode_literals

import io
import os
import re

from setuptools import setup, find_packages


# Get package version number
# Source: https://packaging.python.org/single_source_version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the version of the project
_version = find_version('wagtail_library', '__init__.py')

setup(
    name='wagtail-library',
    version=_version,
    description='Library features for Wagtail',
    author='Omni Digital',
    author_email='dev@omni-digital.co.uk',
    url='https://github.com/omni-digital/omni-wagtail-library',
    download_url='https://github.com/omni-digital/omni-wagtail-library/tarball/{0}'.format(_version),
    packages=find_packages(exclude=['tests']),
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
        'Programming Language :: Python :: 3.6'
    ],
    include_package_data=True,
    keywords=['wagtail', 'django']
)
