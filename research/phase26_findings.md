# Phase 26 — Numerical-gradient versus model-based derivative-free optimization

Date: 2026-10-11. Executed 384 runs: Ackley, Rastrigin, Griewank, Rosenbrock × dimensions 2,5,10 × seeds 1600–1607 × COBYQA, numerical BFGS, numerical L-BFGS-B, WarmBFGS. Same starting points and hard budget of 240 objective calls per matched problem. Synthetic shifted/rotated functions, not official COCO.

## Mathematics, physics and information critique
A numerical gradient from forward finite differences approximates local tangent information and incurs at least d+1 objective probes per evaluation of the full gradient. A quadratic trust-region model amortizes geometry across interpolation points; its information usage can therefore be more effective at low budgets. Physical analogy: local gradient flow follows the immediate energy landscape; global escape and conditioning require other mechanisms. Philosophical distinction: observed gains on selected families are not a general law. This is an analogy and critical framework, **not a new physical theory or original mathematical theorem**.

## Results
| Method | Wins vs COBYQA (96) | Losses | Ties | Mean evaluations |
|---|---:|---:|---:|---:|
| COBYQA | — | — | — | 125.1 |
| Numerical BFGS | 12 | 58 | 26 | 169.4 |
| Numerical L-BFGS-B | 19 | 48 | 29 | 131.7 |
| COBYQA->BFGS warm start | 10 | 19 | 67 | 165.5 |

Wins of numerical L-BFGS-B vs COBYQA by family (24 each): Ackley 5, Rastrigin 4, Griewank 1, Rosenbrock 9. Warm-start wins: Ackley 6, Rastrigin 0, Griewank 0, Rosenbrock 4. Warm-start stage uses at most min(60+8*d,120) evaluations of COBYQA then spends remaining budget on BFGS from the best incumbent. Reported final objective is best-ever across both stages.

## Reproducibility
Exact GitHub source blob e43a817cad190026e1f6edd51a3f95908c209df2 verified against local git hash-object.
Source SHA256 e11272927d5971187743234515919a43c9a54643056c827b627fa0440d6ff29c
Raw SHA256 968b9925d26ff99345c9cbb6679ee4bbffbc424bd6df7bdc713681df1d22a849
Summary SHA256 6dbae20e55686496af90caffd66205848fda8dc962c0d0b8f59555a6e517a210
Environment SHA256 9dea809add038f7b469fcc710f57462a3ffe454b97973c1f198ed3f24325a834

## Originality and Q1 gate
Finite differences, BFGS, L-BFGS-B, COBYQA, and solver warm-start portfolios are known. The specific budget split is a pilot implementation, not an established novel algorithm. No robust superiority over COBYQA, no theorem, and no official BBOB validation. **Not Q1-ready as a novel general-purpose optimizer.**

## Highest-value research gap
For a given evaluation budget B, can one compute a *reliable, low-cost, falsifiable certificate* that a local gradient approximation is more informative than continued quadratic trust-region sampling? The certificate must pay for its own diagnostic evaluations, and its selection regret must be compared against both fixed solvers under independent holdout. Any theoretical result requires explicit smoothness, noise, curvature, and oracle assumptions. Existing automatic solver selection in PDFO and broad algorithm-selection literature must be examined before claiming novelty.
