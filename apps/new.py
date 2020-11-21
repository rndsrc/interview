# run file as python new.py uv1a.csv locations.yaml
# python new.py csv_filename1 csv_filename2 ...... yaml_filename
# python new.py uv1a.csv locations.yaml
import sys
from bokeh.models.layouts import Panel, Row, Tabs

import interview.widget.select as Select

# python new.py
import pandas as pd
import numpy  as np
import bokeh.layouts        as bl
import bokeh.models         as bm
import bokeh.colors         as bc
import bokeh.models.widgets as bw
import bokeh.plotting       as bp
import datetime
import os
import interview.widget as iw
from eat.io import hops, util
from bokeh.io import output_file, show
import matplotlib.pyplot as plt
import bokeh.transform as bt
import yaml
import sys
import ehtim as eh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.io import curdoc
#TODO: 

# ALMA–APEX= AA,AP
# SMA–JCMT = JC,SM
# check yaml file for color to location mappings
# TODO: Load and visualize yaml files
# TODO: Learn diffmap library
# TODO: Implement Tabs
# TODO: Stream instead of static .
# Look at demo.py for examples
# TODO: 

#TODO: CONVERT INTO NON FUNCTIONAL PROGRAMMING

# checks system input
# TODO: Check file types in arguments?
# these are the column values


    



# TODO: Code logic for opening multiple csv files
# . Top panels: aggregate baseline coverage for EHT observations of M87,
#  combining observations on all four days. The left panel shows short-baseline
# coverage, comprised of ALMA interferometer baselines and intra-site EHT baselines (SMA–JCMT and ALMA–APEX). 
#SMA–JCMT and ALMA–APEX

def mirror_uv(df):
    """T1 <-> T2 => u, v -> -u, -v; amp  -> amp, phase -> -phase.
    Returns new array with the additive inverse of the phase, u, v
    and swapped T1 and T2 indexes
    """
    # deepcopy ensures anti-aliasing but check if necessary as it is in different scope.
    df2=df.copy()
    col_list=list(df2)
    # TODO: adjust for column name ( something like for elem in column if U in elem then....)

    col_list[1], col_list[2] = col_list[2], col_list[1]
    # TODO: integrate this with U V and phase
    # TODO: Use YAML file
    df2.columns=col_list
    df2["U(lambda)"]*=-1
    df2["V(lambda)"]*=-1
    df2["Iphase(d)"]*=-1
    return df2


# TODO: Learn iw.Select, bokeh tabs and making multiple plots at once

# TODO : Convert this into RGB values
# Eg: bc.HSL(f * i, 0.75, 0.5).to_rgb()
# TODO : Add hover capabilities
# https://www.kite.com/python/examples/2926/yaml-dump-a-dictionary-to-a-yaml-document

def display_all_uv(uv_fitscode, point_color,fig,fig2,df):
    """Reads the dataframe, filters it by the uv_fitscode values in
    both T1 and T2, mirrors it  by calling mirror_uv and plots both dataframes
    as glyphs
        uv_fitscode: two lettered string like AA, AZ, AP
        point_color: color of the glyph
    """
    rev_df=mirror_uv(df)
    aloc=first_loc.append(rev_loc)
    src1= bm.ColumnDataSource(aloc)
    return src1
    src1= bm.ColumnDataSource(aloc)
    # flipping x axis to decreasing order
    
    fig.circle(x=x1, y=y1, color=point_color,
                    source=aloc, size=6)

    fig2.circle(x=x2,y= y2,\
        color=point_color,source=aloc, size=6)

# Given n csv files grouped m times each
# Create n/m plots
# display them horizontally
# Reduce time inefficiency via streaming
#TODO: Use bokeh tabs to see if you can do that


# cols = ["6","7","10","12"]

# global_cb  = bw.CheckboxButtonGroup(labels=cols)

csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy),sqrtu2v2""".split(',')]

df = pd.concat( map (lambda file : pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).
unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma']))\
,sys.argv[1:-1]) )

df['r'] = np.sqrt(df.u**2 + df.v**2)
df.columns=csv_fields
with open(sys.argv[-1], 'r') as f:
    uvfitscode_color = yaml.load(f)
# auto load the csv headers into the hovertool
tool_tips_list=[]
for title in csv_fields:
    if "(" in title or ")" in title:
    # account for proper format brackets in titles
        tool_tips_list.append((title,"@"+"{"+title+"}"))
    else:
        tool_tips_list.append((title,"@"+title))
hover = bm.HoverTool(tooltips=tool_tips_list)
fig = bp.figure(title="u vs v graph",
    plot_height=800, plot_width=800
    ,x_axis_label="U(lambda)",y_axis_label= "V(lambda)",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
    output_backend="webgl")
fig2 = bp.figure(title="r vs Y",
    plot_height=800, plot_width=800
    ,x_axis_label="r",y_axis_label= "Y value",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
    output_backend="webgl")
    
fig3 = bp.figure(title="Time Series",
    plot_height=800, plot_width=800
    ,x_axis_label="Time(UTC)",y_axis_label= "Y value",
    toolbar_location="right", tools=[hover,
    "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
     output_backend="webgl")
fig3.sizing_mode = 'scale_both'
df=df.assign(colors="black")
for sites,color in uvfitscode_color.items():
    df.loc[((df["T1"] == sites[0]) | (df["T1"] == sites[1])) & ((df["T2"] == sites[0]) | (df["T2"] == sites[1])),"colors"]=color
    

df_final=pd.concat([df,mirror_uv(df)])
src1 = bm.ColumnDataSource(df_final)
fig.x_range.flipped= True
plt1=fig.circle(x="U(lambda)", y="V(lambda)", color="colors",
                    source=src1, size=6)
plt2=fig2.circle(x="sqrtu2v2",y="Iamp(Jy)" ,\
        color="colors",source=src1, size=6)
plt3=fig3.circle(x="time(UTC)",y="Iamp(Jy)" ,\
        color="colors",source=src1, size=6)
        
selected_circle = bm.Circle(fill_alpha=1, fill_color="firebrick")
plt1.selection_glyph=selected_circle

plt3.selection_glyph=selected_circle

plt2.selection_glyph=selected_circle


opts_all={
    "time(UTC)": "time",
    "T1": "Site 1",
    "T2": "Site 2",
    "U(lambda)": "u",
    "V(lambda)": "v",
    "Iamp(Jy)": "Amplitude",        
    "Iphase(d)"   : "Phase",
    "sqrtu2v2": "r"
}

select_x1  = iw.Select(plt1, 'x', opts_all)
select_y1  = iw.Select(plt1, 'y', opts_all)

inputs1  = bm.Column(select_x1, select_y1)
select_y2  = iw.Select(plt2, 'y', opts_all)
scatter = bl.row(inputs1, fig,select_y2,fig2)
select_x3  = iw.Select(plt3, 'x', opts_all)
select_y3  = iw.Select(plt3, 'y', opts_all)
inputs3  = bm.Column(select_x3, select_y3)
timeseries= bl.row(inputs3, fig3)
all = bl.column(iw.Tabs({"Visibility and domain":scatter,
                         "Time Series": timeseries},
                        width=1024))

bp.curdoc().add_root(all)
bp.curdoc().title = "Demo 2"


bm.Glyph()