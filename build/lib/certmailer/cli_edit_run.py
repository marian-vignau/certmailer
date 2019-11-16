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

import sys
import subprocess
import os
import platform

import click
import yaml

from .jobs import jobs



@click.group()
def cli():
    pass



@cli.group()
def edit():
    """Edit current job components"""
    if not jobs.current_job:
        click.echo("No current job selected. Use >> certmailer use <jobname>")
        sys.exit(1)


@edit.command()
def text():
    """Edits the email text template"""
    openfile("textpart.txt")


@edit.command()
def html():
    """Edits the email html template"""
    openfile("htmlpart.html")


@edit.command()
def config():
    """Edits the configuration file"""
    openfile("config.yml")


@edit.command()
def certificate():
    """Edits the certificate using Inkscape."""
    openfile("certificate.svg", editor="inkscape")


@edit.command()
def receivers():
    """Edits the email receivers."""
    openfile("receivers.csv", editor="libreoffice")



def openfile(filename, editor=None):
    """Opens file with default editor."""
    filepath = jobs.current_job.relative_path(
        filename)
    if filepath.exists():
        if editor:
            click.edit(filename=str(filepath), editor=editor)
        else:
            click.edit(filename=str(filepath))
    else:
        click.secho(f"File {filename} doesn't exists", fg="red")
        sys.exit(1)


@cli.group()
def do():
    """Do any needed operations."""
    if not jobs.current_job:
        click.echo("No current job selected. Use >> certmailer use <jobname>")
        sys.exit(1)


@do.command()
def list():
    """Creates recipients list."""
    from . import make_csv
    make_csv.make_csv(jobs.current_job)


@do.command()
def template():
    """Parses and creates and email template."""
    from .make_template import make_template
    make_template(jobs.current_job)


@do.command()
def certificates():
    """Do all certificates using data."""
    from .make_pdf import make_pdf
    make_pdf(jobs.current_job)


@do.command()
def send():
    """Send all the mails."""
    from .send_mails import send_mails
    send_mails(jobs.current_job)


