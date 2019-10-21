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

@click.group()
def cli():
    pass


@cli.group()
def data():
    """Manage current job's data sources"""
    pass


@data.command()
def list():
    """Lists current job's data sources """
    pass


@data.command()
def add():
    """Add a data source to current job."""
    pass


@data.command()
def remove():
    """Remove a data source from current job."""
    pass


@cli.group()
def edit():
    """Edit current job components"""
    pass


@edit.command()
def email():
    """Edits the email template"""
    pass


@edit.command()
def certificate():
    """Edits the certificate using Inkscape."""
    pass


@edit.command()
def receivers():
    """Edits the email receivers."""
    pass

