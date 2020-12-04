from bokeh.plotting import figure

from bokeh.io import curdoc

from bokeh.models import ColumnDataSource

from bokeh.models.widgets import Button

from bokeh.layouts import column

import numpy as np

def b_cb():

global i

for j in range(3): c.data[‘serie_’+str(i+j)]=[el+i+j for el in y]

i+=3

b = Button()

b.on_click(b_cb)

i,n = 0,50

x,y = list(range(n)),[-2,2,1,0,-3]*10

p, dico = figure(), {‘serie_’+str(k):[np.nan]*n for k in range(n)}

dico[‘x’]=x; c = ColumnDataSource(dico)

for k in range(n): p.line(x=‘x’,y=‘serie_’+str(k), source=c)

curdoc().add_root(column(b,p))