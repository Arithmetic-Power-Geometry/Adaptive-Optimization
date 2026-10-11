# Phase 3: rotated and shifted benchmark — 2026-10-11

## Setup
180 runs = 3 dimensions (2, 5, 10) × 3 functions × 5 seeds × 4 methods. Hard cap 300 objective evaluations each. Random orthogonal matrix by seeded QR, fixed seeded shift per instance. Functions: Ellipsoid (condition range 1 to 10^4), Rastrigin, Rosenbrock. Methods: AdaptivePoll, RotatingPoll (random orthogonal basis after stagnation), SciPy differential evolution and SciPy DIRECT.

## Results and interpretation
See [phase3_summary.csv](../results/phase3_summary.csv). RotatingPoll improves median 5D Ellipsoid 18.9955 to 12.1644 and 5D Rosenbrock 4.1771 to 3.9534 compared with AdaptivePoll, but is far worse on 2D Rastrigin (7.9597 versus 0.9950). DIRECT is strongest by median in most 5D and 10D cases. The random-rotation mechanism does not establish superiority or novelty.

## Novelty status
**No validated novel optimizer, no new theorem, no global optimality guarantee.** Randomly changing search directions and adaptive step sizes have extensive prior art. Candidate research gap: develop an inexpensive directional-coupling estimator that decides when rotation is useful, then compare against CMA-ES, modern DE, trust-region and surrogate algorithms. Any new mechanism must survive rotated/noisy/constrained BBOB and proper statistical tests.

## Limitations
Five seeds, synthetic functions, only 300 evaluations, no CMA-ES baseline, no full BBOB, no statistical significance test. Rosenbrock is rotated/shifted; report best objective values, not guaranteed global errors. The exact source used in the local run is provided separately as downloadable artifact; repository reproduction code is a reimplementation and must be independently rerun to establish byte-for-byte reproducibility.

## Prior art verified
Tanabe (2024) GECCO 712–721 DOI 10.1145/3638529.3654019; Braun, Lange and Toussaint (2025) UAI/PMLR 286:398–420; Girardin (2025) GECCO Companion 1867–1874 DOI 10.1145/3712255.3734332; van Stein (2025) GECCO Companion 1–2 DOI 10.1145/3712255.3735092. See [phase3_verified.bib](../references/phase3_verified.bib).
