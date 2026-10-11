# Phase 40 — cross-dimensional and full-rank negative controls

## Experimental design
216 executed optimization runs; 54 matched instances. Families: Sphere, Rastrigin, Rosenbrock. Ambient dimensions 8, 20, 40. Effective ranks 4 and d (full-rank). Three new seeds 3100–3102. Methods: COBYQA, Powell, Embed8 and Restart8. Budget 80 objective calls. Restart8 runs two independent 8D stages capped at 40 calls each, second anchored at the best incumbent. All calls are charged.

## Exact locally executed comparisons
| Regime | Method | Wins/losses/ties vs COBYQA | vs Powell | vs Embed8 |
|---|---|---|---|---|
| r=4 (27 instances) | Powell | 10/17/0 | 0/0/27 | 0/27/0 |
| r=4 | Embed8 | 20/5/2 | 27/0/0 | 0/0/27 |
| r=4 | Restart8 | 18/9/0 | 27/0/0 | 7/20/0 |
| full-rank (27 instances) | Powell | 9/15/3 | 0/0/27 | 7/17/3 |
| full-rank | Embed8 | 14/10/3 | 17/7/3 | 0/0/27 |
| full-rank | Restart8 | 13/11/3 | 21/3/3 | 19/5/3 |

Restart8 vs Embed8 totals: 26 wins, 25 losses, 3 ties. No cross-regime superiority. At d=8, k=8 is full-dimensional, not a dimension reduction. The results are synthetic and selected after earlier phases; three seeds insufficient for publication-grade statistical validation.

## Exact source and data provenance
Local executed phase40.py SHA256 05d458e2c7957b1f2e606cbcb3e66f2bc8fb49517341e12980355d64f08f; Git blob 7be364fb4d26bdb5858d7b917cf970ebf14f2f23. GitHub source blob verified identical to local git hash-object. Raw CSV SHA256 403fbb87d07a5310e72c62d8b582f6923fa4a421ce56228290e102faefbc4999. Summary CSV SHA256 961ccc0580b4de53e4cd09119bc7f3e9cd505c70446c40195455a276e58d1829. Environment SHA256 8fd73f9189c786e7b67afa7e766b68d2c8655d5368e66c4ba5e1120ecf692812. GitHub workflow committed, successful execution and raw upload unverified.

## Verified closest literature
Qian et al. (IJCAI 2026, DOI 10.24963/ijcai.2026/527) adapt embedding dimensions with a regret bound. Cartis and Roberts (Optimization Methods and Software, published online 2026, DOI 10.1080/10556788.2025.2601668) prove randomized subspace quadratic-model DFO complexity. COCO (Hansen et al., Zenodo DOI 10.5281/zenodo.2594848) is the official continuous optimizer benchmarking platform. Its BBOB benchmark includes 24 noiseless functions and a large-scale suite. None of the Phase 40 runs is an official COCO/BBOB run.

## Mathematical and publication verdict
The contribution is a broader falsification test, not an original algorithm or theorem. No universal optimizer can be established by this dataset. Q1 novelty is **not achieved**. Next: preregister an adaptive switching rule with explicit assumptions and finite-budget proof, run independent official COCO/BBOB and modern RSDFO-Q, DSEBO, STARS, CMA-ES comparisons with at least 20 seeds and anytime curves.
