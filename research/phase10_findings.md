# Phase 10: Paired performance audit and Q1 readiness gate
Date: 2026-10-11

## Evidence
No new optimization trials. Phase 9's 960 raw run records (240 matched problems × four methods) were reanalyzed using 5000 paired bootstrap resamples per comparison and budget. The budgets were 40, 80, 120, 180, 240. The executed analysis is downloadable as a local artifact; this repository script reproduces the method if phase9_raw_results.csv is supplied in the same directory.

At 240 evaluations: Adaptive 133/240, Memory 141/240, Powell 162/240, DE 81/240. Memory–Adaptive +8/240 = +3.33 percentage points, exploratory bootstrap 95% interval +0.42 to +6.25 pp. Powell–Adaptive +29/240 = +12.08 pp, interval +6.67 to +17.50 pp. DE–Adaptive -52/240 = -21.67 pp, interval -27.92 to -15.42 pp. At 120 evaluations Memory–Adaptive +6/240 = +2.5 pp, interval -1.25 to +6.25 pp.

## Cautions
Bootstrap samples treat 240 seeded instances as independent; function families and dimensions induce dependence. The budgets were inspected post hoc, no multiple-testing correction. Absolute target thresholds vary by function, and performance is limited to four synthetic families. No new theorem, general convergence improvement, wall-clock benefit, or Q1-ready optimization breakthrough.

## Historical evidence
Phases 1–9 recorded in research/HISTORY_PHASES_1_TO_9.md. Phase 10 adds a paired audit, and the strongest new scientific finding is that a competent Powell baseline is significantly stronger in descriptive aggregate success counts. The claim of globally superior directional memory is unsupported.

## Next decisive experiment
Run official COCO/BBOB Suite and Observer with frozen targets, evaluation budgets, strong baselines including CMA-ES, multiple instances and statistical analysis. Official Suite API https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html; pycma https://github.com/CMA-ES/pycma. The official COCO run has not been completed.
