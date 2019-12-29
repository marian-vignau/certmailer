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
import shutil
from mailjet_rest import Client
from .gen_pdf import GenPDF
from .utils import load_attachment
from .jobs import jobs
import yaml


class GenMail():
    def __init__(self, job, template):
        self.job = job
        self.total_mails = 0
        self.total_certificates = 0
        self.template = template
        self.genpdf = GenPDF(self.job.relative_path("certificate.svg"))
        self.error = []
        keys = (jobs.config["api_key"], jobs.config["secret_key"])
        self.mailjet = Client(auth=keys, version="v3.1")

    @classmethod
    def get_filename(cls, email, certificate=""):
        filename = email.replace("@", "_").replace(".", "-")
        if certificate:
            filename += "-" + certificate + ".pdf"
        return filename.lower()

    def process(self, receiver):
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
        return result

    def move_to_sent(self, receiver):
        """Moves to other folders sended information"""
        data = receiver.data
        filename = self.get_filename(data["email"])
        glob = self.job.outbox.glob(f"{filename}-*.pdf")
        for src in glob:
            dst = self.job.sent.joinpath(f"{src.name}")
            shutil.move(src=str(src), dst=str(dst))
            self.total_certificates += 1
        self.total_mails += 1

