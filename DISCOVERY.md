# Discovery@Home: accelerator optics

This local pilot tests whether short numerical-search sessions can produce useful,
cheaply verified beam-optics work. The concrete question, sources and claims audit are
in docs/BRIEF.md. The exact model and fixed acceptance contract are in docs/MODEL.md.

The established reference is symmetric thin-lens FODO optics, not a newly discovered
configuration. The current record is literature-backed and awaits local reproduction.
Do not treat the perturbed baseline as the scientific frontier. Report improvements
against both the perturbed baseline and the analytic reference, with all constrained
metrics before and after. Tunability and feasible optimization are known; short-session
research value remains the hypothesis to test.

Bottleneck: scientific fidelity and independent review, rather than a shortage of
optimization evaluations. This tiny linear problem is intentionally transparent and
may be quickly exhausted. Nonlinear effects, realistic error ensembles and more varied
fixed geometries are future versions, not evidence established by the pilot.

Workflow: verify analytic example; run rejection tests; search with the fixed budgets;
check candidates through Xsuite and independent transfer matrices; evaluate held-out
families and multi-particle tracking; render and inspect figures; rerun from a clean
checkout. Record package versions, source hash, seeds, candidate hashes and timings.
Candidate acceptance requires every hard constraint to pass. New scientific claims
also need an independent contributor's reproduction and a consenting maintainer review.

Priority tracks are in discover/catalog.json, reasons in discover/priority-log.md.
The proposed tracks are reference replication, verifier robustness, generalization
and literature/fidelity audit. No live claim board exists in LOCAL mode; local findings
and handoffs live in discover/messages.md. Never post these without permission.

Review: no maintainer is assigned, no review capacity is promised, and donor intake
is closed. The upstream manifest schema requires at least one maintainer; this local
proposal deliberately uses an empty array rather than inventing consent. This known
schema exception must be resolved before publication. No hubs consent record exists.

Credit: record substantive contributors in CONTRIBUTORS.md and each result's provenance.
No automatic paper authorship is promised. Proposed MIT license applies to original
material only. Vendored protocol text retains upstream rights. Literature is cited,
not relicensed. The upstream helper binary is hash-pinned and is optional tooling.
