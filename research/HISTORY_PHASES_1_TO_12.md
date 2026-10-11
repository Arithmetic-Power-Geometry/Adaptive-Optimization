# Cumulative history — phases 1–12

| Phase | Key method / test | Verdict |
|---|---|---|
| 1 | Adaptive coordinate polling | Initial DIRECT cap unfair |
| 2 | Strict-budget baseline tests | No consistent superiority |
| 3 | Random rotation | Some gains, large regressions |
| 4 | Coupling indicator | 0/12 median wins vs adaptive |
| 5 | Directional memory | 3/9 median wins vs adaptive |
| 6 | Gated memory | 93.6% fewer memory probes, not total evaluations |
| 7 | Held-out 960 runs | At 240 calls: Adaptive 262/320, Memory 263/320 |
| 8 | Budget reanalysis | At 120 calls: Memory 235/320 vs Adaptive 214/320, post hoc |
| 9 | Independent 960 runs with Powell | At 240: Adaptive 133/240, Memory 141/240, Powell 162/240 |
| 10 | Paired bootstrap | Small Memory benefit; Powell stronger |
| 11 | Function-family bootstrap and COCO workflow | Generalization uncertain; official COCO results unverified |
| 12 | Finite-transcript theorem and 480 new quadratic runs | Constructive theorem proved but prior-art novelty unverified; LineMemory better in rotated 2/5/10D medians, weaker on diagonal 5/10D |

## Research integrity
The phase-12 finite-transcript ambiguity theorem is proved in research/phase12_theorems.md; it is a candidate mathematical statement, NOT certified novel. The exact quadratic line interpolation theorem is classical. No general-purpose optimizer breakthrough or Q1-level superiority has been demonstrated. All phase-12 numerical results are local and exploratory. Reproducibility debt: exact executed source and 480-row raw data are available locally, not yet in GitHub. Do not treat GitHub repository alone as a complete submission artifact.

## Decision
Stop claiming algorithmic novelty from memory probes alone. Mine information-based complexity literature for genuinely open quantitative oracle questions, or prove a new nontrivial worst-case/instance-dependent bound. Independently test on official COCO/BBOB and modern solvers before manuscript submission.
