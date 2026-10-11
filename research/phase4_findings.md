# Phase 4: budget-accounted directional coupling pilot (2026-10-11)

## Hypothesis
A three-probe mixed-difference indicator can detect whether to rotate coordinate search directions. This is an experimental hypothesis, NOT a new theorem or proven novelty.

For initial incumbent x, coordinate directions e1,e2 and step h=0.12, compute
C = |f(x+h(e1+e2))-f(x+he1)-f(x+he2)+f(x)| / (|f(x+he1)-f(x)|+|f(x+he2)-f(x)|+1e-9).
The f(x) evaluation is reused from the initial incumbent; the other three evaluations are charged to the budget. CouplingPoll rotates its basis after two unsuccessful poll cycles only if C>0.15; the baseline RotatingPoll rotates after two unsuccessful cycles unconditionally. This is an intentionally simple and potentially brittle detector, not a rigorous Hessian/coupling estimator.

## Experimental design
Three objectives: Ellipsoid (condition range 1 to 10^4), Rastrigin, Rosenbrock. Dimensions 2 and 5; seeded shifts and either identity or seeded random orthogonal rotations; five seeds; five methods AdaptivePoll, RotatingPoll, CouplingPoll, differential evolution and DIRECT. 300 runs, hard cap 240 objective calls per run. Python 3.13, NumPy 2.3.5, SciPy 1.17.0. Same per-instance transformation across algorithms.

## Main finding
CouplingPoll improves median best objective over AdaptivePoll in **0 of 12** test configurations. It beats RotatingPoll in 7 of 12 configurations, but is worse than the strongest comparator in most cases. This does not establish improvement or novelty.

Selected medians:
- 2D rotated Ellipsoid: Adaptive 2.98462; Coupling 2.99120; Rotating 2.47051; DE 0.00641; DIRECT 0.13273.
- 2D rotated Rastrigin: Adaptive 0.99496; Coupling 0.99496; Rotating 7.95971; DE 0.99754; DIRECT 0.99499.
- 5D rotated Ellipsoid: Adaptive 20.10830; Coupling 20.10830; Rotating 18.87439; DE 72.17029; DIRECT 18.31522.
- 5D rotated Rosenbrock: Adaptive 4.19012; Coupling 4.19397; Rotating 3.95506; DE 27.11972; DIRECT 5.14096.

## Critical interpretation
MADS already supports adaptive polling in dense directions (Audet and Dennis, 2006); BOBYQA already exploits quadratic models and trust regions (Powell, 2009). Simple direction rotation, coupling tests and adaptation cannot be presented as novel without direct prior-art differentiation. This pilot gives negative evidence for the fixed two-coordinate coupling trigger. No global optimality guarantee and no improved worst-case complexity.

## Methodological caveats
Only five seeds, 12 synthetic configurations, 240 evaluations, no CMA-ES, no COCO/BBOB, no significance test. The coupling probe uses the first two axes only; not permutation invariant. DIRECT's compiled callback may convert the intentional hard-budget stop into SystemError; results retain the incumbent from completed evaluations. All reported medians refer to best objective, not guaranteed global-optimality gaps. The GitHub script and results need a successful independent rerun before claiming cloud reproducibility.

## Verified literature (publisher or primary-host checked)
- Audet & Dennis (2006), SIAM J Optim 17(1), 188–217, DOI 10.1137/040603371, https://epubs.siam.org/doi/10.1137/040603371.
- Audet & Orban (2006), SIAM J Optim 17(3), 642–664, DOI 10.1137/040620886, https://epubs.siam.org/doi/abs/10.1137/040620886.
- Powell (2009), DAMTP 2009/NA06, Cambridge technical report, https://optimization-online.org/2010/05/2616/. No DOI claimed.
