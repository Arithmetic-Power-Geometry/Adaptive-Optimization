# Phase 27 — COBYQA restart ablation, independent pilot

Date 2026-10-11. Four shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock), dimensions 2/5/10, three seeds 1700–1702, four methods = **144 completed executions, 36 matched problems**. A prior attempted 10-seed run timed out and produced no complete results; it is not reported. Same initial point, hard global cap 240 objective evaluations per algorithm. Methods: COBYQA; RestartBest (120 COBYQA then restart at incumbent); RestartKick (restart at incumbent plus N(0,0.8²/d I)); MultiStart (restart near original start). Each method reports best-ever objective.

| Method | Wins vs COBYQA | Losses | Ties | Mean objective calls |
|---|---:|---:|---:|---:|
| COBYQA | 0 | 0 | 36 | 128.33 |
| RestartBest | 4 | 5 | 27 | 162.75 |
| RestartKick | 13 | 11 | 12 | 181.36 |
| MultiStart | 10 | 12 | 14 | 183.50 |

RestartKick wins vs COBYQA by family: Ackley 7/9, Rastrigin 4/9, Griewank 0/9, Rosenbrock 2/9. This is not an overall dominance result; 36 matched cases are insufficient for strong inference. No claim of an original restart idea: Cartis, Roberts and Sheridan-Methven (2022), Optimization 71(8):2343–2373, DOI 10.1080/02331934.2021.1883015, already study restarts for Py-BOBYQA.

## Reproducibility
Exact executed source SHA256 56e48633be62ff1b328322438e719cb40bb25492a7301cc6b579ad0366ac7125.
Git blob fb6e9e18d59f3542590f2b24528ac5a957ceea65, verified against local source.
Raw CSV SHA256 8ade0af4a34792e41290c2bd4bb0380293cc68134455711f99ce4c376aceca93.
Summary CSV SHA256 9c383b619d269ff9d5fa6c8f5ba2f02afb3f84bae642c313f263e835215d9b34.
Environment JSON SHA256 1ec93df478514cd3e807ef2ede517b5f2784b0a62929cf1eab3270648baf4676.
Full raw and summary files exist locally. GitHub workflow configured to publish them, but completion not verified.

## Mathematical critique
Incumbent preservation ensures the second stage cannot worsen the *best observed objective relative to the first stage of the same portfolio*, but gives no guarantee relative to standalone full-budget COBYQA. Perturbation may escape a local basin, yet without explicit basin geometry or a distributional model, no probability of improvement is guaranteed. Mean calls are greater than baseline, so fair comparison must report evaluation counts and data profiles (Moré and Wild, 2009).

## Novelty/Q1 verdict
Restarts are established; no new theorem, no robust advantage over COBYQA, and official COCO/BBOB runs remain unverified. **Not Q1-ready as a novel general-purpose optimizer.** A more promising contribution is a *certified budget-allocation rule* with a nontrivial proof and broad independent benchmarks, subject to a careful prior-art search.
