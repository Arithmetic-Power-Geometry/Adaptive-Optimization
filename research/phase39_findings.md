# Phase 39: held-out independent-seed replication, 384 local runs

## Experiment
A continuation of Phase 38 using a new seed block 2900–2907 and a tighter **80 objective-call cap**. Two ridge families (Sphere, Rastrigin), ambient dimensions d=20,60, intrinsic dimensions r=4,12,20. Four algorithms COBYQA, Embed8, Embed16, Restart8 (two independent eight-dimensional stages, 40 calls each, second stage anchored at best incumbent). This is 96 matched instances, 384 actual runs. Same seeded starts, all objective evaluations charged.

## Exact local results
| r | Embed8 wins/losses vs COBYQA | Embed16 wins/losses | Restart8 wins/losses | Restart8 wins/losses vs Embed8 |
|---|---|---|---|---|
| 4 | 30/2 | 24/8 | 28/4 | 5/27 |
| 12 | 16/16 | 18/14 | 17/15 | 30/2 |
| 20 | 17/15 | 20/12 | 17/15 | 30/2 |
| Total | 63/33 | 62/34 | 62/34 | 65/31 |

No ties for nonidentical methods at tolerance 1e-8. 80 is a strict upper bound; actual average calls at r=20 were COBYQA 76.56, Embed8 70.22, Embed16 74.625, Restart8 79.9375. The outcomes are not a fair statement of per-evaluation efficiency unless plotted as anytime/data profiles. Restart8 wins 60/64 against Embed8 for r=12 and 20, but only 5/32 for r=4. Across all r, Restart8 wins 62/96 vs COBYQA, less than Embed8 63/96. The regime is selected from previous experiments; this is new seeds but NOT independent problem-family selection.

## Mathematically established and prior work
For a ridge objective f(x)=g(Q^T x), a random k-dimensional embedding A with k>=r has rank(Q^T A)=r almost surely, whereas k<r cannot span the entire latent space. Standard linear algebra, already part of REMBO literature. Sequential random embeddings already studied by Qian, Hu and Yu (IJCAI 2016). DSEBO (Qian et al. IJCAI 2026) adaptively changes embedding dimensions with regret analysis. Cartis and Roberts (Optimization Methods and Software, published online January 2026, DOI 10.1080/10556788.2025.2601668) analyze randomized subspace DFO with quadratic models and second-order convergence. Bellavia et al. (Journal of Optimization Theory and Applications 209(2), article 63, May 2026, DOI 10.1007/s10957-026-03004-3) establish random-subspace optimal-complexity results for objective-function-free optimization (a different information model). No new theorem is established by Phase 39.

## Exact local provenance
Executed source: /mnt/data/adaptive_phase39/phase39.py, SHA256 8d3566711bb1190b4cfe8cf5d4196c8bd3677d85007d119df64bdfe20c2e9e43.
Raw CSV: SHA256 d72500690310c19bff297f2beb8c9e4732e6f97190cd3486ce3292230371dd53.
Summary CSV: SHA256 40f7158c49fc3fe4ce6c0a5b75d815c24bcddf023e04833c4aa3d1d1724aab19.
Environment JSON: SHA256 7be6e2bac811c858daf0ba78c4823e86341c8adf82c92f94744731082d6671b6.
GitHub source is a separately transcribed implementation; **do not claim byte identity**. GitHub Actions reproduction is configured to generate its own raw observations, but execution is unverified.

## Next stage and Q1 readiness
**Not Q1-ready.** The positive conditional empirical phenomenon is replicated, but the method is known and no original mathematical result exists. A credible paper would require comparison against the 2016 sequential embedding method, 2026 DSEBO, Cartis–Roberts random-subspace quadratic models, STARS, and standard derivative-free baselines, on COCO/BBOB and independently selected real tasks. The next theorem-first target is a cost-aware restart decision bound that is strictly stronger than established sequential embedding theory and explicitly accounts for rank uncertainty and evaluation overhead.
