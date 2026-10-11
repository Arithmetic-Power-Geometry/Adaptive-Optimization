# Phase48 — Benchmark reliability gate

## Scientific gap and measures
Phase47 showed a progress-stagnation gate loses to full COBYQA. Phases 39–47 only evaluated synthetic rotated objectives, mostly tiny matched sets; no official COCO/BBOB benchmark, and no CMA-ES comparator. Phase48 introduces a COCO pilot with fresh problem retrieval for each method, a strict charged budget, common starts, box constraints, per-call best-so-far traces, and explicit resource cleanup. The official COCO API documents get_problem_by_function_dimension_instance and free() requirements.

## Actually executed locally (mock, NOT BBOB)
A separate local integration runner (phase48.py) completed 30 mock-suite runs on six shifted Sphere/Rastrigin instances (d10, functions 1–2, instances 1–3, 120-call cap) and 2899 objective evaluations. Against COBYQA, Embed8 0W/6L/0T, Restart8 0/6/0, Gate8Full 0/3/3, DE 0/6/0. This is a runner/accounting test only, not COCO benchmark evidence. Locally cocoex and cma were not installed. The GitHub official COCO runner is staged, NOT yet executed, and its exact source differs from the locally executed mock integration runner. No claim of byte-identical GitHub source to the local mock runner.

Local mock runner SHA256 e1c66808f61d8ee0cfb082161f0127a210b66872e86e257e16b8e4367ea229f1; mock raw SHA256 55ff2db30ba56e3687f4360f03186d77522a8a0ef98577c6318629c6a45be172; mock traces SHA256 f3a8202ee824778aaa0ffde25582a19d33ba8699b4db0f4b1c6494a39693d992.

## GitHub official COCO pilot
experiments/phase48/coco_pilot.py is staged with COCO Suite and six methods: COBYQA, Embed8, Restart8, Gate8Full, DE, CMAES. .github/workflows/phase48_coco.yml installs coco-experiment and cma, runs a small 24-run official BBOB smoke test (d10, functions 1–2, instances 1–2, six methods, 120 calls), and uploads raw results as an artifact. Workflow success, installed versions, runtime, and official results are UNVERIFIED until a successful run is inspected. The workflow is deliberately smoke-only; a full benchmark requires preregistered broader functions, independent instances and higher budgets.

## Prior art and novelty
Qian, Hu and Yu, IJCAI 2016, already proposed sequential random embeddings with all ambient coordinates potentially effective. Hansen et al., Optimization Methods and Software 2021, developed COCO benchmarking. The Phase47 gate is empirically unsuccessful, and no original theorem or competitive superiority is established. Q1 novel optimizer readiness: NO.

## Next publication gate
1. Confirm official workflow completed and retrieve raw artifacts/logs.
2. Correct any API errors and record exact dependency versions.
3. Run 24 BBOB functions with at least 20 independent instances, budgets >=100d, full traces and COCO target-attainment metrics.
4. Include CMA-ES, COBYQA, DE, SRE/REMBO and current randomized-subspace DFO competitors, with fair implementation comparisons.
5. Derive and prove a genuinely original budget-aware rank-diagnostic guarantee under explicit assumptions, not a known random-span lemma.
6. Predeclare analysis and report paired effect sizes with confidence intervals; avoid cherry-picking rank regimes.
