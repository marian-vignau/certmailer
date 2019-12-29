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

from .jobfolder import JobFolder


class Receiver():
    def __init__(self, email: str = None, values: dict = None):
        self.data = {
            "certificates": [],
            "send": "send",
            "attach": []
        }
        if email:
            self.data["email"] = email
        if values:
            self.data.update(values)

    def to_row(self, fieldnames: list):
        row = {k: self.data.get(k, "") for k in fieldnames}
        row["name"] = f'{self.data.get("first_name", "")} {self.data.get("last_name", "")}'
        for k in self.data["certificates"]:
            row[k] = "yes"
        return row

    def from_row(self, row):
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
        self.data["attach"].append(filename)

    def __bool__(self):
        return bool(self.data["send"])

    def __str__(self):
        return "--\n" + '\n'.join([f"{k}:{str(v)}" for k,v in self.data.items()])


class Receivers(JobFolder):
    """Persists in a csv the data collected from receivers"""
    def __init__(self, job):
        self.job = job
        self._filename = job.relative_path("receivers.csv")

    def read(self):
        """Reads every receiver"""
        with self._filename.open("r", encoding="utf8") as fh:
            reader = csv.DictReader(fh)
            self.header = reader.fieldnames
            for row in reader:
                yield Receiver().from_row(row)

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
        return self._filename.exists()

    @property
    def filename(self):
        return self._filename

    def __len__(self):
        if self.exists():
            return len(self.filename.open().readlines()) - 1
        else:
            return None

    def describe(self):
        if self.exists():
            with self._filename.open("r", encoding="utf8") as fh:
                reader = csv.reader(fh)
                header = next(reader)
                numbers = [0] * len(header)
                fn = lambda x: 1 if x.strip() else 0
                for cols in reader:
                    cant = map(fn, cols)
                    numbers = [sum(x) for x in zip(numbers, cant)]
            return zip(header, numbers)
        else:
            return False

    @property
    def mails_to_send(self):
        totals = self.describe()
        if totals:
            for k, v in totals:
                if "send" in k:
                    return v
        return 0
