# Phase54 — joint curvature/stationarity diagnostic; critical research audit

## Scope
Synthetic PSD quadratic f(x+z)=f(x)+g^Tz+0.5z^THz, d=20, H=QQ^T orthogonal rank-r projector, r in {2,4,8,20}, ||g|| in {0,1,5}, 100 independent repetitions per cell, 32 Gaussian probes. 1200 total trials. Evaluated quadratic terms analytically, not actual black-box calls. If implemented on an objective oracle, 32 pairs plus shared f(x) require 65 evaluations.

## Exact identities
D(z)=f(x+z)-f(x-z)=2g^Tz; S(z)=f(x+z)+f(x-z)-2f(x)=z^THz.
For z~N(0,I), E[D²/4]=||g||², E[S]=tr H, Var(S)=2tr H², and E[D S]=0. Thus paired probes simultaneously estimate gradient norm squared and curvature effective rank. The gradient norm estimator is unbiased under exact quadratic assumptions; the finite-sample ratio for effective rank is NOT generally unbiased. These identities are established algebra and Gaussian moments, not independently novel theorems.

## Actual measured outcomes at ||g||=5
| rank | median one-sided rank relative error | median symmetric rank relative error | mean estimated ||g||² (true 25) |
|2|0.953801|0.210172|24.70736|
|4|0.895508|0.149750|24.66934|
|8|0.860896|0.199533|25.14550|
|20|0.713265|0.176318|25.67071|

At gradient norm zero, one-sided and symmetric rank measurements agree identically in these exact quadratic simulations. The paired estimator does not save evaluations compared with symmetric probing; it extracts additional information from the same samples. No optimizer was run in Phase54, so do not report end-to-end performance benefit.

## Reproducibility
Local source SHA256 ec908ae645b6a0d73488f81e5c4253e8f0ca29bab7e4f2908b2792272ea9d061; raw CSV 0262c40cbf1bdf7fb8836511022b78a6f1f7b47582ad4f5f710f026b1b3333a0; summary CSV 1e33dd25a01da77d59261b3a36de95ca36a9bfa3bcd4f4fbcd78035b264bb214. Raw observations are available as local generated files. Source and findings committed to GitHub; CI and exact GitHub artifact run not verified.

## All-dimensions publication audit
- Mathematical correctness: exact under quadratic assumptions; general smooth nonquadratic case needs finite-difference remainder and step-size bounds.
- Computational budget: 65/120 calls =54.2% of former benchmark budget; likely too costly as a generic first step.
- Optimization performance: no new end-to-end optimizer tested.
- Prior art: Hutch++ trace estimation assumes a matrix-vector product oracle; do not equate that oracle cost to zeroth-order function evaluation cost. Prior randomized subspace DFO also precludes broad novelty claims.
- Generality: nonconvex indefinite H, noisy f, nonlinear gradient, bounds, scaling, high d, and COCO/BBOB not tested.
- Novelty: paired statistics are a possible ingredient in a new cost-aware switching rule, not an original theorem on their own.
- Q1-ready original optimization paper: not established.

## Hard next gate
Derive a finite-step bias/error guarantee for C^3/C^4 functions with bounded derivatives, add a risk-controlled budget gate, and compare against COBYQA, CMA-ES and sequential embeddings on verified official BBOB with all probe evaluations charged. Do not produce additional toy heuristics without meeting these gates.

## Literature
Meyer, Musco, Musco, Woodruff (2021) Hutch++: Optimal Stochastic Trace Estimation, SIAM J Matrix Anal Appl 42(3),1195–1219, DOI 10.1137/20M1366792; Qian, Hu, Yu (2016) sequential random embeddings IJCAI 1946–1952; Hansen et al. (2021) COCO Optimization Methods and Software 36(1),114–144, DOI 10.1080/10556788.2020.1808977. Existing verified.bib contains these; do not duplicate.
