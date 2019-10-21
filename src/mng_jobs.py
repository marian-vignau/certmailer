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

import shutil, os
import zipfile

import click

from . import data_basedir, cache_basedir, ensure_dir_exists, config_path
from .utils import load_yml, save_yml


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
    pass


@job.command()
def new():
    """Creates a new job"""
    pass


@job.command()
def remove():
    """Remove a job from list"""
    pass


@job.command()
def use():
    """Change the current job"""
    pass


@cli.group()
def attach():
    """Manage attachments"""
    pass


@attach.command()
def add():
    """Add a fixed attachment"""
    pass


@attach.command()
def remove():
    """Removes a fixed attachment"""
    pass


@attach.command()
def list():
    """List fixed attachments added to the email"""
    pass


@cli.group()
def inline():
    """Manage attachments"""
    pass


@inline.command()
def add():
    """Add a fixed attachment"""
    pass


@inline.command()
def remove():
    """Removes a fixed attachment"""
    pass


@inline.command()
def list():
    """List fixed attachments added to the email"""
    pass


class Jobs(object):
    def __init__(self):
        """Load the data structure"""
        config = load_yml(config_path)
        current = config.get("current_job", "")
        self._current_job = False
        if current:
            self._current_job = Job(current)

    def list(self):
        """List all the jobs."""
        return [job for job in data_basedir.iterdir() if job.is_dir()]

    def attachlist(self):
        """Returns the list of attachments in current job"""
        if self._current_job:
            return self._current_job.attach.list()
        else:
            return []

    def inlinelist(self):
        """Returns the list of inline images in current job"""
        if self._current_job:
            return self._current_job.inline.list()
        else:
            return []

    @property
    def current_job(self):
        """Return current job saved on current.txt"""
        return self._current_job.name

    @current_job.setter
    def set_current_job(self, name):
        """Change from one job to other"""
        if name in self.list():
            self._current_job = Job(name)
            save_yml(config_path, {"current_job": name})
        else:
            raise KeyError(f"Job {name} not found")

    def new(self, name, title="", date=None):
        """Creates the basic template of a job"""
        if name in self.list():
            raise KeyError(f"Can't create job {name}. It exists.")
        job = Job(name, title, date)

        self._current_job = job

    def __str__(self):
        s = ', '.join(self.list())
        s += f"\n{self._current_job}"
        return s


class Job(object):
    """Creates and access one job."""

    def __init__(self, name, title="", from_date=None, to_date=None):
        self.name = name
        self._init_dir(name)

    def _init_dir(self, name):
        self.datapath = data_basedir.joinpath(name)
        self.cachepath = cache_basedir.joinpath(name)
        if not self.datapath.exists():
            ensure_dir_exists(self.datapath)
            self.attach = ensure_dir_exists(self.datapath.joinpath("attach"))
            self.inline = ensure_dir_exists(self.datapath.joinpath("inline"))
            zip_ref = zipfile.ZipFile("init.zip", "r")
            zip_ref.extractall(self)
            zip_ref.close()

        ensure_dir_exists(self.cachepath)
        self.outbox = ensure_dir_exists(self.cachepath.joinpath("outbox"))
        self.sent = ensure_dir_exists(self.cachepath.joinpath("sent"))

    def _config(self):
        config_promt = {"title": ("Enter the event's title", lambda x: len(x) > 4),
                        "date": ("Enter the event's date (use YYYY-MM-DD format)", lambda x: len(x) == 10)}

    @property
    def attach(self):
        return self.attach

    @property
    def inline(self):
        return self.inline


class JobFolder(object):
    def __init__(self, job, path):
        self.job = job
        self.path = ensure_dir_exists(job.path.joinpath(path))

    def add(self, path, filename):
        shutil.copyfile(path, self.path.joinpath(filename))

    def remove(self, filename):
        os.remove(self.path.joinpath(filename))

    def list(self):
        return [f for f in self.path.iterdir() if f.is_file()]


jobs = Jobs()
