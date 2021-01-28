import os
import subprocess
run_str="bokeh serve --show new.py"
subprocess.call("python colorpicker.py",shell=True)

subprocess.call("bokeh serve --show new.py",shell=True)
# bokeh serve --show new.py or python demo2.py ( both run bokeh servers)
#
from bokeh.models.layouts import Panel, Row, Tabs
from bokeh.models.widgets.buttons import Button
import bokeh.models.widgets as bw
import os
import pandas as pd
import numpy as np
import bokeh.layouts as bl
import bokeh.models as bm
import bokeh.plotting as bp
import os
import yaml
import ehtim as eh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bokeh.plotting as bp
import bokeh.models.widgets as bw
import bokeh.models.layouts as bml
from bokeh.models import TextInput, Paragraph
from bokeh.plotting import curdoc
from bokeh.layouts import layout
import bokeh.layouts
from datetime import datetime

import subprocess
csv_dir_name = 'session_{}'.format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f"))

subprocess.call("mkdir {}".format(csv_dir_name),shell=True)


def mirror_uv(df):
    """T1 <-> T2 => u, v -> -u, -v; amp  -> amp, phase -> -phase.
    Returns new array with the additive inverse of the phase, u, v
    and swapped T1 and T2 indexes
    """
    # deepcopy ensures anti-aliasing but check if necessary as it is in different scope.
    df2 = df.copy()
    col_list = list(df2)
    # TODO: adjust for column name ( something like for elem in column if U in elem then....)

    col_list[1], col_list[2] = col_list[2], col_list[1]
    # TODO: integrate this with U V and phase
    # TODO: Use YAML file
    df2.columns = col_list
    df2["U(lambda)"] *= -1
    df2["V(lambda)"] *= -1
    df2["Iphase(d)"] *= -1
    return df2


csv_fields = [a.strip() for a in """time(UTC),T1,T2,U(lambda),
V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy),sqrtu2v2""".split(',')]
file_list = []
for root, dirs, files in os.walk('./uvfitsfiles'):
    for file in files:
        if file.endswith('.uvfits'):
            file_list.append(os.path.join(root, file))


# define interaction
def print_datapoints():
    indices = src1.selected.indices
    print(indices)
    
    results = df_final.iloc[indices, :-1]
    csv_fields.append("Custom")
    export_name="./{}".format(csv_dir_name)+"/{}".format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f"))
    print(export_name)
    try:
        results.to_csv(export_name, mode='w', header=False)
    except:
        print("Error")




# Moved select and Tabs here from .io to avoid import errors in DockerFile.
# eq_editor branch contains cleaner code that does not support dockerization
# and concurrent servers.


def Select(ps, a, opts, backend="python"):
    """Create a selector with callback for plots "ps" with glyph attribute "a"
    Args:
        ps:      a list of plots
        a:       glyph attribute
        opts:    a dictionary where the keys are data source columns and
            values are selector labels.
        backend: choose callback backend; the only supported backend is
            "python"
    Returns:
        An instance of Bokeh Select
    Examples:
        >>> import interview as iv
        >>> ...
        >>> plt = fig.circle(...)
        >>> sel = iv.widget.Select(plt, 'x', opts)
    """

    if not isinstance(ps, list):
        ps = [ps]

    s = bw.Select(title=a.upper()+" Axis",
                  options=list(opts.values()),
                  value=opts[getattr(ps[0].glyph, a)])

    if backend == "python":
        def callback(attr, old, new):
            for p in ps:
                setattr(p.glyph, a,
                        list(opts.keys())[list(opts.values()).index(new)])
        s.on_change("value", callback)
    else:
        raise ValueError('the only supported backend is "python"')

    return s


def Tabs(obj, **kwargs):
    """Convert a nested (ordered) dictionary to a Bokeh tabs widget
    Args:
        obj: a nested (ordered) dictionary where the keys are tab
            titles and the values are children of panels
    Returns:
        An instance of Bokeh Tabs
    Examples:
        >>> import bokeh.plotting as bp
        >>> import interview as iv
        >>> fig = bp.figure()
        >>> bp.show(iv.widget.Tabs({'title':fig}))
    """
    if isinstance(obj, bp.Figure) or isinstance(obj, bml.LayoutDOM):
        return obj
    elif isinstance(obj, dict):
        return bw.Tabs(tabs=[bw.Panel(child=Tabs(v, **kwargs), title=k)
                             for k, v in obj.items()], **kwargs)
    else:
        raise ValueError("Input must be a dictionary or a Bokeh figure")


# Loading the dataframe
df = pd.concat(map(lambda file: pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).
                                             unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma'])), file_list))
# defining r
df['r'] = np.sqrt(df.u**2 + df.v**2)

# setting fields.
df.columns = csv_fields
with open('./yaml_files/locations.yaml', 'r') as f:
    uvfitscode_color = yaml.load(f)
# auto load the csv headers into the hovertool
tool_tips_list = []
for title in csv_fields:
    if "(" in title or ")" in title:
        # account for proper format brackets in titles
        tool_tips_list.append((title, "@"+"{"+title+"}"))
    else:
        tool_tips_list.append((title, "@"+title))

tool_tips_list.append(("Custom", "@D"))

hover = bm.HoverTool(tooltips=tool_tips_list)

fig = bp.figure(title="u vs v graph",
                plot_height=800, plot_width=800, x_axis_label="U(lambda)", y_axis_label="V(lambda)",
                toolbar_location="right", tools=[hover,
                                                 "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                output_backend="webgl")
fig2 = bp.figure(title="r vs Y",
                 plot_height=800, plot_width=800, x_axis_label="r", y_axis_label="Y value",
                 toolbar_location="right", tools=[hover,
                                                  "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 output_backend="webgl", y_axis_type="log")

fig3 = bp.figure(title="Time Series",
                 plot_height=1600, plot_width=1600, x_axis_label="Time(UTC)", y_axis_label="Y value",
                 toolbar_location="right", tools=[hover,
                                                  "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                 output_backend="webgl")
fig3.sizing_mode = 'scale_both'
# color assignment. new2.py supports new stations.
df = df.assign(colors="black")
for sites, color in uvfitscode_color.items():
    df.loc[((df["T1"] == sites[0]) |
            (df["T1"] == sites[1])) & ((df["T2"] == sites[0]) |
                                       (df["T2"] == sites[1])), "colors"] = color

df_final = pd.concat([df, mirror_uv(df)])
df_final["D"] = np.nan
src1 = bm.ColumnDataSource(df_final)
fig.x_range.flipped = True
plt1 = fig.circle(x="U(lambda)", y="V(lambda)", color="colors",
                  source=src1, size=6)
plt2 = fig2.circle(x="sqrtu2v2", y="Iamp(Jy)",
                   color="colors", source=src1, size=6)
plt3 = fig3.circle(x="time(UTC)", y="Iamp(Jy)",
                   color="colors", source=src1, size=6)

selected_circle = bm.Circle(fill_alpha=1, fill_color="firebrick")
plt1.selection_glyph = selected_circle

plt3.selection_glyph = selected_circle

plt2.selection_glyph = selected_circle

# options list
opts_all = {
    "time(UTC)": "time",
    "T1": "Site 1",
    "T2": "Site 2",
    "U(lambda)": "u",
    "V(lambda)": "v",
    "Iamp(Jy)": "Amplitude",
    "Iphase(d)": "Phase",
    "sqrtu2v2": "r",
    "D": "custom"
}


btn = Button(label='Write selected points as CSV', button_type='success')
btn.on_click(print_datapoints)
# Selection layouts.
select_x1 = Select(plt1, 'x', opts_all)
select_y1 = Select(plt1, 'y', opts_all)


session_description=Paragraph(text="""The CSV files will be stored in the {} directory
and be marked by a timestamp.
""".format(csv_dir_name))




inputs1 = bm.Column(session_description,btn, select_x1, select_y1)
select_y2 = Select(plt2, 'y', opts_all)
scatter = bl.row(inputs1, fig, select_y2, fig2)
select_x3 = Select(plt3, 'x', opts_all)
select_y3 = Select(plt3, 'y', opts_all)
inputs3 = bm.Column(session_description,btn, select_x3, select_y3)
timeseries = bl.row(inputs3, fig3,)

myMessage = 'Enter an equation'
text_output = Paragraph(text=myMessage, width=200, height=100)


figtemp = bp.figure(title="temp graph",
                    plot_height=800, plot_width=800, x_axis_label="D", y_axis_label="Phase",
                    toolbar_location="right", tools=[hover,
                                                     "pan,box_zoom,box_select,lasso_select,undo,redo,reset,save"],
                    output_backend="webgl")


figtemp.circle(x="D", y="Iamp(Jy)", color="colors",
                        source=src1, size=6)

# Equation editor


def my_text_input_handler(attr, old, new):
    myMessage = "you just entered: {0}".format(new)
    text_output.text = myMessage  # this changes the browser display
    df = df_final
    try:
        df = pd.eval("D={}".format(new), target=df)

        print(df["D"], "assign")
    # Example:pd.eval("D = ,df['U(lambda)']**2 + df['V(lambda)']**2 target=df_1)
        src1.data["D"] = df["D"]
        return src1
    except:
        print('error')




text_input = TextInput(
    value="default", title="Enter a pd.eval compatible equation (with df as the dataframe): Ex: (df['U(lambda)']**2 + df['V(lambda)']**2)**0.5")
text_input.on_change("value", my_text_input_handler)


layout = bokeh.layouts.column(text_input, text_output, figtemp)

# Tab layout
all = bl.column(Tabs({"Visibility and domain": scatter,
                      "Custom plot w/ Default axes": timeseries, "Equation editor": layout},
                     width=1024))
bp.curdoc().add_root(all)
bp.curdoc().title = "Demo 2"






def print_datapoints():
    indices = src.selected.indices
    results = df.iloc[indices, :-1]
    results.to_csv("temp.csv", mode='w', header=False)
