import numpy as np
import pandas as pd

class BokehObjectWrapper:
    def __init__(self, obj):
        self.obj = obj

def create_meshgrid(xlim, ylim, step):
    """Create a meshgrid from x and y axis limits."""
    x = np.arange(xlim[0], xlim[1], step)
    y = np.arange(ylim[0], ylim[1], step)
    xm, ym = np.meshgrid(x, y)
    mg = np.concatenate((xm.reshape(-1, 1), ym.reshape(-1, 1)), axis=1)
    return mg

def create_decision_surface(model, X, y, xlim, ylim, step):
    """Get decision surface for model over specified grid."""
    model.fit(X, y)
    mg = create_meshgrid(xlim, ylim, step)
    preds = model.predict(mg)
    ds = pd.DataFrame(np.concatenate((mg, preds.reshape(-1,1)), axis=1))
    return ds