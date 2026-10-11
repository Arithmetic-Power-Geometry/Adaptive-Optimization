# Phase51: verified reproducibility gate, no new optimizer

## The actual remaining gaps
1. The Phase49 200-run synthetic result had not been independently rerun to a byte-level reproducibility check.
2. The GitHub Phase49 runner is a separate implementation and was not demonstrated byte-identical to the original local Phase48 runner.
3. No official COCO/BBOB results or independent comparison against CMA-ES exist.
4. No new mathematical theorem or demonstrated performance advantage over COBYQA exists.

## Measures actually taken
Executed the original local Phase48 mock runner again with exactly: `OPENBLAS_NUM_THREADS=1 python phase48.py --mode mock --dimension 10 --instances 1-20 --functions 1,2 --budget-mult 12 --methods COBYQA,Embed8,Restart8,Gate8Full,DE --out /mnt/data/adaptive_phase51`.
- 200 runs, 19308 charged objective evaluations.
- The rerun raw CSV is byte-identical to the previous Phase49 raw CSV: SHA256 `5f2a5e3891029e6e1d936a23b115c7afdbe77d5cf224a744d2146e5b27920a6e`.
- The rerun complete anytime trace CSV is also byte-identical: SHA256 `aeed88100349703f287b4786188c20fad7e7618b1bcd05eb93e83e802ade8d5d`.
- Local environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0.
- A standalone, logically matching reproduction script is committed at `experiments/phase51/reproduce_phase49.py` and CI at `.github/workflows/phase51_reproduce.yml`. Its GitHub Actions run and hash verification are **pending**, not represented as passed.

## Performance interpretation
From Phase50 cost-matched audit, on 20 shifted Sphere instances: full COBYQA mean 44.95 evaluations; Gate8Full mean 83.80 evaluations for near-zero objective; gate has 86.4% more evaluation cost. On 20 shifted Rastrigin instances: COBYQA median final objective ~5.4723 vs gate ~15.4526 after at most 120 evaluations; gate loses all 20 at budget 120. Fixed embeddings can outperform COBYQA in earlier low-rank synthetic cases but are not universally superior. These are synthetic shifted objectives, NOT official BBOB.

## Novelty / journal assessment
Original optimization theorem: NO. Universal performance benefit: NO. Novel optimizer Q1-ready: NO. Genuine contribution of this phase: independent exact reproduction of the complete 200-run synthetic raw results and traces, with a verifiable GitHub CI checksum gate. Do not count this as a new optimization experiment or theoretical breakthrough.

## Literature register
Verified official COCO Suite API: https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html (Suite.get_problem_by_function_dimension_instance, Problem.free); Qian, Hu, Yu, IJCAI 2016, https://www.ijcai.org/Abstract/16/278; Hansen et al., COCO, Optimization Methods and Software 36(1), 114-144, DOI 10.1080/10556788.2020.1808977. All previously entered in master references/verified.bib; do not duplicate.

## Next hard gate
Do not start another arbitrary synthetic heuristic phase. Obtain a successful official COCO smoke run and archived artifacts. Only then launch preregistered multi-function comparisons; seek a mathematically provable structural diagnostic rather than progress-based stagnation threshold. No official COCO success is claimed here.
