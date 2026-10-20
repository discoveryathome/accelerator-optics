#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export MPL_IGNORE_SYSTEM_FONTS=1
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export XDG_CACHE_HOME="$PWD/.cache"
mkdir -p results/trial
# Regenerates local author-checked artifacts; never grants scientific acceptance.
.venv/bin/python -m beamopt.verify --reference > results/reference-check.json
.venv/bin/python -m pytest -q tests > results/tests.txt
.venv/bin/python -m beamopt.search | tee results/search.log
.venv/bin/python -m beamopt.experiments | tee results/experiments.log
.venv/bin/python -m beamopt.controls > results/trial/controls.log
.venv/bin/python -m beamopt.trial_audit > results/trial/candidate-audit.log
.venv/bin/python -m beamopt.search --spec results/irregular-spec.json --out results/irregular > results/trial/irregular-search.log
.venv/bin/python -m beamopt.epigraph --spec configs/nominal.json results/longer-spec.json results/alternating-spec.json results/irregular-spec.json > results/trial/epigraph.log
.venv/bin/python -m beamopt.epigraph --spec results/injection-spec.json --output results/trial/injection-search.json > results/trial/injection-search.log
.venv/bin/python -m beamopt.injection_study > results/trial/injection-tracking.log
.venv/bin/python -m beamopt.stress > results/trial/stress.log
.venv/bin/python -m beamopt.plots
.venv/bin/python -m beamopt.trial_plots
.venv/bin/python -m beamopt.demo
.venv/bin/python -m beamopt.records
.venv/bin/python -m beamopt.reproduce > results/trial/full-replay-verification.json
