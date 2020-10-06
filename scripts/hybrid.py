#!/usr/bin/env python3

import sys
import json

"""
Print all hybrid instruction courses
"""

if len(sys.argv) < 2:
    print("File not specified to open", file=sys.stderr)
filename = sys.argv[1]
with open(filename) as json_file:
    classes = json.load(json_file)

options = ['', 'Remote Instruction'] # List of things that show up for remote lab
for k,v in classes.items():
    room = v['meeting']['room']
    if "Remote Instruction" in room:
        discussions = v['discussions']
        for d in discussions:
            room = d['room']
            if room not in options:
                print(k)
                break