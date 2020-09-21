# run file as python new.py uv1a.csv locations.yaml
# python new.py csv_filename1 csv_filename2 ...... yaml_filename
# python new.py uv1a.csv locations.yaml
import sys
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
import yaml
import sys

#TODO: 
# ALMA–APEX= AA,AP
# SMA–JCMT = JC,SM
# check yaml file for color to location mappings
# TODO: Load and visualize yaml files
# TODO: Learn diffmap library
# TODO: Implement Tabs
# TODO: Stream instead of static .
# Look at demo.py for examples
# TODO: Convert 
def main():
    # checks system input
    # TODO: Check file types in arguments?
    # these are the column values
    csv_fields= [a.strip() for a in """time(UTC),T1,T2,U(lambda),
    V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy)""".split(',')]
    #checking for multiple csv files. The last one is ignored as it is a yaml file
    df = pd.concat(\
        map(lambda file: pd.read_csv(file,names=csv_fields,skiprows=2),sys.argv[1:-1]))
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
    output_file('withhover.html')
    hover = bm.HoverTool(tooltips=tool_tips_list)
    title_of_plot=input("Enter title")
    fig = bp.figure(title=title_of_plot,
                plot_height=800, plot_width=800
                ,x_axis_label="U(lambda)",y_axis_label= "V(lambda)",
                toolbar_location="right", tools=[hover,
                "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")

    for uv_fitscode, color in uvfitscode_color.items():
        display_all_uv(uv_fitscode, color, fig, df)
    show(fig)
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
    # deepcopy ensures anti-aliasing but check if necessary
    df2=df.copy(deep=True)
    col_list=list(df)
    # TODO: adjust for column name ( something like for elem in column if U in elem then....)

    col_list[1], col_list[2] = col_list[2], col_list[1]
    df2.columns=col_list
    df2["U(lambda)"]=-1*df2["U(lambda)"]
    df2["V(lambda)"]=-1*df2["V(lambda)"]
    df2["Iphase(d)"]=-1*df2["Iphase(d)"]
    return df2


# TODO: Learn iw.Select, bokeh tabs and making multiple plots at once

# TODO : Convert this into RGB values
# Eg: bc.HSL(f * i, 0.75, 0.5).to_rgb()
# TODO : Add hover capabilities
# https://www.kite.com/python/examples/2926/yaml-dump-a-dictionary-to-a-yaml-document

def display_all_uv(uv_fitscode, point_color,fig,df):
    """Reads the dataframe, filters it by the uv_fitscode values in
    both T1 and T2, mirrors it  by calling mirror_uv and plots both dataframes
    as glyphs

        uv_fitscode: two lettered string like AA, AZ, AP
        point_color: color of the glyph
    """
    # searching for a specific uvfitscode in T1 and T2 and appending it
    first_loc=df.loc[df['T1'] == uv_fitscode]
    second_loc=df.loc[df['T2'] == uv_fitscode]
    first_loc.append(second_loc, ignore_index=True)
    rev_loc=mirror_uv(first_loc)
    src1= bm.ColumnDataSource(first_loc)
    src2=bm.ColumnDataSource(rev_loc)
    # flipping x axis to decreasing order
    fig.x_range.flipped= True
    fig.circle(x="U(lambda)", y="V(lambda)", color=point_color,
                    source=src1, size=6)
    fig.circle(x="U(lambda)", y="V(lambda)", color=point_color,
                    source=src2, size=6)

if __name__ == "__main__":
    main()


# Given n csv files grouped m times each
# Create n/m plots
# display them horizontally
# Reduce time inefficiency via streaming
