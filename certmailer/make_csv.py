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
from . import create_list


def make_header(job):
    """Creates two first rows, that are used as headers"""
    certificates = [act["description"] for act in job.categories.values()]
    header = ["name", "email", "send"]
    header.extend(certificates)
    yield header
    header = ["", "", "mail?"]
    header += [job.name] * len(certificates)

    yield header


def process_list(sendmail, job):
    """Add a row in csv for every receiver,
    and mark every certificate that must be generated"""
    do = create_list.MyList(job)
    for email, value in do.list.items():
        name = value.get("first_name", "") + " "
        name += value.get("last_name", "")
        line = [name, email, sendmail]
        for category in job.categories.values():
            dupla = (job.name, category["description"])
            if dupla in value["certificates"]:
                line.append("yes")
            else:
                line.append("")
        yield line
    click.echo(do.stats)

def make_csv(job):
    """Creates the text file with the selected recipients
    and certificates to generate"""

    receivers = job.relative_path("receivers.csv")

    if receivers.exists():
        click.secho(f"Files exists in {receivers}", fg="red")

    row = 0
    with receivers.open("w", encoding="utf8") as fh:
        for x in make_header(job):
            fh.write(", ".join(x) + "\n")
        for row, x in enumerate(process_list("send", job)):
            fh.write(", ".join(x) + "\n")
    click.echo(f"Created {receivers}. Total {row} rows")

    click.echo("Open to choose mails to send and certificates to generate")
