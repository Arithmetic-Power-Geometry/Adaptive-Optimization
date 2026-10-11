# Phase 15: bounded-noise directional and acceptance certificates

## Theorem 15.1 — two-query robust directional sign
Let f be C² along [x−hv,x+hv], ||v||=1, h>0, with Hessian Lipschitz constant rho >= 0 along this segment. Suppose the observable oracle is y(z)=f(z)+eta(z), |eta(z)|<=delta at every queried z; errors may be deterministic, adversarial, correlated or repeated. Define
gtilde=(y(x+hv)−y(x−hv))/(2h).
Then |gtilde−∇f(x)^T v| <= rho*h²/6 + delta/h.
If |gtilde|>rho*h²/6+delta/h, the direction −sign(gtilde)*v has strictly negative directional derivative.

Proof: centered Taylor expansion bounds the noiseless symmetric difference error by rho*h²/6. The difference of the two errors has magnitude at most 2delta; division by 2h contributes delta/h. Triangle inequality gives the bound. Strict inequality fixes the sign. QED.

For rho,delta>0, the worst-case upper bound B(h)=rho*h²/6+delta/h is minimized at h*=(3delta/rho)^(1/3), provided this h is feasible. This follows from B'(h)=rho*h/3−delta/h². If rho=0, the finite-difference truncation term vanishes; increasing feasible h decreases the error bound.

## Theorem 15.2 — certified true-objective acceptance
For any two queried points x,z, if observed values satisfy y(z)<y(x)−2delta, then f(z)<f(x).
Proof: f(z)−f(x) = y(z)−y(x)−eta(z)+eta(x) <= y(z)−y(x)+2delta < 0. QED.

The threshold 2delta is worst-case sharp: for any observed gap smaller than 2delta, admissible errors can reverse the true comparison.

## Scope and prior art
Both bounds follow from standard finite-difference error analysis and deterministic bounded-error robust comparisons. They are proved here for completeness, not asserted as original literature contributions. They guarantee correct sign/acceptance conditional on known rho and delta, not global convergence, practical superiority or better oracle complexity.

## Implementation alignment
The Phase 15 NoiseAwareFD experiment uses rho=0 on exact quadratic objectives, fixed h=0.5 at delta=0.01, tests |gtilde|>delta/h, and accepts steps only after observed decrease >2delta. For delta=0, it uses h=0.02 and zero threshold. It does not optimize h* for nonquadratic objectives or estimate unknown rho/delta. The finite-difference sign guarantee applies to the quadratic test family; the algorithm's coordinate fallback uses the same >2delta acceptance safeguard.
