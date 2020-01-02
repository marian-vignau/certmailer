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

import base64
import mimetypes
import socket

import yaml

REMOTE_SERVER = "www.google.com"


def load_yml(filepath):
    """Loads yaml data."""
    data = {}
    if filepath.exists():
        with open(filepath, encoding="utf8") as fh:
            data = yaml.safe_load(fh.read())
    return data


def save_yml(filepath, new_data):
    """Updates and saves yaml data."""
    data = load_yml(filepath)
    data.update(new_data)
    with open(filepath, "w", encoding="utf8") as fh:
        fh.write(yaml.safe_dump(data))


def load_attachment(file, add_cid=False):
    """Creates a dict to describe a file attached."""
    # open binary file in read mode
    with file.open("rb") as fh:  # open binary file in read mode
        file_64_encode = base64.standard_b64encode(fh.read())
        attachment = {
            "ContentType": mimetypes.guess_type(str(file))[0],
            "Filename": file.name,
            "Base64Content": file_64_encode.decode("ascii"),
        }
        if add_cid:
            attachment["ContentID"] = file.stem
    return attachment


def is_connected():
    """Test if exists a working internet connection."""
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False


class Stats(dict):
    def count(self, name):
        self[name] = self.get(name, 0) + 1

    def __str__(self):
        return "\n".join([f"{h:>20}:{c}" for h, c in self.items()])


MAXCOLWIDTH = 30


class Table:
    """Auxiliar to print table using command line"""

    def __init__(self):
        self.lenghts = {}
        self.data = []

    def add(self, data):
        """Append a new row to the table and calculate needed column widths"""
        fn = lambda k: min(MAXCOLWIDTH, max([len(str(data[k])), self.lenghts.get(k, 0)]))
        lenghts = {k: fn(k) for k in data.keys()}
        self.lenghts.update(lenghts)
        self.data.append(data)

    def __str__(self):
        """Output the table"""
        fill = lambda s, n, c: (s + c * (n - len(s)))[:n]
        table = ["|".join([fill(k, v, "_") for k, v in self.lenghts.items()])]
        for row in self.data:
            s = "|".join([fill(str(row.get(k, "")), v, " ") for k, v in self.lenghts.items()])
            table.append(s)
        return '\n'.join(table)
