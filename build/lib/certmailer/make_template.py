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

# guide in https://dev.mailjet.com/guides/?python#send-with-attached-files

import re

import click
from .utils import load_yml, save_yml, load_attachment


def _new_inline(attach_path, file_stem):
    """Append inline attachments to email html"""
    newinline = []
    for file in attach_path.glob(file_stem + ".*"):
        newinline.append(load_attachment(file, add_id=True))
    return newinline


def _default_attachments(attach_path, data, used):
    """Append default attachments to email html"""
    data["Attachments"] = []
    attached = []
    for file in attach_path.iterdir():
        if not file.stem in used:
            newattach = load_attachment(file)
            data["Attachments"].append(newattach)
            attached.append(file.name)
    return attached


def _add_inlines(job, data):
    """Check if every inline referenced is attached."""
    html = data["HTMLPart"]
    pattern = "certmailer=['\"]cid:(.+)['\"]"
    missed = []
    data["InlinedAttachments"] = []
    added = []
    for match in re.finditer(pattern, html):
        inline = _new_inline(job.attach.path, match.group(1))
        if inline:
            added.append(match.group(1))
            data["InlinedAttachments"].extend(inline)
        else:
            missed.append(match.group(1))

    return missed, added


def load(job, filename):
    """Loads a text file in job's data folder"""
    with job.relative_path(filename).open(encoding="utf8") as fh:
        return fh.read()


def make_template(job):
    """Creates the email template that includes inline attachments"""
    config = load_yml(job.relative_path("config.yml"))
    data = {"From": {"Email": config["sender_email"],
                     "Name": config["sender_name"]},

            "To": [{"Email": "{email}",
                    "Name": "{name}"}],

            "Subject": config["subject"],

            "TextPart": load(job, "textpart.txt"),
            "HTMLPart": load(job, "htmlpart.html"),
            }

    missed, added = _add_inlines(job, data)
    if missed:
        click.echo("Error: Missing inline attachments referenced " + ', '.join(missed))
    else:
        attached = _default_attachments(job.attach.path, data, added)
        template_path = job.relative_path("emailtemplate.yaml")
        save_yml(template_path, data)
        click.echo(f"Created {template_path.name}")
        click.echo(f"added {len(added)} ({', '.join(added)}) inlined images")
        click.echo(f"added {len(attached)} ({', '.join(attached)}) fixed attachments")

