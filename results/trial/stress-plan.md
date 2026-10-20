# Follow-up stress tests declared before execution

These are exploratory, separate from nominal acceptance, and cannot change the selected
nominal candidates or retrospectively redefine the objective. They test ranking transfer.

- Finite magnets: replace each thin lens by a 0.2 m hard-edge Xsuite Quadrupole with
  k1=k1L/0.2. Shorten following drift by 0.2 m, keeping period length and lens-center
  spacing fixed. No fringe fields, space charge or alignment errors. Compare reference,
  perturbed baseline, generic-search candidate, analytic symmetry control. This is a
  model-fidelity check, not a calibrated machine model or matched optics comparison.
- Aperture challenge: keep thin maps and the common reference injection; use aperture
  half-widths 20,12,8,6 mm. Use 4096 particles, 256 periods, seeds 401,503,607.
  Evaluate survival first, then report survivor moments with explicit selection bias.
  These hardware apertures differ from the nominal 20 mm contract and results must not
  be used as evidence that the nominal benchmark selected a throughput optimum.
- Robust errors: existing declared 0.1% gradient errors and k2L=.15 m^-2, same seeds
  and common injection for each setting. Not a realistic calibrated error ensemble.
