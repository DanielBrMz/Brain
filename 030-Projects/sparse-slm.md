---
title: "ActivSparse-SLM — Puentes Collaboration"
type: project
status: complete
created: 2026-03-20
updated: 2026-03-20
tags: [project, research, bch, sparse, slm, puentes, moe, wanda, grant-lab]
---

# ActivSparse-SLM — Puentes Collaboration

> 125M sparse LLM combining SLTrain + ReLU + DeepSeekMoE + Wanda post-training pruning.

---

## Status: Complete (v9, Mar 9, 2026)

**Best checkpoint:** `experiments/runs/125m_v9/ckpt_step_0002500_fixed.pt`
**Wanda-pruned:** `experiments/runs/125m_v9/ckpt_best_wanda_s50.pt`

| Metric | Dense | Wanda 50% |
|--------|-------|-----------|
| PPL (wikitext-103) | 6,582 | 6,605 |
| Activation sparsity | 49.2% | 49.2% |
| FFN weight sparsity | ~20% (SLTrain S) | ~50% (Wanda) |
| PPL degradation | — | **+0.3%** |

**Key result: 50% FFN weight pruning for only 0.3% PPL increase.**

---

## Architecture

- **Activation:** ReLU (NOT dReLU — dReLU caused 100% neuron death)
- **SLTrain:** rank=32, density=0.20
- **MoE:** 1 shared + 4 routed experts, top-2, aux_coeff=0.05
- **ProSparse:** lambda=1e-5
- **Dataset:** allenai/c4 (en) — 350B tokens
- **LR:** 5e-5, warmup=500, stable=5000, decay=6000

---

## Critical Bugs Found (9 runs)

1. **dReLU train/inference split** (v1-v3): sigmoid gate training vs hard threshold at inference → 100% neuron death. Fix: use ReLU.
2. **MoE router collapse** (v4): aux_loss_coeff=0.01 too weak. Fix: raise to 0.05.
3. **Dataset cycling** (v5): wikitext-103 only 103M tokens, cycled 3.8x. Fix: use C4.
4. **SLTrain zero init** (v6-v7, CRITICAL): `low_rank_b` and `sparse_values` initialized to zeros → FFN had zero weights entire training. Model trained attention only. Fix: kaiming init.
5. **LR too high** (v8): lr=1e-4 diverged once FFN contributed real gradients. Fix: lr=5e-5.
6. **MoE tuple unpack** (NeuronScope inference): `sum(expert(x) for expert in shared_experts)` → TypeError. Fix: `sum(expert(x)[0] ...)`.

---

## Key Files

| File | Purpose |
|------|---------|
| `src/model/ffn.py` | `SLTrainLinear._init_weights()` — critical training bug fix |
| `src/model/moe.py` | Tuple unpack fix (lines 109, 127) |
| `scripts/wanda_prune.py` | Post-training Wanda pruning |
| `src/eval/eval_main.py` | PPL + activation sparsity evaluation |

---

## Run History

| v | Key Change | Best Loss | Status |
|---|-----------|-----------|--------|
| v1-v3 | dReLU variants | 7.4-7.9 | Neuron death |
| v4 | ReLU + dense FFN | 7.56 | MoE collapse |
| v5 | Fix MoE, SLTrain | 8.37 | Dataset cycling |
| v6-v7 | C4 dataset | 7.16* | SLTrain zero (FFN=0) |
| v8 | Fix SLTrain init | 8.56 | LR too high |
| **v9** | **lr=5e-5** | **7.90** | **Complete** |

*v6/v7 losses from attention-only model (broken SLTrain)

---

## Related Notes

- [[neuronscope|NeuronScope (visualization)]]
- [[../040-Roles/research-engineer-bch|Research Engineer Role]]
