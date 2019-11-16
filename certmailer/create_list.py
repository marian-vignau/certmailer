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


"""
Create a csv list of candidates to do a certificate
"""


import yaml
from datetime import datetime
import unicodedata


class Stats(dict):
    def count(self, name):
        if not name in self.keys():
            self[name] = 1
        else:
            self[name] += 1

    def __str__(self):
        return '\n'.join([f"{k}: {v}" for k, v in self.items()])


class MyList(object):
    def __init__(self, job):
        """Parses data exported from EventoL"""
        self.stats = Stats()
        self.job = job
        self.search_file_names()
        self.list = {}
        self.speakers = {}
        for category in self.job.categories.values():
            if category["regtype"] == "person":
                self._process_file(category, self._append_list)
        category = self.job.categories["Speaker"]
        self._process_file(category, self._append_speakers)

    def search_file_names(self):
        """Find yaml exported from EventoL into data directory."""
        for file in self.job.data.path.iterdir():
            if file.suffix == ".yaml":
                for key, category in self.job.categories.items():
                    if isinstance(category["fileprefix"], str) and \
                            file.name.startswith(category["fileprefix"]):
                        category["file"] = file


    def _process_file(self, category, function):
        """Process an exported yaml file """
        if "file" in category:
            self.stats.count("Readed data files ")
            with open(category["file"]) as fh:
                items = yaml.safe_load(fh.read())
                if not items:
                    return
                for item in items:
                    function(item, category)

    def _append_list(self, item, category):
        """Add every person in yaml in work directory to list"""
        registry = self._supress_event_user_prefix(item)
        email = self._add_person(registry)
        self._append_cert(email, registry, category["description"])

    def _add_person(self, user):
        """Creates a email's list.
        Each person is identified by it's email"""
        if not user["email"] in self.list:
            self.stats.count('total email receivers found ')
            user["certificates"] = []
            user["ascii_name"] = self.unaccented(
                user.get("first_name", ""), user.get("last_name", "")
            )
            self.list[user["email"]] = user
        return user["email"]

    def _append_cert(self, email, person, category):
        """Create cert on the corresponding year/month"""
        date_fields = ["registration_date", "date_joined", "created_at"]
        cert_date = False
        cert_event = None
        for date_field in date_fields:
            if date_field in person:
                try:
                    # founded the date that this person relates to the event
                    cert_date = datetime.strptime(person[date_field], "%Y-%m-%d %H:%M:%S")
                    break
                except Exception as e:
                    print(person[date_field])
                    print(e)
                break

        if cert_date:
            # if this person relates to the event in a date corresponding
            # the event's inscription period, it is considered to had participated of it

            if self.job.config["from_date"] <= cert_date <= self.job.config["to_date"]:
                cert_event = self.job.name
            else:
                self.stats.count('outdated incriptions type: ' + category)
                #print(f"{email} {self.job.name} {category} {cert_date:%Y-%m-%d}")

        if not cert_event is None:
            # add a certificate related to the event to this person certificates
            certificate = (cert_event, category)
            certificates_lists = self.list[email]["certificates"]
            if certificate and not certificate in certificates_lists:
                self.stats.count('certificated added type ' + category)
                certificates_lists.append(certificate)

    def _supress_event_user_prefix(self, item):
        """Extract the prefix event_user__user__ whenever it's necessary"""
        user = {}
        prefix = "event_user__user__"
        for key, value in item.items():
            if key.startswith(prefix):
                user[key[len(prefix):]] = value
            else:
                user[key] = value
        return user

    def _append_speakers(self, item, category):
        """"""
        for speaker in item["speakers_names"].split(","):
            search_name = self.unaccented(speaker)
            email = self._match_speakers(search_name)
            person = {
                "certificates": [],
                "last_name": speaker.strip(),
                "email": email,
                "registration_date": item["created_at"],
            }

            if email:
                self._append_cert(email, person, category["description"])
            else:
                self.stats.count("Speakers without known email")
            self.speakers[search_name] = person

    def _match_speakers(self, key):
        """Speakers don't put their emails,
        so I have to find the name in the list to
        use the mail informed there"""
        for email, item in self.list.items():
            name = item["ascii_name"].split()
            j = 0
            for word in key.split():
                if word in name:
                    j += 1
            if j > 1:
                return email
        return ""

    def unaccented(self, *parts):
        """Remove unicode chars, to match the same name's
        person even with (some) spelling errors"""
        s = " ".join(parts)
        s = s.lower()

        unaccented = "".join(
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        )
        return unaccented
