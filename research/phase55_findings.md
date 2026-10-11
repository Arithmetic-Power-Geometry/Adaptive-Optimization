# Phase55 — Nonlinear finite-step curvature bias across dimensions

## New gap addressed
Phase52–54 exact quadratic identities do not establish a reliable effective-rank diagnostic for general nonlinear objectives. The untested failure mode is finite-step truncation bias that grows with ambient dimension. This phase tests and quantifies it rather than proposing another heuristic optimizer.

## Exact model and derivation
For f(x)=g^Tx + 0.5x^THx + (lambda/24) sum_i x_i^4 with H=QQ^T a rank-r orthogonal projector, define S_h(z)=[f(hz)+f(-hz)-2f(0)]/h², z~N(0,I_d).
Then S_h(z)=z^THz+(lambda h²/12)sum_i z_i^4, and E[S_h]-tr(H)=lambda h²d/4 exactly. For lambda>0, enforcing absolute *mean curvature* bias ≤ epsilon requires h≤sqrt(4epsilon/(lambda d)). This does NOT directly bound effective-rank ratio bias.

More generally, if f is C4 on the sampled segments and |D⁴f(x)[z,z,z,z]|≤M||z||⁴ uniformly along them, Taylor's integral remainder yields |E S_h(z)-tr Hess f(x)|≤(M h²/12) E||z||⁴ = (M h²/12)d(d+2). This elementary finite-difference inequality is a useful proof obligation, not established new mathematical novelty. For unbounded Gaussian z the derivative bound must hold globally or samples must be truncated; local-only smoothness is insufficient.

## Executed experiment
d=5,10,20,40,80; rank r=2,min(4,d),d; lambda=0,0.1,1; h=0.1,0.5,1; 20 independent replications per setting; 64 Gaussian directions; 2700 rows. Synthetic oracle signals computed analytically, not 129 actual black-box function calls. 129 calls is the cost to deploy 64 central pairs plus a shared baseline.

For r2 lambda1 h1:
|d|theory mean bias|observed mean bias|median relative effective-rank error|
|5|1.25|1.264134|0.219298|
|10|2.5|2.449839|0.522779|
|20|5|4.901498|1.443989|
|40|10|9.939956|3.833569|
|80|20|20.054740|7.268043|

## Provenance
Locally executed source SHA256 f8e86036489deff7ebb4d02acb8d7b14c0848716a2da2c4849082501e2ae64c2; raw 2700-row CSV SHA256 2428101f332cf53f686137b1be6bb2b703bbc9477039840fe253e1580b6ea396; summary SHA256 fdf542194c4667e865f91292bc375ccc6bbf50cedebaa7f9f8d9131ff79ac526. GitHub source committed separately; GitHub CI and raw-data upload are not verified.

## Closest prior art and limitations
Cartis & Roberts (2026), DOI 10.1080/10556788.2025.2601668, already provide random-subspace DFO quadratic models and second-order complexity. COCO suite API https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html documents proper official BBOB experiments. The finite-difference truncation identity is elementary and cannot be represented as a novel convergence theorem. No official BBOB performance, no noisy oracle analysis, no original optimizer advantage. Q1 general-purpose optimizer not established.

## Publication gate
A credible paper requires (1) a new algorithm with provable budget-aware diagnostic decision, including finite-step bias and statistical confidence, (2) official BBOB comparisons against COBYQA, CMA-ES and RSDFO-Q, (3) full evaluation accounting, paired target-attainment and confidence intervals, (4) independent multi-dimensional tests. Stop repeating quartic simulations after this bias mechanism is established.
