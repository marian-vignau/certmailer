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


# simple attributes to have this calculated at one place only
app = appdirs.AppDirs("certmail")

ensure_dir_exists(Path(app.user_config_dir))
ensure_dir_exists(Path(app.user_data_dir))
ensure_dir_exists(Path(app.user_cache_dir))

data_basedir = Path(app.user_data_dir)
cache_basedir = Path(app.user_cache_dir)
config_basedir = Path(app.user_config_dir)

config_path = config_basedir.joinpath("config.cfg")

if config_path.exists():
    with open(config_path, encoding="utf8") as fh:
        config_data = yaml.safe_load(fh.read())



