# Phase 12 — Finite-transcript directional ambiguity and certified line probes

## Proposition 1 (finite-transcript directional ambiguity)
Let Ω⊂R^d be compact, convex, with nonempty interior, d≥1. Let Q={q_1,…,q_m}⊂int(Ω) be a finite set of distinct points and x∈Q. For any unit vector v, there exist C∞ functions f_+,f_- defined on a neighborhood of Ω, both strongly convex on Ω, such that f_+(q)=f_-(q) for every q∈Q, while ∇f_+(x)=c v and ∇f_-(x)=−c v for some c>0.

### Proof
Define P(z)=∏_{q∈Q\{x}} ||z−q||² (empty product 1) and h(z)=(v·(z−x))P(z). For every q∈Q, h(q)=0. At x, ∇h(x)=P(x)v; since points are distinct, P(x)>0. Choose f_±(z)=(λ/2)||z−x||² ± εh(z) for λ>0. Since Ω is compact and h is polynomial, M=max_{z∈Ω}||∇²h(z)||₂<∞. Choose 0<ε<λ/(1+M). Then ∇²f_±(z)=λI±ε∇²h(z) is positive definite everywhere on Ω, hence f_± are strongly convex. Both agree at every q∈Q, yet ∇f_±(x)=±εP(x)v. Taking c=εP(x)>0 proves the claim. QED.

### Corollary (transcript-only limitation)
Any deterministic rule that receives only the finite transcript {(q,f(q)):q∈Q} and selects a fixed nonzero direction d at x cannot certify that d is a strict descent direction for both objectives: their directional derivatives at x are ±c(v·d). Choosing v=d/||d|| makes one derivative positive and the other negative. The claim concerns *uniform certificates over this objective class*, not whether practical adaptive methods can succeed on typical instances.

### Prior-art warning
This proposition is a constructive instance of finite-information indistinguishability and should NOT be claimed novel without a deeper literature audit. It is not a lower bound on all adaptive algorithms, because additional queries can distinguish the functions.

## Proposition 2 (exact directional quadratic minimizer)
For f(z)=zᵀAz+bᵀz+c with symmetric positive definite A, x∈R^d, unit v and h>0, let F0=f(x), F+=f(x+hv), F-=f(x−hv). Then the unique line minimizer along x+αv is

α* = −h(F+−F−) / [2(F++F−−2F0)].

The denominator is positive. If the three values are exact and the trial point is unconstrained, f(x+α*v)≤f(x), with strict inequality unless the directional derivative is zero.

### Proof
Write f(x+αv)=F0+Bα+Cα² where B=2vᵀAx+bᵀv and C=vᵀAv>0. Then F+−F−=2Bh, F++F−−2F0=2Ch², so α*=−B/(2C) yields the expression. Strict convexity of the line restriction gives the conclusion. QED.

### Novelty warning
Three-point quadratic interpolation and exact line minimization are classical; this proposition is an implementation identity, NOT a new theorem.

## Candidate research gap
A genuinely new result would quantify how many extra probes are necessary for a *validated* history-conditioned directional decision under an explicitly stated curvature/noise class, and improve known oracle-complexity bounds. Neither Proposition 1 nor 2 by itself establishes such a gap or a breakthrough.
