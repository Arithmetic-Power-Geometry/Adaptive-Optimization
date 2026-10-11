# Phase 21 — APG curvature-filtered symmetric polling: exact experiment
Date 2026-10-11. 288 newly executed runs. 4 shifted/rotated functions × 3 dimensions (2,5,10) × 6 independent seeds (1100–1105) × 4 methods (APGCurvature, SymmetricPoll, COBYQA, Powell). Hard maximum 160 function evaluations per run. No official COCO/BBOB.

## Proposed mechanism
At current x and coordinate e_j, sample f(x+h e_j) and f(x-h e_j), estimate g_j=[f(x+h e_j)-f(x-h e_j)]/(2h), c_j=[f(x+h e_j)+f(x-h e_j)-2f(x)]/h². If c_j>10^-8, query bounded secant step t=clip(-g_j/c_j,-2h,2h), accept only true objective improvement. Otherwise, reuse the best of the two symmetric probes. After success h increases by factor 1.15, else halves. This is a derivative-free coordinate quadratic interpolation heuristic; **not yet a novel theorem**. A direct symmetric-poll control removes only the interpolated step.

## Results
| Method | Paired wins vs COBYQA (72) | Wins vs SymmetricPoll (72) | Mean objective calls |
|---|---:|---:|---:|
| APGCurvature | 14 | 40 | 159.375 |
| SymmetricPoll | 13 | 0 | 158.778 |
| COBYQA | 0 | 54 | 104.194 |
| Powell | 12 | 43 | 147.097 |

APGCurvature wins against COBYQA by function: Ackley 9/18, Rastrigin 2/18, Griewank 1/18, Rosenbrock 2/18. Selected medians: Ackley d5 APG 1.280407 vs COBYQA 5.921653; Ackley d10 APG 3.809217 vs COBYQA 3.882072; Rastrigin d10 APG 52.048037 vs COBYQA 30.346158; Rosenbrock d10 APG 161.970420 vs COBYQA 37.260285. APG curvature improves its control in 40/72 paired problems but does not dominate modern COBYQA.

## Reproducibility
Executed script SHA256 8778eb1030ffe50297b676e23890f79ae2db7f7f8047c6b6fb43610507536a0f.
Raw CSV SHA256 09249a301993da5786fa04806a85071e56d760649d180bae413e557b3a002c66.
Summary CSV SHA256 bef98e1e314c879709b36bb18a68c09034177b540e32fec70c0fb37089af9b93.
Environment JSON SHA256 e1efb6c3110b81225a2545e4204dd3f3a3bb6ae8e246194920def71e5e1af16e.
Git blob exact match verified: 28138faf0b332c1d55eaa32b1807a9362669570d. Raw outputs remain local until GitHub CI execution is confirmed.

## Closest verified literature
Ragonneau and Zhang (2024) prove optimality of an interpolation set for model-based DFO, DOI 10.1080/10556788.2024.2330635; PDFO 2024, DOI 10.1007/s12532-024-00257-9, is an established Powell model-based solver package; Ascia et al. (2025) report FuRBO, PMLR vol 293, 2/1–28. This mechanism overlaps established finite-difference/quadratic-interpolation ideas. A new theorem and substantially broader benchmarking are necessary.

## Q1 gate
**Not Q1-ready as a novel superior optimizer.** Strongest new experimental signal is the Ackley-family conditional performance and 40/72 wins over the symmetric control. No proof of original oracle complexity and no robust COBYQA superiority. Next experiment: independently preregister a classifier for Ackley-like geometry, validate on unseen functions and official COCO, include the cost of selecting the algorithm, and compare against a competitive portfolio with equal wall-clock and evaluation budgets. Avoid cherry-picking families.
