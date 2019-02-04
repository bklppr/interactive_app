# Interactive App

This repository provides a toy [bokeh](http://bokeh.pydata.org/en/latest/) app for visualizing the decision surfaces of different classification models for data that is added by the user by double-clicking into the plot.

# Quick Start

If you have a local Conda installation, you can run the app directly:

```
./run.sh
```

The app will be available at [http://localhost:5006](http://localhost:5006).

Alternatively, you can run the app via Docker:

```
./run-docker.sh
```

# Tests

To run the tests:

```
cd interactive_app
python setup.py test
```
