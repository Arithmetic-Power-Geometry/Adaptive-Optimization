# Adaptive Optimization Phases 1–25: evidence ledger (2026-10-11)

Phases 1–6: adaptive/memory/gated polling: mixed performance.
7–11: held-out experiments, Powell baselines, weak robust advantages.
12: finite-transcript ambiguity construction; originality not established.
13: finite-difference sign/descent certificates; known techniques.
14: LineMemory replication weak.
15: bounded-noise conditional certificates.
16: COBYQA outperforms AdaptivePoll in 48/48 noiseless and 45/48 noisy quadratics.
17: two-start COBYQA only 16/96 wins vs COBYQA.
18: plateau-triggered restart never activates.
19: APG power polling 22/120 wins vs COBYQA.
20: power-exponent ablation fails to support weighting.
21: curvature polling 40/72 vs symmetric control but only 14/72 vs COBYQA.
22: helix polling 59/96 vs random-axis but 17/96 vs COBYQA.
23: golden angle 43/72 vs rational and 41/72 vs random; source GitHub/local mismatch disclosed.
24: **independent replication**: golden 105 wins/100 losses/35 ties vs rational, 104/104/32 vs random, 39/177/24 vs COBYQA on 240 matched instances (960 runs). Phase 23 apparent advantage did not replicate. Exact executed Phase 24 source Git blob verified. Full local raw CSV SHA256 42f43f15e71adf9082a17214d737b3319a3ca4c223f264734308ee2614c0b5d6; CI raw publication pending.
25: **official COCO/BBOB pilot configured but not yet executed/verified**. Code at experiments/phase25/phase25_coco.py and workflow .github/workflows/phase25_coco.yml; do not report BBOB results without raw outputs.

## Novelty gate
Van Dyke 2014, DOI 10.1155/2014/619249, establishes equal-angle direct-search polling. Ragonneau and Zhang 2024, DOI 10.1007/s12532-024-00257-9, establish PDFO baselines. No novel theorem, no reproducible golden-angle advantage, no verified official BBOB result. **Not Q1-ready as a new general-purpose optimizer.** Future effort should target a genuinely new theorem or narrower empirical study, not another arbitrary heuristic.
