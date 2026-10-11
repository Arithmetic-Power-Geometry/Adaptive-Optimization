# Phase 13: Validated directional descent under Hessian regularity

**Theorem (two-probe directional certificate).** Let f:R^d→R be twice differentiable on the line segment [x-hv,x+hv] and [x,x+αd], where ||v||=1, h>0, and the Hessian is ρ-Lipschitz in operator norm on the first segment. Assume ∇f is L-Lipschitz on the second segment. Define
g_h=[f(x+hv)-f(x-hv)]/(2h), e=ρh²/6.
Then |g_h-∇f(x)^Tv|≤e. If |g_h|>e, d=−sign(g_h)v is a strict descent direction. Let γ=|g_h|−e>0. If α=γ/L>0 is feasible and L>0, then
f(x+αd)≤f(x)−γ²/(2L).
The certificate requires two *new* function probes (if f(x) was already known), and an additional evaluation to observe the trial point.

**Proof.** For φ(t)=f(x+tv), the Lipschitz Hessian assumption gives |φ''(t)−φ''(0)|≤ρ|t|. Taylor with integral remainder yields |φ(h)−φ(0)−hφ'(0)−h²φ''(0)/2|≤ρh³/6 and the analogous bound at −h. Subtracting and dividing by 2h gives |g_h−φ'(0)|≤ρh²/6. Consequently ∇f(x)^Td≤−γ. By L-smoothness, f(x+αd)≤f(x)+α∇f(x)^Td+Lα²/2≤f(x)−αγ+Lα²/2. Substitute α=γ/L. QED.

**Scope and novelty.** This is a mathematically valid *conditional certificate* but the underlying centered finite-difference error bound and descent lemma are classical. It is NOT claimed to be a literature-new theorem or a novel oracle-complexity result. To achieve new theory, prove an original adaptive selection or complexity guarantee that improves established results and audit prior art carefully.

**Implementation warning.** The Phase 13 implementation called 'CertifiedLine' uses quadratic interpolation of a historical direction, but does **not** estimate or enforce a known ρ or L. Its numerical successes are **not** certified by this theorem. Do not conflate this theoretical candidate with the implemented heuristic.
