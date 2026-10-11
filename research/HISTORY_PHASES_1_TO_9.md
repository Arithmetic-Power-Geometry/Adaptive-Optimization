# Optimization research programme — cumulative history, Phases 1–9

| Phase | Tested mechanism | Outcome |
|---|---|---|
| 1 | Adaptive coordinate poll | No novelty; DIRECT budget not equal |
| 2 | Strict-budget adaptive vs fixed poll/DE/DIRECT | No consistent superiority |
| 3 | Random rotated polling | Some rotated Ellipsoid gains, severe Rastrigin regressions |
| 4 | Two-coordinate coupling gate | No median win vs Adaptive in 12 settings |
| 5 | Directional memory | Improved 3/9 median settings, regressed 6/9 |
| 6 | Memory probe gate | ~93.6% fewer memory probes, not total evaluations |
| 7 | Held-out target success, 960 runs | At 240 evaluations: Adaptive 262/320, Memory 263/320, Gated 263/320 |
| 8 | Reanalysis across budgets | At 120 evaluations: Adaptive 214/320, Memory 235/320; post-hoc exploratory |
| 9 | New 960-run experiment, seeds 200–209, Powell and DE included | At 240: Adaptive 133/240, Memory 141/240, Powell 162/240, DE 81/240 |

## Best validated performance claim
In a held-out but synthetic Phase 8 budget slice, directional memory gained 21/320 target hits at 120 evaluations relative to adaptive coordinate polling; the gain was post-hoc and nearly vanished at 240. In a new Phase 9 seed range and additional 10D configurations, MemoryPoll gained 8/240 at 240 evaluations, but Powell won by 21/240 against MemoryPoll. A gate reduces memory-probe overhead without proven overall savings.

## Publication audit
No demonstrated novel optimization principle, theoretical global guarantee, or consistently superior optimizer. Not presently Q1-ready as a novel optimization algorithm paper. The research could be developed as a transparent evaluation of budget-aware directional reuse after proper official COCO/BBOB validation, modern baselines, uncertainty analysis and code/data provenance. Existing COCO and CMA-ES literature must be compared and cited.

## Data provenance
Phases 1–8 details in research/HISTORY_PHASES_1_TO_8.md. Phase 9 ran locally and produced raw_results.csv, summary.csv and phase9.py in conversation artifacts. The committed results/phase9_aggregate.csv reports aggregate results only; raw data and exact executed source are NOT yet committed to GitHub. No GitHub CI success is claimed.
