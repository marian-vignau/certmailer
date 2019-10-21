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

from . import data_basedir, cache_basedir, ensure_dir_exists
from .config_init import load_config, save_config
from .mktree import Dir
import yaml
import zipfile
import pathlib


def parser(parent):
    sp = parent.add_parser("job",
        help="Manage jobs")
    sp_2 = sp.add_subparsers(dest="operation", help="Posible job operations")
    sp_2.required = True
    job_parser(sp_2)

def job_parser(parent):
    parser = parent.add_parser("list", help="List existing jobs")

    parser = parent.add_parser("new", help="Creates a new job")
    parser.add_argument("jobname", type=str, required=True)
    parser.add_argument("--title", type=str, optional=True)
    parser.add_argument("--from_date", type=str, optional=True)
    parser.add_argument("--to_date", type=str, optional=True)

    parser = parent.add_parser("remove", help="Removes a job")
    parser.add_argument("jobname", type=str, required=True, choices=jobs.list())

    parser = parent.add_parser("use", help="Change the current job.")
    parser.add_argument("jobname", type=str, required=True, choices=jobs.list())
    return parser

def edit_parser(parent):
    parser = parent.add_parser("certificate", help="Edits the certificate using Inkscape")
    parser = parent.add_parser("email", help="Edits the email template")
    parser = parent.add_parser("receivers", help="Edits the email receivers")

def attach_parser(parent):
    parser = parent.add_parser("list", help="List fixed attachments added to the email")
    parser = parent.add_parser("add", help="Add a fixed attachment")
    parser.add_argument("filename", type=str, required=True)

    parser = parent.add_parser("remove", help="Removes a fixed attachment")
    parser.add_argument("filename", type=str, required=True, choices=jobs.attachlist())
    return parser


def inline_parser(parent):
    parser = parent.add_parser("list", help="Lists inline images")
    parser = parent.add_parser("add", help="Add an inline image")
    parser.add_argument("filename", type=str, required=True)

    parser = parent.add_parser("remove", help="Removes an inline image")
    parser.add_argument("filename", type=str, required=True, choices=jobs.inlinelist())
    return parser


class Jobs(object):
    def __init__(self):
        """Load the data structure"""
        config = load_config()
        self._current_job = config.get("current_job", "")

    def list(self):
        """List all the jobs."""
        return [job for job in data_basedir.iterdir() if job.is_dir()]

    def attachlist(self):
        """Returns the list of attachments in current job"""
        return []

    def inlinelist(self):
        """Returns the list of inline images in current job"""
        return []


    @property
    def current_job(self):
        """Return current job saved on current.txt"""
        return self._current_job

    @current_job.setter
    def set_current_job(self, name):
        """Change from one job to other"""
        if name in self.list():
            self._current_job = name
            save_config({"current_job": name})
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


class Job(Dir):
    """Creates and access one job."""
    def __init__(self, name, title, date):
        self.datapath = data_basedir.joinpath(name)
        self.cachepath = cache_basedir.joinpath(name)
        if not self.datapath.exists():
            ensure_dir_exists(self.datapath)
            zip_ref = zipfile.ZipFile("init.zip", "r")
            zip_ref.extractall(self)
            zip_ref.close()

        if not self.cachepath.exists():
            ensure_dir_exists(self.cachepath)
        self.outbox = ensure_dir_exists(self.cachepath.joinpath("outbox"))
        self.sent = ensure_dir_exists(self.cachepath.joinpath("sent"))

    def wizard(self):
        config_promt = {"title": ("Enter the event's title", lambda x: len(x) > 4),
            "date": ("Enter the event's date (use YYYY-MM-DD format)", lambda x: len(x) == 10)}



    @property
    def config(self):
        self._configpath =
        if not self._configpath.exists():
            config = {"events":
                      [{"name": "Evento",
                        "title": "Mi GRAN evento",
                        "date": "2019-10-10"}]}

            with open(self._configpath, "w") as fh:
                fh.write(yaml.safe_dump(self.config))
                error = ""


    @property
    def datapath(self):
        return self.paths["datapath"]()

    @property
    def outbox(self):
        return self.paths["outbox"]()

    @property
    def sentpath(self):
        return self.paths["sentpath"]()

jobs = Jobs()


def run(args):
    config = load_config()
    jobs = Jobs(config)
    if args.operation == "new":
        job = jobs.new(args.filename)
        if job:


