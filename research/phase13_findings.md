# Phase 13: strong numerical-gradient baseline stress test

Date 2026-10-11. **600 newly executed runs**, 3 dimensions (2,5,10), 2 geometries (diagonal/rotated), seeds 20–39 (20 per configuration), five methods (AdaptivePoll, quadratic-interpolated historical-line heuristic labeled CertifiedLine, Powell, numerical-gradient BFGS, numerical-gradient L-BFGS-B), hard cap 180 objective evaluations, equal local start point. Each BFGS/L-BFGS-B finite-difference gradient evaluation is charged as objective calls. Source and full raw results generated locally in /mnt/data/adaptive_phase13; repository does not yet contain the exact executed source or raw CSV.

## Median final objective on rotated ill-conditioned quadratics
| d | Adaptive | CertifiedLine | Powell | BFGS | L-BFGS-B |
|---|---:|---:|---:|---:|---:|
| 2 | 0.845846 | 1.147804 | 2.6653e-23 | 1.7030e-10 | 7.5660e-11 |
| 5 | 52.432442 | 40.413239 | 66.387714 | 1.7415e-10 | 6.5125e-10 |
| 10 | 233.859908 | 194.023339 | 374.228389 | 26.931096 | 5.960595 |

## Median final objective on diagonal ill-conditioned quadratics
| d | Adaptive | CertifiedLine | Powell | BFGS | L-BFGS-B |
|---|---:|---:|---:|---:|---:|
| 2 | 1.3207e-11 | 2.2016e-15 | 1.0655e-25 | 5.5507e-13 | 2.4993e-13 |
| 5 | 0.006948 | 0.013600 | 1.5384e-25 | 6.0806e-13 | 5.4130e-9 |
| 10 | 29.601224 | 22.277343 | 1.4832e-24 | 4.104513 | 2.491428 |

## Interpretable result
CertifiedLine is 22.92% lower median objective than Adaptive in rotated 5D and 17.03% lower in rotated 10D, but worse in rotated 2D and diagonal 5D. In rotated 5D/10D it also beats Powell, while numerical-gradient BFGS/L-BFGS-B are substantially better. At target f<1e-6, rotated 5D BFGS hits 20/20 and L-BFGS-B 19/20; neither polling method hits. No general superiority, no statistical significance claim, and no official BBOB performance.

## Reproducibility hashes
Exact locally executed phase13.py SHA256 d0e939be12a9b7a7b27d142c43624bebb221a356e52f67900c669f2754fe11a9; raw_results.csv SHA256 92a37886b1d28a743fa47d210435026b353c15421d5eea2c1297f1c549a0a564; summary.csv SHA256 8462b53a62bc003ea61fe78db49383bf3909f0f709c803e88b1651cd118fac80. Python NumPy 2.3.5 SciPy 1.17.0.

## Literature and Q1 gate
2025 Model-and-Search (Ma et al.) already hybridizes model-based and direct search. 2025 BBOB workshop compares PDFO solvers and CMA-ES/BFGS. 2024 JMLR work establishes gradient-free convergence rates and lower bounds. A Q1 novel-algorithm claim requires a distinctly new result beyond these, verified official COCO/BBOB and stronger baselines. This phase is not Q1-ready.
