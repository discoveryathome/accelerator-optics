# Literature update for the featured-pilot decision

Accessed 2026-10-20. This is a scoped source audit, not an exhaustive novelty search.

1. Xsuite's official Match guide already implements changing bounded knobs to satisfy
   Twiss targets. Thus the pilot cannot claim numerical optics matching itself as new.
   https://xsuite.readthedocs.io/en/latest/match.html
2. L. Yang et al., *Multiobjective optimization of dynamic aperture*, PRSTAB 14,
   054001 (2011). The paper combines particle tracking and analytical nonlinear
   driving-term estimates to improve optimization convergence on an NSLS-II example.
   This supports looking for value in informed objectives and physical structure,
   rather than merely rerunning a population optimizer.
   https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.14.054001
3. *Genetic algorithm for chromaticity correction in diffraction limited storage rings*,
   PRAB 19, 044001 (2016). Sextupole/octupole optimization addresses chromaticity,
   dynamic aperture and lifetime together. It provides precedent for explicit
   competing objectives, error sensitivity and momentum acceptance in a harder pilot.
   Its reported computing setup is not evidence that such a pilot fits this home PC.
   https://journals.aps.org/prab/abstract/10.1103/PhysRevAccelBeams.19.044001
4. Z. Zhang et al., *Efficient dynamic and momentum aperture optimization for lattice
   design using multipoint Bayesian algorithm execution*, APS accepted paper,
   accepted 2026-09-01. The authors report reduced tracking cost compared with genetic
   algorithms using particle-level query selection and learned models. This is
   evidence of active work and strong modern baselines, not a result reproduced here.
   https://journals.aps.org/prab/accepted/10.1103/4t6l-7jmg

Inference for this pilot: meaningful accelerator optimization is real, but the simple
linear example is mostly a teaching/reproducibility task. A nonlinear follow-up should
benchmark against established matching and modern optimization controls before making
agent-intelligence or novelty claims. A real accelerator expert should choose the
physical question and acceptance constraints.
