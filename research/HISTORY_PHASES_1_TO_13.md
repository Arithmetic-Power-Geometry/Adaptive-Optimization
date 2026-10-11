# Adaptive Optimization — cumulative research history (Phases 1–13)
Date: 2026-10-11

| Phase | Main contribution | Honest outcome |
|---|---|---|
| 1 | Adaptive polling pilot | DIRECT budget mismatch |
| 2 | Strict-budget poll/DE/DIRECT comparison | No consistent wins |
| 3 | Rotating poll | Conditional gains and large regressions |
| 4 | Coupling-triggered poll | 0/12 median wins |
| 5 | Directional MemoryPoll | 3/9 median wins |
| 6 | GatedMemory | 93.6% fewer memory probes, not total evaluations |
| 7 | 960 held-out runs | Adaptive 262/320, Memory 263/320 at 240 |
| 8 | Five-budget analysis of Phase 7 | Memory +21/320 at 120, post-hoc; fades by 240 |
| 9 | 960 new runs incl. Powell | At 240 Adaptive 133/240, Memory 141/240, Powell 162/240 |
| 10 | Paired bootstrap | Memory modest gain, Powell stronger |
| 11 | Cluster audit and official COCO implementation | Four-family inference weak; official workflow success not verified |
| 12 | Finite-transcript ambiguity theorem and 480 new runs | Correct constructive theorem, literature novelty not established; LineMemory conditional gain |
| 13 | Two-probe conditional descent theorem; 600 new runs incl. BFGS/L-BFGS-B | LineMemory improves rotated 5D/10D over polling/Powell, numerical-gradient methods decisively stronger; no Q1-ready superiority |

## Research integrity
The Phase 13 'CertifiedLine' experimental label does not mean it implements the Phase 13 two-probe certificate: it does not enforce curvature regularity constants. The theorem is valid but derived from classical finite-difference error and smoothness bounds, not verified as novel. The experiment uses six synthetic quadratic configurations and 20 new seeds per setting, not official COCO/BBOB. No broad superiority, new worst-case complexity guarantee, or Q1-ready breakthrough established. Exact executed source and raw data are local artifacts only; SHA256 listed in research/phase13_findings.md.

## Next meaningful theory question
Find a *new* oracle-complexity or optimal adaptive probing theorem for history-conditioned directional certificates under realistic noise/curvature assumptions; distinguish rigorously from existing finite-difference and probabilistic-descent work. Benchmark on official COCO/BBOB with CMA-ES, BOBYQA/UOBYQA, model-and-search and modern optimizers under identical objective budgets.
