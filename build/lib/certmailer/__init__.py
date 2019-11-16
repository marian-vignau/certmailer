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

from pathlib import Path

import appdirs
import yaml


def ensure_dir_exists(dirpath):
    """If the directory doesn't exist, create it."""
    if not dirpath.exists():
        dirpath.mkdir()
    return dirpath


class Dir(object):
    def __init__(self, app):
        self.data_basedir = ensure_dir_exists(Path(app.user_data_dir))
        self.cache_basedir = ensure_dir_exists(Path(app.user_cache_dir))
        self.config_basedir = ensure_dir_exists(Path(app.user_config_dir))

        self.config_path = self.config_basedir.joinpath("config.cfg")


def main(app):
    global base
    global config_data
    base = Dir(app)
    if base.config_path.exists():
        with open(base.config_path, encoding="utf8") as fh:
            config_data = yaml.safe_load(fh.read())

# simple attributes to have this calculated at one place only
base = None
config_data = None
app = appdirs.AppDirs("certmailer")
main(app)

