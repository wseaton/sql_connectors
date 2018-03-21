#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

from setuptools.command.develop import develop
from setuptools.command.install import install

from codecs import open
import os
import re
import shutil

exec(open('sql_connectors/_version.py').read())

here = os.path.abspath(os.path.dirname(__file__))

def post_install():
    config_dir = os.path.expanduser("~/.config/sql_connectors")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        os.makedirs(os.path.join(config_dir, 'certs'))
        shutil.copy2('example_connection.json', config_dir)
    print("Please place your config files in {0}. Take a look at example_connection.json")


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        post_install()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        post_install()


vcs = "^(git|hg)\\+"

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if not re.search(vcs, x) and x.strip() != '']
dependency_links = [re.sub(vcs, '', x.strip()) for x in all_reqs if re.search(vcs, x)]

for dep in dependency_links:
    match = re.search('egg=((?:\w|-)+)', dep)
    if match:
        install_requires.append(match.group(1))

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Diego Fernandez",
    author_email='aiguo.fernandez@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A simple wrapper for SQL connections using SQLAlchemy and Pandas read_sql to standardize SQL workflow.",
    install_requires=install_requires,
    license="MIT license",
    long_description=long_description,
    include_package_data=True,
    keywords='sql_connectors',
    name='sql_connectors',
    packages=find_packages(include=['sql_connectors']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aiguofer/sql_connectors',
    version=__version__,
    zip_safe=False,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
