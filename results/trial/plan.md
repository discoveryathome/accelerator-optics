# Contributor trial: pre-run plan

Start: 2026-10-20T20:08:55Z. Target: roughly 30 minutes (up to 60 for verification).
User authorized local installation/execution on this unsandboxed host. No publication.
Single agent continuing its own implementation: this is a simulated contributor
session and independent-implementation check, not an independent reviewer or randomized
agent-versus-solver study.

1. Time cold install, reference check, negative tests and ordinary baseline search.
2. Run fixed-budget SLSQP and random controls; inspect hard constraints and textbook gap.
3. Use domain reasoning to propose a strong symmetry/analytic control. Compare its
   evaluation cost and score to the generic solver; do not count setup fixes as discoveries.
4. Run held-out geometry/injection/error tests. Record failures, not only successful cases.
5. Assess public demo and remaining headroom; inspect plots and reproduce check from a clone.

Criteria: tangible early progress, sustainable hill-climbing, public-explainable gains,
scientific meaning, home-PC suitability, agent intelligence beyond solver compute.
All original nominal benchmark limits stay fixed. New objectives require separately
labelled configurations. No benchmark tuning based on held-out outcomes.

Additional diagnostic declared at 20:19 UTC, after nominal results: an irregular
16 m period with drift lengths [1.5,2.3,1.8,2.6,2.1,1.7,2.4,1.6] m. Start from
uniform +/-0.5 strengths, rather than an artificially perturbed strength baseline.
Preserve its reference tunes to 1e-4, and require chromaticity magnitude, each plane's
beta maximum and off-momentum maximum to be no worse than the reference (1e-6 numerical
slack). Keep the same strength bounds, 20 mm aperture and stability bound. This is an
exploratory NEW fixture, not a retrospective modification of the nominal benchmark.
Compare original SLSQP/random with the same epigraph method; do not tune its parameters.

Additional diagnostic at 20:22 UTC: the irregular optimum changes entrance Twiss
substantially (including beta_y from about 1.85 to 3.41 m). Declare a separate
`injection` fixture that also preserves beta_x, beta_y, alpha_x, alpha_y at the period
entrance to 1e-5. Preserve all other irregular fixture gates. This tests whether useful
internal-envelope progress remains while the injected beam is actually the same.
Original nominal and irregular contracts remain unchanged.
