# Adaptive Optimization research history, Phases 1–22

Phases 1–6: adaptive, rotated, coupled, memory and gated polling; conditional gains only.
Phases 7–11: held-out replication and Powell baselines; no consistent dominance.
Phase 12: finite-transcript ambiguity construction; originality unestablished.
Phase 13: finite-difference directional certificate; classical error bounds.
Phase 14: independent LineMemory replication; inconsistent gains.
Phase 15: bounded-noise descent/acceptance certificates; no performance superiority.
Phase 16: COBYQA dominates adaptive polling (48/48 noiseless, 45/48 noisy matched quadratics).
Phase 17: two-start COBYQA 16/96 wins vs COBYQA; summary reconstruction required.
Phase 18: plateau-triggered restart never activates.
Phase 19: power-weighted directional polling 22/120 wins vs COBYQA.
Phase 20: 360-run power exponent ablation fails to validate power weighting; no-memory beats p0 in 39/60.
Phase 21: curvature-filtered symmetric polling 40/72 wins vs simple symmetric polling, 14/72 vs COBYQA.
Phase 22: Helix Search 384 runs, 59/96 wins vs random-axis polling, 17/96 vs COBYQA, mean calls 155.68 vs COBYQA 107.16. Exact source Git blob verified. Raw observations local; GitHub workflow pending.

**Novelty gate:** 22 phases document exploratory mechanisms and conditional advantages but no established original convergence/complexity theorem and no modern-baseline superiority. Not Q1-ready as a novel optimizer. Do not fabricate publication readiness. Research and bibliography reports live under research/phaseNN_findings.md and references/phaseNN_verified.bib.
