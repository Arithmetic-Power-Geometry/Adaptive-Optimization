# Phase 32 — mathematical gap mining and equal-volume stratification

## Completed experiment
192 locally executed calls = 4 shifted/rotated functions (Ackley, Rastrigin, Griewank, Rosenbrock) × dimensions 2/5/10 × seeds 2200–2203 × four methods. Max 160 objective evaluations per method, same initial points. First 100 COBYQA evaluations, then 20 probes, then remaining-budget COBYQA. Uniform: iid on K=[-5,5]^d. Stratified: 20 independent samples, one per equal-width slice along first coordinate and uniform on remaining coordinates. Gaussian: N(best_incumbent,I). Baseline standalone COBYQA. All methods retain best observed objective. Synthetic benchmark, not official COCO/BBOB.

| Method | Wins vs COBYQA | Losses | Ties | Mean evaluations | Mean improving probes |
|---|---:|---:|---:|---:|---:|
| COBYQA | 0 | 0 | 48 | 106.8125 | 0 |
| Uniform | 7 | 20 | 21 | 140.4583 | 0.0625 |
| Stratified | 7 | 20 | 21 | 140.6667 | 0.2292 |
| Gaussian | 10 | 20 | 18 | 141.3958 | 0.3750 |

Tolerance 1e-10. No overall benefit over COBYQA or uniform probing.

## Mathematical statement (classical, not a novel theorem)
For a fixed measurable A subset of K, divide K into m equal-volume disjoint measurable strata K_j. Independently sample X_j uniformly from each K_j and let p_j=P(X_j in A), p=m^{-1}sum_j p_j. The stratified estimate p_hat=m^{-1}sum_j 1_A(X_j) is unbiased and has variance m^{-2}sum_j p_j(1-p_j) <= p(1-p)/m, the iid uniform Bernoulli sample mean variance. Proof: p_j(1-p_j) is concave, so Jensen yields m^{-1}sum_j p_j(1-p_j)<=p(1-p). This applies to the fixed threshold from stage one, independent stage-two samples. It says NOTHING about improved final optimization objective. The experiment uses stratification along one coordinate, not an optimal partition.

## Prior art / novelty barrier
Zhang et al. (ICML 2023 BALLET) already estimate adaptive regions of interest with regret analysis. Chen et al. (UAI 2017) already optimize information value with regret bounds. Ha & Shashaani (IISE Transactions 2025) already develop finite-time adaptive sampling trust-region analysis. Ding, Rinaldi & Vicente (Optimization Online 2025) study sequential test sampling. Therefore neither Lebesgue sets, stratification, nor simple cost-of-information gates alone constitute a Q1 breakthrough.

## Reproducibility
Local executed source SHA256 ca3fdc1a1f02d4d7efe7261c2a33900906cb2b0d60030172b2f2530e38213a5e.
Local raw CSV SHA256 2ccdd79f069c77349804a0ffb38e718663f4342880e26adff9dd2ca6a5b3fb7a.
Local summary CSV SHA256 9c448ab168452ce1dc63b39e0c27763bc4c36ded3bc7afbac56086aa2dc92fb0.
Environment SHA256 4eb667a37d00e5d5d3293186c2d1e155bbd1e963924272079e27e6afeee73da3.
**GitHub source is a semantically equivalent transcription, NOT verified byte-identical to executed local source.** GitHub source Git blob 6fc27ccb53ff11d08f6596778fc88d2694c3012b vs local Git blob b0d8caaa68f0b52162edb7334d354734cdc6df6e. A workflow has been committed to independently reproduce and archive the complete results; do not treat it as completed without verifying its run.

## Publication gate
No original theorem, no verified benchmark superiority, no independent official COCO/BBOB results. Not Q1-ready as a novel general-purpose optimization algorithm. Most defensible next work: prove a genuinely new finite-budget decision guarantee that links measurable improving-set probability, improvement magnitude, estimation cost, and local-search opportunity cost; then preregister and evaluate on independent COCO/BBOB and real expensive objective problems.
