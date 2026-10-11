# Phase 53 — Cost-versus-bias of one-sided curvature probes

## Problem and mathematical result
Previous Phase52 Gaussian quadratic curvature effective-rank diagnostic costs 2n+1 black-box function evaluations, prohibitive at B=120. We tested whether one-sided probes reduce the cost. For f(x)=f(0)+g^T x+0.5 x^T H x with PSD H, z~N(0,I), symmetric Yc=f(z)+f(-z)-2f(0)=z^T H z; one-sided Yo=2[f(z)-f(0)]=z^T H z+2g^T z. Gaussian symmetry yields E[Yo]=tr H and Var(Yo)=2tr(H²)+4||g||²; Cov(z^THz,g^Tz)=0. Thus the population ratio 2E[Yo]²/Var(Yo) = (tr H)²/[tr(H²)+2||g||²], systematically **underestimates** curvature effective rank when g is nonzero. Symmetric probes eliminate g exactly. This exact bias identity is a mathematical consequence of known Gaussian moment identities, NOT a claim of a new theorem.

For H an orthogonal rank-r projector, the one-sided population estimate is r²/(r+2||g||²). For r=4 and ||g||=5 this equals 16/54=0.2963, whereas the true effective rank is 4. A one-sided probe cannot be treated as a curvature-only observation without a stationarity condition.

## Actual experiment
9600 locally executed estimator trials: d=20; ranks 2,4,8,20; n=8,16,32,64; gradient norm 0,1,5; 100 replicates per cell; both central and one-sided estimators. Shared Gaussian probes and same random Hessian per matched pair. One-sided evaluation cost n+1, central 2n+1. Simulation directly evaluates quadratic forms, so function-call costs are **hypothetical costs if deployed on a black-box objective**, not the number of matrix computations performed in this simulation.

For n32:
| rank | ||g|| | one-sided median relative error | central median relative error |
|---:|---:|---:|---:|
|2|0|0.180|0.180|
|2|1|0.563|0.180|
|2|5|0.961|0.180|
|4|0|0.218|0.218|
|4|1|0.331|0.218|
|4|5|0.928|0.218|
|8|5|0.847|0.182|
|20|5|0.696|0.214|

## Reproducibility
Source SHA256 8a07f4c22da3f3be5b46211c4a2f16ff516bf798205219d4832b2763b284d85d
Raw 9600 rows SHA256 de84a44e755fc6b1091e46a7600f5f4d84af1b19cb3273e98143b8e1001ef1c9
Summary 96 rows SHA256 d5647b86f1427116d855fed961f19edc0875249b93a468690678a9b602dca153
Environment SHA256 b6efc67bfffac32ece7cb21bdbf9acd1ab762cdd55674e26ac662f8583599ae5
The full raw CSV exists locally; GitHub Actions reproduction is configured but not confirmed executed.

## Novelty and paper gate
This is a verified negative ablation and an exact analytical explanation of why the cheap probe is biased. Gaussian trace estimation is well established (Hutchinson/Girard; Hutch++). The population identity is not a new contribution in isolation. There is no demonstrated improvement in end-to-end optimization over COBYQA, CMA-ES, or SRE, and no official COCO/BBOB result. Q1-level original optimizer is NOT established. Next target: prove a cost-aware decision threshold and design a stationarity-certified diagnostic with an explicit error bound; then compare full end-to-end performance with charged diagnostic calls.

## Primary literature
Meyer, Musco, Musco, Woodruff (2021), Hutch++: Optimal Stochastic Trace Estimation, SIAM Journal on Matrix Analysis and Applications 42(3), 1195–1219, DOI 10.1137/20M1366792. Martinsson and Tropp (2020), Randomized Numerical Linear Algebra: Foundations and Algorithms, Acta Numerica 29, 403–572, DOI 10.1017/S0962492920000021. Both provide prior art for stochastic trace estimation. Consult the primary published work and do not claim originality of the underlying moment estimator.
