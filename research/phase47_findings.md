# Phase 47: diagnostic-gated switching test (negative result)

## Hypothesis and design
Can objective-progress diagnostics choose when to abandon a low-dimensional subspace? The proposed Gate8Full spends 60 objective evaluations in a fresh 8D subspace; computes early gain over the first 30 calls and late gain over the next 30; if late gain is less than 10% of early gain, switch to full-dimensional COBYQA for the remaining budget, otherwise start a fresh 8D subspace. The rule uses only observed objective values and charges diagnostic evaluations to the total. This is a preliminary heuristic, not a validated estimator of intrinsic rank.

48 actual local runs: d=20; Sphere/Rastrigin; r=4/20; seeds 3900–3902; Full COBYQA, Embed8, Restart8, Gate8Full; max B=160 calls, bounds [-5,5]^20. Matched instances, starts, and seed logic. Full anytime traces archived locally. Three seeds and two function families are not sufficient for generalization.

## Actual paired W/L/T (6 matched problems per rank)
| Regime | Gate8Full vs Full | Gate8Full vs Embed8 | Gate8Full vs Restart8 |
|---|---|---|---|
| r4 | 0/6/0 | 0/5/1 | 1/5/0 |
| r20 | 0/3/3 | 5/1/0 | 3/3/0 |

Low-rank: Embed8 beats full COBYQA 5/6; Gate8Full loses to full COBYQA 6/6. Full rank: Full COBYQA beats Embed8 6/6; Gate8Full never beats full COBYQA. This is a decisive negative result for the particular heuristic on this small benchmark, not a theorem ruling out adaptive switching.

## Methodological limitations
- Gate is based on objective improvement, which confounds conditioning, local stationarity, nonconvexity and rank.
- The initial 60 calls can be a large opportunity cost. Full COBYQA can stop before its cap, so analyze objective vs actual evaluations.
- The restart policy differs in stage allocation from Restart8; not a fully isolated causal test.
- Synthetic objective families only, no COCO/BBOB evaluation. No external independent implementation.
- Gate rule was designed in response to earlier experiments; claims require precommitted, unseen test suites.

## Verified primary literature and novelty
COCO official Suite API: https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html (verified against primary documentation). SciPy COBYQA maxfev, maxiter, constraints: https://docs.scipy.org/doc/scipy-1.15.0/reference/optimize.minimize-cobyqa.html. Qian, Hu, Yu, 2016 IJCAI sequential random embeddings, https://www.ijcai.org/Abstract/16/278. Hansen et al. 2021 COCO methodology DOI 10.1080/10556788.2020.1808977. No new distinct verified citation needs to be added to the existing master BibTeX.

## Reproducibility
Executed local script SHA256 2fc8bdb69999b40fff1fb5707b3b79c72b4e568fc75992b70c807a0d5c567a75.
Raw observations SHA256 fd6ce4a300237e033489cd6026ea27e6e615de8782f52f2a6befbf66ddca70fc.
Summary SHA256 2fdaa48a62cc763df4b000579c26016a7603900b211b10b11b7ad3c7e930bb17.
Anytime traces SHA256 f296ae694eba0516a0859824bb3639616d8e3f0b9450e911fc28b05303baf84c.
Environment SHA256 4677c46a6e5aad2f7e53b705e24243a1cc9ae53659f2be60023a9d113b9fddfb.
Local files available in /mnt/data/adaptive_phase47. No GitHub raw-data upload or workflow execution is claimed without verification.

## Publication gate
Not Q1-ready as a novel optimizer. Existing sequential random embedding methods and current full-rank performance prevent broad superiority claims. Next: official COCO/BBOB, matched instances, fair strong baselines including CMA-ES, 20+ instances, realistic budgets, and a mathematically justified rank diagnostic with explicit cost. The current phase rejects the naive diagnostic and should be included as a negative ablation, not sold as a breakthrough.
