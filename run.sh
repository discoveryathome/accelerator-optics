#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export XDG_CACHE_HOME="$PWD/.cache"
mkdir -p results
.venv/bin/python -m beamopt.verify --reference > results/reference-check.json
.venv/bin/python -m pytest -q tests > results/tests.txt
.venv/bin/python -m beamopt.search | tee results/search.log
.venv/bin/python -m beamopt.experiments | tee results/experiments.log
.venv/bin/python -m beamopt.plots
.venv/bin/python -m pip freeze > requirements.lock
