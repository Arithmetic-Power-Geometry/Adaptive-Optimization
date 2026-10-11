# Cumulative adaptive optimization research, Phases 1–18
Updated 2026-10-11.

| Phase | Finding |
|---|---|
| 1–6 | Adaptive, rotated, coupled, memory and gated polling: mixed results; memory-probe savings do not imply evaluation savings |
| 7–8 | Held-out and budget analyses: small, budget-sensitive memory improvements |
| 9–11 | Powell and statistical comparisons: Powell often stronger; official COCO not verified |
| 12 | Finite-transcript ambiguity theorem: valid, not verified original |
| 13 | Finite-difference descent certificate: classical ingredients; mixed performance |
| 14 | Independent replication: prior LineMemory gains mostly vanished |
| 15 | Bounded-noise sign and acceptance certificates: correct, NoiseAwareFD mostly worse |
| 16 | 480-run modern-baseline comparison: COBYQA dominates AdaptivePoll |
| 17 | 384 multimodal tests: two-start COBYQA 16/96 paired wins against COBYQA; Phase 17 local empty summary corrected from 384 raw rows |
| 18 | 54-run warm-start/restart diagnostic: fixed restart 1/18 wins, plateau rule 2/18; plateau never triggered |

## Q1 scientific gate
**No new theorem shown beyond the literature, no robust modern-baseline superiority, and no official BBOB. Not Q1-ready as a novel optimizer.** Published literature: Scheinberg (2026), ICM Vol 7, DOI 10.1137/25M1806016, proves model-based DFO complexity, including inexact oracles. Ma et al. (2025), DOI 10.1007/s10589-025-00686-9, evaluate model-and-search on 501 public problems. Generic complexity and switching are not novel.

## Reproducibility
Phase 18 exact executed source committed and Git blob verified; raw records remain local until CI executes and hashes are checked. The GitHub workflow is configured but **not verified successful**. Phase 17 regenerated local summary has 48 rows; previous empty file should not be used.
