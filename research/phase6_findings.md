# Phase 6: Gated directional-memory experiment (2026-10-11)

## Research question
Can a cheap gate reduce wasted historical-direction evaluations without compromising optimization quality? This is a heuristic ablation, not an established new optimizer.

## Method
GatedMemory uses an exponentially weighted accepted-step direction. It tests that direction only after at least two unsuccessful polling sweeps and if its norm exceeds 0.2. MemoryPoll tests memory directions after one unsuccessful sweep. AdaptivePoll never uses memory probes. Every probe is charged to the objective evaluation budget. These thresholds were chosen for this exploratory pilot and were not tuned by independent validation.

## Experimental protocol
Four shifted functions (Sphere, Ellipsoid with condition ratio 10^4, Rastrigin, Rosenbrock); dimensions 2/5/10; axis-aligned or rotated via seeded QR; ten seeds; five algorithms (Adaptive, Memory, GatedMemory, DE, Powell); 240 evaluation cap; 1200 runs. Python 3.13, NumPy 2.3.5, SciPy 1.17.0. Initial points for three polling variants and Powell are shared; DE uses its standard population initialization, so this is not identical-start fairness across all algorithms.

## Findings
Against AdaptivePoll, GatedMemory has lower median objective in 4/24 configurations, higher in 6/24 and numerically tied (tolerance 1e-9) in 14/24. Against MemoryPoll, GatedMemory has lower median objective in 13/24, higher in 8/24, and approximately tied in 3/24. Across 24 configurations, mean probes/run: MemoryPoll 22.35417 versus GatedMemory 1.4375, a 93.57% reduction in memory probes, NOT in total function evaluations.

## Interpretation
The gate avoids probes, but those evaluations can be spent on ordinary coordinate polling instead. No overall evaluation-efficiency advantage against AdaptivePoll has been demonstrated. No global-optimality certificate, convergence theorem or verified novelty. Sphere rotation has no mathematical effect; it is retained as a reproducibility control, not independent evidence of rotation robustness.

## Literature novelty barrier
Ma et al. (2025) already combine model and direct search with convergence analysis. Kimiaei & Neumaier (2024) investigate matrix adaptation in noisy derivative-free optimization. Cartis & Roberts (2026) establish randomized-subspace quadratic-model methods with second-order convergence. A memory gate alone is insufficient novelty. The next test must measure evaluations to fixed targets and compare strong modern methods on held-out problems.

## Reproducibility register
Local executed source SHA256: 8efd94983b094d3a51d83fd358e07e701bd2e5a0606686677aa789e1c6c958d8
Raw results SHA256: f2737b069a2c7014616f5e8f36d9b1ba5bed98aee613b0212144a1768b60cbd8
Summary SHA256: 0f8a5c936b6a71a6ffa207ec0bb3cb507336af4c0e66a5f83f5bd9b5793652f0
Trajectories SHA256: 3ee90f4a1a379fc433c37e1326aaa58397aef420202935546dbb68a807629e03
The full raw, summary and trajectory files are available as local downloadable artifacts. They have not yet been uploaded to GitHub. The repository workflow generates independent artifacts on execution; a successful run is not yet verified.

## Verified references
- Ma et al. (2025), Computational Optimization and Applications 92:889–921, DOI 10.1007/s10589-025-00686-9; Springer primary publication.
- Kimiaei & Neumaier (2024), Mathematical Programming Computation 16:459–501, DOI 10.1007/s12532-024-00261-z; Springer primary publication.
- Cartis & Roberts (2026), Optimization Methods and Software, published online 26 January 2026, DOI 10.1080/10556788.2025.2601668; Taylor & Francis primary publication.
