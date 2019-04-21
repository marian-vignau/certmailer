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

from pathlib import Path
import sys
import yaml


config = None


OUTBOX = Path("work/outbox")
CSVPATH = Path("work/cert_sheet.csv")
SENTMAIL = Path("work/sent")
CONFIGPATH = Path("work/config")
MAILTEMPLATE = CONFIGPATH.joinpath("email.yaml")
CERTTEMPLATE = CONFIGPATH.joinpath("certificate.svg")
DATAPATH = Path("work/data")

for x in [OUTBOX, SENTMAIL, CONFIGPATH, MAILTEMPLATE, CERTTEMPLATE, DATAPATH]:
    if not x.exists():
        print("Path {} is missing".format(str(x)))
        sys.exit(2)
try:
    with CONFIGPATH.joinpath("config.yaml").open("r", encoding="utf8") as fh:
        config = yaml.safe_load(fh)
except FileNotFoundError:
    print("You must init working directories")
    sys.exit(2)
