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

from pathlib import Path
import os
import sys
import yaml
from . import config, OUTBOX, CERTTEMPLATE, CSVPATH
from pprint import pprint

#path_to_certg = "certg/certg"
#sys.path.append(path_to_certg)
import certg


e = config["events"]
events = {}
for item in e:
    events[item["name"]] = item["title"]

total_mails = 0
total_certificates = 0


def add_to_jobs(mail, certificates):
    global total_certificates
    global total_mails
    mail["attach"] = ["-" + x["filename"] for x in certificates]
    certg.process(
        str(CERTTEMPLATE), str(OUTBOX) + "/", "filename", certificates, images=[]
    )
    with OUTBOX.joinpath("{}.yaml".format(mail["filename"])).open(
        "w", encoding="utf8"
    ) as fh:
        fh.write(yaml.safe_dump(mail))
    total_certificates += len(certificates)
    total_mails += 1


def read_csv(filepath):
    with filepath.open("r", encoding="utf8") as fh:
        header1 = [x.strip() for x in fh.readline().split(",")]
        header2 = [x.strip() for x in fh.readline().split(",")]
        for line in fh.readlines():
            data = [x.strip() for x in line.split(",")]
            if data[2].strip():
                person = {
                    "name": data[0],
                    "email": data[1],
                    "filename": data[1].replace("@", "_").replace(".", "-"),
                }
                certificates = []

                for idx, cert in enumerate(data[3:]):
                    if cert.strip():
                        idx_header = idx + 3
                        certificate = {
                            "event": events[header2[idx_header]],
                            "category": header1[idx_header],
                        }
                        certificate.update(person)
                        certificate["filename"] += (
                            "-" + header2[idx_header] + header1[idx_header]
                        )
                        certificates.append(certificate)

                add_to_jobs(person, certificates)


def make_pdf():
    if not CSVPATH.exists():
        print("File doesn't exists")
        sys.exit(1)
    else:
        rows = read_csv(CSVPATH)
        print(
            "To send {} certificates in {} mails".format(
                total_certificates, total_mails
            )
        )
        print("Use sendmail option to send them")
