#!/usr/bin/env python

#
# qtripp
# Copyright (C) 2017 Jan-Piet Mens <jp@mens.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#/

import os
import sys
import glob
import yaml
import datetime
import codecs
import json
from jinja2 import Environment, FileSystemLoader

TEMPLATE_ENV = Environment(
    autoescape=False,
    trim_blocks=True,
    loader=FileSystemLoader(".")
    )

def render_template(filename, context):
    return TEMPLATE_ENV.get_template(filename).render(context)


def loadf(filename):

    try:
        f = codecs.open(filename, 'r', 'utf-8')
        str = f.read()
        doc = yaml.load(str)
        f.close()

        if not doc:
            print "Can't load file %s" % filename

        return doc

    except KeyboardInterrupt:
        sys.exit(1)
    except:
        print >> sys.stderr, "*********** File == ", filename
        raise


if __name__ == '__main__':
    try:
        (otype, path) = sys.argv[1:]
    except:
        print "Usage: report-type filename"
        sys.exit(1)

    doc = loadf(path)
    # print json.dumps(doc, indent=4)

    devicelist = []

    for o in doc:
        if 'subtypes' in o:
            devicelist.append(o)
            continue

        if otype in o:
            data = {
                otype : o[otype],
            }
            # print data
            output = render_template('%s.j2' % otype, data)
            print output
            sys.exit(0)

    if len(devicelist):
        # print json.dumps(devicelist, indent=4)
        data = {
            'devices' : devicelist,
        }
        output = render_template('devices.j2', data)
        print output
        sys.exit(0)

