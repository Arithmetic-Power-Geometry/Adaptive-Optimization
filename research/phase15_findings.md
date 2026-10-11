# Phase 15: 480-run bounded-noise experiment and theorem audit
Date 2026-10-11

## Frozen design and implementation
3 dimensions (2,5,10) × 2 geometries (diagonal, rotated) × 10 new seeds (500–509) × 2 deterministic noise levels (0,0.01) × 4 algorithms (Adaptive, NaiveFD, NoiseAwareFD, Powell) = 480 runs. 160 objective evaluations maximum per run. Common initial point and objective per matched problem. Quadratic Hessian eigenvalues geometric 1..100. Noise is bounded deterministic function delta*sin(17.3*sum(sin(3.1*x))+11.7*sum(cos(2.7*x))); objective meter records the best **true** objective at evaluated points. The noise-aware finite difference uses two symmetric evaluations and threshold delta/h, and accepts only observed decreases >2delta; it does not enforce general nonquadratic Hessian assumptions. No official COCO/BBOB or CMA-ES in this phase.

## Median best true objective under noise delta=0.01 (lower is better)
| d | geometry | Adaptive | NaiveFD | NoiseAwareFD | Powell |
|---|---|---:|---:|---:|---:|
|2|diagonal|0.000491|0.000273|0.001097|0.000261|
|2|rotated|0.051865|0.184252|0.536055|0.000121|
|5|diagonal|0.00314|0.01297|0.01096|0.00042|
|5|rotated|0.63101|1.20818|1.18115|5.62494|
|10|diagonal|0.45193|1.92308|2.00892|0.00991|
|10|rotated|3.61703|10.07833|10.09153|23.63694|

Noisy paired wins against Adaptive over 60 matched instances: NaiveFD 17/60, NoiseAwareFD 12/60, Powell 38/60. NoiseAwareFD is NOT superior. Without noise, NoiseAwareFD and NaiveFD coincide and both win only 7/60 vs Adaptive. No statistical significance claim.

## Theory
See research/phase15_theory.md. The two-probe directional sign and >2delta acceptance bounds are correct under explicit oracle and smoothness assumptions but are standard robust finite-difference results, not demonstrated original theorems. The observed algorithm does not produce a Q1-level breakthrough.

## Reproducibility
Exact local executed source: phase15.py SHA256 13880e078bb2158abac7177032c51445c4b29f7627f440a24242f756adfaddda.
Raw CSV SHA256 f947373b163480e5997076ecb3036e04e9c1ad15e37c426c09fa45e4805e5ac8 (480 rows).
Summary CSV SHA256 0e24ef3b3e9b2f07717ca42c44f944e16f5cab55379b5d9c93937c8f32f2b308.
Environment JSON SHA256 6aaad48c70364a7e2e7a30a1d76908e6a710b9e37cd16a29749f217d14bcec81.
Exact raw/source stored as conversation artifacts locally; repository-only reproduction incomplete until they are committed.

## Publication verdict
No general algorithmic superiority, no new complexity bound, no confirmed theorem novelty, no official BBOB. Not Q1-ready as novel optimizer. The main honest contribution is an explicit robustness/speed tradeoff with negative numerical evidence. Next milestone: rigorous theory of optimal certificate cost under noise, and official benchmark with CMA-ES/Py-BOBYQA, NOT a claim of breakthrough.
