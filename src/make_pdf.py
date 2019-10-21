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

import sys
import yaml
from . import config, OUTBOX, CERTTEMPLATE, CSVPATH

import certg


total_mails = 0
total_certificates = 0


def _add_to_jobs(receiver, certificates):
    """Generate PDF using the certificate template"""
    global total_certificates
    global total_mails
    receiver["attach"] = ["-" + x["filename"] for x in certificates]
    certg.process(
        str(CERTTEMPLATE), str(OUTBOX) + "/", "filename", certificates, images=[]
    )
    with OUTBOX.joinpath("{}.yaml".format(receiver["filename"])).open(
        "w", encoding="utf8"
    ) as fh:
        fh.write(yaml.safe_dump(receiver))
    total_certificates += len(certificates)
    total_mails += 1


def _gen_certificates(receiver, data, cert_types):
    """Generate certificate's PDF for one receiver"""
    certificates = []
    for idx, cert in enumerate(data):
        if cert.strip():  # if this field has something.
            certificate = cert_types[idx].copy()
            certificate.update(receiver)
            certificate["filename"] += certificate["suffix"]
            certificates.append(certificate)
    _add_to_jobs(receiver, certificates)


def _parse_header(header1, header2):
    """Parses header to find different certificates to generate"""
    e = config["events"]
    events = {}
    for item in e:
        events[item["name"]] = item["title"]

    send_column = header1.index("send")
    first_cert_col = send_column + 1
    cert_types = []
    for i, cat in enumerate(header1[first_cert_col:]):
        idx = first_cert_col + i
        evt = header2[idx]
        cert_types.append({
            "event": events[evt],
            "category": cat,
            "suffix": f"-{evt}-{cat}"
        })
    return cert_types, send_column, first_cert_col


def _read_csv(filepath):
    """Read file and generate certificate's PDFs."""
    with filepath.open("r", encoding="utf8") as fh:
        header1 = [x.strip() for x in fh.readline().split(",")]
        header2 = [x.strip() for x in fh.readline().split(",")]
        cert_types, send_column, first_cert_col = _parse_header(header1, header2)

        for line in fh.readlines():
            data = [x.strip() for x in line.split(",")]
            if data[send_column].strip():  # if column 'send' has something
                receiver = {
                    "name": data[0],
                    "email": data[1],
                    "filename": data[1].replace("@", "_").replace(".", "-"),
                }
                _gen_certificates(receiver, data[first_cert_col:], cert_types)


def make_pdf():
    """Generate certificate's PDFs."""
    if not CSVPATH.exists():
        print("File doesn't exists")
        sys.exit(1)
    else:
        rows = _read_csv(CSVPATH)
        print(
            "To send {} certificates in {} mails".format(
                total_certificates, total_mails
            )
        )
        print("Use sendmail option to send them")
