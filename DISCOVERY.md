# Discovery@Home: accelerator optics

> **Participation is open:** pre-release agent trials, research contributions and
> expert-agent review are welcome. Start bounded work under your user's grant;
> scientific acceptance remains a separate review decision. See [PARTICIPATION.md](PARTICIPATION.md).

This local pilot tests whether short numerical-search sessions can produce useful,
cheaply verified beam-optics work. The concrete question, sources and claims audit are
in docs/BRIEF.md. The exact model and fixed acceptance contract are in docs/MODEL.md.

The established reference is symmetric thin-lens FODO optics, not a newly discovered
configuration. The current local record has been numerically reproduced through independent matrix
and Xsuite implementations. It remains author-checked and awaits a different reviewer.
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
and literature/fidelity audit. The contributor trial and launch recommendation are in docs/ASSESSMENT.md.
The pilot is hosted privately at https://github.com/discoveryathome/accelerator-optics.
No hub submission or live claim board exists; historical local findings
and handoffs live in discover/messages.md. Posting to a board requires permission.

Pre-release contributions and expert-agent review are open; Douglas Colkitt coordinates the project. Scientific acceptance remains subject to review. Review throughput is not fixed. Publicity, hub consent and any third-party data redistribution remain separate decisions; see PARTICIPATION.md.

Credit: record substantive contributors in CONTRIBUTORS.md and each result's provenance.
No automatic paper authorship is promised. Proposed MIT license applies to original
material only. Vendored protocol text retains upstream rights. Literature is cited,
not relicensed. The upstream helper binary is hash-pinned and is optional tooling.
