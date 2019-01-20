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
columns = [TableColumn(field=s) for s in colnames]
source = ColumnDataSource(data=dict(x=[], y=[], level=[], color=[]))
table = DataTable(source=source, columns=columns, editable=True, height=200)
surface = ColumnDataSource(data={k: [] for k in colnames_color})

# classifier definitions
classifiers = [LogisticRegression(solver='lbfgs'), GaussianNB(),
                LinearSVC(C=1.0), RandomForestClassifier(n_estimators=100)]

# create figure
p = figure(title='Decision Surface (double tap to add data)', tools=tools,
            width=700, height=700, x_range=xlim, y_range=ylim)
p.background_fill_color = 'white'
p.xaxis.axis_label = 'X'
p.yaxis.axis_label = 'Y'
p.circle(source=source, x='x', y='y', color='color', alpha=1, legend=field('level'))
p.square(source=surface, x='x', y='y', color='color', alpha=.1, size=5.4, legend=field('level'))

# callbacks
def callback_button_reset():
    """Callback for reset button."""
    source.data = {k: [] for k in list(source.data.keys())}
    coordinates.clear()
    surface.data = {k: [] for k in list(surface.data.keys())}

def callback_add_dot_on_double_tap(event):
    """Callback for adding dot on double tap."""
    coords = (event.x, event.y, current_level[0], color_dict[current_level[0]])
    coordinates.append(coords)
    source.data = {k: [co[i] for co in coordinates] for i, k in enumerate(colnames_color)}

def callback_button_update():
    """Callback for button to update the decision surface."""
    df = source.to_df()
    model = classifiers[current_model[0]]
    df = utils.create_decision_surface(model, df[['x', 'y']].values, df['level'].values,
                                        xlim, ylim, step)
    df.columns = ['x', 'y', 'level']
    df['color'] = [color_dict[i] for i in df['level'].values]
    surface.data = {c: s.tolist() for c, s in df.items()}

def callback_button_class(event):
    """Callback for button to choose the class."""
    current_level.pop()
    current_level.append(event)

def callback_button_select_model(event):
    """Callback for button to choose the class."""
    current_model.pop()
    current_model.append(event)

# reset data
button_reset = Button(label='Reset', button_type='primary')
button_reset.on_click(callback_button_reset)

# add data on double tap
p.on_event(DoubleTap, callback_add_dot_on_double_tap)

# update model
button_update = Button(label='Train model', button_type='success')
button_update.on_click(callback_button_update)

# choose class
button_class = RadioButtonGroup(labels=['Class 0', 'Class 1'], active=0)
button_class.on_click(callback_button_class)   

# choose classifier
button_model = RadioButtonGroup(labels=['Log. Reg.', 'Naive Bayes', 'SVC', 'RF'], active=0)
button_model.on_click(callback_button_select_model)   

# create document
curdoc().add_root(column(p, row(button_class, button_model), row(button_update,
                    button_reset), table))