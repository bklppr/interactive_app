#!/usr/bin/env bash

docker run -i -t --rm \
  --mount type=bind,source="$(pwd)",target=/app \
  --publish 5006:5006 \
  continuumio/miniconda3 \
  /bin/bash -c 'cd /app && ./run.sh'
