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
import zipfile


def unziptemplate():
    zip_ref = zipfile.ZipFile("init.zip", "r")
    zip_ref.extractall(".")
    zip_ref.close()


def exec_command(command):
    from mod import make_csv, make_pdf, send_mails

    commands = {
        "makecsv": make_csv.make_csv,
        "makepdf": make_pdf.make_pdf,
        "sendmails": send_mails.send_mails,
    }
    commands[command]()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must select some command")
        sys.exit(2)
    else:
        command = sys.argv[1].lower().strip()
        commands = ["init", "makecsv", "makepdf", "sendmails"]
        if not command in commands:
            print("You must provida a valid command")
            print("choose from: ", ",".join(commands))
        else:
            if command == "init":
                unziptemplate()
            else:
                exec_command(command)
