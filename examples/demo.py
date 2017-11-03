#!/usr/bin/env bokeh serve --show
#
# Run this app with `./demo.py [--args FILE]` or
#                   `bokeh serve --show demo.py [--args FILE]`
#
# where FILE is the file to be opened.

import sys

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ["er1/hops-lo/5.+close/data/alist.v6"]

print('Inspecting file{} "{}"'.format('s' if len(files) > 1 else '', files))
