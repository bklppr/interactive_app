#!/usr/bin/env bash

conda env create -f environment.lock.yaml --prefix ./conda_env
source activate ./conda_env

cd interactive_app
python setup.py develop
cd ..

bokeh serve --show interactive_app/src/interactive_app
