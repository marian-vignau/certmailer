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

import argparse
from datetime import datetime

def validate_key(arg:str) -> (str, str):
    return True, str

def validate_date(arg:str) -> (datetime, str):
    return None,


operations = {
        "config": ("Init or edit the configuration.\nIncludes private/public key from mailjet",
                   ("api_key", validate_key),
                   ("secret_key", validate_key)),
        "job": {
            "help": "Manage jobs",
            "new": ("Creates a new job",
                    ("name", validate_new_job_name),
                    ("date", validate_date),
                    ("title", validate_title)),
            "list": "List existing jobs",
            "remove": ("Remove a job from list",
                       ("name", validate_job_name)),
            "use": ("Change the current job."
        },
        "edit": {
            "help": "Edit job components",
            "certificate": "Edits the certificate using Inkscape",
            "job": "Edit job configuration",
            "email": "Edits the email template",
            "recipients": "Edits the email recipients"
        },
        "attach": {
            "help": "Manage attachments",
            "add": "Add a fixed attach",
            "remove": "Remove an attach from the list",
            "list": "List attachs added to the email"
        },
        "inline": {
            "help": "Manage inline images",
            "add": "Add an inline image",
            "remove": "Remove an inline image",
            "list": "Lists inline images",
        },
        "data": {
            "help": "Manage data sources",
            "add": "Add a data source",
            "remove": "Remove a data source",
            "list": "Lists data sources",
        },
        "do": {
            "help": "Do any needed operations",
            "list": "Creates one recipients lists",
            "template": "Parses and creates and email template",
            "certificates": "Do all certificates using data",
            "mails": "Send all the mails"
        },
        "run": "Do all needed steps to sendmail, after proper configuration.",
    }


def init_parser():
    """Creates the arguments parser."""
    parser = argparse.ArgumentParser(prog='certmail')
    subparsers = parser.add_subparsers(help='Command purpose', dest="command")
    subparsers.required = True

    for key, value in operations.items():
        if not isinstance(value, dict):
            subparsers.add_parser(key, help=value)
        else:
            subparser = subparsers.add_parser(key, help=value["help"])
            sp2 = subparser.add_subparsers(dest="operation", help=f"Posible {key} operations")
            sp2.required = True
            for operation, help in value.items():
                if operation != "help":
                    parser3 = sp2.add_parser(operation, help=help)
                    if operation in ["new", "add", "remove", "use"]:
                        parser3.add_argument("filename", type=str)
    return parser


def run(args):
    """Runs command line."""
    parser = init_parser()
    pargs = parser.parse_args(args[1:])
    if pargs.command == "config":
        from . import config_init
        config_init.config_init()
    elif pargs.command == "job":
        from . import manage_jobs
        manage_jobs.run(pargs)
    print(pargs)
