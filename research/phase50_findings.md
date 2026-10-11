# Phase 50: stopping the loop — evaluation-cost audit and publication gate

## Research gap, identified and tested
Previous phases repeatedly varied restart and switching heuristics without establishing an advantage over strong full-dimensional COBYQA. The concrete gap is *evaluation opportunity cost*: objective equality at a 120-evaluation cap does not imply equal efficiency when one solver used 45 evaluations and another used 84. A progress-based gate cannot infer effective dimension from stagnation alone.

## New analysis of existing data (no additional optimization trials)
Analyzed the 19,308 actual per-evaluation traces of 200 Phase49 runs on 40 matched mock problems. Compared best-so-far objective at precisely 40, 80 and 120 charged evaluations, carrying forward final best values when a solver stopped early. A fixed 1e-8 absolute tolerance defines ties. New data files: results/phase50_anytime_summary.csv (30 rows), locally generated detailed 600-row phase50 anytime matched CSV. No official COCO results.

## Verified results
- Shifted Sphere (20 instances, d10): full COBYQA mean 44.95 calls, Gate8Full mean 83.80 calls; ratio 1.8643 (86.43% more evaluations). Both reach near-zero final objective. Gate8Full loses all 20 at 40 calls and ties all 20 at 80 and 120.
- Shifted Rastrigin (20 instances, d10): median best after 120 calls COBYQA 5.472276 vs Gate8Full 15.452601 (Gate is ~2.82x larger). Gate loses all 20 at 80 and 120; at 40 it wins 10 and loses 10.
- Gate8Full beating Embed8 does not imply it beats full COBYQA. Diagnostic overhead dominates on easy convex cases and provides no demonstrated benefit on these multimodal cases.
- These are exploratory mock functions, not COCO/BBOB; the 20 instances vary shifts but are not 20 distinct problem classes.

## Gap measures
1. **Killed repeated synthetic variants**: no new optimizer proposed in this phase.
2. **Cost-matched performance**: objective at 40/80/120 evaluations, actual mean calls and stopping behavior.
3. **Paper-quality negative result**: progress-gate opportunity-cost failure quantified and reproducible.
4. **Official COCO still required**: Phase48 official pilot staged, successful GitHub Actions execution not verified. Do not assert official benchmark results.
5. **Mathematical novelty not yet present**: sequential random embeddings and random-subspace DFO are prior art; need original theorem and independent strong-baseline comparisons.

## Research novelty and publication assessment
Novel general-purpose optimizer: NO. Empirical insight: diagnostic opportunity cost can erase gains from conditional switching, quantified here for one particular heuristic and synthetic family. The insight is not a general impossibility theorem and should not be advertised as mathematical novelty. Q1-ready as new optimizer: NO.

## Literature
COCO official Suite API https://numbbo.github.io/coco-doc/apidocs/cocoex/cocoex.Suite.html ; SciPy COBYQA https://docs.scipy.org/doc/scipy-1.15.0/reference/optimize.minimize-cobyqa.html ; Qian et al. 2016 IJCAI https://www.ijcai.org/Abstract/16/278 ; Hansen et al. 2021 COCO DOI 10.1080/10556788.2020.1808977. These references already appear in the master BibTeX and should not be duplicated.

## Hard next gate
Do not run Phase51 synthetic variants. First obtain actual official COCO BBOB GitHub Actions run with logs, dependency versions, raw results, and independently verifiable baseline. Only then expand the benchmark. If no official data or new theorem, do not claim Q1 novelty.
