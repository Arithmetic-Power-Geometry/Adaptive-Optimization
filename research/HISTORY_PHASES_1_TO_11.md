# Optimization research history, Phases 1–11 (2026-10-11)

| Phase | Study | Evidence-based verdict |
|---|---|---|
| 1 | Adaptive coordinate poll | Unfair DIRECT budget in first pilot |
| 2 | Strict-budget fixed/adaptive vs DE/DIRECT | No consistent dominance |
| 3 | Randomly rotated polling | Some gains and major regressions |
| 4 | Coupling trigger | No win over adaptive across 12 median settings |
| 5 | Directional memory | Wins in 3/9 median settings |
| 6 | Gated memory | ~93.6% fewer *memory probes*, not objective evaluations |
| 7 | Held-out 960-run target study | At 240 calls: Adaptive 262/320, Memory 263/320 |
| 8 | Budget sweep (reanalyzed Phase 7) | At 120 calls: Memory 235/320 vs Adaptive 214/320, exploratory post hoc |
| 9 | Independent seeds 200–209; 960 runs; Powell and DE | At 240: Adaptive 133/240, Memory 141/240, Powell 162/240, DE 81/240 |
| 10 | Paired bootstrap on Phase 9 | Memory +3.33 pp vs adaptive at 240, naive instance-bootstrap CI +0.42 to +6.25 pp |
| 11 | Family-level dependence audit, official BBOB implementation | Cluster bootstrap 95% interval ~0 to +5.83 pp with only four families; BBOB workflow prepared, not verified |

## Strongest scientific claim
MemoryPoll has a conditional advantage over AdaptivePoll on selected synthetic tests. It is weaker than Powell in the Phase 9 aggregate. GatedMemory saves directional probes, but total evaluation benefit is unproven. Existing MADS/direct-search prior art constrains novelty claims.

## What would constitute a breakthrough?
A clearly original method with mathematically justified guarantees beyond existing derivative-free search, or large, reproducible, independently confirmed COCO/BBOB improvements over strong baselines under equal budgets. Neither has been achieved.

## Current action
Official COCO/BBOB pilot code and GitHub Actions workflow are committed. No successful CI run or official BBOB measurements verified. Full raw Phase 9 files are still not committed; the family-level CSV and analysis findings are in the repository. Reproduction and validation remain required before manuscript submission.
