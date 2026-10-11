# Phase 2: strictly capped evaluation benchmark

Date: 2026-10-11. Exploratory only. Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0.

Methods: adaptive coordinate polling, fixed coordinate polling (ablation), DE, DIRECT, random search. Functions: Sphere, Rastrigin, Rosenbrock, Ackley; dimensions 2,5,10; five seeds; 300 evaluations maximum per run; 300 runs total.

Median errors by dimension/function (AdaptivePoll / FixedPoll / DE / DIRECT):

|Dimension|Function|AdaptivePoll|FixedPoll|DE|DIRECT|
|---|---|---:|---:|---:|---:|
|2|Sphere|2.18e-13|2.28e-13|4.21e-10|0|
|2|Rastrigin|0.99496|0.99496|~0.00001|0|
|2|Rosenbrock|0.11069|0.16030|~0.00003|0.01235|
|2|Ackley|~0|~0|~0.00003|0|
|5|Sphere|~0|~0|0.18850|0|
|5|Rastrigin|5.96980|4.97479|20.53264|0|
|5|Rosenbrock|2.42925|3.88500|21.32385|2.32952|
|5|Ackley|0.00058|0.00009|2.45131|0|
|10|Sphere|0.00138|0.00034|14.82181|0|
|10|Rastrigin|12.12779|26.04403|75.33650|0|
|10|Rosenbrock|9.04064|8.04271|216.65647|8.84880|
|10|Ackley|0.10323|0.05288|5.02926|0|

Finding: no consistent superiority for adaptive coordinate polling; DIRECT usually has the lowest median error on these axis-aligned benchmark functions. Adaptive polling is not a new certified optimizer. Results should not be used as a novelty or Q1 publication claim.

Limitations: five seeds; small function suite; axis-aligned functions; no noise/constraints; hard stopping of DIRECT by exception may interrupt its internal routine, but retains all feasible evaluations and incumbent trace; no CMA-ES or surrogate baseline yet.
