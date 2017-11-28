#!/usr/bin/env python
#
# A minimal static HTML Bokeh demo.  Run this app with `./static.py`
# or `python static.py`---this will save and open a static HTML file
# "static.html".

import bokeh.models   as bm
import bokeh.plotting as bp

from eat.io import hops, util

#------------------------------------------------------------------------------
# TODO: load both HOPS and AIPS data into Pandas DataFrames
df = hops.read_alist("er1/hops-lo/5.+close/data/alist.v6")

# TODO: df['ampdiff'] = hops_amp - aips_amp
df['ampdiff'] = df['snr']

# Add other useful columns
util.add_path(df)

df['site1'] = df.baseline.str[0]
df['site2'] = df.baseline.str[1]

cmap = {'3C279' : "red",
        'OJ287' : "green",
        'others': "blue"}
df['color'] = df.apply(lambda r: cmap.get(r['source'], cmap['others']), axis=1)

# Create hover tool with some useful information
hover = bm.HoverTool(tooltips=[
    ("Baseline", "@site1 @site2"),
    ("(u,v)",    "(@u, @v)"),
    ("Path",     "@path"),
])

# only include useful columns to reduce html size
src = bm.ColumnDataSource(data=df[['amp', 'ampdiff', 'color',
                                   'site1', 'site2', 'u', 'v', 'path']])

#------------------------------------------------------------------------------
# Make scatter plot
fig = bp.figure(tools=[hover,"pan,box_zoom,reset"])
plt = fig.circle(x="amp", y="ampdiff", color="color", source=src)

#------------------------------------------------------------------------------
# Output and show static HTML
bp.output_file("static.html")
bp.show(fig)
