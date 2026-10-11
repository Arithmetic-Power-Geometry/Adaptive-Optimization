# Cumulative research: Adaptive Optimization Phases 1–20

1–6: Adaptive/rotated/coupled/memory/gated polling; mixed results, memory probe savings not equal total objective savings.
7–11: held-out and Powell comparisons, cluster uncertainty; Powell often better, official COCO not executed.
12: finite-transcript ambiguity construction; mathematical validity established, literature novelty not.
13: conditional two-query finite-difference descent certificate; classical error bound.
14: independent replication weakens LineMemory apparent gains.
15: bounded-noise sign and acceptance certificates; no speed superiority.
16: COBYQA outperforms AdaptivePoll on 48/48 noise-free and 45/48 noisy matched quadratics.
17: two-start COBYQA wins only 16/96; Phase 17 local summary corrected from raw data.
18: plateau-triggered restart activates 0/18, hence decision mechanism untested.
19: APG power-weighted memory polling: 480 runs, 22/120 wins vs COBYQA; isolated median gains.
20: exponent ablation 360 independent runs: NoMemory 17/60, P0 17/60, P1 17/60, P2 16/60, P4 16/60 wins vs COBYQA. NoMemory beats P0 39/60; P2 beats P0 19/60. Power mechanism not validated.

## Reproducibility gate
Phase 20 executed script verified by matching Git blob. Raw and full summary are locally saved, with hashes in research/phase20_findings.md. GitHub Actions configured to regenerate and commit raw; successful run unverified. Earlier phases' raw GitHub gaps remain.

## Novelty and Q1 verdict
No established novel oracle complexity theorem, no consistent algorithmic superiority, no official BBOB execution. **Not Q1-ready as a new optimization algorithm.** Full literature includes MADS (Audet/Dennis 2006 and 2008 erratum), COCO (Hansen et al. 2021), recent trust-region and model-based DFO work. Do not present a heuristic exponent identity as a new mathematical breakthrough.
