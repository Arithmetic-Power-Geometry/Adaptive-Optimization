# Phase 12 — Independent theorem construction and rotated-quadratic stress test

## Experiment
Executed 480 objective-optimization runs: 3 dimensions (2,5,10) × 2 geometries (diagonal, rotated) × 20 independent seeds × 4 methods (Adaptive, Memory, LineMemory, Powell), strict 180 objective-call cap. Quadratic f(x)=(x−s)^T H (x−s), eigenvalues 10^linspace(0,4,d), orthogonal Q from seeded QR for rotated cases, shift s uniform [-1,1]. LineMemory performs symmetric two-point probes and one candidate evaluation using the exact quadratic line formula. It is not a global optimizer or a novel line-search theorem. All methods use the same initial point for each matched problem.

## Median final objective, rotated problems
| Dimension | Adaptive | Memory | LineMemory | Powell |
|---|---:|---:|---:|---:|
| 2 | 1.706583 | 1.716277 | 0.981987 | 1.36576e-22 |
| 5 | 42.312483 | 41.301202 | 35.177212 | 45.635936 |
| 10 | 300.760306 | 298.595373 | 294.742648 | 643.130046 |

## Median final objective, diagonal problems
| Dimension | Adaptive | Memory | LineMemory | Powell |
|---|---:|---:|---:|---:|
| 2 | 7.25973e-12 | 9.83167e-12 | 1.29891e-14 | 5.06795e-26 |
| 5 | 0.00871239 | 0.02445513 | 0.01739152 | 1.54027e-25 |
| 10 | 27.854435 | 37.644978 | 35.567858 | 1.53570e-24 |

LineMemory lower median than Adaptive on 3/3 rotated cases but only 1/3 diagonal cases. 5D rotated median reduction versus Adaptive = 16.86%; 10D rotated = 2.00%. No statistical significance or broad superiority established. Powell dominates diagonal problems and 2D rotated; on 5D/10D rotated it is weaker than LineMemory in this cap. Absolute target 1e-6 reached by Powell on 20/20 diagonal instances for each dimension, by LineMemory on 20/20 only for 2D diagonal.

## Theory
See research/phase12_theorems.md. Proposition 1 is an explicit finite-transcript ambiguity construction for strongly convex smooth objectives. Proposition 2 is classical exact quadratic interpolation. Neither can be honestly claimed a literature-new theorem without a focused prior-art audit.

## Readiness
A mathematical proposition is now formulated and proved, but Q1 algorithm-paper readiness is NOT established: no official COCO run, no novel complexity bound, no independent confirmation, and no clear superiority over strong baselines. Full local raw CSV and exact executed script must be committed for repository-only reproducibility; summary and source record are available as conversation artifacts.
