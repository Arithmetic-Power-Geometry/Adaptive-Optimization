# Phase 20: independent arithmetic-power exponent ablation
Date: 2026-10-11

## Frozen comparison
4 synthetic shifted/rotated functions (Ackley, Rastrigin, Griewank, Rosenbrock) × 3 dimensions (2,5,10) × 5 new seeds (1000–1004) × 6 methods (NoMemory, P0, P1, P2, P4, COBYQA) = **360 executed runs**. Budget 180 objective evaluations, shared start per instance. The exponent changes ONLY the sampling weights of successful-direction memory, (gain+1e-9)^p, not the coordinate safeguard. This is an ablation, not official COCO/BBOB.

## Exact paired wins (60 matched problems)
| Method | Wins vs COBYQA | Wins vs uniform-memory P0 | Mean evaluations |
|---|---:|---:|---:|
| NoMemory | 17 | 39 | 179.067 |
| P0 | 17 | 0 | 180 |
| P1 | 17 | 18 | 180 |
| P2 | 16 | 19 | 180 |
| P4 | 16 | 14 | 180 |
| COBYQA | — | 38 | 110.867 |

Wins defined as best objective strictly lower than comparator by >1e-10. Ties/non-wins are not all losses. No p>0 shows a majority advantage over p=0, and NoMemory outperforms P0 on 39/60. COBYQA consumes substantially fewer evaluations on average and achieves better objective on 38/60 compared with P0. Strict cap is identical, actual consumed budgets differ; this favors COBYQA in evaluation efficiency.

## Reproducibility
Exact executed source SHA256 725df5e9b52e8ccee02e390cd293b33605b481e1ccdb81bbca0bbbbac1598c2e
Raw 360-row CSV SHA256 0daea0c3f332d477a5fb93e5544e9077da09f48ccfb99aa69aa43bf10a5e0a2d
72-row summary SHA256 003d91a16ee31a3fad8470f66dd96186e14fb3d8d9338dc8e0466377cfc544d9
Environment JSON SHA256 d93536fec3c8afb634477181bab5312c98383219243ca5cd59965e133197b5bd
Python 3.13.5; NumPy 2.3.5; SciPy 1.17.0. Exact source Git blob verified. Raw data local, workflow configured to commit results but CI success has not been verified.

## Theory
The p-weighted sampling distribution is well-defined and scale-invariant only without the regularizer. For gains g_i>0 and p>0, if the largest gain is at least k times each other gain, its probability is at least k^p/(k^p+m−1). Elementary proof: bound the denominator by g_max^p(1+(m−1)/k^p). This is not a novel oracle-complexity theorem and does not guarantee better optimization.

## Verified closest literature
Audet & Dennis (2006) introduced MADS directional polling and asymptotic dense directions; erratum (2008). Hansen et al. (2021) established COCO benchmarking protocol and official BBOB test suite. See phase20_verified.bib. Existing master BibTeX retains 2025–2026 model-based prior art.

## Research verdict
The Phase 19 APG PowerPoll proposal has failed the direct power-exponent ablation. **No verified algorithmic novelty or Q1-level performance superiority.** Do not claim power weighting improves convergence, robustness, or oracle complexity. The most defensible paper at present is a negative comparative study with reproducible experimental methods, not a Q1 breakthrough algorithm paper. Further work should shift to a clearly differentiated theorem and COCO evaluation, not further tuning on these same families.
