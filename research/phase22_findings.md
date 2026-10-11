# Phase 22: Helix Search — changed mechanism and independent evaluation

## Definition
A two-coordinate direction v=(cos(theta),sin(theta)) embedded in a randomly chosen coordinate plane, with theta advanced by 2*pi*(sqrt(5)-1)/2 each iteration. Query +/- h*v, accept the first strict improvement; update h by 1.08 after improvement and 0.7 otherwise. Unlike Phase 21, no curvature estimate or quadratic interpolation is used. Unlike Phase 19, no power-weighted direction memory. This is an **implemented candidate heuristic**, not proven original.

## Frozen experimental design
4 shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock) x 3 dimensions (2,5,10) x 8 seeds (1200–1207) x 4 algorithms = 384 runs. Maximum 160 objective calls per run, same starting point for matched runs. Comparators: random-axis +/- poll, SciPy COBYQA, SciPy Powell. These are synthetic test problems, not official COCO/BBOB.

## Results
Helix beats random-axis in 59/96 matched instances, COBYQA in 17/96; Powell beats COBYQA in 21/96. COBYQA beats random-axis in 79/96. Mean actual objective calls: Helix 155.677, RandomAxis 158.042, COBYQA 107.156, Powell 145.063. Median objectives: Rastrigin 2D Helix 8.45713, COBYQA 9.45208; Rastrigin 5D Helix 19.40163, COBYQA 20.39660; Rosenbrock 10D Helix 101.23384, COBYQA 46.57292. Performance is family-dependent; the paired-win rate does not establish broad superiority.

## Reproducibility
Exact executed source Git blob 975213b27f37a0c54d71b2a8198fccb37e8e9a49 verified against GitHub.
SHA256 source 1e4eae1f8219c00ccde4a9320261d28b33e25a32198092cb517d67160d889dc9.
SHA256 raw CSV e30085fc61bb9a3e823a4c1808359defda51ab82ca64ce081b2d2d9de38ffafa.
SHA256 summary CSV 20a8993411f2fb5452be62f0bc49add54f4de7873cc88b2fea5927716103e3eb.
SHA256 environment 54afeedf0ff4620860f80e25829681c2236590ad39b24ab06b7ab5bf6549def5.
Exact raw CSV and summary exist in local artifacts. GitHub Actions workflow is intended to reproduce and commit them; completion is unverified.

## Closest literature and novelty limits
Ha and Shashaani (2025), IISE Transactions 57(5), 541–555, DOI 10.1080/24725854.2024.2335513, already combine coordinate-based diagonal trust-region models and direct search. Ragonneau and Zhang (2024), PDFO, DOI 10.1007/s12532-024-00257-9, document Powell model-based methods. Chaudhry, Scheinberg and Sun (2026), arXiv:2609.09441, develop modern Powell-style complexity bounds. Rotating directions and irrational angular sequences require additional originality checking before novelty can be claimed.

## Mathematical limitation
The golden-angle sequence is dense on the circle for a fixed coordinate plane, but the implementation selects planes randomly, adapts h, and stops at a finite budget. Density alone gives neither a global convergence guarantee nor an oracle-complexity bound. This is not yet a Q1-ready novel optimization method.

## Next pre-registered experiment
Compare golden-angle vs rational-angle vs random-angle under the **same plane sequence**, include deterministic orthogonal poll safeguarding and a COBYQA baseline, and evaluate on official COCO/BBOB. Count actual calls and report data profiles across targets and function-family clusters.
