#!/usr/bin/env python3

import sys
import json

"""
Print all combined courses, aka those that are taught under multiple names
"""

if len(sys.argv) < 2:
    print("File not specified to open", file=sys.stderr)
filename = sys.argv[1]
with open(filename) as json_file:
    classes = json.load(json_file)

courses = {}
for k,v in classes.items():
    room = v['meeting']['room']
    if "Combined" in room:
        course_title = k.split("   ")[1]
        course_number = k.split("   ")[0]
        if course_title in courses:
            courses[course_title].append(course_number)
        else:
            courses[course_title] = [course_number]

num_spaces = 35
for k,v in courses.items():
    print('{}{}{}'.format(k, " "*(num_spaces-len(k)), ', '.join(v)))