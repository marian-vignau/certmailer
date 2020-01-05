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

import yaml
from mailjet_rest import Client

from .gen_pdf import GenPDF
from .jobs import jobs
from .utils import load_attachment, reuse_filename


class GenMail:
    """Generates all the PDF and Emails"""

    def __init__(self, job, template):
        """Create and sends mails"""
        self.job = job
        self.template = template
        svg_certificate = self.job.relative_path("certificate.svg")
        self.genpdf = GenPDF(svg_certificate)
        self.mailjet = Client(auth=jobs.key_pair, version="v3.1")
        self.total_mails = 0
        self.total_certificates = 0
        self.unsended_mails = 0
        self.log = job.sent.joinpath("log.log")
        reuse_filename(self.log)

    @classmethod
    def get_filename(cls, email, certificate=""):
        """Creates a filename for certificate"""
        filename = email.replace("@", "_").replace(".", "-")
        if certificate:
            filename += "-" + certificate + ".pdf"
        return filename.lower()

    def process(self, receiver):
        """Creates PDF certificates, and
        prepares email replacing variables in templates"""
        data = receiver.data
        message = self.template.format(data)
        for certificate in data["certificates"]:
            data["category"] = certificate
            filename = self.get_filename(data["email"], certificate)
            filepath = self.job.outbox.joinpath(filename)
            self.genpdf.process(str(filepath)[:-4], data)
            message["Attachments"].append(load_attachment(filepath))
        return message

    def sendmail(self, receiver):
        """Calls the api to actually send the mails"""
        msg = self.process(receiver)
        data = {"Messages": [msg]}
        result = self.mailjet.send.create(data=data)
        receiver.result = result.json()
        receiver.data["status_code"] = result.status_code
        receiver.data["msg"] = msg
        return result

    def clean_n_log(self, receiver):
        """Clear information and writes the log."""
        data = receiver.data
        if receiver.data["status_code"] == 200:
            filename = self.get_filename(data["email"])
            glob = self.job.outbox.glob(f"{filename}-*.pdf")
            for src in glob:
                src.unlink()
                self.total_certificates += 1
            self.total_mails += 1
            del receiver.data["msg"]  # don't save debug data it it's ok
        else:
            self.unsended_mails += 1
        sep = "-" * 40 + "\n"
        with self.log.open("a", encoding="utf8") as fh:
            fh.write(yaml.safe_dump(receiver.data))
            fh.write(yaml.safe_dump(receiver.result))
            fh.write(sep)
