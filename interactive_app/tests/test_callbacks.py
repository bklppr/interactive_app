#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from interactive_app import callbacks
import numpy as np
from bokeh.models import ColumnDataSource
from collections import namedtuple
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

__author__ = "bklppr"
__copyright__ = "bklppr"
__license__ = "mit"


@pytest.fixture
def state():
    """Namedtuple containing variables describing the app and its current state."""
    State = namedtuple('State', ['current_level', 'current_model', 'xlim', 'ylim', 'step', 'color_dict', 'colnames',
                                 'colnames_color'])
    state = State(current_level=[0], current_model=[0], xlim=(0, 1), ylim=(0, 1), step=0.2,
                  color_dict={0: 'darkblue', 1: 'darkorange'}, colnames=['x', 'y', 'level'],
                  colnames_color=['x', 'y', 'level', 'color'])
    return state


@pytest.fixture
def empty_source():
    """Empty ColumnDataSource instance for points added from double clicks."""
    return ColumnDataSource(data={'x': [], 'y': [], 'level': [], 'color': []})


@pytest.fixture
def source(state):
    """ColumnDataSource instance for points added from double clicks.

    :param state: pytest fixture namedtuple containing variables of app and its state.
    :return: BokehObjectWrapper wrapping ColumnDataSource containing dummy data.
    """
    x = [.2, .4, .6]
    y = [.6, .2, .4]
    level = [0, 1, 1]
    color = [state.color_dict[l] for l in level]
    return ColumnDataSource(data={'x': x, 'y': y, 'level': level, 'color': color})


@pytest.fixture
def surface(state):
    """ColumnDataSource instance for decision surface."""
    x = list(np.repeat([0, .5, 1], 3))
    y = list(np.tile([0, .5, 1], 3))
    level = list(np.repeat([0, 1, 1], 3))
    color = [state.color_dict[l] for l in level]
    return ColumnDataSource(data={'x': x, 'y': y, 'level': level, 'color': color})


@pytest.fixture
def classifiers():
    """List containing sklearn classifiers."""
    cls = [LogisticRegression(solver='lbfgs'), GaussianNB(), LinearSVC(C=1.0), RandomForestClassifier(n_estimators=100)]
    return cls


@pytest.fixture
def double_tap_event():
    """Namedtuple as mock bokeh event for double tap."""
    return namedtuple('Event', ['x', 'y'])(.5, .5)


def test_callback_button_reset(source, surface):
    """Test callback for reset button."""
    callbacks.callback_button_reset(source, surface)
    for s in [source, surface]:
        for v in s.data.values():
            assert v == []


def test_callback_add_dot_on_double_tap(double_tap_event, state, empty_source):
    """Test callback for adding dot on double tap."""
    callbacks.callback_add_dot_on_double_tap(double_tap_event, state, empty_source)
    assert empty_source.data['x'] == [.5]
    assert empty_source.data['y'] == [.5]
    assert empty_source.data['level'] == state.current_level
    assert empty_source.data['color'] == [state.color_dict[state.current_level[0]]]


def test_callback_button_update(source, classifiers, state, surface):
    """Test callback for button to update the decision surface."""
    callbacks.callback_button_update(source, classifiers, state, surface)
    xy = np.arange(state.xlim[0], state.xlim[1], state.step)
    assert surface.data['x'] == list(np.tile(xy, len(xy)))
    assert surface.data['y'] == list(np.repeat(xy, len(xy)))
    assert all([l in state.color_dict.keys() for l in surface.data['level']])
    assert all([c in state.color_dict.values() for c in surface.data['color']])


def test_callback_change_current_state(state):
    """Test callback for updating current state."""
    assert state.current_level == [0]
    assert state.current_model == [0]
    callbacks.callback_change_current_state(1, state.current_level)
    callbacks.callback_change_current_state(2, state.current_model)
    assert state.current_level == [1]
    assert state.current_model == [2]
