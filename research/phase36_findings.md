# Phase 36 — costed gradient-screened subspace ablation

## Hypothesis and prior-work gap
Evaluate whether 16 objective evaluations devoted to estimating a descent direction can improve an eight-dimensional random embedding enough to outperform fixed Embed8 and Embed16. The method is a **screening ablation**, not an original algorithm or new theorem. Active-subspace discovery is established (Constantine 2015); random-subspace optimization with convergence theory is established (Dzahini & Wild 2024, 2026).

## Experimental design and results
Locally executed 144 runs: Sphere and Rastrigin ridge functions f(x)=g(Q^T x-s), ambient d=20,60, effective rank r=4,12,20, seeds 2600,2601,2602, methods COBYQA, Embed8, Embed16, Screen8. All methods capped at 120 objective calls. Screen8 spends 16 evaluations on eight paired central directional differences with h=0.05, includes their projected gradient in an eight-dimensional subspace, and optimizes in the remaining budget. The controls optimize from matched starts. No objective evaluations are free.

| r | Embed8 vs COBYQA wins/losses | Embed16 | Screen8 |
|---|---|---|---|
| 4 | 12/0 | 9/3 | 12/0 |
| 12 | 6/6 | 7/5 | 6/6 |
| 20 | 6/6 | 6/6 | 6/6 |
| Total | 24/12 | 22/14 | 24/12 |

Direct comparison with Embed8:
| r | Screen8 wins/losses/ties | Embed16 wins/losses/ties |
|---|---|---|
| 4 | 2/7/3 | 0/12/0 |
| 12 | 3/9/0 | 12/0/0 |
| 20 | 9/3/0 | 12/0/0 |
| Total | 14/19/3 | 24/12/0 |

The selected high-dimensional low-rank regime reproduces fixed embedding's advantage over ambient COBYQA, but **Screen8 fails to beat Embed8 overall**. Embed16 is superior to Embed8 when r=12 or 20 and worse when r=4. A new adaptive dimension selector remains unproved.

## Reproducibility and important provenance limitation
Local executed source SHA256 ffa88c95d3c685faf0c0fcd8f8d29b5ea4aac75d94d5767f11c2e32d120b8ace; local Git blob 3260e7dd85f883e1c58012e1a6df3414668bda70.
Raw CSV SHA256 14a223c8816ef763c85c8ed42e3d1f593bc26dd433f119107485708943844cb8.
Summary CSV SHA256 4c5ed041df67a33ad7925e9c53e5404f3018692f91b5b438f3e44804e1bd9736.
Environment SHA256 33788d6f9243a867c977a00c49909b38c07b8c046a9026ecec8a754bb254d1f4.
**The committed GitHub source is a transcription and its Git blob b35ef2bde1880b1ce77fed1ad5a75b2c2b2b3aac is not byte-identical to the executed local source.** The exact local executed source and raw observations remain available for audit. The GitHub Actions workflow will independently generate and commit its own outputs when executed; its execution is not yet verified. Do not claim that the existing raw observations came from GitHub.

## Literature and novelty
Constantine (2015), Active Subspaces, SIAM, DOI 10.1137/1.9781611973860; Dzahini & Wild (2024), SIAM J Optim 34(3):2671–2699, DOI 10.1137/22M1524072; Dzahini & Wild (2026), Mathematical Programming, DOI 10.1007/s10107-026-02404-7. These sources show that derivative-free dimension reduction, subspace discovery and random-subspace convergence theory are not new. The comparison does not include STARS, StoDARS, REMBO, CMA-ES or official COCO/BBOB.

## Research decision
No Q1-level new optimizer established. Next best work: a *theorem-first* budgeted dimension selector with independently estimated spectral tail uncertainty and a cost-aware choice between k=4,8,16 and ambient optimization, including full-rank controls, more seeds and modern subspace competitors. Avoid using true r to choose k, since that leaks synthetic generator information.
