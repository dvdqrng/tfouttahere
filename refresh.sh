#!/bin/zsh
# Fetch the latest 16-day forecast and rebuild sun-finder.html. Publishing is done by the scheduled task.
set -e
cd "$(dirname "$0")"
python3 -I tools/forecast.py data/climate.json data/forecast.json
python3 -I tools/build.py
