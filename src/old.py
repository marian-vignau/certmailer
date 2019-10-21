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

from .mktree import Dir
from pathlib import Path
from .manage_jobs import Jobs
import yaml
import sys


class Job(Dir):
    def __init__(self, name):
        self.name = name
        self.content = [Dir("attach"), Dir("data")]


struct = Dir("work", root="..",
             content=[Job("job"),
                      Dir("tmp", content=[Dir("outbox"), Dir("sent")])]
             )

config = None
WORKDIR = Path("work")
OUTBOX = WORKDIR.joinpath("tmp/outbox")
SENTMAIL = WORKDIR.joinpath("tmp/sent")
CURRENTJOB = WORKDIR.joinpath("job")

CSVPATH = CURRENTJOB.joinpath("cert_sheet.csv")
DATAPATH = CURRENTJOB.joinpath("data")
MAILTEMPLATE = CURRENTJOB.joinpath("email_template.yaml")
CONFIGPATH = CURRENTJOB
ATTACHPATH = CURRENTJOB.joinpath("attach")

MAILDATA = CONFIGPATH.joinpath("email.yaml")
CERTTEMPLATE = CONFIGPATH.joinpath("certificate.svg")


for x in [WORKDIR, CURRENTJOB,
          OUTBOX, SENTMAIL,
          CONFIGPATH, MAILDATA,
          CERTTEMPLATE, DATAPATH]:
    if not x.exists():
        print(f"Path {x} is missing")
        sys.exit(2)
try:
    with WORKDIR.joinpath("config.yaml").open("r", encoding="utf8") as fh:
        config = yaml.safe_load(fh)
    with CONFIGPATH.joinpath("config.yaml").open("r", encoding="utf8") as fh:
        config.update(yaml.safe_load(fh))
except FileNotFoundError:
    print("You must init working directories")
    sys.exit(2)
