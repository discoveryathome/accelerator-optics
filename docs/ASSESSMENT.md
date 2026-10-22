# Featured-pilot assessment: accelerator optics

> **Current participation:** pre-release contributions and expert-agent review are open.
> Any closed-intake or missing-coordinator statement below records an earlier stage;
> see [the current policy](../PARTICIPATION.md). Scientific results and review requirements remain in force.

**Recommendation: keep this as an onboarding/demo pilot; do not yet lead the launch
with it as a flagship discovery project.** The topic is compelling, runs comfortably
on a home computer, and supports visible, verifiable progress. The current fixtures
are small, synthetic and rapidly solved by standard methods. They do not yet offer a
credible supply of scientifically meaningful improvements for many contributors.

This was one agent continuing its own implementation, not a blind independent
contributor study. It tested the contributor workflow and independent implementations;
it did not establish a causal advantage of agents over a well-written solver.
The run began at 2026-10-20 20:08:55 UTC. The timed contributor work and validation
ran for roughly half an hour. Exact environment and outputs are in
`results/trial/`. Setup, research and validation are distinguished below.

## What the trial actually achieved

The original four-cell FODO benchmark passed the analytic reference and Xsuite checks.
The perturbed starting configuration has peak beta **7.657629 m**, versus **6.928203 m**
for the textbook symmetric reference. Six original searches used 1,200 full physics
evaluations apiece (random and SLSQP, seeds 7/19/41). The best generic search reached
**6.885626 m**: 10.08% less beta than the perturbed baseline, but only 0.61% less than
the textbook control. Beam width scales as the square root of beta, so the apparent
10% gain is about **5.2% less maximum matched width**, not 10% less width or emittance.

A symmetry argument gives **6.883446 m** in one evaluation. It selects the highest
allowed phase advance in this interval. The result is a textbook-derived comparator,
not a new accelerator discovery or a proof of the global eight-variable optimum.
It changes the period tune from 0.666667 to 0.681667 and chromaticity from about
-0.735105 to -0.755243. Those changes fit the declared contract; they would fail a
strict requirement to preserve the reference optics. Both facts are explicitly checked.

The useful agent intervention was diagnosing the nonsmooth maximum objective. A
naive two-family solver reported success without improving the reference. Replacing
`min max(beta)` by an equivalent epigraph formulation (minimize a scalar that bounds
every beta value) exposed the active branches to SLSQP. It reached **6.883446 m in
45 physics evaluations**, compared with 1,200 evaluations for the original weaker
result. The change preserved the physics score and all acceptance gates. This is
standard optimization knowledge applied effectively, not a novel algorithm.

To avoid basing the assessment solely on repairing deliberately perturbed strengths,
a separately declared irregular-spacing fixture starts from uniform magnet strengths.
Its tune target is preserved to 1e-4, and each plane's chromaticity magnitude, peak beta,
and off-momentum peak may not worsen. The peak beta falls from **10.822649 m** to about
**7.285910 m**. However, that solution changes the entrance beam's matched covariance.
A second, stricter fixture also fixes entrance beta and alpha to 1e-5 and still reaches
**9.210605 m** (14.9% less peak beta, about 7.75% less matched width). The epigraph
solver reaches these irregular-fixture solutions in about **94 evaluations**. These
are useful design exercises, but standard solvers exhaust this headroom quickly.
Both fixtures are exploratory additions declared during this trial, not untouched
held-out tests of the original research question.

## What did not generalize

The nominal candidate fails the acceptance gates when transplanted unchanged into the
longer-spacing family. Reoptimizing the method works on both longer and alternating
families. Method transfer and settings transfer are different claims.

All 36 nominal tracking cases (three configurations, four injection/error scenarios,
three seeds; 1,024 particles for 256 periods) had 100% survival. There was therefore
**no measured nominal transmission gain**. With the same reference-matched injected
beam, the optimized setting has slightly worse projected-emittance growth and period-start
RMS envelope than the textbook reference in several cases, especially mismatched
injection. It improves over the perturbed baseline without uniformly dominating the
known reference. Period-start RMS is not the maximum envelope throughout the lattice.

An independently declared tighter-aperture stress test used 4,096 particles, three new
seeds and 20/12/8/6 mm half-widths. At 6 mm, mean survival was 80.69% for the perturbed
baseline, 85.26% for the reference, and 85.33% for the optimized/control settings.
The optimized-versus-reference difference is only 0.065 percentage points; this tiny
sample difference is not convincing evidence of a useful transmission advantage.
Survivor emittances are explicitly reported separately from particle losses.

A finite-magnet check replaced the thin lenses with 0.2 m hard-edge quadrupoles at the
same center spacing. The reference tune changed from 0.666667 to about 0.641842.
This demonstrates material model dependence. Endpoint beta samples in that check do
not certify maxima inside thick magnets, and no real machine calibration was used.

The irregular-fixture study exposes a substantial failure that a width-only score
would miss: the free-entrance solution causes about **20.5% mean growth** in the larger
projected-emittance ratio under common injection. The fixed-entrance solution keeps
that ratio near unity while retaining its 14.9% beta improvement. All its tested
particles survive. This is a useful example of agent judgment improving the task
contract, rather than just finding lower numbers. It remains a synthetic, finite-seed
study; ratios slightly below one are not evidence of cooling. Full results are in
`results/trial/injection-tracking.json`, visualized in `results/injection-tradeoff.png`.

A final element-by-element tracking diagnostic sampled the complete lattice in periods
1, 16, 64 and 256. With the same injected particles, the fixed-injection setting reduced
the largest sampled RMS width by **5.47% on average** across three seeds (individual
reductions 3.03–8.03%); with the declared gradient/sextupole errors, the mean was **5.57%**.
All particles survived. This is a tangible multi-particle improvement in this synthetic
model, not merely a better Twiss score. The free-entrance candidate was actually wider
in these common-injection measurements despite its better matched-envelope score.
These four sampled periods do not establish the maximum over every period or long-term
stability. Data: `results/trial/full-lattice-tracking.json` and `full-profile-summary.json`. None of these simulations includes space charge, RF, scattering, alignment
errors or a validated machine error ensemble. They cannot establish operational gains.

## Suitability against the launch criteria

| Criterion | Assessment | Evidence and limitation |
|---|---|---|
| Tangible first-session progress | Strong | Working checks, candidate improvements, 45/94-evaluation convergence, and a found objective-formulation issue. Some initial work was setup/debugging rather than research. |
| Sustainable hill-climbing | Weak in the present version | The symmetric case is essentially solved analytically; even stricter irregular cases converge in seconds of physics work. Repeating random starts has little purpose. |
| Public story and demo | Strong | “Use eight magnets to keep a beam narrow while preserving its behavior.” Real computed envelopes and a traveling-particle animation are provided, with honest labels. |
| Meaningful scientific results | Unproven | Synthetic fixtures and textbook controls; no accelerator partner, expert acceptance or independently reviewed new physics/design. |
| Home-PC accessibility | Strong | CPU-only on Apple M2 with 24 GB RAM; no GPU or cluster. A single candidate check used about 147 MB maximum RSS; the 4,096-particle tracking probe used about 418 MB. Disk footprint and timings are recorded separately. |
| Agent intelligence matters | Moderate, demonstrated once | Physical symmetry, smoother formulation, and recognizing fixed-injection requirements helped. Once encoded, ordinary numerical optimization performs the search. No agent-versus-solver controlled study was run. |

The single-candidate check took **7.63 s wall time** in the timed run. The original
searches took roughly 10–30 s each. Other CPU-intensive sessions were active on the
host; these are observed shared-machine latencies, not isolated speed benchmarks.
Use evaluation counts for efficiency comparisons. Cold dependency installation took
about 27 s; first plotting was delayed by macOS font discovery, which subsequent
runs avoid by using Matplotlib's bundled fonts.

## What would earn a featured slot

1. **A physics owner and a real, public design question.** Obtain a consenting expert
   maintainer, a documented beamline/lattice, realistic field/aperture/error limits,
   and a useful target such as acceptance under errors or robust transport of a
   specified incoming beam. No maintainer is currently assigned.
2. **A ladder of independently checkable cases with remaining headroom.** Provide
   strong matching/optimizer baselines first, then demonstrate contributions that
   survive held-out errors, momenta and injections. Do not manufacture progress by
   comparing only to broken settings or silently loosening constraints.
3. **A contribution model beyond magnet-number search.** Give agents scoped work on
   physical parameterizations, robust objectives, sensitivity analysis, verification,
   multi-fidelity evaluation and failure diagnosis. A strong baseline should leave
   enough useful tasks for the first several contributors, not merely the first one.

A reasonable next go/no-go experiment is a few separate contributor sessions
on one expert-approved nonlinear or robust-transport fixture, with equal-budget strong
baselines and blinded held-out validation. Feature it only if those sessions produce
repeated useful improvements that the expert accepts. Until then, the present pilot
is honest and effective as “learn and verify accelerator optimization,” with no claim
that donated agents are discovering better real accelerators.

The field itself is meaningful: published work combines tracking and analytic physics
for dynamic-aperture optimization, and modern methods address expensive multiobjective
queries. That also means strong baselines already exist. See the linked primary
sources and scoped novelty audit in [LITERATURE-UPDATE.md](LITERATURE-UPDATE.md).

## Reproduction record

The retained candidates and five-case table were checked from a separate clean local
clone using the pinned virtual environment. All four task-card first steps completed.
A generic-search seed and an epigraph-search seed were replayed from that clone and
matched saved strengths/scores to 1e-10. The source-level test suite has 16 passing
tests, including false claims, invalid strengths, chromaticity/aperture failures,
loss handling and the fixed-injection gate. Raw logs are in `results/trial/`.
The fresh clone reused the installed dependency environment; this was not a second
machine or a second independent reviewer.

The upstream protocol validator reports the missing consenting maintainer as the
remaining schema error. It also notes optional absent public coordination/review
infrastructure, appropriate to this unlisted proposal. Nothing was published during
the trial; the user subsequently authorized a private GitHub repository, without a hub PR.
The verifier and frontier deserve the most care; expert review capacity, rather than
more donated optimizer evaluations, is likely to set this project's useful pace.

Trial receipt: 29.4 minutes elapsed, including setup, research, visualization and clean-clone validation. The final replay passed all 30 retained reference/candidate/table checks; two full-profile tracking cases also reproduced to 1e-12. Source snapshot: `5fe496369bd253b85ca482ae41e08c1495a87723`.
