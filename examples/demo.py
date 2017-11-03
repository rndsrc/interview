#!/usr/bin/env bokeh serve --show
#
# Run this app with `./demo.py [--args FILE]` or
#                   `bokeh serve --show demo.py [--args FILE]`
#
# where FILE is the file to be opened.

import sys
import numpy as np

import bokeh.models   as bm
import bokeh.plotting as bp

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

# Create empty Bokeh column data source with column names matching the
# pandas data frmae
src = bm.ColumnDataSource(data={k:[] for k in df.columns})

# Create hover tool with some useful information; use it for a Bokeh
# figure; create a scatter plot
hover = bm.HoverTool(tooltips=[
    ("Baseline",     "@site1 @site2"),
    ("(u,v)",        "(@u, @v)"),
    ("Polarization", "@pol"),
    ("Path",         "@path"),
])
fig = bp.figure(title="Scatter plot",
                plot_height=720, plot_width=720,
                toolbar_location="above", tools=[hover,
                "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")
plt = fig.circle(x="datetime", y="phase", source=src, size=5)

# Add everything to the root
bp.curdoc().add_root(fig)
bp.curdoc().title = "Demo"
