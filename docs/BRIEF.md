# Local pilot research brief

Question: can short, deterministic numerical searches improve a perturbed four-cell
FODO channel without violating predeclared optics, chromaticity, stability, aperture
and integrated-gradient limits? Is any improvement more than recovery of a known solution?

Model: uncoupled thin-lens quadrupoles with fixed drift geometry, proton reference
momentum 1 GeV/c, no bending or RF. Integrated quadrupole strength k1L in m^-1.
An independent NumPy matrix implementation and CERN Xsuite must agree.
Primary metric: maximum beta over both planes and the full period, proportional to
squared matched RMS envelope for equal fixed geometric emittances. Constraints are
hard acceptance gates, never a weighted tradeoff score. Report both planes separately.

Known reference: symmetric 60 degree cells, k1L=+/-0.5 m^-1 and 2 m lens spacing.
For one cell L=4 m, mu=pi/3, beta_max=L(1+sin(mu/2))/sin(mu),
beta_min=L(1-sin(mu/2))/sin(mu), and chromaticity=-tan(mu/2)/pi.
Four cells multiply tune and chromaticity by four. This is textbook optics, not a
research frontier. A distorted reference is a recovery challenge, not a best-known result.

Evidence: pinned numerical model, reproducible seeds, independent implementation checks,
negative tests and Xsuite particle tracking. Independent implementation does not imply
independent human/agent review. Evidence remains author-checked until another reviewer reruns it.

Claims audit:
- Xsuite computes maps, Twiss and chromaticity: confirmed by official Twiss documentation.
- Bounded optics matching is established: confirmed by official Match documentation.
- FODO optics has an analytic reference: confirmed by CERN lecture below.
- Useful new magnet configurations can be discovered in short sessions: unverified hypothesis.
- Linear envelope reduction implies realistic performance gains: unverified; explicitly test
  momentum spread, mismatched injections and apertures, and state missing physics.

Sources, accessed 2026-10-20:
- https://xsuite.readthedocs.io/en/latest/twiss.html (periodic/off-momentum Twiss)
- https://xsuite.readthedocs.io/en/latest/match.html (bounded targets and matching)
- https://xsuite.readthedocs.io/en/latest/track.html (tracking and monitors)
- https://cds.cern.ch/record/1533020/files/CERN-2013-001-p171.pdf
  B. Holzer, Beam Optics and Lattice Design for Particle Accelerators (2013).
- https://arxiv.org/abs/1107.2797 V. Balandin et al. (2011), apochromatic
  drift-quadrupole optics with symmetries; relevant follow-up, not a reproduced result.
- https://arxiv.org/abs/2310.00317 Xsuite framework paper.

Settled for this scope: a quadrupole focuses one plane and defocuses the other;
minimizing one beta alone is inadequate. Zero dispersion in a straight ideal channel
is not evidence of chromatic correction. A linear, Hamiltonian map does not cool a beam.
Repeated straight periodic cells are a mathematical channel, not a closed physical ring.

No maintainer has consented; review capacity is zero and donor intake is closed.
License: MIT for original code and text; upstream documents retain their licenses.
Credit in CONTRIBUTORS.md plus named result records; no promised scientific authorship.
