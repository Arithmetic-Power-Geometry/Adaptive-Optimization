# Phase 41: Cross-dimensional stress test, costed portfolio and negative results

## Experimental design
Five dimensions d=4,8,20,40,80; two rank regimes r=4 and r=d; three objective families Sphere, Rastrigin, Rosenbrock; seeds 3200–3202; five methods COBYQA, Powell, Embed8, Restart8, Portfolio40; B=80 objective calls maximum. 90 matched instances, 450 actual locally executed runs. All methods receive the same seeded objective and start within each matched instance. All objective calls are charged. Portfolio40 gives full COBYQA up to 40 calls and then a fresh random eight-dimensional COBYQA subspace up to 40 calls anchored at the best incumbent. Restart8 runs two independent eight-dimensional subspaces of up to 40 calls each. At d=4 and d=8, Embed8 is not dimension reduction. The full-rank and r=4 regimes coincide at d=4, so the same instance is duplicated in these two regime summaries; they are not independent observations.

## Actual local results
Each regime contains 45 matched cases (including the overlapping d=4 cases).

| Method | r=4 vs COBYQA win/loss/tie | r=d vs COBYQA win/loss/tie | r=4 vs Embed8 win/loss/tie | r=d vs Embed8 win/loss/tie |
|---|---|---|---|---|
| Powell | 23/19/3 | 21/18/6 | 4/38/3 | 13/26/6 |
| Embed8 | 34/7/4 | 26/13/6 | 0/0/45 | 0/0/45 |
| Restart8 | 34/8/3 | 29/10/6 | 6/33/6 | 30/6/9 |
| Portfolio40 | 25/14/6 | 22/14/9 | 5/37/3 | 25/14/6 |

The proposed costed portfolio fails to outperform Embed8 in either regime. Restart8 is conditionally effective on full-rank cases, but loses to Embed8 on r=4 cases. This is a negative result for naive dimension-agnostic budget splitting, not evidence of a new universally successful algorithm. Differences in actual calls (especially high-dimensional COBYQA early termination) require anytime performance profiles.

## Source and provenance
Local executed source: SHA256 4f3ebaf14b8adb215df43c348285ce63052c24e5fe3005c58ecc9c4607e3af0f, Git blob dee637249a7d20912d74c869e5b5a5fc68e40c3d. The committed GitHub source Git blob was independently checked and matches exactly.
Raw local CSV SHA256 e723e540917e33dbcb86752ed4f7f5e79c730ad4bb0e1df344897fca207840a5.
Summary CSV SHA256 ed7d5b0c7fbdb98d91a9fc5f3b5d8f9e8c6289514f5e7bbcbfc8ffbb34fece6a.
Environment JSON SHA256 89bccbf251960d276a21177214687a17d87ede26662e0570b37b13e26ee1d956.
Local raw observations are retained. GitHub Actions workflow will generate raw files and hashes when executed, but its execution and GitHub raw-data commit are NOT yet confirmed.

## Prior art verified against primary publication pages
Hansen et al. (2021), COCO, Optimization Methods and Software 36(1):114–144, DOI 10.1080/10556788.2020.1808977. Qian, Hu & Yu (2016), sequential random embeddings, IJCAI 25, pp. 1946–1952. Qian et al. (2026), DSEBO, IJCAI 35, pp. 4732–4740, DOI 10.24963/ijcai.2026/527. Both sequential embedding and dynamic embedding choice are prior art. The COCO BBOB suite has 24 noiseless functions; this phase is NOT a COCO/BBOB evaluation.

## Paper conclusion and next step
No novel algorithmic theorem and no broad superiority have been demonstrated. Phase 41 is not independently Q1-ready. Next decisive test: official COCO/BBOB with more seeds and precommitted methods, including SRE, DSEBO, STARS, CMA-ES; performance profiles by evaluation count, time-to-target, confidence intervals, and realistic application tasks. For a theorem-first contribution, specify smoothness, gradient-covariance eigengap and budget assumptions, and derive a genuinely new switching bound with an explicit evaluation cost and closest-prior-work separation. Avoid post hoc performance claims.
