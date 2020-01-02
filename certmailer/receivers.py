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

import csv


class Receiver:
    """Represents an email receiver."""

    def __init__(self, email: str = None, values: dict = None):
        """Starts with default data"""
        self.data = {"certificates": [], "send": "send", "attach": []}
        if email:
            self.data["email"] = email
        if values:
            self.data.update(values)

    def to_row(self, fieldnames: list):
        """Extract data from internal structures and put in a csv's row."""
        row = {k: self.data.get(k, "") for k in fieldnames}
        row[
            "name"
        ] = f'{self.data.get("first_name", "")} {self.data.get("last_name", "")}'
        for k in self.data["certificates"]:
            if k in fieldnames:
                row[k] = "yes"
        return row

    def from_row(self, row):
        """Reads a csv's row and complete the receiver's data."""
        in_certificates = False
        for k, v in row.items():
            if "send" in k:
                in_certificates = True
                self.data["send"] = v
            elif not in_certificates:
                self.data[k] = v
            elif v.strip():
                self.data["certificates"].append(k)
        return self

    def add_generated(self, filename):
        """Add a newly generated attached file."""
        self.data["attach"].append(filename)

    def is_flag(self, flag=""):
        if not "send" in self.data:
            return True
        if not flag:
            return bool(self.data["send"].strip())
        else:
            return self.data["send"].strip() == flag.lower()

    def __str__(self):
        return "--\n" + "\n".join([f"{k:>20}:{str(v)}" for k, v in self.data.items()])


class Receivers:
    """Persists in a csv the data collected from receivers"""

    def __init__(self, job):
        self.job = job
        self._filename = job.relative_path("receivers.csv")

    def read(self, flag=""):
        """Reads every receiver, a create receiver object."""
        if not self.exists():
            return False
        else:
            with self._filename.open("r", encoding="utf8") as fh:
                reader = csv.DictReader(fh)
                self.header = reader.fieldnames
                for row in reader:
                    receiver = Receiver().from_row(row)
                    if receiver.is_flag(flag):
                        yield receiver

    def write(self, do):
        """Writes receivers collected. It may use eventoL exported files"""
        self.do = do
        self.header = ["name", "email", "send"]
        certificates = [act["description"] for act in self.job.categories.values()]
        self.header.extend(certificates)
        with self._filename.open("w", encoding="utf8") as fh:
            writer = csv.DictWriter(fh, fieldnames=self.header)
            writer.writeheader()
            for email, value in self.do.list.items():
                row = Receiver(email, value).to_row(self.header)
                writer.writerow(row)

    def exists(self):
        """If receivers' csv is created."""
        return self._filename.exists()

    @property
    def filename(self):
        """Name of receivers' csv file"""
        return self._filename

    def __len__(self):
        """How many rows there are in csv"""
        if self.exists():
            return len(self.filename.open().readlines()) - 1
        else:
            return None

    def describe(self):
        """Describe de csv, put every column and how many cell has values in it."""
        if self.exists():
            with self._filename.open("r", encoding="utf8") as fh:
                reader = csv.reader(fh)
                header = next(reader)
                numbers = [0] * len(header)
                fn = lambda x: 1 if x.strip() else 0
                self.send_flags = {}
                for cols in reader:
                    cant = map(fn, cols)
                    numbers = [sum(x) for x in zip(numbers, cant)]
            return zip(header, numbers)
        else:
            return False

    def send_flags(self):
        """Check how many mails will be sent, group by flag.
        TOTAL is a special flag, meaning the grand total."""
        flags_data = {}
        if not self.exists():
            flags_data["TOTAL"] = 0
        else:
            with self._filename.open("r", encoding="utf8") as fh:
                reader = csv.reader(fh)
                header = next(reader)

                # finds the col headed send
                send_col = list(map(lambda x: "send" in x.lower(), header))
                send_col = send_col.index(True)
                if not send_col:
                    flags_data["TOTAL"] = len(self)
                else:
                    for cols in reader:
                        flag = cols[send_col].lower().strip()
                        flags_data[flag] = flags_data.get(flag, 0) + 1
                    flags_data["TOTAL"] = sum([v for v in flags_data.values()])
        return flags_data

    def mails_to_send(self, flag="TOTAL"):
        """Calculates how many emails will be sent."""
        if not flag:
            flag = "TOTAL"
        return self.send_flags().get(flag, 0)
