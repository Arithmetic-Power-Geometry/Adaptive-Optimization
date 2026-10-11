# Phase 37 — finite-query identifiability boundary and costed dimension selection

## Key mathematical theorem: finite-query nonidentifiability (classical oracle indistinguishability)
For any deterministic adaptive algorithm that makes at most N<infinity noiseless function-value queries in R^d, there exist two C-infinity functions with identical entire observed transcripts such that one has effective dimension 0 and the other has effective dimension d.

Proof: Run the algorithm against f0(x)=0 and record its finite queries x^(1),...,x^(N). For each coordinate i choose a nonzero compactly supported C-infinity one-dimensional bump h_i with support in an open interval avoiding the finite set {x_i^(j):j=1,...,N}. Set f1(x)=sum_{i=1}^d h_i(x_i). Then f1(x^(j))=0 for every query, so the deterministic algorithm follows exactly the same transcript. f1 has effective dimension d: its Hessian is diagonal, and for each coordinate i there is a point where h_i'' is nonzero and the other coordinate second derivatives vanish; thus the span of all Hessian ranges is R^d, so no proper linear subspace can contain every direction of variation. Both functions are smooth. Therefore no uniformly correct finite-query intrinsic-dimension certificate exists on unrestricted smooth black boxes. The construction is **not a new discovery**; it is a standard adversarial finite-oracle indistinguishability argument. Randomized algorithms require a more careful distributional/minimax statement; this theorem is not asserted for arbitrary randomized algorithms.

## Experiment
192 executed runs, 48 matched instances: Sphere/Rastrigin ridge functions, d=20,60, r=4,12,20, seeds 2700–2703, B=120. Methods: full COBYQA, Embed8, Embed16, and Select8or16. Selector pays 16 calls for 8 symmetric finite-difference directions, computes second-half energy fraction of directional gradients, and chooses k=16 if fraction>0.45, else k=8. Fixed controls have no screening overhead. This is an intentionally falsifiable diagnostic, not a claimed original method. The 2026 DSEBO algorithm already addresses adaptive embedding dimensions.

| r | Embed8 wins/losses vs COBYQA | Embed16 | Selector |
|---|---|---|---|
| 4 | 16/0 | 14/2 | 11/5 |
| 12 | 8/8 | 8/8 | 9/7 |
| 20 | 8/8 | 8/8 | 8/8 |
| Total | 32/16 | 30/18 | 28/20 |

Selector vs Embed8: r=4:1/13/2 (wins/losses/ties); r=12:12/4/0; r=20:12/4/0; total 25/21/2. Selector chose k=16 in 11/16, 11/16, 8/16 cases for r=4,12,20 respectively, demonstrating that split-half directional gradient energy is NOT a calibrated rank detector. Average evaluations: Embed8 113.52, Embed16 114.81, Selector 115.46. In some instances COBYQA terminates early; compare both final objective and actual cost.

## Closest verified literature and novelty gap
Qian et al. (IJCAI 2026) DOI 10.24963/ijcai.2026/527 already provide Dynamic Shared Embedding Bayesian Optimization (DSEBO) with unknown effective dimension and a regret bound. Hare, Roberts, Royer (Mathematics of Computation, online 2024) DOI 10.1090/mcom/4011 already analyze expected decrease per evaluation in random subspaces. Dzahini & Wild (SIAM Journal on Optimization 2024) DOI 10.1137/22M1524072 already establish random-subspace trust-region convergence and complexity. Therefore no Q1-level algorithmic novelty has been established by this phase.

## Reproducibility
Executed local source SHA256 d8fa51729cd83835efd6a1fdb5b7ee5ed13c1e8c5e6e251f414aee22a0eb9bde; local Git blob 95b8ef3cde7ae3034741c27a1036d36cc4a8810b. GitHub source was manually transcribed; blob 0717fb01b2728e2facc69c9d6f41674c8e3c4262 differs. Do not claim byte-identical provenance. Raw CSV SHA256 acd3baee30a75d708ce485be69be839dffb90fa65a93cf2b7841dd3460291911. Summary CSV SHA256 87a893511b2e474fac7cfd2ede7cb7e4b8a4a40175bb0f58898c41150952eb3e. Environment SHA256 fd4e484bfa9e44fade0d9dc2221699ecf835110a3a78130e32d4c316fdf675fb. Workflow will regenerate results from GitHub source; its execution has not been verified. Exact locally executed source and CSV are available as local artifacts.

## Next defensible research step
If pursuing original mathematics, add an explicit structural assumption (e.g., low-rank ridge objective with bounded Hessian, nondegenerate gradient covariance, controlled noise, and quantitative spectral gap). Prove a **finite-sample cost-aware rank certificate under those assumptions** and compare against 2026 DSEBO, REMBO, STARS and established dimension-estimation algorithms. Under unrestricted C-infinity black-box access, exact finite-query rank certification is impossible. The present result is not Q1-ready.
