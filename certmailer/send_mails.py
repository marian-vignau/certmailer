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

import shutil
import socket
import sys

from mailjet_rest import Client
import yaml
import click

from .jobs import jobs
from .utils import save_yml, load_attachment

REMOTE_SERVER = "www.google.com"


def _load_mails(job):
    """Loads and send every email."""
    template_path = job.relative_path("emailtemplate.yaml")

    with template_path.open() as fh:
        email_template = fh.read()
    for file in job.outbox.glob("*.yaml"):
        error = []
        with file.open("r", encoding="utf8") as fh:
            email_data = job.config.copy()
            email_data.update(yaml.safe_load(fh))
            k = email_template.format(**email_data)
            message = yaml.safe_load(k)
            if "Attachments" not in message:
                message["Attachments"] = []
            for f in email_data["attach"]:
                filename = job.outbox.joinpath(f + ".pdf")
                if filename.exists():
                    message["Attachments"].append(load_attachment(filename))
                else:
                    error.append(str(filename))
            for attach in message["Attachments"]:
                filename = attach["Filename"][:-4]
                email_data["attach"].append(filename)
            data = {"Messages": [message]}
            yield email_data, data, error


def _sendmail(data):
    """Calls the api to actually send the mails"""
    keys = (jobs.config["api_key"], jobs.config["secret_key"])
    mailjet = Client(auth=keys, version="v3.1")
    result = mailjet.send.create(data=data)

    return result


def _move_to_outbox(job, filename, suffix):
    """Moves to other folders sended information"""
    src = job.outbox.joinpath(f"{filename}.{suffix}")
    if src.exists():
        dst = job.sent.joinpath(f"{filename}.{suffix}")
        shutil.move(src=str(src), dst=str(dst))


def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except:
        pass
    return False

def send_mails(job):
    """Send mails."""
    if not is_connected(REMOTE_SERVER):
        click.echo("You need to be connected to Internet")
        sys.exit(1)
    n = 0
    n_mails = len([x for x in job.outbox.glob("*.yaml")])
    click.echo(f"Mails to send {n_mails}")

    prog = click.progressbar(length=n_mails)
    missing_files = []
    for email_data, data, error in _load_mails(job):
        missing_files += error
        prog.update(1)
        result = _sendmail(data)
        if result.status_code == 200:  # its OK
            _move_to_outbox(job, email_data["filename"], "yaml")
            for filename in email_data["attach"]:
                _move_to_outbox(job, filename, "pdf")
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

    click.echo(f"Total {n} mails sent")
    if missing_files:
        s = "\n -".join(missing_files)
        click.echo("Missing files:\n -" + s)
