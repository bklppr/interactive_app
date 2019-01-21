# Interactive App
This repository provides a toy [bokeh](http://bokeh.pydata.org/en/latest/) app for visualizing the decision surfaces of different classification models for data that is added by the user by double-clicking into the plot.

# Quick Start
Run
```
conda env create -f environment.lock.yaml --force
source activate interactive_app
```
to create a `conda` environment with all dependencies and activate it.

Run
```
./run.sh
```
and the app appears under `http://localhost:5006`.

# Develop
The `interactive_app` folder is set up with [PyScaffold](https://pyscaffold.org/en/latest/).
If you want to further develop it, run
```
cd interactive_app
python setup.py develop
```
to install the package.