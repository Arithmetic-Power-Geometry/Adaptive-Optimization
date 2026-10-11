# Literature gap register — 2026-10-11

## Research scope
Deterministic and stochastic derivative-free box-constrained global optimization, expensive objective evaluations, dimensionality, constrained/noisy/mixed-integer extensions, and reproducible benchmarking.

## Verified closest prior art
1. Jones, Perttunen & Stuckman (1993), DIRECT: potentially optimal rectangle selection, DOI 10.1007/BF00941892. New adaptive region selection must be differentiated from this work.
2. Storn & Price (1997), differential evolution, DOI 10.1023/A:1008202821328. Standard stochastic global-search baseline.
3. Hansen & Ostermeier (2001), covariance-matrix adaptation, DOI 10.1162/106365601750190398. Important missing baseline for the exploratory study.
4. Wolpert & Macready (1997), No Free Lunch, DOI 10.1109/4235.585893. Forbids unrestricted superiority under stated assumptions.
5. Namura & Takemori (2025), Regional Expected Improvement for Efficient Trust Region Selection in High-Dimensional Bayesian Optimization, AAAI 39(18), 19624–19632, DOI 10.1609/aaai.v39i18.34161. Trust-region acquisition/selection is already studied.
6. Zaryab, Manno & Martelli (2025), SCR, an efficient global optimization algorithm for constrained black-box problems, Optimization and Engineering 26, 1863–1893, DOI 10.1007/s11081-024-09943-y. Constrained surrogate+CMAES hybrids already exist.
7. COCO benchmarking framework, Hansen et al. (2019), DOI 10.5281/zenodo.2594848. Standard benchmark suite and evaluation methodology.
8. Benchmarking Derivative-Free Global Optimization Algorithms Under Limited Dimensions and Large Evaluation Budgets, IEEE Transactions on Evolutionary Computation 29(1), 187–204, DOI 10.1109/TEVC.2024.3379756. Large algorithm comparison, 25 methods; metadata authors not independently confirmed in this audit and intentionally omitted from BibTeX.

## Hypothesis targets (NOT verified open problems)
- Adaptive polling benefits coordinate-separable, axis-aligned objectives, but may fail under rotations and ill-conditioning.
- A statistically justified switching rule between coordinate polling and population-based exploration may reduce evaluations for a restricted function class.
- Any certified global claim requires valid global lower bounds, not merely heuristic incumbent improvements.

## Missing dimensions and next tests
COCO BBOB 24 functions, 2/5/10/20/40 dimensions, shifted/rotated/ill-conditioned, noisy, constrained, mixed-integer, expensive objectives; CMA-ES, local BFGS where derivatives allowed, surrogate and Bayesian baselines; >=20 seeds, fixed objective budgets, target hitting times, ECDF and confidence intervals, ablation, parameter sensitivity and runtime.

## Important benchmark caveat
SciPy DIRECT's maxfun is approximate. Enforce hard cap at the objective wrapper and retain best-so-far history. In SciPy 1.17.0 a StopBudget exception propagating through the compiled DIRECT wrapper may become SystemError; the exploratory harness catches it after exactly the cap, but this is not a recommended production integration.
