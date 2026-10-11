# Phase 25 dual-engine portfolio: pilot results and Q1 assessment

## Design and executed provenance
Four shifted/rotated families × three dimensions (2,5,10) × four held-out seeds (1500–1503) × four methods (COBYQA, Powell, DualStart, DualWarm) = **192 locally executed runs**, 48 matched problem instances. Strict budget 240 objective evaluations per algorithm. The first attempted 10-seed run exceeded the execution timeout and did not produce results; this report concerns only the completed four-seed pilot. Note the executed source's introductory docstring still says 1500..1509, but the actual executable loop uses 1500..1503 and environment.json agrees. No 10-seed results are claimed.

DualStart spends at most 120 evaluations on COBYQA, then uses remaining budget on Powell from original start. DualWarm starts Powell from the best incumbent of the first COBYQA stage. The best objective seen by either stage is reported. This is a **solver portfolio/restart**, not a novel optimization algorithm or theorem.

## Exact results
| Method | Wins vs COBYQA (48) | Wins vs Powell (48) | Wins vs per-instance best of both standalone solvers (48) | Mean evaluations |
|---|---:|---:|---:|---:|
| COBYQA | 0 | 28 | 0 | 125.33 |
| Powell | 11 | 0 | 0 | 216.29 |
| DualStart | 8 | 26 | 0 | 224.48 |
| DualWarm | 7 | 28 | 3 | 207.46 |

The dual-engine warm-start strategy beats both single solvers in 3/48 matched instances, but beats COBYQA in only 7/48. It does not dominate COBYQA. COBYQA uses fewer evaluations on average.

## Exact hashes and reproducibility
Executed source SHA256 6a9067f1f0af7de9439b8d790ed174f757342bb60727eb176a4f2306e7cfef0c. GitHub source blob 2c8458fcd9cd1990181edfb9dde91da7187166f7 (exact match confirmed).
Raw CSV SHA256 3147b18354254483d319f999fe70392fc420c32f6f198d6e835df3bdcd9f5131.
Summary CSV SHA256 14855f5e365171b8c5eecd5877bdc1d61f696bd81a0424d8512a7258581ccf08.
Environment JSON SHA256 152884b0dd90f1e4ccfdf4cfd0a35841659396e4639397c8c1d3d932cde1fa1d.
Local raw, summary and source available in /mnt/data/adaptive_phase25. GitHub Actions workflow configured to rerun and commit raw data; execution status must be independently verified.

## Closest prior art
Ragonneau and Zhang (2024) PDFO, Mathematical Programming Computation 16:535–559, DOI 10.1007/s12532-024-00257-9, document Powell derivative-free solver families. Ragonneau and Zhang (2024), Optimization Methods and Software 39(4):898–910, DOI 10.1080/10556788.2024.2330635, show theoretical optimality of interpolation sets. IEEE Transactions on Evolutionary Computation 29(1):187–204 (2025), DOI 10.1109/TEVC.2024.3379756, evaluates derivative-free optimizers at large budgets; author metadata needs checking. Solver portfolios, warm starts and restarts are established ideas; no verified originality claim is made.

## Publication gate
**Not Q1-ready as a novel optimizer.** No new convergence/complexity theorem; no overall COBYQA superiority; 48 matched instances are exploratory; official COCO/BBOB Phase 25 pilot configured in experiments/phase25/ but unverified. The research signal is conditional complementarity of COBYQA and Powell. Next worthwhile study: a cost-accounted, prespecified instance-feature gate that selects a solver with a proved regret guarantee relative to the best expert under explicit assumptions, tested on independent COCO/BBOB problems. Do not conflate the elementary expert-regret theorem with original algorithmic novelty.
