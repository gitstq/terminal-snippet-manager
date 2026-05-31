#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeSnap - A blazing fast terminal code snippet manager
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='codesnap-cli',
    version='1.0.0',
    description='A blazing fast terminal code snippet manager for developers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='CodeSnap Team',
    author_email='hello@codesnap.dev',
    url='https://github.com/yourusername/codesnap-cli',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'codesnap=codesnap.cli:main',
            'csp=codesnap.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    keywords='code snippet manager cli terminal developer productivity',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/codesnap-cli/issues',
        'Source': 'https://github.com/yourusername/codesnap-cli',
        'Documentation': 'https://github.com/yourusername/codesnap-cli#readme',
    },
)
