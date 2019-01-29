#!/usr/bin/env python

import numpy as np
import pandas as pd


def create_meshgrid(xlim, ylim, step):
    """Create a numpy meshgrid from x and y axis limits with point distance step.

    :param xlim: list or tuple of length 2 containing the limits of the x axis.
    :param ylim: list or tuple of length 2 containing the limits of the y axis.
    :param step: float specifying the distance between grid points.
    :returns mg: numpy array containing the grid.
    """
    x = np.arange(xlim[0], xlim[1] + step, step)
    y = np.arange(ylim[0], ylim[1] + step, step)
    xm, ym = np.meshgrid(x, y)
    mg = np.concatenate((xm.reshape(-1, 1), ym.reshape(-1, 1)), axis=1)
    return mg


def create_decision_surface(model, x, y, xlim, ylim, step):
    """Get decision surface for model over specified grid.

    :param model: sklearn classifier.
    :param x: numpy array containing features of the training data.
    :param y: numpy array containing the labels of the training data.
    :param xlim: list or tuple of length 2 containing the limits of the x axis.
    :param ylim: list or tuple of length 2 containing the limits of the y axis.
    :param step: float specifying the distance between grid points.
    :returns ds: pandas DataFrame containing the coordinates of grid points and the respective predicted classes.
    """
    model.fit(x, y)
    mg = create_meshgrid(xlim, ylim, step)
    preds = model.predict(mg)
    ds = pd.DataFrame(np.concatenate((mg, preds.reshape(-1, 1)), axis=1))
    return ds
