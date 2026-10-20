# Accelerator beam-optics Discovery@Home pilot

**Status: prepared, not executed. Execution approval pending.** No optimization result,
passing verification, runtime, or particle-tracking performance is claimed yet.
Local-only proposal; no maintainer has agreed and donor intake is closed.

Can short searches improve a perturbed periodic quadrupole channel while retaining
specified optics and operational limits? The experiment compares constrained SLSQP
with an equal-budget random search and a textbook symmetric FODO reference.
See [research brief](docs/BRIEF.md), [agent entry](AGENTS.md), and
[model and acceptance rules](docs/MODEL.md).

The known result is the analytic 60 degree FODO solution: beta_max=6.9282032303 m,
with four-cell tune 2/3 and chromaticity -0.7351051939 in both planes.
Source: [B. Holzer, CERN accelerator-optics lectures](https://cds.cern.ch/record/1533020/files/CERN-2013-001-p171.pdf).
These values are mathematical predictions, **not yet locally reproduced**.

## Execute after approval

Use Python 3.12 or 3.13 and a project-local environment. Initial dependency versions
are unpinned until the first successful install; freeze the environment before running
research and retain the resulting requirements.lock. Do not describe results as
reproducible until that lock and the verification outputs are committed.

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.in
.venv/bin/python -m pip freeze > requirements.lock
.venv/bin/python -m beamopt.verify --reference
.venv/bin/python -m pytest -q
bash run.sh
```

After the first run, reproduce with `pip install -r requirements.lock` in a fresh
virtual environment. Recheck a candidate independently of the search:

```sh
.venv/bin/python -m beamopt.verify results/candidate.json
```

Planned outputs: search history and candidate JSON; independently implemented Xsuite
and NumPy map/Twiss comparison; tracking and held-out-family JSON; optics/envelope,
search, and tracking PNGs. Every physical constraint is a hard gate. No score in a
candidate file is trusted. This is independent *implementation* checking by one author,
not an independent scientific review.

No claim of new accelerator physics or real-machine readiness is justified by this
small model. See [assessment](docs/ASSESSMENT.md) for open validation work.
