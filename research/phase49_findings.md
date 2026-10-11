# Phase 49 — gap-first, 200-run independent mock replication

## What gap was addressed?
Earlier mock-suite pilot had only 6 matched instances, and the official COCO/BBOB workflow remains unverified. This phase tests whether the Gate8Full heuristic generalizes across more independently shifted synthetic instances before investing in a large official benchmark. It does not establish COCO performance.

## Exact executed protocol
Existing local phase48.py mock runner (NOT the distinct staged GitHub coco_pilot.py) was executed with:
```bash
OPENBLAS_NUM_THREADS=1 python phase48.py --mode mock --dimension 10 --instances 1-20 --functions 1,2 --budget-mult 12 --methods COBYQA,Embed8,Restart8,Gate8Full,DE --out /mnt/data/adaptive_phase49
```
200 runs, 40 matched instances, 19,308 charged evaluations; each capped at 120 calls. Objective families shifted Sphere and Rastrigin. Method names are full COBYQA, fixed 8D random embedding, two-stage restart, progress-gated full switch, and SciPy differential evolution. All methods bounded [-5,5]^10. At d10, k8 is an actual reduced subspace. The 20 instances are different shifts, not independent function classes.

## Actual matched results (1e-8 tie tolerance)
| Function | Method | Wins vs COBYQA | Losses | Ties | Median final objective |
|---|---|---:|---:|---:|---:|
| Sphere, n20 | Embed8 | 0 | 20 | 0 | 3.014787 |
| Sphere, n20 | Restart8 | 0 | 20 | 0 | 0.371070 |
| Sphere, n20 | Gate8Full | 0 | 0 | 20 | approx 3.57e-27 |
| Sphere, n20 | DE | 0 | 20 | 0 | 12.243792 |
| Rastrigin, n20 | Embed8 | 0 | 20 | 0 | 23.426763 |
| Rastrigin, n20 | Restart8 | 0 | 20 | 0 | 16.113059 |
| Rastrigin, n20 | Gate8Full | 0 | 20 | 0 | 15.452601 |
| Rastrigin, n20 | DE | 0 | 20 | 0 | 88.754993 |

Gate8Full vs Embed8: 20/0/0 Sphere and 20/0/0 Rastrigin. The gate is better than fixed embedding here, but **not better than full COBYQA**. Comparisons at a 120-call cap should also report actual evaluation counts and anytime curves, as solvers may stop early.

## Raw-data provenance
Executed locally and checked:
- raw_results.csv: 200 rows, SHA256 5f2a5e3891029e6e1d936a23b115c7afdbe77d5cf224a744d2146e5b27920a6e
- traces.csv: 19,308 rows, SHA256 aeed88100349703f287b4786188c20fad7e7618b1bcd05eb93e83e802ade8d5d
- environment.json SHA256 b956a1fd3aa473b0e43dc4d976bc730e63074945e33bf05d6b8401a9faf955fe
These raw data files are locally generated; GitHub workflow is supplied for reproduction, but no GitHub archive of raw files is claimed until a successful workflow run is verified.

## Source audit and critical fixes before official COCO
The existing staged Phase48 official pilot has not been executed. Its `CMAES` loop discards incomplete final generations from `tell`; this is acceptable for budget safety but must be documented as partial-generation truncation and matched to other solvers' budget accounting. The runner lacks COCO observer/target-attainment metrics and dependency lock files. It is an *experimental smoke pilot*, not a finished benchmark. Official Suite.get_problem_by_function_dimension_instance and Problem.free are supported by the primary COCO docs: https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html . The official COCO getting-started guide recommends filtered preliminary suites: https://coco-platform.org/getting-started/index.html .

## Research gap and Q1 assessment
- Validated conditional advantages: random embeddings can be efficient on some low-rank ridge objectives in earlier phases; fresh subspaces can improve a fixed embedding on certain full-rank instances; the gate can beat a fixed embedding on mock shifted functions.
- Demonstrated original mathematical theorem: **none**.
- General performance superiority over COBYQA/CMA-ES: **not established**.
- Official COCO/BBOB benchmark: **not executed or verified**.
- Q1-ready new optimizer: **NO**.
The next defensible research gate is official COCO smoke test with verified CI artifacts, then a preregistered 24-function, >=20-instance suite with 100d+ budget and strong comparators. Novelty must be established against Qian, Hu and Yu (IJCAI 2016) sequential random embeddings and contemporary random-subspace DFO.
