# Phase 23 — Controlled golden-angle versus rational/random directions

**Date:** 2026-10-11. **Status:** 288 locally executed runs; 4 families (Ackley, Rastrigin, Griewank, Rosenbrock) × 3 dimensions (2,5,10) × 6 held-out seeds (1300–1305) × 4 methods. Maximum 160 evaluations per method and instance. These are custom shifted/rotated synthetic problems, **not** official COCO/BBOB.

## Controlled mechanism
The same pseudorandom two-coordinate plane sequence (seed+50000) is used for Golden, Rational, RandomAngle on each problem instance. Golden advances by 2*pi*(sqrt(5)-1)/2; Rational by 2*pi*3/8; RandomAngle draws independently from uniform [0,2*pi) with separate RNG seed+72000. All share symmetric +/- polls and step size multipliers 1.08 after success, 0.7 otherwise. COBYQA is SciPy's established model-based comparator. Same maximum budget, actual objective calls may differ.

## Paired comparisons (72 instances)
| Comparator | Golden wins | Comparator wins | Numerical ties |
|---|---:|---:|---:|
| Rational angle | 43 | 21 | 8 |
| Random angle | 41 | 22 | 9 |
| COBYQA | 17 | 48 | 7 |

Win tolerance 1e-10. Mean evaluations Golden 155.58, Rational 156.18, RandomAngle 155.81, COBYQA 106.38. Family-specific Golden wins vs COBYQA: Ackley 7/18, Rastrigin 7/18, Griewank 1/18, Rosenbrock 2/18. Golden therefore wins a majority vs both angle controls, but loses the majority vs COBYQA.

## Reproducibility integrity
Local executed source SHA256 b546a3bcd8445dd3f39203c985e076f0324a8510ea98d6dd0a4486e892054d65.
Local raw CSV SHA256 3c4dc2307c6caec2f1d3db4e842f51bc3d4b64282146504cab9ad4bb5e9c39c8.
Local summary SHA256 cefcc47b7c6209bd69e2f661910247b973a58a26f661c6ee3759a3a7541b3720.
Local environment SHA256 d6a2974c871e20a1f6f5c78dc818cd47067b3e84e6690f1c8ae62190961350b8.
The GitHub script is a reconstruction of the executed source and has NOT been verified byte-identical. The workflow may generate semantically equivalent outputs but requires verification. Full raw data exists locally and is not yet confirmed in GitHub.

## Closest verified prior art
Van Dyke (2014), DOI 10.1155/2014/619249, studies equal-angle distribution of polling directions and deterministic directional search. Roberts & Royer (2023), SIAM J Optim 33(4):3057–3082, DOI 10.1137/22M1488569, establish probabilistic descent in random subspaces with complexity guarantees. Gratton et al. (2015), DOI 10.1137/140961602, establish probabilistic direct-search theory. Hansen et al. (2021), DOI 10.1080/10556788.2020.1808977, establish the COCO benchmarking protocol.

## Originality and journal gate
**Novelty not established.** Golden-angle sequence is a known equidistribution device, and deterministic/equal-angle polling is established prior art. Our exact 2D-plane scheduling plus golden-angle combination is a candidate experimental variation, not yet a verified novel convergence or complexity theorem. No official BBOB and no robust superiority over COBYQA. **Not yet Q1-ready as a novel general-purpose optimizer.** A focused experimental analysis of directional sequence effects may be publishable after larger, independently preregistered COCO comparisons and a rigorous contribution statement.

## Next high-value action
Freeze algorithm, verify local-vs-CI source and hashes, then execute COCO BBOB with matched budgets, target attainment and ECDF/data profiles, include CMA-ES, BOBYQA and a direct-search solver. Do not introduce further heuristics until mechanism and provenance are settled.
