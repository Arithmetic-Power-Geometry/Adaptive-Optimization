# Cumulative history — Adaptive Optimization, Phases 1–17

| Phase | Research direction | Result |
|---|---|---|
| 1–6 | Adaptive, rotated, coupled and gated memory polling | Mixed outcomes; gating reduces memory probes, not total oracle cost |
| 7–8 | Held-out and budget reanalysis | Small, budget-dependent memory benefits |
| 9–11 | Powell comparisons and cluster uncertainty | Powell stronger overall; four-function cluster evidence insufficient; COCO not verified |
| 12 | Finite-transcript directional ambiguity | Constructive proof valid; prior-art novelty not established |
| 13 | Finite-difference directional certificate | Conditional classical result; mixed numerical results |
| 14 | Independent LineMemory replication | Earlier advantages did not consistently replicate |
| 15 | Bounded-noise acceptance/sign certificates | Correct conditional guarantees; NoiseAwareFD loses most tests |
| 16 | COBYQA/BFGS baseline on 480 quadratics | COBYQA wins 48/48 noiseless and 45/48 noisy vs Adaptive |
| 17 | 384 nonquadratic runs, 4 algorithms | RestartCOBYQA wins 16/96 vs COBYQA; some median improvements but large Rosenbrock regressions |

## Publication-readiness gate
Theory: no demonstrated new theorem beyond recent model-based complexity results.
Performance: no robust superiority over COBYQA.
Reproducibility: Phase 17 exact executed source and summary committed; raw data awaits successful CI execution and SHA confirmation.
External benchmark: official COCO/BBOB not yet verified.
**Q1 novel-optimizer paper is not submission-ready.**

## Research pivot
Focus on a provably useful, low-query decision rule for model-based solver restart versus continuation, explicitly accounting for certificate cost. Test on held-out COCO functions with modern model-based and evolutionary baselines; do not infer novelty or superiority from exploratory synthetic median differences.
