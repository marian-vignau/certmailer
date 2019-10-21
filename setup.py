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
>>> src --help
"""

from setuptools import setup

setup(
    name='certmailer',
    version='0.1',
    py_modules=['src'],
    install_requires=[
        'PyYaml', "mailjet_rest", "certg", "appdirs"
    ],
    entry_points='''
        [console_scripts]
        certmail=certmail:cli
    ''',
)