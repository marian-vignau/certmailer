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
import click
from .utils import load_yml, save_yml
from . import base

class KeyString(click.ParamType):
    name = "integer"

    def convert(self, value, param, ctx):
        error = "You must enter the provided key, a 32 digits hex number."
        try:
            value = value.strip().lower()
            if len(value) == 32:
                n = int(value, 16)
                return value
        except TypeError:
            pass
        except ValueError:
            pass
        self.fail(
            "You must enter the provided key, a 32 digits hex number.",
            param,
            ctx,
        )


KEYSTRING = KeyString()


@click.group()
def cli():
    pass

@cli.command()
@click.option("--api_key", prompt="Enter api key", type=KEYSTRING)
@click.option("--secret_key", prompt="Enter secret key", type=KEYSTRING)
def config(api_key, secret_key):
    """Init or edit the configuration.
    Includes private/public key from mailjet"""
    config_data = load_yml(base.config_path)
    config_data["api_key"] = api_key
    config_data["secret_key"] = secret_key
    save_yml(base.config_path, config_data)
