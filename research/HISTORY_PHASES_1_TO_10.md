# Research history: Phases 1–10 (updated 2026-10-11)

| Phase | Tested approach | Main finding |
|---|---|---|
| 1 | Adaptive coordinate polling | No established novelty; DIRECT cap not comparable |
| 2 | Strict-cap adaptive vs fixed polling, DE and DIRECT | No consistent superiority |
| 3 | Random rotated directions | Conditional Ellipsoid gains; Rastrigin regression |
| 4 | Two-coordinate coupling gate | No wins over adaptive across 12 median configurations |
| 5 | Directional memory | 3/9 median wins, 6/9 losses |
| 6 | Gated directional memory | ~93.6% fewer *memory probes*, not total evaluations |
| 7 | Held-out targets, seeds 100–119 | At 240 evaluations: Adaptive 262/320, Memory 263/320 |
| 8 | Post-hoc budget sweep | At 120: Memory +21/320 target hits; fades at 240 |
| 9 | New seeds 200–209 and Powell baseline | At 240: Adaptive 133, Memory 141, Powell 162, DE 81 out of 240 |
| 10 | Paired bootstrap audit of Phase 9 (no new runs) | Memory +3.33 pp vs Adaptive, 95% exploratory CI +0.42 to +6.25 pp; Powell +12.08 pp, CI +6.67 to +17.50 pp |

## Cumulative conclusion
Research produces evidence of conditional directional-memory benefits, but no validated algorithmic novelty or global optimization breakthrough. Powell is a stronger comparator than either polling variant on the studied synthetic instances. Confidence intervals are exploratory, unadjusted for multiple comparisons and instance-family dependence. Phase 10 reuses Phase 9 runs; do not double-count its 960 records as new runs.

## Q1 journal paper gate
Not ready for a Q1 novel algorithm claim. Complete official COCO/BBOB with fixed budgets/targets, 15+ independent instances, CMA-ES and model-based DFO comparators, held-out parameter tuning, per-function target ERT/ECDF and multiplicity-aware inference. Prove an original mechanism or present a rigorously designed negative/conditional empirical paper.
