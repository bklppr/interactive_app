#!/usr/bin/env python

import pytest
from interactive_app import utils
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


@pytest.fixture
def model():
    """Create sklearn model."""
    return RandomForestClassifier(n_estimators=1)


def test_create_meshgrid():
    """Test meshgrid creation."""
    mg = utils.create_meshgrid((0, 1), (0, 1), .5)
    assert (mg == np.array([[0, 0], [.5, 0], [1, 0], [0, .5], [.5, .5], [1, .5], [0, 1], [.5, 1], [1, 1]])).all()


def test_create_decision_surface(model):
    """Test creation of decision surface for model over specified grid."""
    x = np.array([[0, 0], [1, 1]])
    y = np.array([0, 1])
    ds = utils.create_decision_surface(model, x, y, (0, 1), (0, 1), .5)
    assert isinstance(ds, pd.DataFrame)
    assert (ds.values[:,:-1] == np.array([[0, 0], [.5, 0], [1, 0], [0, .5], [.5, .5], [1, .5], [0, 1], [.5, 1],
                                          [1, 1]])).all()
    assert ds.iloc[:,-1].isin(y).all()
