# Phase 30 — Lebesgue-measure-motivated probe portfolio

## The mathematical premise
Let K be a bounded measurable set with 0 < lambda_d(K) < infinity and A_tau={x in K: f(x)<tau} measurable. Uniform iid X_1,...,X_m on K satisfy P(min_j f(X_j)<tau)=1-(1-lambda_d(A_tau)/lambda_d(K))^m. This identity is classical and does NOT establish a novel algorithm. A genuinely adaptive algorithm would need to estimate the unknown improving-set measure with uncertainty, account for all probe costs, and select actions accordingly. **The current implementation does not estimate Lebesgue volume; it samples from a uniform distribution.**

## Actual matched experiment
Four shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock), dimensions 2,5,10, seeds 2000–2003, four methods: 192 executed runs on 48 matched problems. Budget 160 objective calls per method; same initial points. COBYQA baseline; Uniform searches in [-5,5]^d; LebesgueProbe uses 100 COBYQA calls, 20 uniform probes in [-5,5]^d, and remaining COBYQA calls from best observed point; GaussianProbe substitutes 20 Gaussian probes around incumbent (standard deviation 1 per coordinate). This is a synthetic benchmark, not official COCO/BBOB.

| Method | Wins vs COBYQA | Losses | Ties | Mean evaluations |
|---|---:|---:|---:|---:|
| COBYQA | 0 | 0 | 48 | 108.44 |
| Uniform | 7 | 41 | 0 | 160.00 |
| LebesgueProbe | 7 | 21 | 20 | 141.00 |
| GaussianProbe | 6 | 21 | 21 | 140.96 |

Tolerance for wins/losses: 1e-10. No broad superiority, and volume-based novelty is unproven. Because the baseline terminates early on many cases, using a full 160 calls in portfolios does not demonstrate better efficiency. The bounded uniform probe region is a sampling design, not an enforced constraint on COBYQA iterates.

## Executed reproducibility and exact provenance
Source SHA256 2959e48b0902b3774f04c56895d18702b42d9c18bc8c4ecd455d76eaabd499a7
GitHub source Git blob a66cc7a1bfea5976ea212fd1ec84ebd8743e4bf4 (verified exact match).
Raw CSV SHA256 61b2860d8b919747b885b47c1a156fce1a9edfa5d9ee4521a6efcf8318b77ff8
Summary CSV SHA256 107444b2b90b693e34e4ddc4371f945b0ba78a077c7103dacdc8950cfd7b7a91
Environment JSON SHA256 d10084948c36cdbc7d0da5457556f5e3274571a0011b305707cd7e5e6c92200b
Executed local raw/summary/source/environment and log retained. GitHub workflow provided for reproduction and upload; do not claim it ran until confirmed.

## Prior art and originality
Random search and probability of descent are established (Gratton et al., 2015, DOI 10.1137/140961602; Larson et al., 2019, DOI 10.1017/S0962492919000060). Evaluation-budget comparisons require data profiles (Moré and Wild, 2009, DOI 10.1137/080724083). Literature on measurable improving sets and uniform random search also predates this phase. A novel result must go beyond the elementary success-probability identity.

## Publication gate
**Not Q1-ready as a novel optimizer.** No new theorem, no certified measure estimator, no COBYQA dominance, and no completed official COCO/BBOB evaluation. Next substantive work: construct an uncertainty-calibrated confidence interval for improving-set measure, derive an evaluation-cost-aware decision rule with a rigorous performance bound relative to a specified comparator, and test it on held-out official COCO problems. An adaptive claim must be compared against a non-adaptive identical-cost uniform baseline and a Gaussian control.
