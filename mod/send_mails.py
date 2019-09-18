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

from mailjet_rest import Client
import base64
import yaml
import shutil
from . import config, MAILTEMPLATE, OUTBOX, SENTMAIL


def _load_mails():
    with MAILTEMPLATE.open() as fh:
        email_template = fh.read()
    for file in OUTBOX.iterdir():
        if file.suffix == ".yaml":
            with file.open("r", encoding="utf8") as fh:
                email_data = yaml.safe_load(fh)
                attach = [_load_attachment(f) for f in email_data["attach"]]
                k = email_template.format(**email_data)
                message = yaml.safe_load(k)
                message["Attachments"] = attach
                data = {"Messages": [message]}
                yield email_data, data


def _load_attachment(file_name):
    file_name = file_name.lower() + ".pdf"
    with open(OUTBOX.joinpath(file_name), "rb") as fh:  # open binary file in read mode
        file_64_encode = base64.standard_b64encode(fh.read())
    return {
        "ContentType": "application/pdf",
        "Filename": file_name,
        "Base64Content": file_64_encode.decode("ascii"),
    }


def _sendmail(data):
    keys = (config["keys"]["api_key"], config["keys"]["api_secret"])
    mailjet = Client(auth=keys, version="v3.1")
    result = mailjet.send.create(data=data)

    return result


def _move_to_outbox(filename, suffix):
    src = OUTBOX.joinpath(f"{filename}.{suffix}")
    dst = SENTMAIL.joinpath(f"{filename}.{suffix}")
    shutil.move(src=str(src), dst=str(dst))


def send_mails():
    """Send mails. If it"""
    n = 0
    max_mails = 0
    for email_data, data in _load_mails():
        result = _sendmail(data)
        if result.status_code == 200:  # its OK
            _move_to_outbox(email_data["filename"], "yaml")
            for filename in email_data["attach"]:
                _move_to_outbox(filename.lower(), "pdf")
            attemp = 0
            while True:
                result_path = SENTMAIL.joinpath(
                    "Rep%03d-" % attemp + email_data["filename"] + ".yaml"
                )
                if result_path.exists():
                    attemp += 1
                else:
                    break

            with result_path.open("w") as fh:
                fh.write(yaml.safe_dump(result.json()))

        n += 1
        if max_mails > 0 and n >= max_mails:
            break

    print("Total {} mails sent".format(n))
