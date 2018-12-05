# -*- coding: utf-8 -*-

from setuptools import setup
import re
from io import open

## from https://gehrcke.de/2014/02/distributing-a-python-command-line-application/
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pip_upgrade_outdated/upgrade_pip_packages.py', 'r').read(),
    re.M
    ).group(1)

with open('README.md', 'r') as f:
    long_description = f.read()   #.decode("utf-8")

setup(name='pip_upgrade_outdated',
      version=version,
      description='Command-line tool to updated outdated python packages',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/defjaf/pip_upgrade_outdated',
      author='Andrew H. Jaffe',
      author_email='a.h.jaffe@gmail.com',
      license='MIT', ### see https://choosealicense.com/licenses/mit/#
      packages=['pip_upgrade_outdated'],
      install_requires=['pip'],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Packaging',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
      ],
      keywords='pip',
      entry_points = {
        'console_scripts': ['pip_upgrade_outdated=pip_upgrade_outdated.upgrade_pip_packages:main'],
    }
)
