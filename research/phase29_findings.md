# Phase 29 — Exponential ZigZag Turning Search: negative result

**Status:** 192 actual local executions, 48 matched instances; 160 function evaluations maximum per method. Four shifted/rotated synthetic families (Ackley, Rastrigin, Griewank, Rosenbrock), dimensions 2,5,10, held-out seeds 1900–1903. Methods: ExpoZigZag, ZigZag, RandomPoll, SciPy COBYQA. These are not official COCO/BBOB functions.

## Proposed mechanism
For accepted previous direction u and fresh random perpendicular direction v, ExpoZigZag polls +/-[cos(theta_k)u + (-1)^k sin(theta_k)v], with theta_k=(pi/3)exp(-k/8)+pi/18. Turns reset after 4d failed polls. Steps increase 1.08 on improvement, decrease 0.7 on failure. Objective calls include the initial point. Parameters fixed before held-out testing.

## Outcomes
| Algorithm | Wins vs COBYQA | Losses vs COBYQA | Mean objective evaluations |
|---|---:|---:|---:|
| ExpoZigZag | 1/48 | 47/48 | 160.00 |
| ZigZag | 4/48 | 39/48 | 157.33 |
| RandomPoll | 7/48 | 37/48 | 156.65 |
| COBYQA | — | — | 110.15 |

ExpoZigZag vs original ZigZag: **6 wins, 42 losses, zero ties**. This experiment provides evidence AGAINST the chosen exponential-turn rule. It does not support any breakthrough or robust improvement.

## Mathematical critique
Exponential decay in angular displacement produces persistent alignment with the previous successful direction. On curved or badly oriented landscapes, such persistence may reduce directional coverage and spend nearly all of the evaluation budget without sufficient decrease. The angular formula alone does not establish positive spanning, sufficient decrease, or global convergence. Existing grid-based convergence analysis already permits rotation, scaling and shearing of search grids (Coope & Price, DOI 10.1137/S1052623499354989). Direct-search geometry and positive bases are covered by Conn, Scheinberg & Vicente (2009), DOI 10.1137/1.9780898718768. Model-based trust-region competitors are documented by Ragonneau & Zhang (2024), DOI 10.1007/s12532-024-00257-9.

## Provenance
Executed Python SHA256 bc16583128f4470dd19b9b351bd23cd5dd8b4f627ce6bca6e71dfa1ac5b63794.
Git blob 044a02a8c2051acd83bb22bc6e177a599933de96; verified exact GitHub match.
Raw CSV SHA256 feb7fa2f2c07967d4a08710e2b9eeec242fd107fff5a386ffa9e479e17915aff.
Summary CSV SHA256 fbe17dc21266c50099778216c2f2dc359d6f95c23b0d745110430afeed0bd792.
Environment JSON SHA256 9e05a9c614c58718ef135ed005fed0f8ab9a90f74d9b254a302ad69d9b144347.
Raw CSV, summary, source, environment and log were generated locally; GitHub Actions workflow is configured to regenerate and commit raw data but run success not yet confirmed.

## Q1 assessment
No superiority over COBYQA, no original mathematical theorem, no verified COCO/BBOB benchmark. **Not Q1-ready as a novel general-purpose optimizer.** This result is a useful negative ablation and motivates abandoning ad-hoc turning schedules. A more promising gap is certified, evaluation-budget-aware model switching, subject to independent prior-art verification and proof.
