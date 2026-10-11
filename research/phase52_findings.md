# Phase52: Gaussian curvature effective-rank estimation

## Mathematical formulation
For an exactly quadratic function f(x)=f(0)+0.5*x^T H x with H positive semidefinite, and z ~ N(0,I), Y=f(z)+f(-z)-2f(0)=z^T H z. Standard Gaussian quadratic-form identities yield E[Y]=tr(H) and Var(Y)=2 tr(H^2). Therefore r_eff=(tr H)^2/tr(H^2)=2 E[Y]^2/Var(Y). For an orthogonal projector H=QQ^T of rank r, r_eff=r. These are known identities; NOT a new theorem, and r_eff is not the algebraic rank for a general PSD spectrum.

## Executed test
20-dimensional random orthogonal projectors, true ranks 2,4,8,20; 100 independent replications each; probe counts 16,32,64,128,256. 2000 records. RNG seed 520000 + rank*1000 + replication. Estimator 2*(sample mean)^2 / unbiased sample variance. Code executed locally with NumPy; synthetic quadratic values computed analytically as sum((zQ)^2). The stated 2n+1 function-call cost applies to actual black-box central differences with one shared f(0), NOT to the direct-matrix simulation.

| rank | n=16 median relative error | n=64 | n=256 |
|---|---|---|---|
|2|0.3534|0.1681|0.0806|
|4|0.3213|0.1316|0.0720|
|8|0.2950|0.1192|0.0704|
|20|0.2478|0.1169|0.0572|

At n=64, black-box cost 129 evaluations exceeds the previous B=120 optimization budget. This is a NEGATIVE feasibility result for the naive diagnostic. No full optimizer with diagnostic was run in this phase.

## Reproducibility
Executed script SHA256 007bbc854a9ace7665e7235d47cb96adf4c980534904e8c1e0d520853491ef59.
2000-row raw CSV SHA256 a760714305645f45c7d2f6752c52fdf40b6c59abf2223cf49dd06bddbf6b9223.
20-row summary SHA256 01f93e19ad7936dfa0c53a6354049d24b2cd6135d4b4d61b90f63120ce495a13.
Raw files generated locally; GitHub source and summary committed, raw upload not yet verified.

## Novelty and next gate
The effective-rank identity is established. Empirical observation: probe accuracy increases with evaluation cost. The potential new contribution would require a provably budget-beneficial policy, cheaper curvature-information reuse, or an estimator with a new bound and validated improvement over strong baselines. Current Q1 novel optimizer verdict: not yet. Do not represent known identities as original theorems.

## Verified closest work
Cartis and Roberts (2026), Optimization Methods and Software, DOI 10.1080/10556788.2025.2601668: random subspace quadratic models and second-order convergence. Bellavia, Gratton, Morini, Toint (2026), Journal of Optimization Theory and Applications 209, article 63, DOI 10.1007/s10957-026-03004-3: random-subspace objective-function-free optimization. Dzahini and Wild (2026), Mathematical Programming, DOI 10.1007/s10107-026-02404-7: stochastic random-subspace direct search. All from primary publisher sources. Distinguish their objectives and assumptions from the present black-box quadratic probe study.
