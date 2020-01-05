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

import click

from .eventoL_import import MyList
from .gen_mail import GenMail
from .jobs import jobs
from .make_template import Template
from .receivers import Receivers
from .utils import is_connected, Table
from .utils import reuse_filename


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
def list():
    """Edits the email receivers."""
    openfile("receivers.csv", editor="libreoffice")


def openfile(filename, editor=None):
    """Opens file with default editor."""
    filepath = jobs.current_job.relative_path(filename)
    if filepath.exists():
        if editor:
            click.edit(filename=str(filepath), editor=editor)
        else:
            click.edit(filename=str(filepath))
    else:
        click.secho(f"File {filename} doesn't exists", fg="red")
        sys.exit(1)


def need_current_job(func):
    def inner(*args, **kargs):
        if not jobs.current_job:
            click.echo("No current job selected. Use >> certmailer use <jobname>")
            sys.exit(1)
        print("ok")
        func(*args, **kargs)

    return inner


@need_current_job
@cli.command("import", help="Imports data")
def impo():
    """Imports data exported from eventoL
    and creates de data sheet
    of certificates to generate"""

    do = MyList(jobs.current_job)
    receivers = Receivers(jobs.current_job)
    if receivers.exists():
        s = reuse_filename(receivers.filename)
        click.secho(f"Receivers list exists. Renamed to {str(s)}", fg="red")
    receivers.write(do)
    click.echo(f"Created {receivers.filename}.")
    click.echo("Open to choose mails to send and certificates to generate")


@need_current_job
@cli.command()
@click.option("--flag", default="", help="Flag that mark receivers.")
def send(flag):
    """Send all the mails."""
    if not is_connected():
        click.secho("You need to be connected to Internet", fg="red")
        sys.exit(1)
    template = Template(jobs.current_job)
    if template.missed:
        click.secho(
            "Error: Missing inline attachments referenced "
            + ", ".join(template.missed),
            fg="red",
        )
        sys.exit(1)
    receivers = Receivers(jobs.current_job)
    to_send = receivers.mails_to_send(flag)
    if not to_send:
        click.secho("Error: No mails to send", fg="red")
        sys.exit(1)
    else:
        sender = GenMail(jobs.current_job, template)
        prog = click.progressbar(length=to_send)
        for receiver in receivers.read(flag):
            sender.sendmail(receiver)
            prog.update(1)
            sender.clean_n_log(receiver)
        click.echo(f"\nTotal {sender.total_mails} mails sent")
        click.echo(f"Total {sender.total_certificates} certificates sent")
        if sender.unsended_mails != 0:
            click.secho(f"Total {sender.unsended_mails} mails not sended.", fg="red")
        click.echo(f"See detailed log file at {sender.log}")


@need_current_job
@cli.command()
@click.option("--flag", default="", help="Flag that mark receivers.")
def show(flag):
    """List all the mails."""
    receivers = Receivers(jobs.current_job)
    if receivers.exists():
        table = Table()
        for receiver in receivers.read(flag):
            table.add(receiver.data)
        click.echo(str(table))
    to_send = receivers.mails_to_send(flag)
    click.echo(f"Total {to_send} receivers.")
