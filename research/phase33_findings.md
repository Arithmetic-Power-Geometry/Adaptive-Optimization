# Phase 33 — finite-budget value-of-information gate

## Question
Can a distribution-free lower confidence bound on normalized improvement justify spending additional objective evaluations on global search rather than a local model-based method?

## Mathematically valid but non-novel bound
After a first-stage incumbent with value tau, independently draw n=16 points uniformly on K=[-5,5]^d. Let Y_i=min(1,max(0,(tau-f(X_i))/(1+|tau|))) in [0,1]. Conditional on first-stage history, Y_i are iid with fixed mean mu. Hoeffding gives P(mu < mean(Y)-sqrt(log(1/alpha)/(2n)) | history)<=alpha. With alpha=0.05 the radius is ~0.306. The gate spends 20 more uniform evaluations iff max(0,mean(Y)-radius)>0.01. This is a valid certificate for **expected normalized gain per random probe**, not a certificate that global search outperforms continuation of COBYQA. It does not include the local opportunity-cost distribution; therefore it cannot support the stronger optimal allocation claim.

## Actual experiment
192 locally executed runs = 4 shifted/rotated synthetic families (Ackley, Rastrigin, Griewank, Rosenbrock) x dimensions 2,5,10 x held-out seeds 2300–2303 x 4 methods. Max 160 function evaluations. Baseline: standalone COBYQA. PilotOnly: first stage up to 80 COBYQA evaluations + 16 diagnostic uniform probes + remaining-budget COBYQA. AlwaysGlobal: PilotOnly plus 20 further global probes. VOIGate: further 20 probes only if the confidence certificate passes. Same starting point per instance; best-ever objective retained. Pilot sample and decision costs counted. This is not official COCO/BBOB.

| Method | Wins vs COBYQA | Losses | Ties | Mean evaluations |
|---|---:|---:|---:|---:|
| COBYQA | 0 | 0 | 48 | 103.7083 |
| PilotOnly | 9 | 14 | 25 | 137.7917 |
| AlwaysGlobal | 9 | 20 | 19 | 146.0625 |
| VOIGate | 9 | 14 | 25 | 137.7917 |

VOIGate triggered **0/48**. Average normalized pilot gain was 0.000418677; the one-sided 95% radius was approximately 0.306. No observed advantage over PilotOnly and no general COBYQA superiority. Note that pilot and portfolio methods spend more evaluations on average, even when objective values tie.

## Reproducibility
Exact executed source SHA256 f6ee20eed1274dea942e3522c850d8ec72158e25aadbe23e8308312f7f99e24a; Git blob e72d20ad458ae49f7b2d7dba87d53010e7ac8d21, verified identical with committed source.
Raw CSV SHA256 b43efc6721672252c67bb4285b392d848b4795924f0e684318e93967bede0352.
Summary CSV SHA256 15ff69e69ad342cf3d778116577b1a1daa475f37d9e9ecdce38894e690f1d210.
Environment SHA256 8944999a624380a8669cef55e570373c1779a6afb36dd2e9b2afc89fcfc33301.
Local executed raw data and environment available. GitHub Actions workflow provided to regenerate/commit full raw data; execution not yet confirmed.

## Closest verified literature
Moré and Wild (2009), SIAM J Optim 20(1):172–191, DOI 10.1137/080724083: finite-budget data profiles.
Shashaani, Hashemi and Pasupathy (2018), SIAM J Optim, DOI 10.1137/15M1042425: ASTRO-DF adaptive sampling trust regions.
Ha and Shashaani (2025), IISE Transactions 57(5):541–555, DOI 10.1080/24725854.2024.2335513: iteration complexity and finite-time adaptive sampling.
Ma et al. (2025), Computational Optimization and Applications 92:889–921, DOI 10.1007/s10589-025-00686-9: model-and-search derivative-free optimization.
These are publisher-grounded records. Hoeffding confidence inequalities are classical.

## Research gap and next hypothesis
A distribution-free bounded-gain certificate is often vacuous under a strict diagnostic budget. To establish a nontrivial novel guarantee, the algorithm must bound **the difference** between global-search benefit and local continuation opportunity cost, not merely global benefit. A defensible next study could target a restricted class where smoothness or prior trajectory information supplies a nontrivial lower bound on global improvement and an upper bound on local benefit. Validate any theorem against counterexamples, and benchmark against full-budget COBYQA, identical-cost PilotOnly, AlwaysGlobal, and an independent official COCO/BBOB suite.

## Q1 gate
**Not Q1-ready as a new optimizer**. No original theorem, no benchmark dominance, no official COCO validation, and the adaptive gate never activated. The negative result is reproducible and suitable as a documented ablation, not a standalone breakthrough.
