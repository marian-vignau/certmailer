#!/usr/bin/env python3

# Copyright 2019 María Andrea Vignau

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check

__author__ = "María Andrea Vignau"

"""
Used to create a command-line tool with setup tools
-- Add path to venv into PyCharm
       - Project Settings/Project Interpreter/<right click on gear icon>
        /Show all/<click on dirtree icon>
        /<click on add icon>/
        select the path of current tools project
-- Go to command prompt, navigate to current project subfolder
-- Activate virtualenv,
>>> virtualenv venv
>>> . venv/bin/activate
>>> pip install --editable .
-- Install actual module in develop mode
>>> python setup.py develop --no-deps
-- Use on console
>>> certmailer --help
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='certmailer',
    version='1.0',
    py_modules=['certmailer'],
    install_requires=[
        'PyYaml', "mailjet_rest", "certg", "appdirs", "click"
    ],
    entry_points='''
        [console_scripts]
        certmail=certmail:cli
    ''',
    author="María Andrea Vignau",
    author_email="mavignau@gmail.com",
    description="To download, create and mail certificate on events",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marian-vignau/certmailer",
    packages=["certmailer"],
    scripts=["certmail.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Email"
    ],
    python_requires='>=3.6',
    setup_requires=['wheel'],
    package_data={'certmailer': ['template.zip']},
    include_package_data=True
)