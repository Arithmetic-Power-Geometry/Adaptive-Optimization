# Phase 16 — 480 new objective-budget-matched experiments (2026-10-11)

## Design
Independent seeds 600–607, dimensions 2/5/10, diagonal and rotated SPD quadratics (eigenvalues 1–100), bounded deterministic noise delta=0 and 0.01. Five solvers: Adaptive coordinate polling, noise-aware finite-difference polling, Powell, COBYQA, BFGS with finite-difference gradients. 3 × 2 × 8 × 2 × 5 = **480** runs. Hard cap **160 true oracle calls** per solver; noise oracle is y(x)=f(x)+delta sin(17.3 sum sin(3.1x)+11.7 sum cos(2.7x)). All solvers share the same initial point on matched instances. Objective meter records best true objective at evaluated points, not final returned objective. This is a synthetic benchmark, NOT COCO/BBOB. COBYQA is a modern model-based derivative-free method; BFGS uses numerically approximated gradients and is included for context.

## Aggregate matched wins against Adaptive
At delta=0 (48 matched problems): COBYQA 48, BFGS 43, Powell 34, NoiseAwareFD 6.
At delta=0.01 (48 matched problems): COBYQA 45, BFGS 33, Powell 29, NoiseAwareFD 11.

## Rotated 10D noisy median best true objective (8 matched problems)
COBYQA 0.047452149237810014; BFGS 1.7646318407850248; Adaptive 4.551909215841597; NoiseAwareFD 8.157537933709419; Powell 33.972477269057954.

## Reproducibility
Local executed source SHA256 7919f417628bd6a657d662c3839f984ec3297d4bb37dfd4b6e939774f43deb71
Raw CSV SHA256 b44d8c0d85894809041ab3dd5e584c659ced7cb399decc4bdeaff5d980cae32c
Summary CSV SHA256 fc0b03ff15dfaba022321c2a03734e4680438ab328844ac6d1bd1c8f39b9031c
Environment JSON SHA256 1d201007839c2d84915aba503758b4a26a684fe330396b86c037917fda573d62.
Exact executed source is committed to experiments/phase16.py. GitHub workflow phase16.yml is configured to rerun and commit raw results; its success and exact hash agreement have not been verified. The original raw and summary remain available as local conversation artifacts.

## Theory and novelty
Phases 12–15 establish conditional finite-transcript ambiguity and finite-difference robustness certificates; these are mathematically correct but not established novel relative to existing information-based lower bounds and adaptive finite-difference literature. In particular, Shi et al. already address noisy finite-difference interval selection; Davar & Grapiglia (2025) establish a trust-region finite-difference method with evaluation complexity for composite nonsmooth problems. These papers are more directly relevant than generic direct-search references.

## Q1 assessment
The current algorithm is **not** Q1-ready as a superior new optimizer: COBYQA wins 48/48 noise-free and 45/48 noisy matched problems against AdaptivePoll, and NoiseAwareFD loses in the majority of cases. The defensible result is a rigorous negative/conditional benchmark with a theory-practice distinction. Further work should formulate a nontrivial *certificate cost lower bound* beyond known results, implement a competitive model-based certificate-aware algorithm, and test on official COCO/BBOB with independent holdouts. No breakthrough is claimed.
