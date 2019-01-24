import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import DataTable, TableColumn, ColumnDataSource
from bokeh.models.widgets import Button, Paragraph, RadioButtonGroup
from bokeh.events import DoubleTap

import utils
import callbacks

# variable definitions   
coordinates = []
current_level = [0]
current_model = [0]
tools = []
xlim = (-1,1)
ylim = (-1,1)
step = 0.01
tools = []
color_dict = {0: 'darkblue', 1: 'darkorange'}
colnames = ['x', 'y', 'level']
colnames_color = colnames + ['color']
columns = [TableColumn(field=s, title=s) for s in colnames]
source = ColumnDataSource(data=dict(x=[], y=[], level=[], color=[]))
surface = ColumnDataSource(data={k: [] for k in colnames_color})
# since callbacks must not return anything wrap ColumnDataSource objects
# so they can be altered by callbacks that do not use the global variables
wrapped_source = utils.BokehObjectWrapper(source)
wrapped_surface = utils.BokehObjectWrapper(surface)
table = DataTable(source=wrapped_source.obj, columns=columns, editable=True, height=200)

# classifier definitions
classifiers = [LogisticRegression(solver='lbfgs'), GaussianNB(),
                LinearSVC(C=1.0), RandomForestClassifier(n_estimators=100)]

# create figure
p = figure(title='Decision Surface (double tap to add data)', tools=tools,
            width=700, height=700, x_range=xlim, y_range=ylim)
p.background_fill_color = 'white'
p.xaxis.axis_label = 'X'
p.yaxis.axis_label = 'Y'
p.circle(source=wrapped_source.obj, x='x', y='y', color='color',
         alpha=1, legend=field('level'))
p.square(source=wrapped_surface.obj, x='x', y='y', color='color',
         alpha=.1, size=5.4, legend=field('level'))

# create buttons and add callbacks
# reset data
button_reset = Button(label='Reset', button_type='primary')
button_reset.on_click(lambda: callbacks.callback_button_reset(wrapped_source, coordinates, wrapped_surface))

# add data on double tap
p.on_event(DoubleTap, lambda event: callbacks.callback_add_dot_on_double_tap(event, current_level,
                                                                             color_dict, coordinates,
                                                                             wrapped_source, colnames_color))

# update model
button_update = Button(label='Train model', button_type='success')
button_update.on_click(lambda: callbacks.callback_button_update(wrapped_source, classifiers, current_model,
                                                        xlim, ylim, step, color_dict, wrapped_surface))

# choose class
button_class = RadioButtonGroup(labels=['Class 0', 'Class 1'], active=0)
button_class.on_click(lambda event: callbacks.callback_button_class(event, current_level))   

# choose classifier
button_model = RadioButtonGroup(labels=['Log. Reg.', 'Naive Bayes', 'SVC', 'RF'], active=0)
button_model.on_click(lambda event: callbacks.callback_button_select_model(event, current_model))   

# create document
curdoc().add_root(column(p, row(button_class, button_model), row(button_update,
                    button_reset), table))