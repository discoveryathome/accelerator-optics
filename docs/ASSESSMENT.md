# Assessment and execution handoff

Status: **not yet measured**. The initial session prepared code and documents but did
not install dependencies or execute project code because the requested startup
protocol requires permission for unsandboxed execution. No response to that question
had arrived when these files were prepared. The code is untested.

Expected usefulness (hypothesis, not a measured conclusion): short sessions should be
well suited to reproductions, checker hardening, paired experiments and scoped
robustness audits. Novel linear FODO optimization is unlikely to be a rich frontier:
there are few variables, standard analytical solutions and established matching tools.
An improvement over intentionally perturbed settings is primarily a recovery exercise.

A credible conclusion needs the following completed work:

1. Install Xsuite, NumPy, SciPy, matplotlib, pytest and jsonschema in .venv; pin the
   resolved environment before experiments. Use local caches and record disk footprint.
2. Review source and screen the project with the hash-verified protocol helper. Check
   upstream installation metadata before any unexpected build. Do not run on high findings.
3. Run `python -m beamopt.verify --reference`, then negative tests. Resolve API and
   physical-coordinate discrepancies before doing any search.
4. Run `bash run.sh`; save seeds, full search histories and wall-clock times. Compare
   both methods at equal evaluation budgets and against the analytic reference.
5. Check nominal candidate with Xsuite, matrix maps, periodic covariance, chromaticity,
   zero dispersion/orbit and all acceptance gates. Add dense held-out momentum scans
   and finite-difference-step sensitivity before final conclusions.
6. Compare all tracking scenarios and seeds. Acknowledge any losses or worsening
   emittance/RMS values. A faster/smaller linear envelope alone is not realistic success.
7. Inspect generated PNGs. Run the checker and each task-card first step from a fresh
   local clone with pinned dependencies. Record actual runtimes and machine context.
8. Run `python protocol/discover.pyz validate .`; the empty maintainers array is an
   anticipated local-proposal schema issue, never fill it with a fictitious maintainer.
9. Update README, this report and frontier with measured results, artifact hashes and
   honest evidence levels. Obtain independent scientific review before promotion.

Decision rule for promise: report setup time, verifier time, evaluations/second,
repeatability across seeds, feasible improvements, comparison to textbook controls,
and held-out/tracking failures. Distinguish educational/verification usefulness from
scientific novelty. No runtime or expected gain is currently asserted.
