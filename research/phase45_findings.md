# Phase 45 — Independent anytime restart ablation

## Protocol
Locally executed 80 runs, 16 matched instances: 2 objective families (Sphere and Rastrigin), ambient d=8,20, ranks r=4 and r=d, seeds 3600–3601, and five methods: full COBYQA, fixed Embed8, fresh-subspace restart anchored at incumbent (NewBest), same-subspace restart anchored at incumbent (SameBest), fresh-subspace restart anchored at original x0 (NewOrigin). Box [-5,5]^d enforced for every method. Maximum objective evaluations B=12d. All evaluations recorded as anytime traces. Methods use identical instances and starts. Note d=8,r=8 means Embed8 is full-dimensional, not reduced-dimensional. Two seeds are too few for reliable inference.

## Executed paired results
| Rank regime (n=8) | Method | vs full COBYQA W/L/T | vs Embed8 W/L/T | Mean calls |
|---|---|---|---|---|
| r=4 | Embed8 | 4/1/3 | 0/0/8 | 129.38 |
| r=4 | NewBest | 4/2/2 | 0/3/5 | 153.62 |
| r=4 | SameBest | 4/2/2 | 0/3/5 | 153.50 |
| r=4 | NewOrigin | 4/3/1 | 1/3/4 | 168.00 |
| r=d | Embed8 | 0/6/2 | 0/0/8 | 79.25 |
| r=d | NewBest | 0/6/2 | 4/2/2 | 119.12 |
| r=d | SameBest | 0/6/2 | 0/2/6 | 112.25 |
| r=d | NewOrigin | 0/6/2 | 3/2/3 | 125.38 |

The evidence confirms conditional tradeoffs and shows the importance of reporting actual calls, not just capped budgets. Fresh directions help some full-rank cases compared with fixed embedding, but do not beat full COBYQA. No new superior optimizer is established.

## Literature and novelty
Qian, Hu, Yu, IJCAI 2016 (official conference page, pp1946–1952), already proposes sequential random embeddings for high-dimensional optimization with low optimal epsilon-effective dimensions, explicitly allowing all ambient coordinates to matter. Hansen et al. 2021 COCO is the standardized benchmarking platform. These sources rule out claiming the restart idea or all-dimensional applicability as novel. No original convergence or finite-budget switching theorem has been established. Phase 45 is not Q1-ready as a new algorithm.

## Reproducibility
GitHub source byte-identical to executed local script, Git blob d46b2c3816092f4f3e47be24e60172b090277712; SHA256 4b7173bb7ccb268a34d3e0b6cbb60168500cf2bda57e56832539774b10f4f5ab.
Combined raw SHA256 744113b96953a46d37eede8a2b3884eb04ef5259cf9c942ef9aa67604ae2db98; summary SHA256 ace6f252675a1094de87b7a069e07c3f4b0618a983f189658d51f0f0f16f041e.
d8 raw SHA256 bc3634bb5ef377560a9bf860ce6e38655146824892817a271b6b8328c592b357; trace SHA256 d94a8e3fe4366230cfbb82d5df73a2fcacb9203ae20efa12dc4ba85879ed5a49.
d20 raw SHA256 1ea8d64f82a806c7f5dfedbbb5203984d29282b47e2cb0f27d79d7a9923cd50b; trace SHA256 cfdb4cf4cae3fe40c562bec6471982146b5e247fd19eea9e7f262fc65a15a656.
Workflow committed to reproduce and archive raw traces, execution unverified.

## Next rigorous milestone
The previously staged COCO pilot has not been executed. First validate its cocoex Suite API and fair evaluation accounting on GitHub Actions, including error handling and restart incumbent updates. Then run official COCO/BBOB, 20+ independent instances, full anytime curves, matched budgets proportional to d, and CMA-ES and sequential random embedding baselines. Do not claim Q1 novelty until a new theorem or robust performance superiority is independently established.
