# Phase 28: ZigZag turning search — controlled pilot

## Exact executed design
144 executed runs = 4 shifted/rotated families (Ackley, Rastrigin, Griewank, Rosenbrock) × dimensions 2/5/10 × four held-out seeds 1800–1803 × three methods. Strict cap 160 objective evaluations, same starting points. Local NumPy 2.3.5, SciPy 1.17.0. These are synthetic functions, not official COCO/BBOB.

ZigZag chooses a random vector orthogonalized against the last successful direction, combines them at 45 degrees, and alternates the sign of the turn. Tests +/- each candidate; step expands 1.08 on success and contracts 0.7 otherwise. After 4d consecutive unsuccessful polls, direction resets to a coordinate vector. RandomPoll uses independent isotropic Gaussian directions with identical step rule. COBYQA uses SciPy's model-based method.

## Matched outcomes
| Method | Wins vs COBYQA | Wins vs RandomPoll | Mean objective evaluations |
|---|---:|---:|---:|
| ZigZag | 8/48 | 15/48 | 157.65 |
| RandomPoll | 9/48 | 0/48 | 155.98 |
| COBYQA | 0/48 | 34/48 | 105.25 |

ZigZag vs COBYQA: 8 wins, 35 losses, 5 ties. ZigZag vs RandomPoll: 15 wins, 28 losses, 5 ties. Wins vs COBYQA by family (12 cases each): Ackley 2, Rastrigin 5, Griewank 0, Rosenbrock 1. Win/loss tolerance 1e-10.

## Reproducibility checksums
Local executed source SHA256 33e0f587bed83c06a5a00723448bc2a13de1f6afd85de134451750391def32f1.
Local raw CSV SHA256 05a9d554b95c09801f81f3857f4dd78c37ac9ce838ccb8834bf74bd9eebc2b56.
Local summary CSV SHA256 9eab2b9cc1fc47a64044c7d3c1153c73440abe1b1b434b353a9b18ddfe200ea5.
Environment SHA256 93874932646859025b47d984ca9f37ec579b8736716da0e2e596faf88e263a4c.
GitHub source Git blob 4bf2005ede1d13ebe9a8baccdb1470b533fa8ab4, verified byte-identical with local executed source. Raw and summary exist locally. GitHub Actions configured to reproduce/commit raw outputs; success not yet verified.

## Mathematical gap
Alternating direction signs and orthogonalized random turns do not imply a positive spanning poll set. Under Lipschitz-gradient assumptions, a positive spanning set or probabilistic descent assumptions can be necessary to prove stationarity, as discussed by Gratton et al. (2015), DOI 10.1137/140961602. The method currently has no such theorem and no demonstrated superiority.

## Closest verified literature
Gratton et al. (2015), SIAM Journal on Optimization 25(3):1515–1541, DOI 10.1137/140961602; Moré and Wild (2009), SIAM Journal on Optimization 20(1):172–191, DOI 10.1137/080724083; Ragonneau and Zhang (2024), Mathematical Programming Computation 16:535–559, DOI 10.1007/s12532-024-00257-9. These are verified against SIAM and Springer publisher pages.

## Research and Q1 conclusion
ZigZag is a precisely specified, tested directional search candidate; it is not yet an established new theoretical contribution. 8/48 wins against COBYQA and 15/48 wins against random polling do not support practical superiority. **Not Q1-ready as a new optimizer**. Do not market a breakthrough. A worthwhile next step is to investigate an original information-limited lower bound or a certificate for switching search regimes, with proofs and official BBOB benchmarks.
