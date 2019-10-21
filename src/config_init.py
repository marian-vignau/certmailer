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

import argparse
import yaml

from . import config_path

def parser(parent) -> argparse.ArgumentParser:
    """Returns the config parser"""
    sp = parent.add_parser("config",
        help="Init or edit the configuration.\nIncludes private/public key from mailjet")
    sp.add_argument("--api_key", type=str, optional=True)
    sp.add_argument("--secret_key", type=str, optional=True)
    return sp


def load_config():
    """Loads config data."""
    config_data = {"current_job": ""}
    if config_path.exists():
        with open(config_path, encoding="utf8") as fh:
            config_data = yaml.safe_load(fh.read())
    return config_data


def save_config(new_data):
    """Updates and saves config data."""
    config_data = load_config()
    config_data.update(new_data)
    with open(config_path, "w", encoding="utf8") as fh:
        fh.write(yaml.safe_dump(config_data))


def validate_key(res):
    """Validates & returns a key."""
    res = res.strip().lower()
    if len(res) == 32:
        try:
            n = int(res, base=16)
            return True
        except ValueError:
            return False


def _enter_key(prompt):
    while True:
        res = input(f"Enter {prompt} or exit: ")
        if res == "exit" or validate_key(res):
            break
        print(f"You must enter the provided {prompt} (32 digits hex number) or 'exit'")


def wizard(config_data):
    """Interacts with user asking config values."""
    config_data["api_key"] = _enter_key("api key")
    if config_data["api_key"] == "exit":
        return None
    config_data["secret_key"] = _enter_key("secret key")
    if config_data["secret_key"] == "exit":
        return None


def config_init(pargs):
    """Creates or edits a config file."""
    config_data = load_config()
    use_wizard = False
    for key in [pargs.api_key, pargs.secret_key]:
        if not key or not validate_key(key):
            use_wizard = True
    if use_wizard:
        wizard(config_data)
    else:
        config_data["api_key"] = pargs.api_key
        config_data["api_secret"] = pargs.secret_key
    save_config(config_data)

