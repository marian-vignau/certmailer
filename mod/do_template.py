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

import yaml
import base64
from . import config, CONFIGPATH, MAILDATA, MAILTEMPLATE


def _inline_attachments():
    """Append inline attachments to email html"""
    attached = []
    for file in CONFIGPATH.iterdir():
        if file.suffix == ".png":
            with file.open("rb") as fh:  # open binary file in read mode
                file_64_encode = base64.standard_b64encode(fh.read())
            newinline = {
                "ContentType": "image/png",
                "Filename": file.name,
                "ContentID": file.stem,
                "Base64Content": file_64_encode.decode("ascii"),
            }
            attached.append(newinline)
    return attached

def _check_inlines(data):
    """Check if every inline referenced is attached."""
    import re
    html = data["HTMLPart"]
    pattern = "src='cid:(\w+)'"
    missed = []
    inlined = [item["ContentID"] for item in data["InlinedAttachments"]]
    for match in re.finditer(pattern, html):
        if not match.group(1) in inlined:
            missed.append(match.group(0))
    return missed


def do_template():
    """Creates the email template that includes inline attachments"""
    with open(MAILDATA) as fh:
        data = yaml.safe_load(fh.read())

    data["From"] = config["from"]

    data["InlinedAttachments"] = _inline_attachments()
    missed = _check_inlines(data)
    if missed:
        print("Error: Missing inline attachments referenced", ', '.join(missed))
    else:
        with open(MAILTEMPLATE, "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(data))

        print(f"Created {MAILTEMPLATE}")

