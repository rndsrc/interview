from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from pybase64 import b64decode
import pandas as pd
import io
import ehtim as eh

def upload_fit_data(attr, old, new):
    print(new)
    process_list(new)

def process_uvfits_data(attr, old,new):
    file_list=[]
    for file in new:
        f = io.BytesIO(b64decode(file)
        file_list.append(f)
    df = pd.concat(map(lambda file: pd.DataFrame(eh.obsdata.load_uvfits(file).avg_coherent(inttime=300).unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma'])), file_list))
    

def process_list(file_list):
    for file in file_list:
        decoded = b64decode(file)
        f = io.BytesIO(decoded)
        new_df = pd.read_csv(f)
        print(new_df)

file_input = FileInput(accept=".csv,.json,.txt,.pdf,.xls,.uvfits,.v6", multiple=True)
file_input.on_change('value', upload_fit_data)

uvfits_input=FileInput(accept=".uvfits", multiple=True)
uvfits_input.on_change('value', process_uvfits_data)

doc=curdoc()
doc.add_root(uvfits_input)