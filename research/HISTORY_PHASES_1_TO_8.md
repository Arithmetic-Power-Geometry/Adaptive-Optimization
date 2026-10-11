# Research history and evidence ledger — phases 1–8
Date: 2026-10-11. This is an internal factual research record, not a claim of external peer review.

| Phase | Hypothesis or method | Evidence | Verdict |
|---|---|---|---|
| 1 | Coordinate adaptive poll (CGCP) | 2D/5D small synthetic study, nominal 400 evaluations; DIRECT overshot cap | Unfair budget for DIRECT; no novelty |
| 2 | Strict-budget adaptive/fixed polling vs DE/DIRECT | 300 runs, 2/5/10D, four axis-aligned functions, 5 seeds, cap 300 | DIRECT strong on axis-aligned center-optimum tests; no dominance |
| 3 | Rotate polling directions after stagnation | 180 runs, shifted/rotated functions, 5 seeds, cap 300 | Some improvements on Ellipsoid/Rosenbrock; large regression on 2D Rastrigin |
| 4 | Two-coordinate mixed-difference coupling trigger | 300 runs, 2/5D, 5 seeds, cap 240 | 0/12 median wins over AdaptivePoll |
| 5 | Reuse exponentially weighted successful steps (MemoryPoll) | 180 runs, shifted/rotated, 5 seeds, cap 300 | 3/9 median wins over AdaptivePoll; conditional benefit |
| 6 | Gate directional memory probes (GatedMemory) | 1200 runs, 2/5/10D, 10 seeds, cap 240 | ~93.6% fewer *memory probes* than MemoryPoll; not total evaluations; 4/24 wins vs Adaptive |
| 7 | Held-out seed target hits | 960 runs, seeds 100–119, 2/5D, cap 240 | Successes Adaptive 262/320, Memory 263/320, Gated 263/320 |
| 8 | Evaluation-budget sweep of phase-7 raw hit times | Same 960 runs reanalyzed at 40/80/120/180/240, paired bootstrap | MemoryPoll +21/320 target hits at budget 120; +1/320 at 240. Post-hoc budget selection limits inference |

## Novelty and Q1 readiness
- Proven novel mathematical mechanism: **none**.
- Proven global convergence / better complexity: **none**.
- Strongest conditional observation: memory-assisted polling has an intermediate-budget advantage in the held-out synthetic study (120 evaluations; 235 vs 214 successes), but advantage vanishes at 240 (263 vs 262).
- Gating memory probes is efficient in *probe count* but loses the intermediate-budget success advantage (217/320 at 120).
- The claimed 120-budget confidence interval is exploratory; the budget was selected after examining five budgets and function/instance dependence may reduce effective sample size.
- Q1-level novel algorithm paper: **not supported** by evidence so far. Q1-level benchmarking paper would require official COCO/BBOB, strong methods (CMA-ES, MADS, BOBYQA), multiple targets, independent reruns, statistics with multiplicity and instance dependence handled, and transparent negative results.
- No evidence of better total evaluations, wall-clock, or universal robustness. Do not claim them.

## Next research design (frozen before running)
Use official cocoex Suite('bbob', 'instances: 1-5', 'dimensions: 2,5,10') with all 24 functions; register fixed target precisions and budgets in advance; benchmark Adaptive, Memory, Gated, CMA-ES, DE and a model-based derivative-free baseline; 15+ instances or seeds; use official COCO Observer and cocopp postprocessing. Record all objective evaluations, hashes, environment, code version and failures. Use a separate holdout for any tuning.

## Source/verification
- Original phase-7 raw file is copied byte-for-byte into results/phase8_phase7_raw.csv, SHA-256 7b4e02c6512b002634da5c9eeaf93111855679f7f9c3fd9ba1f3b17f3d16d727.
- Phase-8 analysis code computes the exact five-budget success curves and paired bootstrap comparisons from that raw file. No new optimizer runs in phase 8.
- COCO 2021 journal paper metadata confirmed via publisher and COCO official repository DOI 10.1080/10556788.2020.1808977.
- COCO Performance Assessment arXiv:1605.03560 confirmed via arXiv; this is a preprint citation.
