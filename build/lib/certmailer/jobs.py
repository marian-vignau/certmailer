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
import zipfile
from pkg_resources import resource_stream

import click

from . import base
from . import ensure_dir_exists
from .utils import load_yml, save_yml


class Jobs(object):
    """Jobs manager and conteiner. Singleton."""
    def __init__(self):
        """Load the data structure"""
        self.config = load_yml(base.config_path)
        current = self.config.get("current_job", "")
        self._current_job = None
        if current:
            self._current_job = Job(current)

    def list(self):
        """List all the jobs."""
        return [job.name for job in base.data_basedir.iterdir()]

    @property
    def current_job(self):
        """Return current job"""
        return self._current_job

    @current_job.setter
    def current_job(self, name):
        """Change from one job to other"""
        if name != self._current_job.name:
            if name is None:
                self._current_job = None
                save_yml(base.config_path, {"current_job": None})
            elif name in self.list():
                self._current_job = Job(name)
                save_yml(base.config_path, {"current_job": name})
            elif name:
                raise KeyError(f"Job {name} not found")

    def new(self, name, job_data):
        """Creates the basic template of a job"""
        self._current_job = Job(name, job_data)
        save_yml(base.config_path, {"current_job": name})

    def remove(self, name):
        """Removes a job folder."""
        shutil.rmtree(base.data_basedir.joinpath(name))
        if self._current_job and \
                name == self.current_job.name:
            if self.list():
                self.current_job = self.list()[0]
            else:
                self.current_job = None

    def __str__(self):
        """A human-readable representation of the job string"""
        if self.list():
            s = ', '.join(self.list())
            if self.current_job:
                s += f"\nCurrent job: {self.current_job}"
            return s
        else:
            return "No jobs created"


class Job(object):
    """Creates and access one job."""
    def __init__(self, name, job_data=None):
        """Configure a job"""
        self.name = name
        self.path = ensure_dir_exists(base.data_basedir.joinpath(name))
        self.config_path = self.relative_path("config.yml")
        if self.config_path.exists():
            self.config = load_yml(self.config_path)
        else:
            self.config = job_data
            self.config["name"] = name
            template_zip = resource_stream(__name__, 'template.zip')
            zip_ref = zipfile.ZipFile(template_zip, "r")
            zip_ref.extractall(self.path)
            zip_ref.close()
        save_yml(self.config_path, self.config)
        self.categories = load_yml(self.relative_path("categories.yaml"))
        self._init_dir(name)

    def relative_path(self, filename):
        """Return filepath relative to job path."""
        return self.path.joinpath(filename)

    def _init_dir(self, name):
        """Creates the folder structure"""
        self.attach = JobFolder(self, "attach")
        self.data = JobFolder(self, "data")

        self.cache = ensure_dir_exists(base.cache_basedir.joinpath(name))
        self.outbox = ensure_dir_exists(self.cache.joinpath("outbox"))
        self.sent = ensure_dir_exists(self.cache.joinpath("sent"))

        #self.p = Paths(self.path)

    def __str__(self):
        """An human-readable expresion of key information about the job"""
        if not self.config:
            return self.name
        s = "{name} ->"
        s += " '{title}'"
        s += " from {sender_name} <{sender_email}>"
        s += " / inscrip {from_date:%d/%m/%Y}"
        s += " to {to_date:%d/%m/%Y}"
        s += '\n Subj: "{subject}"'
        return s.format(**self.config)

    def __repr__(self):
        """Shows the data inside the job object"""
        s = map(str, [self, self.attach, self.data])
        return '\n'.join(s)


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
            return s + '\n  - '.join(self.list())
        else:
            return s + "none"


jobs = Jobs()
