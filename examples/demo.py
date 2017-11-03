#!/usr/bin/env bokeh serve --show
#
# Run this app with `./demo.py [--args FILE]` or
#                   `bokeh serve --show demo.py [--args FILE]`
#
# where FILE is the file to be opened.

import sys
import numpy as np

from eat.io import hops, util

if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ["er1/hops-lo/5.+close/data/alist.v6"]

print('Inspecting file{} "{}"'.format('s' if len(files) > 1 else '', files))

# Read an alist file
df = hops.read_alist(files[0])
df.rename(columns={
    'polarization': "pol",
    'ref_freq'    : "freq",
    'resid_phas'  : "phase",
}, inplace=True)

df['site1'] = df.baseline.str[0]
df['site2'] = df.baseline.str[1]
util.add_path(df)

df["r"] = np.sqrt(df.u**2 + df.v**2)
