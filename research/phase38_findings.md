# Phase 38 — budgeted sequential independent random embeddings

## Executed results (local, 2026-10-11)
192 runs, 48 matched problems: two objective families (rotated/shifted ridge Sphere and Rastrigin), ambient d=20 and 60, intrinsic r=4,12,20, seeds 2800–2803, budget 120 objective calls. COBYQA, Embed8, Embed16, Restart8. Restart8 optimizes in a random eight-dimensional subspace for at most 60 calls and then draws a fresh independent eight-dimensional subspace anchored at the best incumbent, spending remaining budget. All objective calls charged; no access to the true rank when selecting methods.

| r | Embed8 wins/losses vs COBYQA | Embed16 wins/losses | Restart8 wins/losses | Restart8 wins/losses vs Embed8 |
|---|---|---|---|---|
| 4 | 16/0 | 11/5 | 16/0 | 2/14 |
| 12 | 9/7 | 9/7 | 10/6 | 16/0 |
| 20 | 8/8 | 8/8 | 8/8 | 15/1 |
| Total | 33/15 | 28/20 | 34/14 | 33/15 |

Wins/losses use objective-value tolerance 1e-8. All methods share starting points and budgets; some optimizers terminate early. The 33/48 overall restart wins are exploratory because the algorithm and test class were developed after observing earlier experiments; not independent validation.

## Theorem (standard rank argument; not novel)
Let f(x)=g(Q^T x) where Q is d-by-r orthonormal. For A in R^{d x k} drawn from an absolutely continuous random matrix distribution, rank(Q^T A)=min(r,k) almost surely. If k>=r, every latent vector can be represented by the embedding; if k<r, a single embedding cannot cover all latent vectors. The proof is that the determinants of maximal minors are nonzero polynomials in entries of A and hence vanish with probability zero. This is established REMBO mathematics, not a novel theorem.

## New interpretation, limitations
Two independent 8-dimensional subspaces can improve finite-budget performance when r>8, but the improvement is not a universal guarantee. In particular, Restart8 loses to Embed8 in 14/16 r=4 cases. Sequential random embedding and adaptive dimension changes already appear in Qian, Hu & Yu (IJCAI 2016) and Qian et al. (IJCAI 2026). These papers preclude a novelty claim based on restarting in independent subspaces.

## Reproducibility
Local exact executed source: SHA256 b4154fdd2d952287406ffba05b2e010b6e9d775839422bedc50a0cb2336d0a96, Git blob 3c4c737bd6349bb3631221202ec0a1a8c12ff947.
Raw local CSV: SHA256 f67c43f5c6b8c36f08505227ec641c8a4607dffdcde608c619a4ceb82bdcba88.
Summary local CSV: SHA256 f7e3cf81091e6317dceae0659fff95bfa3336f79ca2cae55fba756892d4b7406.
Environment: SHA256 9dd6f443d751772dd0eca79970a411a5f5fb90e535726e021a975519fafdb6cd.
The GitHub implementation is a separately transcribed semantically equivalent version (Git blob 1b1454e61b860325ec18008b27700de5886cfabd), not byte-identical. The workflow should generate and archive fresh data from the GitHub version; its successful execution is not yet confirmed. Do not misattribute local data to GitHub Actions.

## Publication decision
Not Q1-ready: no new mathematical theorem; sequential random embeddings already known; selected synthetic family and four seeds insufficient; official COCO/BBOB and competitive SRE/DSEBO/STARS/CMA-ES baselines missing. Best next question: derive a cost-aware **precommitted** stopping/restart certificate under explicit distributional assumptions, compare with DSEBO's regret theory, and test on independent functions. Do not claim novelty until theorem and closest-prior-work proof audit.
