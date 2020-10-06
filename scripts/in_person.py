#!/usr/bin/env python3

import sys
import json

"""
Print all in person courses
"""

if len(sys.argv) < 2:
    print("File not specified to open", file=sys.stderr)
filename = sys.argv[1]
with open(filename) as json_file:
    classes = json.load(json_file)

m = 0
num_spaces = 46
for k,v in classes.items():
    if len(k) > m:
        m = len(k)
    room = v['meeting']['room'].strip()
    options = ['Combined', 'Online', 'Remote Instruction', 'N/A', '']
    if room not in options:
        space = " " * (num_spaces - len(k))
        print("{}{}{}".format(k, space, room))