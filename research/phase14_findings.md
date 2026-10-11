# Phase 14: New 600-run independent replication and closest-prior-art review
Date: 2026-10-11

## Design and provenance
Exactly 600 new locally executed optimization runs = dimensions 2,5,10 × diagonal/rotated × 20 seeds (400–419) × 5 algorithms (AdaptivePoll, LineMemory, Powell, BFGS with numerical gradients, L-BFGS-B with numerical gradients). Every run uses a 240-objective-call cap; common initial point per matched problem; eigenvalues log-spaced 1 to 10000; quadratic shift uniform [-1,1]. Numerical gradient evaluations are counted by the objective meter. Source is the locally executed /mnt/data/adaptive_phase14/phase14.py; raw results and summary are available as conversation artifacts, not yet uploaded as exact bytes to GitHub.

## Results: median best objective (lower is better)
| d | geometry | Adaptive | LineMemory | Powell | BFGS | L-BFGS-B | LineMemory paired wins vs Adaptive (out of 20) |
|---|---|---:|---:|---:|---:|---:|---:|
|2|diagonal|6.93406e-12|6.89475e-16|1.58016e-25|5.45777e-13|2.47643e-13|20|
|2|rotated|1.771585|1.504436|2.31654e-22|1.68702e-10|9.09311e-11|12|
|5|diagonal|0.000106382|0.000477138|1.47519e-25|6.15025e-13|8.64995e-12|4|
|5|rotated|40.925905|40.638978|10.599882|4.24535e-11|1.26826e-10|7|
|10|diagonal|2.117644|3.319488|2.90189e-24|3.507e-12|2.217332|10|
|10|rotated|176.704736|183.647087|324.978133|7.02835e-10|3.739286|11|

LineMemory's rotated 5D advantage shrank to 0.7% median and was worse on 13/20 paired instances; rotated 10D reversed to a 3.9% worse median. Numerical-gradient baselines dominate these smooth quadratic problems. No robust superiority or Q1-level novel optimization breakthrough.

## Theory / novelty audit
Phase 12 finite-transcript ambiguity construction is correct but an instance of information-based indistinguishability; Phase 13 two-probe descent bound follows from classical centered finite differences and descent lemma. The algorithm called CertifiedLine in Phase 13 did not enforce the theoretical curvature certificate; Phase 14 labels it LineMemory accurately. A new theorem or improved oracle-complexity result has NOT been established.

2025 Bollapragada–Karamanli–Wild already study adaptive sampling with convergence and sample complexity. 2026 Dzahini–Wild establish expected complexity for stochastic random-subspace direct search. 2025 Brockhoff–Villain benchmark BOBYQA/COBYLA/LINCOA/NEWUOA/UOBYQA against CMA-ES and BFGS on BBOB. Shi et al. study adaptive finite-difference interval selection under noise. A claimed breakthrough must distinguish itself from these prior methods.

## Research decision
Do not continue tuning LineMemory on the same six quadratics. Next study should implement a *genuine* uncertainty-aware certificate with known error bounds, and compare on COCO/BBOB and constrained/noisy objectives. Any new theoretical result needs formal assumptions, explicit constants, and a prior-art separation theorem. No GitHub Actions run has been verified.
