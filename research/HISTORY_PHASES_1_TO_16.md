# Cumulative Adaptive Optimization research history — Phases 1–16
Updated 2026-10-11

| Phase | Main study | Result / limitation |
|---|---|---|
| 1 | Adaptive coordinate polling | DIRECT budget mismatch |
| 2 | Strict-budget polling vs DE/DIRECT | No consistent superiority |
| 3 | Rotating directions | Conditional gains and regressions |
| 4 | Coupling trigger | 0/12 median wins |
| 5 | MemoryPoll | 3/9 median wins |
| 6 | Gated memory | 93.6% fewer memory probes, not total objective evaluations |
| 7 | 960 held-out runs | Adaptive 262/320 vs Memory 263/320 target hits at 240 |
| 8 | Budget reanalysis | Memory 235/320 vs Adaptive 214/320 at 120, post hoc |
| 9 | 960 independent runs incl. Powell | At 240 Adaptive 133/240, Memory 141/240, Powell 162/240 |
| 10 | Paired bootstrap | Small conditional Memory advantage |
| 11 | Function-family bootstrap and COCO code | Family-level inference weak; official COCO execution unverified |
| 12 | Finite-transcript ambiguity and 480 runs | Theorem proved, literature novelty unestablished; conditional rotated gains |
| 13 | Finite-difference certificate and 600 runs | BFGS/L-BFGS-B dominate smooth quadratics |
| 14 | Independent 600-run replication | 5D rotated gain nearly vanishes, 10D rotated reverses |
| 15 | Bounded-noise certificate and 480 runs | NoiseAwareFD wins only 12/60 noisy instances vs Adaptive |
| 16 | 480 independent runs, COBYQA and BFGS baseline | COBYQA wins 48/48 noiseless and 45/48 noisy vs Adaptive; NoiseAwareFD only 6/48 and 11/48 |

## Theory register
Phase 12 finite-transcript ambiguity proposition: proved under compact convex domain and finite interior query set; not established novel.
Phase 13 centered-difference sign certificate: correct under Hessian Lipschitz and gradient smoothness; classical components.
Phase 15 deterministic bounded-noise acceptance threshold >2delta: correct, sharp for two observations; classical robust comparison.
No original nontrivial oracle-complexity theorem has been verified against the closest literature.

## Paper readiness
No evidence for a generally superior new optimizer; not ready for Q1 algorithmic novelty submission. Strong negative evidence supports shifting to theory of certificate cost and model-based uncertainty-aware optimization. Official COCO/BBOB still pending. Phase 16 exact executed source committed; raw CSV is local until GitHub Actions reproduction commits it. Verify CI SHA256 against research/phase16_findings.md before declaring repository reproducible.

## Verified literature updates
Davar and Grapiglia (2025) TRFD, SIAM J. Optim. 35(3):1792–1821, DOI 10.1137/24M1701587. Shi et al., SIAM J. Sci. Comput., DOI 10.1137/21M1452470 (already represented in master bibliography). See references/phase16_verified.bib.
