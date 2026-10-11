# Phase 9: Independent-seed optimizer comparison

Date: 2026-10-11

## Design
New seeded instances 200–209 (not used in phases 1–8); dimensions 2,5,10; four functions (Sphere, Ellipsoid, Rastrigin, Rosenbrock); identity or seeded orthogonal rotation; four methods AdaptivePoll, MemoryPoll, Powell, DE. Total 960 runs; strict cap 240 evaluations. The function shifts and orthogonal matrices are seeded independently of prior phases. Each method sees the same function instance per matched case. Adaptive/Memory/Powell use the same initial point; DE uses population initialization. Python SciPy implementations.

Targets: Sphere 0.001; Ellipsoid 1; Rastrigin 5; Rosenbrock 5. All target values are absolute function values, not standardized COCO target gaps. Method choices and thresholds remain exploratory.

## Measured successes (240 problem instances per method)
| Method | <=120 evaluations | <=240 evaluations |
|---|---:|---:|
| Adaptive | 101 | 133 |
| Memory | 107 | 141 |
| Powell | 148 | 162 |
| DE | 74 | 81 |

MemoryPoll advantage versus AdaptivePoll: +6/240 hits at 120, +8/240 at 240. Powell is substantially stronger than either polling variant. Mean MemoryPoll direction probes: 22.6375 per run. These are subset-specific descriptive outcomes, not statistical significance.

## Scientific verdict
Directional memory shows conditional improvements but is not the leading algorithm under these test conditions. No new theorem, convergence bound, or Q1-level algorithmic novelty established. This study is independent of phases 1–8 by seed range but reuses the same four synthetic function families; it is not independent COCO/BBOB validation. Baselines do not have identical initialization structure (DE population vs local methods); budget counts include all evaluations. No wall-clock or implementation-overhead comparison. Powell bounds and stopping can differ from polling behavior.

## Research history update
See HISTORY_PHASES_1_TO_8.md for the previous eight stages. Phase 9 adds a stronger local optimizer, demonstrates the importance of baseline selection, and weakens claims of algorithmic superiority.

## Next pre-registered experiment
Official COCO/BBOB with observer and standard target precisions; compare against CMA-ES and model-based derivative-free solvers. Use multiple dimensions and independent instances; publish ERT/ECDF, per-function analyses, and uncertainty. Do not declare Q1 readiness before replication.
