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
import bokeh.colors         as bc
import bokeh.models.widgets as bw
import bokeh.plotting       as bp

import interview.widget as iw

from eat.io import hops, util
from bokeh.models.widgets.buttons import ButtonClick

#------------------------------------------------------------------------------
# Get a list of files from the arguments
if len(sys.argv) > 1:
    files = sys.argv[1:]
else:
    files = ["alist.v6"]

print('Inspecting file{} "{}"'.format('s' if len(files) > 1 else '', files))

#------------------------------------------------------------------------------
# Read an alist file; rename columns; add new columns
df = hops.read_alist(files[0])



df["Custom"] = np.nan


df['r']     = np.sqrt(df.u**2 + df.v**2)
df['site1'] = df.baseline.str[0]
df['site2'] = df.baseline.str[1]
df['color'] = "black"
df.to_csv('acsv.csv')
util.add_path(df)
util.add_gmst(df)

# Create empty Bokeh column data source with column names matching the
# pandas data frmae
src = bm.ColumnDataSource(data={k:[] for k in df.columns})
print(src)

# Map pandas column names to selection box options;
opts_time = {
    "datetime"     : "Time",
    "gmst"         : "GMST",
}
opts_all =dict()
for header in df.columns:
    opts_all[header]=header

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

# Create selection boxes for the and y-axes
select_x = iw.Select(plt, 'x', opts_time)
select_y = iw.Select(plt, 'y', opts_all)

# Layout widgets;
inputs     = bm.Column(select_x, select_y, sizing_mode="scale_both")
timeseries = bl.column(fig, inputs)

#------------------------------------------------------------------------------
# Scatter plot
fig = bp.figure(title="Scatter plot",
                plot_height=720, plot_width=720,
                toolbar_location="above", tools=[hover,
                "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")
plt = fig.circle(x="datetime", y="resid_phas", color="color",
                 source=src, size=5)

# Create selection boxes for the x- and y-axes
select_x = iw.Select(plt, 'x', opts_all)
select_y = iw.Select(plt, 'y', opts_all)

# Layout widgets;
inputs  = bm.Column(select_x, select_y, sizing_mode="scale_both")
scatter = bl.row(inputs, fig)

#------------------------------------------------------------------------------
# Horizontal linked view
fig1 = bp.figure(plot_height=720, plot_width=360,
                 toolbar_location="above", tools=[hover,
                 "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 output_backend="webgl")
plt1 = fig1.circle(x="datetime", y="resid_phas", color="color",
                   source=src, size=5)

fig2 = bp.figure(plot_height=720, plot_width=360,
                 y_range=fig1.y_range,
                 toolbar_location="above", tools=[hover,
                 "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 y_axis_location=None,
                 output_backend="webgl")
plt2 = fig2.circle(x="datetime", y="resid_phas", color="color",
                   source=src, size=5)

# Create selection boxes for the x- and y-axes
select_x1  = iw.Select(plt1, 'x', opts_all)
select_x2  = iw.Select(plt2, 'x', opts_all)
select_y12 = iw.Select([plt1, plt2], 'y', opts_all)

# Layout widgets;
inputs  = bm.Column(select_x1, select_x2, select_y12, sizing_mode="scale_both")
hlinked = bl.row(inputs, bl.gridplot([[fig1, fig2]]))

#------------------------------------------------------------------------------
# Vertical linked view
fig1 = bp.figure(plot_height=360, plot_width=720,
                 toolbar_location="above", tools=[hover,
                 "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 x_axis_location=None,
                 output_backend="webgl")
plt1 = fig1.circle(x="datetime", y="resid_phas", color="color",
                   source=src, size=5)

fig2 = bp.figure(plot_height=360, plot_width=720,
                 x_range=fig1.x_range,
                 toolbar_location="above", tools=[hover,
                 "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 output_backend="webgl")
plt2 = fig2.circle(x="datetime", y="resid_phas", color="color",
                   source=src, size=5)

# Create selection boxes for the x- and y-axes
select_x12 = iw.Select([plt1, plt2], 'x', opts_all)
select_y1  = iw.Select(plt1, 'y', opts_all)
select_y2  = iw.Select(plt2, 'y', opts_all)

# Layout widgets;
inputs  = bm.Column(select_x12, select_y1, select_y2, sizing_mode="scale_both")
vlinked = bl.row(inputs, bl.gridplot([[fig1], [fig2]]))

#------------------------------------------------------------------------------
# Global controls and layout
#sites     = sorted(np.union1d(df.site1.unique(), df.site2.unique()))
pols       = sorted(df.polarization.unique(), reverse=True)
print(pols)
cols       = ["ALMA, others, auto", "Site1", "Site2"]
last       = [1,2,3,4]
global_cb  = bw.CheckboxButtonGroup(labels=["Auto-correlation"]+pols,
                                    active=last)
colored_by = bw.RadioButtonGroup(labels=cols,
                                 active=0)
index_list="datetime,version,root_id,two,extent_no,duration,length,offset,expt_no,scan_id,procdate,year,timetag,scan_offset,source,baseline,quality,freq_code,polarization,lags,amp,snr,resid_phas,phase_snr,datatype,sbdelay,mbdelay,ambiguity,delay_rate,ref_elev,rem_elev,ref_az,rem_az,u,v,esdesp,epoch,ref_freq,total_phas,total_rate,total_mbdelay,total_sbresid,srch_cotime,noloss_cotime,ra_hrs,dec_deg,resid_delay,Custom,r,site1,site2".split(",")
btn = bw.Button(label="Save as CSV", button_type="success")
btn.js_on_event(ButtonClick, bm.CustomJS(
    args=dict(source_data=src,index_list=index_list),
    code="""
        var inds = source_data.selected.indices;
        var data = source_data.data;
        var out = '';
        out+=index_list;
        out+=',color\\n';
        for (var i = 0; i < inds.length; i++) {
            var j;
                for (j = 0; j < index_list.length; j++) {
                    out+=data[index_list[j]][inds[i]]+',';
                }
            out+=data['color'][inds[i]]+'\\n';
        }
        var file = new Blob([out], {type: 'text/plain'});
        var elem = window.document.createElement('a');
        elem.href = window.URL.createObjectURL(file);
        elem.download = 'selected-data.csv';
        document.body.appendChild(elem);
        elem.click();
        document.body.removeChild(elem);
        """
        )
                         )
                        


def update():
    global last
    
    active = global_cb.active
    color  = colored_by.active

    if color == 0:
        df['color'] = ["red" if (df.site1[i] == 'A' or
                                 df.site2[i] == 'A') else "green"
                       for i in range(len(df))]
        df.color[df.site1 == df.site2] = "blue"
    elif color == 1:
        sites = sorted(df.site1.unique())
        f     = 256 / len(sites)
        for i, v in enumerate(sites):
            df.color[df.site1 == v] = bc.HSL(f * i, 0.75, 0.5).to_rgb()
    elif color == 2:
        sites = sorted(df.site2.unique())
        f     = 256 / len(sites)
        for i, v in enumerate(sites):
            df.color[df.site2 == v] = bc.HSL(f * i, 0.75, 0.5).to_rgb()

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
def my_text_input_handler(attr, old, new,df=df):
    myMessage = "you just entered: {0}".format(new)  # this changes the browser display
    try:
        df_2 = pd.eval("Custom={}".format(new), target=df)
        df_2 = df_2[df_2.u != 0]
        print(df_2["Custom"], "assign")
    # Example:pd.eval("D = ,df['U(lambda)']**2 + df['V(lambda)']**2 target=df_1)
        src.data["Custom"] = df_2["Custom"]

        return src

    except:
        print('error')

text_input = bw.TextInput(
    value="default", title="Enter a pd.eval compatible equation (with df as the dataframe): Ex: (df['u']**2 + df['v']**2)**0.5")
text_input.on_change("value", my_text_input_handler)


global_cb.on_change("active", lambda attr, old, new: update())
colored_by.on_change("active", lambda attr, old, new: update())
update() # update once to populate the bokeh column data source

# Add everything to the root


all = bl.column(bm.Column(global_cb, colored_by,btn,text_input),
                iw.Tabs({"Time Series":           timeseries,
                         "Scatter Plot":          scatter,
                         "Horizontal Linked View":hlinked,
                         "Vertical Linked View":  vlinked},
                        width=1024))


bp.curdoc().add_root(all)
bp.curdoc().title = "Demo"
# df1['U(lambda)']**2 + df1['V(lambda)']**2