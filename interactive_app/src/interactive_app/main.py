#!/usr/bin/env python

from collections import namedtuple

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import DataTable, TableColumn, ColumnDataSource
from bokeh.models.widgets import Button, RadioButtonGroup
from bokeh.events import DoubleTap

from interactive_app import callbacks

# variable definitions
State = namedtuple('State', ['current_level', 'current_model', 'xlim', 'ylim', 'step', 'color_dict'])
state = State(current_level=[0], current_model=[0], xlim=(-1,1), ylim=(-1,1), step=0.01,
              color_dict={0: 'darkblue', 1: 'darkorange'})
column_names = ['x', 'y', 'level']
columns = [TableColumn(field=s, title=s) for s in column_names]
source = ColumnDataSource(data={k: [] for k in column_names + ['color']})
surface = ColumnDataSource(data={k: [] for k in column_names + ['color']})
table = DataTable(source=source, columns=columns, editable=True, height=200)

# classifier definitions
classifiers = [LogisticRegression(solver='lbfgs'), GaussianNB(), LinearSVC(C=1.0),
               RandomForestClassifier(n_estimators=100)]

# create figure
p = figure(title='Decision Surface (double tap to add data)', tools=[], width=700, height=700, x_range=state.xlim,
           y_range=state.ylim)
p.background_fill_color = 'white'
p.xaxis.axis_label = 'X'
p.yaxis.axis_label = 'Y'
p.circle(source=source, x='x', y='y', color='color', alpha=1, legend=field('level'))
p.square(source=surface, x='x', y='y', color='color', alpha=.1, size=5.4, legend=field('level'))

# create buttons and add callbacks
# reset data
button_reset = Button(label='Reset', button_type='primary')
button_reset.on_click(lambda: callbacks.callback_button_reset(source, surface))

# add data on double tap
p.on_event(DoubleTap, lambda event: callbacks.callback_add_dot_on_double_tap(event, state,
                                                                             source))

# update model
button_update = Button(label='Train model', button_type='success')
button_update.on_click(lambda: callbacks.callback_button_update(source, classifiers, state, surface))

# choose class
button_class = RadioButtonGroup(labels=['Class 0', 'Class 1'], active=0)
button_class.on_click(lambda event: callbacks.callback_button_class(event, state))

# choose classifier
button_model = RadioButtonGroup(labels=['Log. Reg.', 'Naive Bayes', 'SVC', 'RF'], active=0)
button_model.on_click(lambda event: callbacks.callback_button_select_model(event, state))

# create document
curdoc().add_root(column(p, row(button_class, button_model), row(button_update, button_reset), table))
