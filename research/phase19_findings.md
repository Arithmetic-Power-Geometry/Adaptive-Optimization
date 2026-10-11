# Phase 19 — Arithmetic-Power Directional Polling (APG PowerPoll)
Date: 2026-10-11

## Mechanism
Maintain up to 12 previously successful unit poll directions v_i with observed objective decrease g_i>0. Sample a stored direction with probability
p_i=(g_i+10^{-9})^2 / sum_j(g_j+10^{-9})^2.
Poll this direction and its opposite before a randomized coordinate-direction safeguard. Increase the radius by factor 1.12 after accepted descent (maximum 1.5); halve it after no improvement. This is a newly implemented **heuristic** inspired by arithmetic-power weighting, NOT a proven new optimization principle.

## Exact experiment design
4 shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock) × 3 dimensions (2,5,10) × 10 seeds (900–909) × 4 methods (APGPowerPoll, COBYQA, Powell, Nelder-Mead) = 480 executed runs. Hard cap 180 objective evaluations. Common starts per matched family/dimension/seed. Strict objective meter counts all evaluations. Synthetic benchmark, not official COCO.

## Primary results
Paired wins against COBYQA across 120 instances: APGPowerPoll 22; Powell 27; Nelder-Mead 8. Selected medians (APG vs COBYQA): Ackley 5D 1.65951 vs 4.52384; Rastrigin 2D 8.95461 vs 12.43693; Rastrigin 5D 25.2532 vs 13.9294; Griewank 10D 0.07961 vs 0.00863; Rosenbrock 10D 80.0777 vs 62.3212. No robust superiority.

## Elementary structural observation (NOT novel theorem)
With zero regularizer, scaling all gains by a common positive constant leaves normalized power-selection probabilities unchanged. If the largest gain is at least kappa times each of the other m−1 gains, its selection probability is at least kappa^2/(kappa^2+m−1). This follows directly from the probability formula and does not imply an optimization complexity guarantee. With 10^{-9} regularizer, exact scale invariance fails.

## Closest prior art
Ma et al. (2025) already combine model-based optimization and search; Davar and Grapiglia (2025) provide finite-difference trust-region complexity guarantees; Brockhoff and Villain (2025) compare Powell-family solvers with CMA-ES on BBOB; Ascia et al. (2025) study adaptive trust-region Bayesian optimization on constrained COCO. The APG weighting heuristic has not been established original against full literature.

## Reproducibility
Executed local phase19.py SHA256 e431a24ea1e00a95813483b25645e44fe424d0e55f998e0316f2bc2682dd686a.
Raw CSV SHA256 2e9f70fb95d17e59f9085d16465dd648525c815cd0984c0a2ed8f14c3bb58a69.
Summary CSV SHA256 b109b2b8828e184303bfd52cb5eb1522942c5dcf0a5ba74e8739e92d6d1d0012.
Environment SHA256 6eda6bc0ce4e5cda4afc50df6d49aab9af9d9276097f991edd99e33c41880f9d.
The local executed source and raw CSV must be committed to GitHub and SHA checked before claiming repository-only reproduction.

## Verdict
The experimental APG rule offers selective median benefits but is inferior to COBYQA on 98/120 matched cases (counting all non-wins, including ties). No established Q1-level algorithmic novelty, theorem or overall performance superiority. Avoid describing this as a breakthrough.

## Paired-win stratification and evaluation usage
APGPowerPoll wins versus COBYQA by family: Ackley 10/30, Rastrigin 5/30, Griewank 2/30, Rosenbrock 5/30. Eight additional matched cases are numerical ties within tolerance 1e-10. Mean objective calls: APGPowerPoll 180.0, COBYQA 111.28, Powell 155.01, Nelder-Mead 150.66. These are **maximum budgets**, not equal numbers of consumed evaluations; early termination can make baselines cheaper. The source code comment referring to gain/evaluation-distance is inaccurate: the implemented weight uses raw observed gain, not gain divided by distance. The code is authoritative.
