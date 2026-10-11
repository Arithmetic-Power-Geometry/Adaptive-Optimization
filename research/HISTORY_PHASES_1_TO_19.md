# Adaptive Optimization: cumulative research, Phases 1–19

Phases 1–6: Adaptive/rotating/coupling/memory/gated polling; conditional performance, memory-probe savings only.
Phases 7–11: Independent held-out experiments, Powell comparisons, statistical uncertainty; no robust dominance.
Phase 12: finite-transcript ambiguity proposition, mathematical construction valid, novelty unestablished.
Phase 13: finite-difference conditional descent certificate; established techniques.
Phase 14: independent replication weakens earlier LineMemory claims.
Phase 15: bounded-noise sign and acceptance certificates; no speed superiority.
Phase 16: COBYQA dominates AdaptivePoll in 48/48 noiseless and 45/48 noisy matched problems.
Phase 17: simple two-start COBYQA wins 16/96 vs COBYQA, with Rosenbrock regressions.
Phase 18: plateau restart triggers 0/18; negative diagnostic.
Phase 19: arithmetic-power weighted successful-direction polling, 480 new runs, wins 22/120 vs COBYQA; isolated median gains Ackley 5D and Rastrigin 2D but significant family regressions. Source Git blob matches executed file; raw CSV local, GitHub Actions workflow pending verification.

## Scientific verdict
No theorem beyond known optimization literature has been established. APG PowerPoll is an experimentally implemented heuristic; elementary gain-weight probability identities do not constitute novel convergence/complexity theory. No robust superiority vs modern model-based DFO. **Not yet Q1-ready as a new optimization algorithm.**

## Next pre-registered study
Ablate power exponent p=0,1,2,4; include random-memory, no-memory and COBYQA controls. Lock hyperparameters and use new COCO/BBOB instances, multiple budgets, bootstrap clustered by function family. Derive an original nontrivial complexity or instance-dependent oracle bound before claiming breakthrough.
