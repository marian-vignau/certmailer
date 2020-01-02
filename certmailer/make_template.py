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

import yaml

from .utils import load_yml, load_attachment


class Template:
    """Creates the email template data structure from
    job's files."""

    def __init__(self, job):
        """Initializa data structure."""
        self.job = job
        config = load_yml(job.relative_path("config.yml"))
        self.data = {
            "From": {"Email": config["sender_email"], "Name": config["sender_name"]},
            "To": [{"Email": "{email}", "Name": "{name}"}],
            "Subject": config["subject"],
            "TextPart": self._load("textpart.txt"),
            "HTMLPart": self._load("htmlpart.html"),
            "Attachments": [],
        }
        self.missed, self.added = self._add_inlines()
        self.attached = self._default_attachments(job.attach.path)

    def _new_inline(self, attach_path, file_stem):
        """Append inline attachments to email html"""
        newinline = []
        for file in attach_path.glob(file_stem + ".*"):
            newinline.append(load_attachment(file, add_cid=True))
        return newinline

    def format(self, replace_info):
        """Replace fields with correspondent email receiver data."""
        temp = yaml.safe_dump(self.data)
        data = self.job.config.copy()
        data.update(replace_info)
        temp = temp.format(**data)
        return yaml.safe_load(temp)

    def _default_attachments(self, attach_path):
        """Append default attachments to email html."""
        self.data["Attachments"] = []
        attached = []
        for file in attach_path.iterdir():
            if not file.stem in self.added:
                newattach = load_attachment(file)
                self.data["Attachments"].append(newattach)
                attached.append(file.name)
        return attached

    def _add_inlines(self):
        """Check if every inline referenced is attached."""
        html = self.data["HTMLPart"]
        pattern = "src=['\"]cid:(.+)['\"]"
        self.data["InlinedAttachments"] = []
        missed = []
        added = []
        for match in re.finditer(pattern, html):
            inline = self._new_inline(self.job.attach.path, match.group(1))
            if inline:
                added.append(match.group(1))
                self.data["InlinedAttachments"].extend(inline)
            else:
                self.missed.append(match.group(1))

        return missed, added

    def _load(self, filename):
        """Loads a text file located in job's data folder."""
        with self.job.relative_path(filename).open(encoding="utf8") as fh:
            return fh.read()
