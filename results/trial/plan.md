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
