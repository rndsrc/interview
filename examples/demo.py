#!/usr/bin/env bokeh serve --show
#
# Run this app with `./demo.py [--args FILE]` or
#                   `bokeh serve --show demo.py [--args FILE]`
#
# where FILE is the file to be opened.

import sys
import pandas as pd
import numpy  as np

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
util.add_gmst(df)

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
    "datetime"     : "Time",
    "gmst"         : "GMST",

    "r"            : "r",
    "u"            : "u",
    "v"            : "v",
    "ref_elev"     : "Reference (Site 1) Elevation",
    "rem_elev"     : "Remainder (Site 2) Elevation",
    "ref_az"       : "Reference (Site 1) Azimuth",
    "rem_az"       : "Remainder (Site 2) Azimuth",

    "amp"          : "Amplitude",
    "resid_phas"   : "Residual Phase",
    "total_phas"   : "Total Phase",
    "snr"          : "Signal-to-Noise Ratio",
    "quality"      : "Quality",

    "delay_rate"   : "Delay Rate",
    "total_rate"   : "Total Delay Rate",
    "sbdelay"      : "Single-Band Delay",
    "resid_delay"  : "Single-Band Residual Delay",
    "total_sbresid": "Total Single-Band Residual Delay",
    "mbdelay"      : "Multi-Band Delay",
    "total_mbdelay": "Total Multi-Band Delay",
    "ambiguity"    : "Ambiguity",

    # Unused columns:
    # "baseline", "datatype", "dec_deg", "duration", "epoch", "esdesp",
    # "expt_no", "extent_no", "freq_code", "lags", "length",
    # "noloss_cotime", "offset", "phase_snr", "polarization", "procdate",
    # "ra_hrs", "ref_freq", "root_id", "scan_id", "scan_offset", "site1",
    # "site2" "source", "srch_cotime", "timetag", "two", "version",
    # "year",
}
select_x = iw.Select(plt, 'x', opts)
select_y = iw.Select(plt, 'y', opts)

# Layout widgets;
inputs  = bl.widgetbox(select_x, select_y, sizing_mode="fixed")
scatter = bl.row(inputs, fig)

#------------------------------------------------------------------------------
# Global controls and layout

pols      = sorted(df.polarization.unique(), reverse=True)
last      = [1,2,3,4]
global_cb = bw.CheckboxButtonGroup(labels=["Auto-correlation"]+pols,
                                   active=last)
def update():
    global last
    active = global_cb.active

    if 0 in active:
        # include auto-correlation
        df1    = df
        active = active[1:]
    else:
        # no auto-correlation
        df1    = df[df.site1 != df.site2]

    if len(active) == 0:
        global_cb.active = global_cb.active + last
        active += last
    else:
        last = active

    df2 = pd.DataFrame()
    for i in active:
        pol = pols[i-1]
        df2 = df2.append(df1[df1.polarization == pol])

    src.data = src.from_df(df2)

global_cb.on_change("active", lambda attr, old, new: update())
update() # update once to populate the bokeh column data source

# Add everything to the root
all = bl.column(bl.widgetbox(global_cb),
                iw.Tabs({"Time Series":time_series,
                         "Scatter Plot":scatter}))

bp.curdoc().add_root(all)
bp.curdoc().title = "Demo"
