# Phase 17 — 384 newly executed nonquadratic tests and current research verdict

Executed locally on 2026-10-11: 4 shifted/rotated test functions (Ackley, Rastrigin, Griewank, Rosenbrock) × 3 dimensions (2,5,10) × 8 seeds (700–707) × 4 methods = 384 runs. Strict 180 objective-call meter. Methods: COBYQA, a simple **two-start COBYQA** (108 initial +72 restarted from x0+U[-1.5,1.5]^d), Powell and SciPy differential evolution (popsize 5, no polishing). All methods share the same objective and initial x0, except DE uses its own population and the second COBYQA run is deliberately restarted. No official COCO/BBOB; these are hand-constructed rotated/shifted functions, not independent COCO instances.

## Findings
Two-start COBYQA beats COBYQA in 16/96 paired instances, Powell 19/96, DE 16/96. It improves the median Rastrigin 5D from 15.9193 to 13.4319, Rastrigin 10D 42.7831 to 41.7981 and Ackley 10D 6.1199 to 5.1384. It regresses on Rosenbrock 10D (83.1932 vs 183.5400). Median improvements do not imply consistent paired wins. Simple restarts are prior art and not a new theorem or algorithmic breakthrough.

## Latest closest theory
Chaudhry, Scheinberg and Sun (2026) prove complexity results for Powell-style interpolation and random-subspace model-based trust regions, including a noisy case (arXiv:2609.09441, preprint). Chaudhry and Scheinberg (2025) address complexity of model-based derivative-free methods (arXiv:2510.14935, preprint). These significantly narrow any claim of new complexity guarantees. The official COBYQA documentation describes a quadratic interpolation model-based trust-region SQP method. See references/phase17_verified.bib.

## Reproducibility
Exact executed local phase17.py SHA256 b00eeb876190dd24c15eca45b3730357640233048afd90e4fb4a7fb300b4475b.
Raw CSV SHA256 75c7d16616b338c6223dd6c45a2c689da9615ba1377a4ab38b13ff0c7bcc7c79.
Summary CSV SHA256 53dfba2b7acb1fc5719a6ebea497f8d0bfec334fc5074e032319680ed1770fe9.
Environment JSON SHA256 596c5cde2a1c449dbda6109df7dab422685fc232ff3fd50edb45f86db7847b49.
The GitHub source and summary have been uploaded; check source SHA before asserting exact byte identity. Original local raw CSV is not yet committed to GitHub. A workflow can regenerate and commit the outputs, but its run status must be checked.

## Q1 verdict
Not Q1-ready as a new optimizer. No demonstrated superiority over modern baselines, no proven new theorem beyond recent literature, no official COCO results, only eight seeds per family/dimension. Next best: stop manual restart heuristics, derive and test a nontrivial *predictive certificate for when restarting is worthwhile* with held-out calibration and explicit oracle cost; compare to COBYQA, CMA-ES and BOBYQA on official COCO.
