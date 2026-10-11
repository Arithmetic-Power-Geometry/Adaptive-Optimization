# Adaptive Optimization — Evidence Ledger, Phases 1–23

1–6: Adaptive/rotating/coupled/memory/gated polling; mixed results.
7–11: held-out replication and Powell baselines; no consistent dominance.
12: finite-transcript ambiguity construction; originality not established.
13: finite-difference sign certificate; established error bounds.
14: independent LineMemory replication; weak advantage.
15: bounded-noise certificates; no algorithmic superiority.
16: COBYQA wins 48/48 noiseless and 45/48 noisy matched quadratics.
17: simple two-start COBYQA 16/96 wins versus COBYQA.
18: plateau restart triggered 0/18; not validated.
19: APG power-weighted memory polling 22/120 wins vs COBYQA.
20: 360-run power ablation; p=2 16/60 vs COBYQA; NoMemory beats p0 39/60.
21: curvature-filtered polling 40/72 vs symmetric control, 14/72 vs COBYQA.
22: Helix 59/96 vs random-axis, 17/96 vs COBYQA.
23: controlled golden angle 43 wins/21 losses/8 ties vs rational, 41/22/9 vs random, 17/48/7 vs COBYQA, 288 independent runs.

**Closest-prior-work warning:** Van Dyke 2014 already studies equal-angle direct-search polling; Roberts/Royer 2023 already study randomized reduced-space direct-search with complexity guarantees. No new complexity theorem or robust COBYQA dominance. Q1 general-purpose optimizer paper not yet substantiated. Exact local Phase 23 source and raw CSV have hashes in phase23_findings.md; GitHub reconstruction of source is not byte-identical and CI status is unverified.
