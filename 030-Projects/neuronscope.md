---
title: "NeuronScope — Activation Sparsity Visualization"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, research, bch, neuronscope, sparsity, interpretability, llm, grant-lab]
---

# NeuronScope — Activation Sparsity Visualization

> Research project at BCH/HMS FNNDSC Grant Lab. Real-time visualization of LLM activation sparsity.

---

## Status: v2 Complete (Mar 6, 2026)

**Stack:** FastAPI + WebSocket + Canvas 2D heatmap (no Gradio)
**Env:** `neuronscope` (Python 3.12, PyTorch 2.10, transformers 5.3, websockets 16)
**Location:** `/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/activ_sparse_slm/neuronscope_v2/`

```
neuronscope_v2/
├── backend/
│   ├── inference.py    # TEAL sparsifier + async stream_generation
│   ├── main.py         # FastAPI + /ws/generate WebSocket
│   └── activ_sparse.py # Hooks on expert.act, streams per-layer data
├── frontend/
│   ├── index.html      # Dark sci-fi UI
│   └── static/
│       ├── heatmap.js      # Canvas 2D 28×96 lerp heatmap
│       ├── app.js          # WebSocket client + UI state
│       ├── activ_sparse.js # 2 heatmaps + layer bars + sparkline + arch diagram
│       └── styles.css      # Dark theme + animations
└── run.sh              # Launcher (NS_MODEL/NS_SPARSITY/NS_DEVICE env vars)
```

**Launch:**
```bash
cd neuronscope_v2 && ./run.sh [--port 7861] [--sparsity 0.3]
# For ActivSparse model:
bash run.sh --activ-sparse experiments/runs/125m_v9/ckpt_step_0002500_fixed.pt --port 7860
```

**E2E Results:** 25 tok dense + 25 tok sparse | 700 activation snapshots/run | 26-31 tok/s

---

## Critical Finding

**"NeuronScope" paper already exists:** arXiv:2601.03671 (Jan 7, 2026) — multi-agent framework for polysemantic neuron explanation. Our demo needs to differentiate or align.

---

## Key Research Threads

### Sparsity
- **TEAL** (ICLR 2025): Training-free activation thresholding, 40-50% sparsity, no PPL loss
- **Deja Vu**: 85% contextual sparsity, 2x speedup on OPT-175B
- **DeepSeek-V3.2**: Weight + activation + attention sparsity combined (DSA)

### Interpretability
- **SAEs (Sparse Autoencoders)**: Decompose polysemantic neurons into monosemantic features
- Anthropic scaled to Claude 3 Sonnet — thousands of interpretable features
- **Next step:** Train SAE on Qwen2.5-1.5B activations, show feature-level heatmap

### MCP Integration Opportunity
NeuronScope MCP server = expose `analyze_sparsity`, `explain_neuron` as tools

---

## MVP v2 Priority List

1. TEAL (2 days): Fix sparsity quality, achieve 40% coherent sparsity
2. Agent commentary (2 days): Model explains its own heatmap
3. SAE integration (1 week): Feature-level interpretability
4. MCP server (1 day): Expose as AI tool
5. Reasoning chain viz (2 days): Show sparsity through chain-of-thought

---

## Publishable Research Questions

1. Do RL-trained reasoning models have different activation sparsity than SFT models?
2. Does activation sparsity correlate with hallucination rate?
3. Can TEAL + SAE decomposition give a unified theory of "what the model chooses to compute"?

---

## Related Notes

- [[sparse-slm|ActivSparse-SLM (Puentes)]]
- [[../040-Roles/research-engineer-bch|Research Engineer Role]]
- [[fetenh-net|FetEnhNet (main project)]]
