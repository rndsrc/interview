#!/usr/bin/env bokeh serve --show
#
# Run this app with `./demo.py [--args FILE]` or
#                   `bokeh serve --show demo.py [--args FILE]`
#
# where FILE is the file to be opened.

import sys
import numpy as np

import bokeh.layouts        as bl
import bokeh.models         as bm
import bokeh.models.widgets as bw
import bokeh.plotting       as bp

import interview.widget as iw

from eat.io import hops, util

#------------------------------------------------------------------------------
# Get a list of files from the arguments
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ["er1/hops-lo/5.+close/data/alist.v6"]

print('Inspecting file{} "{}"'.format('s' if len(files) > 1 else '', files))

#------------------------------------------------------------------------------
# Read an alist file; rename columns; add new columns
df = hops.read_alist(files[0])

df["r"]     = np.sqrt(df.u**2 + df.v**2)
df['site1'] = df.baseline.str[0]
df['site2'] = df.baseline.str[1]

df["color"] = ["red" if df.site1[i] == "A" or df.site2[i] == "A" else "green"
               for i in range(len(df))]
df.color[df.site1 == df.site2] = "blue"

util.add_path(df)

# Create empty Bokeh column data source with column names matching the
# pandas data frmae
print(df.columns)
src = bm.ColumnDataSource(data={k:[] for k in df.columns})

#------------------------------------------------------------------------------
# Create hover tool with some useful information; use it for a Bokeh
# figure; create a scatter plot
hover = bm.HoverTool(tooltips=[
    ("Baseline",     "@site1 @site2"),
    ("(u,v)",        "(@u, @v)"),
    ("Polarization", "@polarization"),
    ("Path",         "@path"),
])

#------------------------------------------------------------------------------
# Time series
fig = bp.figure(title="Time series",
                plot_height=360, plot_width=1024,
                x_axis_type='datetime',
                toolbar_location="above", tools=[hover,
                "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")
plt = fig.circle(x="datetime", y="resid_phas", color="color",
                 source=src, size=5)

# Layout widgets;
time_series = bl.column(fig)

#------------------------------------------------------------------------------
# Scatter plot
fig = bp.figure(title="Scatter plot",
                plot_height=720, plot_width=720,
                toolbar_location="above", tools=[hover,
                "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")
plt = fig.circle(x="datetime", y="resid_phas", color="color",
                 source=src, size=5)

# Map pandas column names to selection box options; create selection
# boxes for the x- and y-axes
opts = {
    "datetime"   : "Time",
    "r"          : "r",
    "u"          : "u",
    "v"          : "v",
    "amp"        : "Amplitude",
    "resid_phas" : "Phase",
    "snr"        : "Signal-to-Noise Ratio",
}
select_x = iw.Select(plt, 'x', opts)
select_y = iw.Select(plt, 'y', opts)

# Layout widgets;
inputs  = bl.widgetbox(select_x, select_y, sizing_mode="fixed")
scatter = bl.row(inputs, fig)

#------------------------------------------------------------------------------
# Global controls and layout

checkbutton_auto = bw.CheckboxButtonGroup(labels=["Autocorrelation"],
                                          active=[])

# List polarization and create a selection box for it; define a call
# back and connect it with the selection box
pols       = ["All"] + sorted(df.polarization.unique(), reverse=True)
select_pol = bw.Select(title="Polarization", options=pols, value=pols[0])

def update():
    pol  = select_pol.value
    auto = len(checkbutton_auto.active) > 0
    tmp  = df
    tmp  = tmp if auto         else tmp[tmp.site1 != tmp.site2]
    tmp  = tmp if pol == "All" else tmp[tmp.polarization == pol]
    src.data = src.from_df(tmp)

checkbutton_auto.on_change("active", lambda attr, old, new: update())
select_pol.on_change("value", lambda attr, old, new: update())
update() # update once to populate the bokeh column data source

# Add everything to the root
all = bl.column(bl.widgetbox(checkbutton_auto, select_pol),
                iw.Tabs({"Time Series":time_series,
                         "Scatter Plot":scatter}))

bp.curdoc().add_root(all)
bp.curdoc().title = "Demo"
