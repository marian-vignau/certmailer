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


class Dir(object):
    def __init__(self, name, content=None, root="."):
        self.name = name
        self.content = content
        self.root = Path(root)
        self.parent = True
        if content:
            for item in self.content:
                item.parent = self
                item.root = False

    def __call__(self, *args, **kwargs):
        if self.root:
            parent = self.root
        else:
            parent = self.parent()
        return parent.joinpath(self.name)

    def __bool__(self):
        if self.parent:
            if self().exists():
                return True
        return False

    def ensure(self):
        if not self:
            self().mkdir()
        if self.content:
            for item in self.content:
                item.ensure()


# struct.ensure()