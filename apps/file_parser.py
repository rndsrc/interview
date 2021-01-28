# bokeh serve --show new.py or python demo2.py ( both run bokeh servers)
#
import pandas as pd
import ehtim as eh
import pandas as pd
import bokeh
from bokeh.models import Paragraph
from bokeh.io import curdoc
from bokeh.models.widgets import FileInput
from pybase64 import b64decode
import io
import subprocess
from datetime import datetime
from random import randint 

df=[]


csv_fields = [a.strip() for a in """time(UTC),T1,T2,U(lambda),
    V(lambda),Iamp(Jy),Iphase(d),Isigma(Jy)""".split(',')]
def process_uvfits_data(attr, old,new):
    file_list=process_generic_file(new)
    global df
    df = pd.concat(map(lambda file: pd.DataFrame(eh.obsdata.load_uvfits(file).\
        avg_coherent(inttime=300).unpack(['time_utc', 't1', 't2', 'u', 'v', 'amp', 'phase', 'sigma'])), file_list))
    generic_start_server()
        

def generic_start_server():
    csv_name="{}.csv".format(datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f"), header=csv_fields)
    df.to_csv(csv_name, index=False)
    print(df)
    subprocess.call("bokeh serve --show new.py --port {} --args {}".format(randint(1000,9999),csv_name), shell=True)

def process_generic_file(file_list):
    new_list=[]
    for file in file_list:
        f = io.BytesIO(b64decode(file))
        new_list.append(f)
    return new_list


def upload_regular_data(attr, old, new):
    file_list=process_generic_file(new)  
    global df
    df = pd.concat(\
        map(lambda file: pd.read_csv(file,names=csv_fields,skiprows=2),file_list))
    generic_start_server()



file_input = FileInput(accept=".csv,.json,.txt,.pdf,.xls,.uvfits,.v6", multiple=True)
file_input.on_change('value', upload_regular_data)
genericp=Paragraph(text="Use this button to choose csv files")

uvfits_input=FileInput(accept=".uvfits", multiple=True)
uvfits_input.on_change('value', process_uvfits_data)
uvfitsp=Paragraph(text="Use this button to choose uvfits files")


bokCol=bokeh.models.Column(uvfitsp,uvfits_input,genericp,file_input)



doc=curdoc()
doc.add_root(bokCol)