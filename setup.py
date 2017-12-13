#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open('src/__init__.py') as f:
    for line in f:
        if line.find('__version__') >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as requirements_file:
    requirements = requirements_file.read()

setup(
    name='ldap-group-acl-helper',
    version=version,
    description='Squid external acl ldap group helper',
    long_description=readme,
    author='Vadim Aleksandrov',
    author_email='valeksandrov@me.com',
    url='https://github.com/verdel/ldap-group-acl-helper',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    entry_points={'console_scripts': ['ext_acl_ldap_group=src.ext_acl_ldap_group:main', ], },
    include_package_data=True,
    install_requires=requirements,
    keywords='squid external acl ldap group',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
