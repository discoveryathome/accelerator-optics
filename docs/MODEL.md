# Model and acceptance contract (v1, proposed before execution)

Eight zero-length quadrupole lenses alternate F and D. Each is followed by a 2 m drift,
forming a 16 m period. The period is mathematically repeated; there are no bends, RF,
radiation, collective fields, acceleration, material scattering or fringe fields.
Coordinates are canonical x, px/p0, y, py/p0. Delta=dp/p0. Proton p0c=1 GeV.
Thin-lens integrated gradient k1L has units m^-1; drift lengths never vary in a search.
The allowed 0.35–0.65 m^-1 magnitudes with fixed signs are synthetic hardware bounds,
not certified settings for an existing accelerator. For actual magnets, finite length,
gradient/power, polarity, calibration and aperture limits must be supplied.

The config is the authoritative contract. Geometric emittance is 1 micrometre in each
plane. Objective is max(beta_x,beta_y) over the period, not emittance reduction.
Each drift's beta is convex, so lens/end-point samples capture its maximum exactly
in this linear model. Smooth plots sample drift interiors as well.

Hard constraints:
- Correct F/D signs and integrated-strength bounds, finite values, exactly 8 variables.
- Each four-cell tune within 0.015 of 2/3. This tolerance permits tune movement; it is
  not exact matching. Report movement, not just the envelope gain.
- Absolute chromaticity in each plane <=0.772, about 5% above the textbook reference.
  This is an explicit budget, not a promise of unchanged chromaticity. Report both values.
- Peak beta <=9 m in each plane, off-momentum peak <=10 m in each plane.
- For delta=-.02,-.01,0,.01,.02: stable maps and max absolute trace <=1.9.
- Matched 6-sigma envelope <=20 mm in each plane throughout those sampled momenta.
  This is an envelope constraint, not an absolute guarantee for Gaussian tails.

Finite momentum samples do not prove stability over the continuous interval; add a
dense held-out scan before operational claims. Dispersion and reference orbit must be
zero to numerical tolerance in this ideal straight channel. Chromaticity is dQ/d(delta),
computed by a centered finite difference with h=1e-5 and checked against Xsuite.
Tune branch must remain the same near the reference; no claim for arbitrary high-phase lattices.

Search: 1200 unique full evaluations per seed (7,19,41), each for SLSQP and random
search. Baseline is explicitly perturbed from the symmetric reference. SLSQP uses
multistart, fixed finite-difference step and hard inequality constraints. The reported
incumbent is the best actually evaluated feasible point, including intermediate points.
No analytic solution is injected into either method. All evaluation histories are saved.

Validation split: longer (2.1 m) and alternating (1.8/2.2 m) drift families are excluded
from nominal candidate selection. Evaluate zero-shot settings and separately rerun the
same method/budget. Tune targets and chromaticity budgets for each held-out family are
derived from that family's symmetric reference. These are different benchmark tasks;
method transfer is not zero-shot settings transfer.

Tracking uses 1024 particles, 256 periods and seeds 103,211,307 with Gaussian phase-space
samples and 0.5% RMS momentum spread clipped at +/-2%. Compare candidate-matched beams,
identical reference-matched injection for all configurations, 30%/20% beta mismatch
plus alpha offset, and common injection with 0.1% RMS gradient errors and fixed
sextupole errors k2L=0.15 m^-2. These error amplitudes are synthetic stress tests.
Square +/-20 mm apertures are checked at lenses and period boundary. Transverse position
is linear in drift path for ideal drift motion, so endpoints suffice for rectangular
aperture crossings. Tracking uses Xsuite's particle map rather than the linear checker.
Report survival separately from survivor moments to avoid hiding losses.
Turn monitors measure RMS only at period starts, not the maximum throughout the lattice.
Projected emittance growth with momentum spread/errors is not a cooling measurement.
No space charge, alignment errors, long-term dynamic-aperture or machine validation.

A candidate passes numerical verification if all hard gates pass and Xsuite agrees with
the independent matrix calculation. A claim of improved realistic performance also
requires paired tracking evidence; optics improvement alone cannot authorize that claim.
