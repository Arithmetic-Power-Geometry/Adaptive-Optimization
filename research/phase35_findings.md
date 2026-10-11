# Phase 35: intrinsic-dimension boundary and split-embedding negative control

## Executed experiment
**180 actual local runs**: 2 families (Sphere, Rastrigin), ambient dimensions d=20 and d=60, intrinsic dimensions r=4,12,20, seeds 2500–2502, five methods: COBYQA, Embed4, Embed8, Split4to8, Split8to4. Each method gets up to 120 objective calls. Problem f(x)=g(Q^T x-s), where Q is a seeded orthonormal d-by-r matrix and s is a seeded latent shift. For d=20,r=20 the objective is full-rank; this is a negative control. All starts matched. The first stage of split methods uses 60 evaluations; the second uses remaining budget and a fresh independent random subspace anchored at the best incumbent. This is a **synthetic pilot, not COCO/BBOB**.

| r | Embed4 wins/losses vs COBYQA | Embed8 wins/losses | Split4to8 wins/losses | Split8to4 wins/losses |
|---|---|---|---|---|
| 4 | 11/1 | 12/0 | 11/1 | 12/0 |
| 12 | 5/7 | 6/6 | 6/6 | 6/6 |
| 20 | 2/10 | 6/6 | 6/6 | 6/6 |
| Total | 18/18 | 24/12 | 23/13 | 24/12 |

Each r group contains 12 matched problems. The 24/36 Embed8 record is **not** a statistically validated superiority claim: only 3 seeds per family/dimension, synthetic problem selection, and previous phase selected this regime. No advantage from split embeddings over Embed8 is established. An initial 720-run protocol was interrupted by execution timeout before producing outputs; the completed protocol above is the only dataset claimed.

## Mathematically relevant boundary
For r<=k and continuous random A, rank(Q^T A)=r almost surely; therefore an embedded k-dimensional affine search can represent any latent point. For r>k, rank(Q^T A)<=k<r; the embedded search cannot generally represent all latent coordinates. This is a standard rank result, not an original theorem. When r>k, no universal optimization advantage can be inferred, even if an occasional finite-budget win occurs.

## Prior work / novelty check
Wang et al. (IJCAI 2013) introduced REMBO and formal effective-dimensionality theory; their paper already proves the almost-sure random-embedding representability result. Dzahini & Wild (SIAM J Optim 2024, DOI 10.1137/22M1524072) establish random-subspace trust-region convergence and expected complexity. Hansen & Ostermeier (Evolutionary Computation 2001, DOI 10.1162/106365601750190398) establish covariance adaptation. Therefore neither random embeddings, switching between embedding dimensions, nor the rank lemma alone are novel.

## Reproducibility
Executed Python SHA256 7eac016b79824decf5db929a65a9f4160bfa1d4f52daab1f080c1d16c068253e
Git blob 4af3f5c0181caf6302bb7b319da662f7da4d9c98 (GitHub file verified byte-identical).
Raw CSV SHA256 aed311890053fcdcc368550f49819f8d01b7767d14154e9f0812a566f3e31d7a
Summary CSV SHA256 1e7ccefde108865a58b9b6a49513b57f8506c1bbf705a262bf241ebb8035cf83
Environment SHA256 0af89d98d0906e497e1bf045f13c876e463b3648df348d467ee7da62a4ec19e2

## Publication assessment and next falsifiable experiment
**Not Q1-ready.** The strongest defensible result is a replicated qualitative phase transition: random embedding works best at low intrinsic dimension, deteriorates when the intrinsic dimension exceeds the embedding dimension. This is expected from prior theory. No original theorem and no superiority over established random-subspace methods. Next: independently evaluate an adaptive intrinsic-dimension detector against fixed Embed4/8, STARS/RSDFO, REMBO, CMA-ES and COBYQA on official COCO and high-dimensional full-rank controls, with 20+ seeds, pre-registered budgets, anytime data profiles, and statistical uncertainty. Any adaptive detector must prove a finite-budget dimension-identification or regret result that is not already in REMBO/STARS.
