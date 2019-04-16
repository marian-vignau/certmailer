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
from pathlib import Path
import yaml
from . import create_list
from . import config, CSVPATH


certificates = [act["description"] for act in config["categories"].values()]
events = config["events"]


def make_header():
    header = ["name", "email", "send"]
    header.extend(certificates * len(events))
    yield header
    header = ["", "", "mail?"]
    for event in events:
        header += [event["name"]] * len(certificates)

    yield header


def process_list(sendmail):
    do = create_list.MyList()
    for email, value in do.list.items():
        name = value.get("first_name", "") + " "
        name += value.get("last_name", "")
        line = [name, email, sendmail]
        for event in events:
            for certificate in certificates:
                if (event["name"], certificate) in value["certificates"]:
                    line.append("yes")
                    # line.append(event["name"] + " " + certificate)
                else:
                    line.append("")
        yield line


def make_csv():
    if CSVPATH.exists():
        print("Files exists")
        sys.exit(1)
    else:
        row = 0
        with CSVPATH.open("w", encoding="utf8") as fh:
            for x in make_header():
                fh.write(", ".join(x) + "\n")
            for row, x in enumerate(process_list("send")):
                fh.write(", ".join(x) + "\n")
        print("Created {}. Total {} rows".format(str(CSVPATH), row))
        print("Open to choose mails to send and certificates to generate")




