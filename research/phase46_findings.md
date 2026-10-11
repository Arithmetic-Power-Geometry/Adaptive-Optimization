# Phase 46: gap-first evaluation and independent mechanism replication

## Gaps identified from Phases 39–45
1. No evidence of a single optimizer dominating low-rank and full-rank problems.
2. The restart improvement mixes new directions, reinitialization and anchoring. Need mechanism ablations with common random seeds.
3. Actual evaluation counts vary even under identical caps. Need anytime target curves and cost-adjusted comparisons.
4. Small post-selected synthetic benchmarks, and d8/r8 embeddings are full-dimensional; no independent COCO/BBOB benchmark.
5. Existing sequential random embedding work (Qian, Hu and Yu, IJCAI 2016) prevents novelty claims for restarts alone. A new theorem or empirically strong distinct adaptive decision rule is missing.

## Phase 46 design (executed)
60 optimization runs = d20 × two families (Sphere, Rastrigin) × r4/r20 × seeds 3700–3702 × five methods. Each method starts at identical x0 per instance and has maximum B=240 evaluations. All methods constrained to [-5,5]^20. Methods: Full COBYQA, Embed8, NewBest (fresh subspace anchored at best incumbent), SameBest (same subspace, best incumbent), NewOrigin (fresh subspace, original anchor). Per-evaluation best-so-far trace recorded. This is a new-seed exploratory replication, NOT the planned 20-seed study: a longer initial run timed out and was reduced to three seeds. Do not misstate sample size.

## Actual results (6 matched instances per regime)
| Regime | Method | W/L/T vs Full | W/L/T vs Embed8 | Mean evaluations |
|---|---|---|---|---|
| r4 | Embed8 | 2/0/4 | 0/0/6 | 172.33 |
| r4 | NewBest | 2/0/4 | 0/0/6 | 213.83 |
| r4 | SameBest | 2/0/4 | 0/0/6 | 215.67 |
| r4 | NewOrigin | 1/0/5 | 0/3/3 | 240 |
| r20 | Embed8 | 0/6/0 | 0/0/6 | 102.5 |
| r20 | NewBest | 0/6/0 | 6/0/0 | 157.33 |
| r20 | SameBest | 0/6/0 | 0/1/5 | 147.67 |
| r20 | NewOrigin | 0/6/0 | 3/2/1 | 161.83 |

Fresh-subspace best-incumbent restart beats fixed embedding on all six full-rank instances, but all six still lose to full COBYQA. Fresh directions have a conditional benefit; no universal advantage or new algorithm is demonstrated. Low-rank results are often within the 1e-8 tie threshold. Statistical inference is weak with six matched instances and two function families.

## Reproducibility
GitHub committed source verified byte-identical with local executed source: Git blob a8ab53ba1b15de5e9b3fdec4cc8c499c810deebe; SHA256 f88ed0e26c4d5bc713b059ae88ea99fe4612fb8b4e7d35a9c05888974d8d4935.
Raw SHA256 eced88d20f17ed1188eb8c20ee63065fcdeaaf632c292f8e283a8add1891d1b5.
Traces SHA256 dbf36a292638e51c4baef03ef76ea01cafe3e3b380a40aa1ef44967e90e25296.
Summary SHA256 1a0b597bef24386d823233d89ff52c636d17679fcccc0f4f766acaa77764e824.
Environment SHA256 164e9799923c71ff63ede7d69874e5cf79fa021c2e55b0e9566af8574a69298a.
GitHub workflow prepared for raw archive; workflow execution unverified.

## Literature and next test
Hansen & Ostermeier 2001, Evolutionary Computation 9(2), 159–195, DOI 10.1162/106365601750190398 (verified PubMed). Hansen et al. 2021 COCO platform, Optimization Methods and Software 36(1), 114–144, DOI 10.1080/10556788.2020.1808977. COCO official Python API documentation verifies Suite('bbob', '', 'dimensions:20 instance_indices:1') and warns about freeing problems before retrieving others. The existing staged coco_pilot.py should not be described as validated or runnable without a dedicated smoke test. Official BBOB comparisons with >=20 independent instances and 100d or larger budgets are needed.

## Novelty/Q1 gate
No new mathematical theorem or general-purpose superior optimizer. Current value: carefully documented failure modes and a conditional restart mechanism. **Not Q1-ready as a novel optimizer**. Next original target: predeclared cost-aware selection of embedding/full-dimensional search, proof under a restricted objective class, and independent COCO/BBOB validation with strong baselines and target-attainment curves.
