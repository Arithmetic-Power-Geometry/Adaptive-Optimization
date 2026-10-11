# Phase 44 — causal-mechanism ablation, theorem, and novelty gate

## Experiment (executed locally)
80 runs = 2 families (Sphere, Rastrigin) × d=8,20 × r=4 or r=d × seeds 3500,3501 × 5 methods. All methods use box [-5,5]^d and budget B=12d. COBYQA full, Embed8 full budget, NewBest fresh subspace with best-incumbent anchor, SameBest same subspace with best-incumbent anchor, NewOrigin fresh subspace with original anchor. Split variants receive B/2 calls per stage. 16 matched cases. At d=8, k=8 is the entire ambient space, and d=8 low/full regimes overlap only in rank but share identical problem generator for given seed; avoid treating overlapping cases as independent replication.

| Regime (n=8) | NewBest vs Embed8 W/L/T | SameBest vs Embed8 W/L/T | NewOrigin vs Embed8 W/L/T | NewBest vs COBYQA W/L/T | NewOrigin vs COBYQA W/L/T |
|---|---|---|---|---|---|
| r=4 | 0/2/6 | 0/2/6 | 3/2/3 | 0/4/4 | 1/5/2 |
| r=d | 4/2/2 | 0/2/6 | 6/0/2 | 0/6/2 | 2/4/2 |

Fresh subspace shows a possible conditional advantage over reusing the same subspace; retaining the best incumbent as anchor is not reliably helpful in this small sample. NO statistical generalization warranted, especially given prior adaptive experimentation and low sample size.

## Mathematical result: finite-query global optimization impossibility (known, not novel)
Let D=[-5,5]^d with d>=1. Consider any deterministic value-query optimizer that makes at most N<infinity queries and returns a point in D, on the class of all infinitely differentiable functions on an open neighborhood of D. Fix epsilon>0. Run it against f0(x)=0 and record its finite queried points and final output. Choose an open ball B contained in the interior of D whose closure excludes all these points. Choose a C-infinity bump phi supported in B, with 0<=phi<=1 and max phi=1. Define f1(x)=-2 epsilon phi(x). Since all observed values are 0 under both objectives, the deterministic optimizer makes the same queries and returns the same output; f1(output)=0, while min_D f1=-2 epsilon. Hence its suboptimality exceeds epsilon. Therefore no deterministic finite-query optimizer guarantees epsilon-global optimality uniformly over unrestricted C-infinity objectives. This standard adversarial indistinguishability argument is not a new theorem and does not preclude guarantees for restricted smoothness classes with bounded constants, convexity, or probabilistic success criteria. A randomized optimizer requires a separate minimax/distributional argument.

## Verified literature and novelty assessment
Primary IJCAI official proceedings verify Qian, Hu and Yu 2016 sequential random embeddings (pp. 1946–1952). Publisher/Oxford verify Cartis and Roberts 2026 randomized quadratic-model DFO (DOI 10.1080/10556788.2025.2601668). Springer verifies Bellavia et al. 2026 random subspace objective-function-free optimization (JOTA 209, article 63). Cartis and Roberts 2026 arXiv 2608.17307 is explicitly a PREPRINT discussing dimension-dependence improvements via rescaled JLTs. These are substantial prior-art obstacles. No theorem unique to our optimizer has been proved. Q1 new-optimizer readiness: **NO**.

## Reproducibility
Source SHA256 a68c606b86f966c9bd70454cb342bd6aa6c678483de7c167d9350b38a6efe8be, Git blob bc8cf613bd1213fc823d43626cc20c71cd708119; fetched GitHub source blob verified byte-identical. Raw CSV SHA256 86d8b67bde26470b9c357d085a7eeb773291db2baf20477bce09a309a4c0c72c. Summary CSV SHA256 c0bb8ee9dfd3314c38f0afcf44fef4ade76327796dd221ff613bd3d8af743fc1. Environment SHA256 f63e45f34a5d5f485982a9eea1215828b072aebf3b86db5b49482cb053ef19ee. Complete raw data generated locally; GitHub workflow saved to reproduce and archive; workflow execution not yet verified.

## Next gate
Official COCO BBOB must be implemented and executed with independent suite instances and a fixed budget, standardized target metrics, complete traces, 20+ instances/seeds, CMA-ES and RSDFO/SRE baselines. The previously staged COCO pilot has not been validated and should not be described as a working benchmark. A genuinely new theorem would require explicit assumptions and a cost-aware dimension-switching policy stronger than sequential random embeddings, plus ablations isolating switching overhead and information gain. Do not assert that such a theorem is already proved.
