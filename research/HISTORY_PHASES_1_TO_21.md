# Adaptive Optimization: Phase 1–21 cumulative evidence

Phases 1–6: adaptive polling, rotation, coupling, memory and gating; conditional gains, fewer memory probes but not total objective evaluations.
Phases 7–11: held-out experiments, budget sensitivity, Powell comparisons and family-level uncertainty; no robust dominance.
Phase 12: finite-transcript ambiguity construction; mathematical validity established, originality unverified.
Phase 13: conditional finite-difference sign/descent certificate; known mathematical ingredients.
Phase 14: independent LineMemory replication; gains not consistently reproduced.
Phase 15: bounded-noise directional and acceptance certificates; no superiority.
Phase 16: COBYQA beats Adaptive on 48/48 noiseless and 45/48 noisy paired quadratics.
Phase 17: two-start COBYQA wins 16/96 vs COBYQA; local empty summary corrected from raw data.
Phase 18: plateau restart triggered 0/18, failed mechanism validation.
Phase 19: APG power-weighted direction memory wins 22/120 vs COBYQA; isolated median gains.
Phase 20: 360-run exponent ablation p=0,1,2,4; no power-weighting advantage; no-memory beats p=0 on 39/60.
Phase 21: 288 new runs; curvature-filtered coordinate interpolation wins 40/72 vs symmetric polling, but only 14/72 vs COBYQA; Ackley d5 median 1.280 vs 5.922, Rosenbrock d10 161.97 vs 37.26.

## Novelty gate
Conditional curvature-filtered coordinate interpolation is not established new relative to model-based derivative-free optimization. No original complexity theorem, official COCO results, or robust modern-baseline dominance. **Not yet Q1-ready as a new optimizer.** Phase 21 exact source committed and Git blob verified. Local raw CSV and full summary have checksums; GitHub Actions configured but its success is not yet verified.

## Research direction
Preregister and independently validate a low-cost diagnostic of when interpolation-based polling is better than COBYQA, using official COCO/BBOB and a cost-accounted solver portfolio. The diagnostic itself must show nontrivial theory and reproducible benefit, not rely on post-hoc selection of Ackley.
