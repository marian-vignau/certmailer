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

import shutil
from pathlib import Path

import click

from . import ensure_dir_exists


class JobFolder(object):
    """To manage subfolders into data folder."""

    def __init__(self, job, path):
        """Creates the subfolder, if it's needed."""
        self.job = job
        self.name = path
        self.path = ensure_dir_exists(job.path.joinpath(path))

    def add(self, filepath):
        """Add (copy) a new file into the folder"""
        for filename in filepath:
            dst = self.path.joinpath(Path(filename).name)
            shutil.copyfile(filename, dst)
            click.echo(f"Added as {self.name} {dst.name}")

    def remove(self, filename):
        """Remove a file from the subfolder"""
        dst = self.path.joinpath(filename)
        dst.unlink()
        click.echo(f"Removed from {self.name} {dst.name}")

    def list(self):
        """Returns the list of files into the folder"""
        return [f.name for f in self.path.iterdir()]

    def __str__(self):
        s = self.name + ": \n  - "
        if self.list():
            return s + "\n  - ".join(self.list())
        else:
            return s + "none"
