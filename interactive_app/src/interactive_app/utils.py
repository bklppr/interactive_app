#!/usr/bin/env python

import numpy as np
import pandas as pd


def create_meshgrid(xlim, ylim, step):
    """Create a meshgrid from x and y axis limits."""
    x = np.arange(xlim[0], xlim[1] + step, step)
    y = np.arange(ylim[0], ylim[1] + step, step)
    xm, ym = np.meshgrid(x, y)
    mg = np.concatenate((xm.reshape(-1, 1), ym.reshape(-1, 1)), axis=1)
    return mg


def create_decision_surface(model, x, y, xlim, ylim, step):
    """Get decision surface for model over specified grid."""
    model.fit(x, y)
    mg = create_meshgrid(xlim, ylim, step)
    preds = model.predict(mg)
    ds = pd.DataFrame(np.concatenate((mg, preds.reshape(-1, 1)), axis=1))
    return ds
