
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
from pathlib import Path
from datetime import datetime
import unicodedata
from . import config, DATAPATH

events = config["events"]


class MyList():
    def __init__(self):
        self.search_file_names()
        self.list = {}
        self.speakers = {}
        for category in config["categories"].values():
            if category["regtype"] == 'person':
                self._append_list(category)

        self._append_speakers(config["categories"]["Speaker"])

    def search_file_names(self):
        for file in DATAPATH.iterdir():
            if file.suffix == ".yaml":
                for key, category in config["categories"].items():
                    if file.name.startswith(category["fileprefix"]):
                        category["file"] = file

    def _append_list(self, category):
        with open(category["file"]) as fh:
            items = yaml.safe_load(fh.read())
            if not items:
                return
            for item in items:
                registry = self._supress_event_user_prefix(item)
                email = self._add_person(registry)
                self._append_cert(email, registry, category["description"])

    def _add_person(self, user):
        if not user["email"] in self.list:
            user["certificates"] = []
            user["ascii_name"] = self.unaccented(user.get("first_name", ""), user.get("last_name", ""))
            self.list[user["email"]] = user
        return user["email"]

    def _append_cert(self, email, person, category):
        """Just create cert on the corresponding year/month"""
        date_fields = ["registration_date", "date_joined", "created_at"]
        cert_date = False
        cert_event = None
        for key in date_fields:
            if key in person:
                try:
                    cert_date = datetime.strptime(person[key], "%Y-%m-%d %H:%M:%S")
                    break
                except Exception as e:
                    print(person[key])
                    print(e)
                break

        if cert_date:
            for event in events:
                if cert_date < datetime.strptime(event["date"], "%Y-%m-%d"):
                    cert_event = event["name"]
                    # print(email, event["name"], category, str(cert_date))
                    break

        if not cert_event is None:
            certificate = (cert_event, category)
            certificates_lists = self.list[email]["certificates"]
            if certificate and not certificate in certificates_lists:
                certificates_lists.append(certificate)

    def _supress_event_user_prefix(self, item):
        user = {}
        prefix = "event_user__user__"
        for key, value in item.items():
            if key.startswith(prefix):
                user[key[len(prefix):]] = value
            else:
                user[key] = value
        return user

    def _append_speakers(self, category):
        with open(category["file"]) as fh:
            items = yaml.safe_load(fh.read())
            if not items:
                return
            for item in items:
                for speaker in item["speakers_names"].split(","):
                    search_name = self.unaccented(speaker)
                    email = self._match_speakers(search_name)
                    person = {
                        "certificates": [],
                        "last_name": speaker.strip(),
                        "email": email,
                        "registration_date": item["created_at"]
                    }

                    if email:
                        self._append_cert(email, person, category["description"])
                    self.speakers[search_name] = person

    def _match_speakers(self, key):
        """ Speakers don't put their emails, so I have to"""
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
        """Remove unicode chars, to match the same name's person w/ spelling errors"""
        s = " ".join(parts)
        s = s.lower()

        unaccented = ''.join(c for c in unicodedata.normalize('NFD', s)
                             if unicodedata.category(c) != 'Mn')
        return unaccented






