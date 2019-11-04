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

import base64
import mimetypes
import shutil

from mailjet_rest import Client
import yaml
import click

from .jobs import jobs
from .utils import save_yml


def _load_mails(job):
    """Loads and send every email."""
    template_path = job.relative_path("emailtemplate.yaml")
    with template_path.open() as fh:
        email_template = fh.read()
    for file in job.outbox.iterdir():
        if file.suffix == ".yaml":
            with file.open("r", encoding="utf8") as fh:
                email_data = yaml.safe_load(fh)
                email_data.update(job.config)
                attach = [_load_attachment(job, f) for f in email_data["attach"]]
                k = email_template.format(**email_data)
                message = yaml.safe_load(k)
                default_attachs = message.get("Attachments", [])
                for attach in default_attachs:
                    filename = attach["Filename"][:-4]
                    email_data["attach"].append(filename)
                message["Attachments"] = attach

                data = {"Messages": [message]}
                yield email_data, data


def _load_attachment(job, file_name):
    file_name = file_name.lower() + ".pdf"
    with open(job.outbox.joinpath(file_name), "rb") as fh:  # open binary file in read mode
        file_64_encode = base64.standard_b64encode(fh.read())
    return {
        "ContentType": mimetypes.guess_type(file_name)[0],
        "Filename": file_name,
        "Base64Content": file_64_encode.decode("ascii"),
    }


def _sendmail(data):
    keys = (jobs.config["api_key"], jobs.config["secret_key"])
    mailjet = Client(auth=keys, version="v3.1")
    result = mailjet.send.create(data=data)

    return result


def _move_to_outbox(job, filename, suffix):
    src = job.outbox.joinpath(f"{filename}.{suffix}")
    dst = job.sent.joinpath(f"{filename}.{suffix}")
    shutil.move(src=str(src), dst=str(dst))


def send_mails(job, max_mails=0):
    """Send mails. If it"""
    n = 0
    n_mails = len([x for x in job.outbox.glob("*.yaml")])
    click.echo(f"Mails to send {n_mails}")

    prog = click.progressbar(length=n_mails)

    for email_data, data in _load_mails(job):
        prog.update(1)
        result = _sendmail(data)
        if result.status_code == 200:  # its OK
            #_move_to_outbox(email_data["filename"], "yaml")
            for filename in email_data["attach"]:
                pass
                #_move_to_outbox(filename.lower(), "pdf")
            attemp = 0
            while True:
                result_path = job.sent.joinpath(
                    "Rep%03d-" % attemp + email_data["filename"] + ".yaml"
                )
                if result_path.exists():
                    attemp += 1
                else:
                    break

            save_yml(result_path, result.json())

        n += 1
        if max_mails > 0 and n >= max_mails:
            break

    click.echo("Total {} mails sent".format(n))
