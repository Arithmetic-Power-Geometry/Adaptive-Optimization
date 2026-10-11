# Adaptive Optimization — Exploratory Benchmark

Initial reproducible comparison of candidate-guided coordinate polling (CGCP) against Random, Differential Evolution, and DIRECT on Sphere, Rastrigin, Rosenbrock and Ackley in dimensions 2 and 5.

- Five independent seeds (0–4), nominal evaluation budget 400, convergence target absolute error <= 0.001.
- **Limitation:** SciPy DIRECT can exceed maxfun as it evaluates sets of points; its actual consumption was 403–537 evaluations. DIRECT results are NOT equal-budget comparisons. Raw results record actual counts.
- Candidate CGCP is an adaptive coordinate-poll heuristic, NOT claimed to be a new global optimizer, not a certified algorithm, and not a demonstrated across-the-board improvement.
- Median results in [results/exploratory_summary.csv](results/exploratory_summary.csv).
- Verified bibliographic metadata in [references/verified.bib](references/verified.bib) and [references/verification.md](references/verification.md).
- Local experimental run used Python 3.13, NumPy 2.3.5, SciPy 1.17.0.

This is exploratory, not a publication-grade assessment. Additional baselines including CMA-ES, equal-budget traces, confidence intervals, higher-dimensional and rotated problems, ablations and rigorous novelty audit are still needed.
