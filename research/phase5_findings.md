# Phase 5 — directional-memory pilot (2026-10-11)

## Method
MemoryPoll reuses an exponentially weighted direction from accepted incumbent improvements. Following a failed coordinate polling sweep, it tests a normalized memory direction and its negative. Both are charged to the same objective evaluation budget. This is a heuristic implementation, not a novel theoretical principle.

## Experiment
3 shifted and rotated functions (Ellipsoid with condition range 1 to 10^4, Rastrigin, Rosenbrock); dimensions 2/5/10; seeds 0–4; AdaptivePoll, MemoryPoll, SciPy DE and SciPy Powell; maximum 300 function evaluations. Total 180 runs. Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. Source code and local raw/trace outputs supplied as separate downloadable artifacts.

## Findings
MemoryPoll beats AdaptivePoll in 3/9 configurations, loses in 6/9. Median 5D Rosenbrock 4.1771 to 3.0474 (~27.0% lower); 10D Ellipsoid 268.0710 to 228.8280 (~14.6% lower); 10D Rosenbrock 10.2493 to 9.3833 (~8.45% lower). On 5D Ellipsoid, MemoryPoll is worse (29.3313 versus 18.9955). Powell or DE remains superior on several problems. No general improvement demonstrated.

## Critical novelty audit
Reusing successful directions and local directional models has extensive prior art. See Cartis & Roberts (2019), Cartis et al. (2019), Cartis & Roberts (2023), Roberts (2025), and randomized subspace optimization. No new theorem, no global optimum certificate, no general evaluation savings. Candidate-specific benefit is conditional and not statistically established.

## Research next gate
20+ seeds, full COCO BBOB rotated/ill-conditioned functions, common initial points, target hitting-time ECDF, CMA-ES/Py-BOBYQA/modern DE, ablation on memory decay and probe frequency, no tuning on final test instances. Commit raw run-level data and independent GitHub Actions rerun before paper submission.
