# Phase 31: Lebesgue measure confidence gate — completed pilot

## Hypothesis and precise algorithm
For measurable K=[-5,5]^d and threshold tau equal to the incumbent objective after up to 80 COBYQA calls, p_tau=lambda_d({x in K:f(x)<tau})/lambda_d(K). Twelve iid uniform diagnostic probes yield k improving points. Compute a **one-sided 95% Clopper-Pearson lower bound** L=Beta^{-1}(0.05;k,13-k) for k>0, else L=0. When L>0.02, spend 20 more uniform probes; otherwise resume COBYQA. Always retain best observed incumbent. PilotOnly pays for the same 12 diagnostic samples without additional global probing; AlwaysGlobal always spends 20 more; COBYQA is standalone. The confidence guarantee applies only to the fixed conditional threshold and iid diagnostic sample, not to an adaptively reused sample or a claim about solver performance. No bound on comparative optimization regret is established.

## Completed held-out experiment
4 shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock) x dimensions 2,5,10 x seeds 2100-2103 x 4 methods = **192 executed runs, 48 matched problems**, global cap 160 function evaluations. This is a synthetic pilot, not official COCO/BBOB.

| Method | Wins vs COBYQA | Losses | Ties | Mean calls | Extra-global decisions |
|---|---:|---:|---:|---:|---:|
| COBYQA | 0 | 0 | 48 | 106.29 | 0 |
| PilotOnly | 7 | 19 | 22 | 135.35 | 0 |
| AlwaysGlobal | 10 | 21 | 17 | 144.44 | 48 |
| MeasureGate | 7 | 19 | 22 | 136.56 | 2 |

The gate fired in two cases: Ackley d=2 seed 2100 (6/12 improving, lower bound 0.24530), Rastrigin d=2 seed 2100 (2/12 improving, lower bound 0.03046). Compared with PilotOnly, MeasureGate yielded one strictly better result and no worse result at tolerance 1e-10, but increased average evaluations by 1.21; this is far too little to claim superiority. Against COBYQA it won only 7/48 and lost 19/48.

## Provenance
Executed source SHA256 c7e0686fb0cc5da08575014b9eba40bd154904af965af24e36b5b7d45a1745da
Source Git blob 324c3924a7a7c7f8a894952b34af135aece1b417 (byte-identical GitHub source verified).
Raw CSV SHA256 6cb04649af00c173e6f86e4206e8822a108a8f474a95140e72ed4b57b48c9aee
Summary CSV SHA256 f76e69d4154a6f673e5df94de6cc86cd978d7098b94f485c4dcf2b0af7c14f01
Environment SHA256 d758d080fd03b14712c404b2e4bcffb0882c9e21754712419f6fb1c0ad1cc142

## Novelty and prior work
The Lebesgue success-probability identity and Clopper-Pearson binomial interval are classical (Clopper & Pearson, Biometrika 1934, DOI 10.1093/biomet/26.4.404). Adaptive sampling with convergence/complexity analysis is already developed by Ha & Shashaani (IISE Transactions 2025, DOI 10.1080/24725854.2024.2335513) and by Rinaldi, Vicente & Zeffiro (SIAM Journal on Optimization, DOI 10.1137/22M1543446). The fixed confidence-triggered portfolio is a research prototype; novelty over these sources and other algorithm-selection methods is not established.

## Research gate
**Not Q1-ready as a novel general-purpose optimizer**: no new optimization guarantee, no dominance over COBYQA, insufficient independent instances, no verified official COCO/BBOB run. The next defensible direction is a mathematically nontrivial *value-of-information* guarantee for when a volume diagnostic should be purchased under finite budget, followed by broad independent benchmarks. Do not claim that the confidence interval alone is an original theorem.
