# Research history and novelty register, Phases 1–14
Updated 2026-10-11

| Phase | Main development | Scientific finding |
|---|---|---|
| 1 | Adaptive coordinate poll | Pilot DIRECT comparison had unequal budgets |
| 2 | Fixed/adaptive/DE/DIRECT | No consistent dominance |
| 3 | Rotated polling | Conditional gains, regressions |
| 4 | Coupling trigger | 0/12 median wins |
| 5 | Directional memory | 3/9 median wins |
| 6 | Gated memory | 93.6% fewer *memory probes*, not total evaluations |
| 7 | Held-out 960 runs | Adaptive 262/320 vs Memory 263/320 at budget 240 |
| 8 | Five-budget reanalysis | Memory 235/320 vs Adaptive 214/320 at 120, exploratory post hoc |
| 9 | New 960 runs incl. Powell | Adaptive 133/240, Memory 141/240, Powell 162/240 at 240 |
| 10 | Paired bootstrap | Small conditional benefit; Powell stronger |
| 11 | Family-level uncertainty, BBOB workflow | Cluster inference weak; official BBOB run unverified |
| 12 | Finite-transcript theorem, 480 runs | Constructive theorem valid, prior-art novelty unestablished; rotated gains conditional |
| 13 | Conditional finite-difference certificate, 600 runs | Rotated 5D/10D median gains but BFGS/L-BFGS-B much stronger |
| 14 | Independent 600-run replication (seeds 400–419, budget 240) | Rotated 5D gain collapses to 0.7%; rotated 10D reverses; 5D LineMemory only 7/20 paired wins |

## Q1 novelty verdict
No new proven result clearly beyond established finite-difference, direct-search or information-based complexity theory. No broad superiority over modern baselines. Strongest defensible contribution is an exploratory conditional study of historical directional reuse and an honest replication demonstrating fragility. A Q1 novel algorithm paper is not currently ready.

## Reproducibility ledger
Phase 14 exact executed source SHA256 3c0e1dfdb0038ee3d236908cf86f35ec4fa040ad605d1de178a7de0ddd8c823e; raw CSV SHA256 ecfcae9dcfbe7f3275df6a5261a16b42e62854a92cda5f8a42a6b57ba7e7d53a; summary SHA256 e2ca3673ae6ffc2ad7e3681aa12446d94ccac292a0dc62a5bf48f00f472e06cc. Exact source/raw local, summary values committed. The repository alone is not yet a complete reproducibility package.
