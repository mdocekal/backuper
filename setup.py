# -*- coding: UTF-8 -*-
""""
Created on 23.12.19

:author:     Martin Dočekal
"""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='backuper',
    version='1.0.0',
    description='Tiny tool for fast backup of files. ',
    long_description_content_type="text/markdown",
    long_description=README,
    license='The Unlicense',
    packages=find_packages(),
    author='Martin Dočekal',
    keywords=['utils', 'backups', 'backups by type of files'],
    url='https://github.com/windionleaf/backuper',
    install_requires=[
        'windpyutils @ git+git://github.com/windionleaf/windPyUtils#windpyutils',
    ]
)

if __name__ == '__main__':
    setup(**setup_args)