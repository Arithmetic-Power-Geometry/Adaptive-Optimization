# Phase 24: independent held-out replication of golden-angle polling

Date: 2026-10-11. **960 experiments actually executed locally**: Ackley, Rastrigin, Griewank, Rosenbrock × dimensions 2,5,10 × 20 new seeds 1400–1419 × Golden, Rational, RandomAngle, COBYQA. Each run had a strict maximum 160 objective evaluations. Synthetic shifted/rotated test functions; **NOT official COCO/BBOB**.

## Predefined mechanism and controls
Golden-angle two-coordinate polling uses theta <- theta+2*pi*(sqrt(5)-1)/2. Rational uses theta <- theta+2*pi*3/8. RandomAngle draws an independent uniform angle. The two-coordinate plane sequence is identical for the three polling methods on each matched problem. The same step updates and starting point are used; COBYQA is a model-based comparator. All objective calls counted, including initial evaluation.

## Primary matched-pair results (240 independent instance/seed combinations)
| Comparison | Golden wins | Golden losses | Ties | Exploratory two-sided sign-test p |
|---|---:|---:|---:|---:|
| Golden vs Rational | 105 | 100 | 35 | 0.7800 |
| Golden vs RandomAngle | 104 | 104 | 32 | 1.0000 |
| Golden vs COBYQA | 39 | 177 | 24 | 3.40e-22 |

Tolerance 1e-10 for win/loss/tie. Sign tests assume independent pairs; family-level clustering and multiple comparison concerns limit inference. Actual mean evaluations: Golden 155.94; Rational 156.30; RandomAngle 155.91; COBYQA 107.14. Thus COBYQA also uses fewer evaluations on average.

Golden wins vs COBYQA by family, out of 60 each: Ackley 13, Rastrigin 16, Griewank 1, Rosenbrock 9. Rational wins 47/240 vs COBYQA; RandomAngle 38/240. No robust golden-angle advantage.

## Replication conclusion
Phase 23 Golden vs Rational 43 wins / 21 losses / 8 ties and vs RandomAngle 41/22/9. Phase 24 independent seeds: 105/100/35 and 104/104/32. **Earlier angle superiority did not reproduce.** This is a clear negative result, not a success claim. Changing the mechanism again without addressing prior art and validation would be methodologically weak.

## Provenance
Executed source SHA256 7a31e351de3c8be4be18fd40820bb6d7231e9f478cf57d85ba8fa40073f05b94; GitHub blob SHA d7744978f4e45d5a56dd661639d5cc4decb85423, verified exact match.
Raw CSV SHA256 42f43f15e71adf9082a17214d737b3319a3ca4c223f264734308ee2614c0b5d6.
Summary CSV SHA256 d5202716a1cdb70c2f804a492cd43d6cbb561f63c69e84eabfe76363b068f70c.
Environment JSON SHA256 18913b8f4bb079258cc0529753803e4f3ceda3e85b4885a39585d8198d42d173.
Raw CSV, summary and environment exist locally. GitHub Actions configured to generate/commit exact results; CI run not yet confirmed. Do not claim raw GitHub upload before checking.

## Closest verified prior art
Van Dyke, Benjamin (2014), 'Equal Angle Distribution of Polling Directions in Direct-Search Methods,' Journal of Optimization 2014, article 619249, DOI 10.1155/2014/619249: established deterministic equal-angle polling and positive-basis designs. Ragonneau and Zhang (2024), PDFO, Mathematical Programming Computation 16:535–559, DOI 10.1007/s12532-024-00257-9: strong model-based DFO baselines. Official COCO getting-started guide confirms pip install coco-experiment cocopp and Suite('bbob',...) benchmark.

## Q1 assessment
No proven novel complexity/convergence result and no robust modern-baseline superiority. Phase 24 specifically invalidates Phase 23's proposed empirical golden-angle advantage on new seeds. **Not ready as a novel Q1 general-purpose optimizer.** A scientifically honest publication may focus on comparative directional-sequence sensitivity, but broader official COCO results and novelty review remain necessary.
