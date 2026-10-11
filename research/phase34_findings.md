# Phase 34 — high-dimensional low-intrinsic-dimensional black-box optimization

## Motivation and precise experimental hypothesis
COBYQA's quadratic interpolation models operate in ambient d-dimensional space, but some black-box objectives depend on a much smaller unknown effective subspace. Test whether a fixed random eight-dimensional embedding followed by COBYQA improves performance over ambient-space COBYQA with equal objective-call budgets. **This is a test of established random-embedding methodology, not a new algorithm.** Selection of this dimension regime followed repeated failures in earlier phases; report that selection transparently to avoid post-hoc generalization.

## Problem generator
f(x)=g(Q^T x - s), with Q in R^{d x 4} having orthonormal columns from QR of a seeded Gaussian matrix, s in [-2,2]^4. Four base functions: Sphere, Rastrigin, Rosenbrock, Ackley. Ambient dimensions d=20,40,60; seeds 2400 and 2401. Start x0 uniform [-1.5,1.5]^d. Embed8 uses A=QR(G) with G Gaussian d x 8 and solves min_z f(x0+A z) via COBYQA; full COBYQA and Powell optimize in ambient space. Same x0 and at most 100 objective evaluations each; best-ever objective recorded.

## Completed local results
72 runs, 24 matched instances (4 functions x 3 dimensions x 2 seeds), 3 methods.
| d | Embed8 wins/losses vs COBYQA | Powell wins/losses vs COBYQA |
|---|---|---|
| 20 | 6/2 | 3/5 |
| 40 | 6/2 | 3/5 |
| 60 | 8/0 | 8/0 |
| Total | 20/4 | 14/10 |
All methods used 100 calls. Differences use absolute tolerance 1e-8. This pilot identifies a strong **regime-specific empirical benefit** of random embedding. Only two seeds per function/dimension; no confidence claim or Q1 performance claim is justified.

## Mathematical observation
If the unknown effective subspace has rank r=4, then for an independently sampled continuous random d x k embedding A with k>=r, the r x k matrix Q^T A has rank r with probability one. Thus for any target latent coordinate y in R^r, there exists z in R^k with Q^T(x0+A z)-s=y. The embedded problem can represent every latent target, even though k<<d. This is a standard generic-rank consequence, NOT an original theorem. Finite-budget optimization and numerical conditioning are not guaranteed. The random embedding may be poorly conditioned.

## Closest prior art
Dzahini & Wild (2024), SIAM Journal on Optimization 34(3):2671–2699, DOI 10.1137/22M1524072: random-subspace trust-region methods with convergence and complexity. Hansen & Ostermeier (2001), Evolutionary Computation 9(2):159–195, DOI 10.1162/106365601750190398: covariance adaptation; Hansen, Mueller & Koumoutsakos (2003), Evolutionary Computation 11(1):1–18, DOI 10.1162/106365603321828970. More random embedding, REMBO, and effective-dimension literature must be reviewed before claiming novelty. The current 8-dimensional embedding is a straightforward baseline, not a breakthrough.

## Reproducibility
Executed local source SHA256 5a9d42de3dcbecd28b081975475cb5f7370d596c9e69881e5976e9333d95a7b9.
Git blob 8c67663c4b9b24ffa7b94289a3d2b55a323671bd (verified identical to committed GitHub source).
Local raw CSV SHA256 ab511eceab57e9f569fa384452d5116bac067995892673945a548709f22687f0.
Local summary SHA256 0c0a65c03bbb5de6f8e2c902205d5ab3d2dcc20fb63dfd4506493209128bc036.
Local environment SHA256 5984d0df34434b6efb0d8893bbb763e616a01e79e74c2f020a1893e4aad2cb69.
Local raw observations exist; GitHub workflow committed to regenerate and archive, but not yet verified as executed.

## Next research and publication gate
**Not Q1-ready as a novel algorithm.** This is a positive benchmark result in a constructed class that favors low-rank methods. A serious next phase must (1) replicate on 20+ independent seeds and official COCO/BBOB high-dimensional cases, (2) include random-embedding baseline, REMBO, random-subspace trust-region STARS, CMA-ES, Powell, and COBYQA, (3) test full-rank negative controls and increasing effective dimension r, (4) report wall-clock overhead, numerical rank/conditioning, data profiles and uncertainty intervals, and (5) develop and prove an actually new adaptive dimension-selection guarantee if possible.
