# Phase 18: held-out warm-start/restart comparison and integrity audit

Date 2026-10-11. 54 **newly executed** runs, 3 families (Ackley, Rastrigin, Rosenbrock), dimensions 2/5, seeds 800–802, three methods, budget 90 objective calls per method. Shifted/rotated synthetic functions, not official COCO/BBOB. Methods: standard COBYQA 90 evaluations; fixed two-stage 54+36 with a perturbed second start; plateau-triggered two-stage 54+36 with plateau defined as <1% improvement over previous 30 incumbent observations. When plateau false, it invokes a **new** COBYQA solver at the best observed point, which is a warm restart and **not** uninterrupted continuation.

## Measured result
FixedRestart beats standard COBYQA on only 1/18 paired instances, with 18/18 fixed restarts. PlateauRestart beats COBYQA on only 2/18 instances, and its plateau trigger fires **0/18** times. Therefore the adaptive restart decision is untested in the positive-trigger regime and has not demonstrated benefit. Tiny n=3 per family/dimension, exploratory only; no significance claim.

## Theory / closest literature
Scheinberg (2026), ICM Proceedings Vol. 7, pp. 208–228, DOI 10.1137/25M1806016, derives evaluation complexity bounds for model-based trust regions including inexact oracles, random subspaces and Powell-style geometry correction. Ma et al. (2025), Computational Optimization and Applications 92:889–921, DOI 10.1007/s10589-025-00686-9, benchmark Model-and-Search on 501 public problems. These directly preclude treating ordinary model switching, restarts or generic complexity bounds as novel.

## Reproducibility
Exact executed phase18.py SHA256 17799658b0e1b5573803fc8deec3635698b3e8f4631f8c3c84de09dde4249b62, raw_results.csv SHA256 bed7609d1d94ef7100e347fd3458f97f1703f2a992218825253a388ecda46202, summary.csv SHA256 ac386d1e8fa8509faf2072c5e73caaff50498a8a82a552c9aa082772c56d1ba3, environment.json SHA256 a1c39f89b2f3be43a3c7934a2ec94695133e210fa89e99a6a29c66142644283d. Executed source committed and Git blob verified. GitHub summary committed; raw CSV needs workflow success and SHA verification.

## Phase 17 correction
Local Phase 17 summary was found empty despite 384 raw results. Reconstructed from raw CSV: 48 summary rows; paired wins RestartCOBYQA 16/96, Powell 19/96, DE 16/96. The published aggregate totals remain supported. Regenerated local summary SHA256 10dbe65b2ca4aa03c0d2541037092dad0cf9b07cb59d789904131894fd6aef3b. Do not present the previously empty local file as a valid summary.

## Q1 readiness
No demonstrated new algorithmic theorem, no performance superiority over COBYQA, no official COCO/BBOB. **Not Q1-ready as a novel optimizer.** The right next step is a genuinely testable decision rule that triggers in a prespecified fraction of cases, with held-out evaluation, matched baseline and appropriate model-switching prior-art separation.
