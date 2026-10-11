# Phase 43: Equal-domain negative controls and independent replication

## Exact protocol
144 local optimization runs = 3 objective families (Sphere, Rastrigin, Rosenbrock) x ambient dimensions 8,20 x effective rank 4/full x 3 new seeds (3400–3402) x 4 methods (COBYQA, DE, Embed8, Restart8). Box [-5,5]^d is imposed on **all** methods. Reduced-space COBYQA uses linear constraints lb-anchor <= A z <= ub-anchor, avoiding the clipped-objective confound. DE uses the same bounds, popsize 5, no polishing, x0 included. Objective budget B=12d (96 or 240), strict charged evaluations. No ground-truth rank supplied to the methods.

## Matched results, tolerance 1e-8
| Regime | Embed8 vs COBYQA W/L/T | Restart8 vs COBYQA W/L/T | Restart8 vs Embed8 W/L/T | COBYQA vs DE W/L/T |
|---|---|---|---|---|
| r=4, n=18 | 8/2/8 | 5/7/6 | 1/10/7 | 18/0/0 |
| r=d, n=18 | 2/13/3 | 3/12/3 | 12/3/3 | 18/0/0 |
| all, n=36 | 10/15/11 | 8/19/9 | 13/13/10 | 36/0/0 |

At d=8, Embed8 spans the full ambient dimension and is not a dimension-reducing algorithm. Across full rank d20, Embed8 and Restart8 both lost all nine cases to COBYQA. DE's population initialization consumes much of the strict 12d budget, so DE outcomes do not establish general superiority. For d20 full-rank, actual mean calls COBYQA 182, DE 240, Embed8 99.22, Restart8 180.44, making evaluation-cost normalization important.

## Mathematical status
Standard rank theorem: for Q in R^{d x r} orthonormal and a continuous random embedding A in R^{d x k}, rank(Q^T A)=min(r,k) almost surely. This does not guarantee global optimization in a bounded feasible domain because preimages can violate box constraints. It is not a novel theorem. Sequential random embeddings for objectives in which all dimensions may matter were already introduced by Qian, Hu and Yu (IJCAI 2016), as confirmed on the publisher's abstract page. REMBO was introduced by Wang et al. (IJCAI 2013). These facts rule out claiming novelty for the restart mechanism alone.

## Reproducibility
Local source SHA256 993b602d16889c7c44f27ed0c02f710874139206bb22f90313a256e491f77bfe, Git blob 3c09a90951e8989c6ed77c3d591391ef04c44cb5. GitHub source fetched and verified **byte identical** to locally executed source.
Raw local CSV SHA256 f15691aa7ae9dd576ea67c175f8651d16764d16b66a01ac62142052be48f7f64.
Summary local CSV SHA256 2ed8178e5159d8ea336abd66107a78e3ea5161b22eb1965766ede0065a1f1e9d.
Per-dimension raw CSV SHA256 d8 1505d4a8486af1a10fea6501639c38aff5ec3daaa514936fd19cdd9a65e7f6d3; d20 3f38260fc367cb90033107deb3d6ac83f7121a6a90cbd17e749fdb8886e7930d.
Environment SHA256 2fbce0ec30bd48595ed4b980a4df2efde07b40a0094ced01b4e3167ca81ca46a.
GitHub workflow committed but successful execution/raw archive NOT confirmed.

## Research outcome
The low-rank vs full-rank crossover is replicated under common box constraints. This is useful evidence but neither a new optimization algorithm nor a new theorem. **Not Q1-ready as a novel optimizer.** Official COCO/BBOB benchmarking and strong modern comparators remain unexecuted. Next priority: fix the COCO pilot before running it (restart anchors, strict objective budget, fresh problem instances, suite filters, observer lifecycle), execute with GitHub Actions, and archive full raw target traces.
