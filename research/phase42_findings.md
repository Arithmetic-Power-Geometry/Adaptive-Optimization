# Phase 42: held-out budget-limited differential evolution comparison

## Protocol and execution
360 actual local runs, 90 matched cases. Three synthetic rotated ridge families (Sphere, Rastrigin, Rosenbrock), dimensions 8,20,40; ranks r=4 and r=d; five new seeds 3300–3304; methods COBYQA, SciPy differential_evolution (DE), Embed8, Restart8; strict 120 objective-evaluation cap. DE has bounds [-5,5]^d, popsize=5, no polish; other methods are unbounded. These are NOT directly equivalent domain constraints. No official COCO/BBOB run was possible locally because coco-experiment and cma packages were unavailable and local pip access failed. Official COCO benchmarking is the next essential test.

## Matched objective-value wins/losses/ties (1e-8 threshold)
| Regime | Embed8 vs COBYQA | Restart8 vs COBYQA | Restart8 vs Embed8 | COBYQA vs DE |
|---|---|---|---|---|
| low rank r=4, n=45 | 27/10/8 | 27/13/5 | 8/28/9 | 42/3/0 |
| full rank r=d, n=45 | 4/34/7 | 10/30/5 | 34/6/5 | 45/0/0 |

Full-rank COBYQA dominates both random-embedding strategies under this budget, especially in dimensions 20 and 40. The 120-evaluation cap is unfavorable to DE's dimension-dependent population size and therefore does not establish broad superiority to DE.

## Mathematical status and novelty
Rank(Q^T A)=min(r,k) almost surely for a random k-dimensional subspace, a known random embedding result. Restart8 helps in some higher-rank regimes, but is a sequential random embedding already in the literature. Phase42 is a negative control, not a new algorithm or theorem. The evidence establishes a *conditional performance tradeoff*, not an all-dimensional optimizer. Q1 novel-optimizer readiness: **NO**.

## Reproducibility and provenance
The exact locally executed Python source has SHA256 50e693e752a1c3b92a1a4061cc7db66d9b83c0424fd21f4bf6caeb70152775d9 and Git blob 07ddfe84f41795a8d180d2a6beaf865fcbc73693. GitHub fetched blob matched the local Git blob exactly. Full raw CSV SHA256 a90153e588063c4ed5c4cd29040ddc45976e8953e134f3577277aca470aa983c. Summary CSV SHA256 827d538589a28fcc0176967333b700211a907f90a550ebfd947af2327a380d70. Environment JSON SHA256 9f3ce97f9417fd62aba192459c51f7390d7d07429cb29191f6790106df286e6a. Per-dimension raw SHA256: d8 ae5d5e70a6bc408925ca7b82f05a5a04ac62f4878b3fef1c82a1a0df47b212bb; d20 e678db644cac0f3feaa51583180bd625275148fa412e4c9d3b48728206edf9d1; d40 a74d3c97da81c98dec50e352170e6485694af01eea546e5a65dfe605395891f9.

## Prior literature
Hansen and Ostermeier (2001), Evolutionary Computation 9(2):159–195, DOI 10.1162/106365601750190398, original CMA adaptation paper (MIT Press/PubMed verified). Hansen et al. (2021), Optimization Methods and Software 36(1):114–144, DOI 10.1080/10556788.2020.1808977, official COCO platform methodology. Existing sequential random embedding (IJCAI 2016) and adaptive embedding (IJCAI 2026) remain closest algorithmic prior art.

## Next scientific gate
Freeze algorithms, conduct official COCO BBOB with identical bounded-domain treatment, standardized target attainment, 20+ instances/seeds, sufficient evaluation budgets proportional to d, strong CMA-ES/STARS/RSDFO-Q/DSEBO baselines, and preregistered statistical analyses. The present 360 runs are not a substitute for that gate.
