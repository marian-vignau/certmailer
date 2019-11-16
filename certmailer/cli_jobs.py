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

from .jobs import jobs
import sys

@click.group()
def cli():
    pass


@cli.group()
def job():
    """Manage jobs."""
    pass


@job.command()
def list():
    """List existing jobs"""
    click.echo(str(jobs))


@job.command()
@click.argument("name", type=str)
@click.option("-t", "--title", prompt="Title of event", type=str)
@click.option("-e", "--sender_email", prompt="E-Mail sender address", type=str)
@click.option("-n", "--sender_name", prompt="E-Mail sender name", type=str)
@click.option("-s", "--subject", prompt="E-Mail subject", type=str)
@click.option("-f", "--from_date", prompt="Enter initial date of registration", type=click.DateTime())
@click.option("-d", "--to_date", prompt="Enter final date of registration", type=click.DateTime())
def new(name, **job_data):
    """Creates a new job"""
    if not name in jobs.list():
        jobs.new(name, job_data)
    else:
        click.echo(f"Job {name} exists already!")
        jobs.current_job = name
        click.echo(f"Current job <{name}>")


def use(name):
    """Change the current job"""
    jobs.current_job = name
    click.echo(f"Current job <{name}>")


@job.command()
@click.argument("name", type=click.Choice(jobs.list()), required=False)
def use(name):
    """Change the current job"""
    if name:
        jobs.current_job = name
    click.echo(f"Current job <{name}>")
    click.echo(repr(jobs.current_job))


@cli.group()
def attach():
    """Manage attachments"""
    if not jobs.current_job:
        click.echo("No current job selected. Use >> certmailer use <jobname>")
        sys.exit(1)


@attach.command()
@click.argument("filenames", nargs=-1, type=click.Path(exists=True, resolve_path=True))
def add(filenames):
    """Add a fixed attachment"""
    jobs.current_job.attach.add(filenames)
    click.echo("Use like <img certmailer=\\'cid:the_name_of_file_without_extension\\'> on >> certmailer edit html")


@attach.command()
@click.argument("filename", type=str)
def remove(filename):
    """Removes a fixed attachment"""
    if jobs.current_job and filename in jobs.current_job.attach.list():
        jobs.current_job.attach.remove(filename)


@attach.command()
def list():
    """List fixed attachments added to the email"""
    click.echo(jobs.current_job.attach)


@cli.group()
def data():
    """Manage current job's data sources"""
    if not jobs.current_job:
        click.echo("No current job selected. Use >> certmailer use <jobname>")
        sys.exit(1)


@data.command()
def list():
    """Lists current job's data sources """
    click.echo(jobs.current_job.data)


@data.command()
@click.argument("filenames", nargs=-1, type=click.Path(exists=True, resolve_path=True))
def add(filenames):
    """Add a data source to current job."""
    jobs.current_job.data.add(filenames)


@data.command()
@click.argument("filename", type=str)
def remove(filename):
    """Remove a data source from current job."""
    if jobs.current_job and filename in jobs.current_job.data.list():
        jobs.current_job.data.remove(filename)
    else:
        click.echo("The file wasn't find in the list of attached. Any mistake?")
        click.echo(jobs.current_job.data)
        sys.exit(1)

