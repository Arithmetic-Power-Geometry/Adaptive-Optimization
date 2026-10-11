# Adaptive Optimization — research history, Phases 1–15
Updated 2026-10-11

| Phase | New contribution | Evidence / verdict |
|---|---|---|
|1|Adaptive polling pilot|DIRECT budget mismatch|
|2|Strict budget polling vs DE/DIRECT|No consistent superiority|
|3|Rotating polling|Conditional improvements and regressions|
|4|Coupling gate|0/12 median wins|
|5|MemoryPoll|3/9 median wins|
|6|GatedMemory|93.6% fewer memory probes, not total evaluations|
|7|960 held-out runs|Adaptive 262/320 vs Memory 263/320 at 240|
|8|Budget sweep|Memory 235/320 vs Adaptive 214/320 at 120, post hoc|
|9|960 independent runs incl. Powell|Adaptive 133/240, Memory 141/240, Powell 162/240 at 240|
|10|Paired bootstrap|Small conditional Memory advantage|
|11|Family-level uncertainty, COCO workflow|Only four families; official COCO results not verified|
|12|Finite-transcript ambiguity theorem, 480 runs|Constructive valid theorem, novelty not established|
|13|Finite-difference certificate, 600 runs|Rotated gains, BFGS/L-BFGS-B stronger|
|14|Independent 600-run replication|5D rotated gain collapses; 10D rotated reverses|
|15|480 new bounded-noise runs, sign/acceptance certificates|NoiseAwareFD wins only 12/60 noisy matched cases vs Adaptive; not superior|

## Validated novelty and Q1 readiness
No novel worst-case bound or broadly superior algorithm established. Phases 12–15 include correct conditional mathematical statements but finite-difference and robust-comparison ingredients are classical. Strongest defensible research output: transparent comparative negative/conditional evidence and reproducible theoretical formulation. Not Q1-ready as a novel optimization method.

## Reproducibility
Phase 15 exact source and raw CSV were executed and retained as local conversation files with SHA-256 in research/phase15_findings.md. Only aggregate results are in GitHub; full source/raw GitHub upload still required. COCO workflow run has not been verified.
