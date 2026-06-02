---
title: "FetEnhNet — Tissue Classifier Loss Function Research"
type: reference
status: active
created: 2026-04-23
updated: 2026-04-23
tags: [fetenh-net, loss-function, tissue-classifier, training, research]
related: [[fetenh-net]], [[fetenh-data-pipeline-plan]], [[fetenh-inverse-alignment-pipeline]]
---

# Tissue Classifier Loss Function — Research & Decision

> Researched Apr 23, 2026. Replaces the Run 16/17 loss configuration.

## Problem

Runs 16-17 used focal loss (gamma=2.0) + weighted NLLLoss with weights `[1.0, 25.0, 9.0, 10.0]` (bg, cortical_plate, wm_subplate, csf). The tissue classifier never converged stably — gradient conflict dominated, FiLM conditioning was noisy, and the 4-class tissue FiLM performed worse than the simple 2-class brain mask FiLM (Run 18).

## Root Cause Analysis

1. **Focal loss mines noisy boundary pixels:** Atlas-projected labels have thick-slice averaging artifacts (~3mm) at every tissue boundary. These boundary pixels are "hard examples" because the labels themselves are wrong. Focal's `(1-p_t)^gamma` upweighting forces the model to learn noise.

2. **CP weight of 25 amplifies label noise 25x:** Dice already handles class imbalance at the region level. The CE weight of 25 on top of Dice does double duty AND amplifies every mislabeled CP pixel.

3. **Overconfident probabilities hurt FiLM:** Pure Dice and DiceFocal produce near-binary probability maps. FiLM conditioning works best with calibrated soft probability gradients at tissue boundaries, not hard 0/1 transitions.

## Losses Evaluated

| Loss | Calibration | Imbalance | Label Noise | Verdict |
|------|-------------|-----------|-------------|---------|
| Weighted CE alone | Best | Fragile (weights) | Amplifies | No |
| Soft Dice alone | Poor (overconfident) | Good (implicit) | Moderate | No |
| **DiceCE** | **Good** | **Good** | **Moderate** | **YES — primary** |
| DiceFocal | Poor | Good | **BAD (mines noise)** | No |
| Focal alone | Poor | OK for bg | BAD | No |
| Tversky | Poor | Best | Over-parameterized | No |
| HD Loss | N/A | Thin structures | Bad with noisy labels | Optional, late, light |
| Label smoothing | Improves any | N/A | **Best single fix** | **YES — always** |

## Decision: DiceCE + Label Smoothing

### Primary Loss

```python
L_tissue = L_softDice + 1.0 * L_weightedCE
```

- `L_softDice`: per-class averaged, softmax-based (MONAI `DiceLoss(softmax=True)`)
- `L_weightedCE`: standard CE with **reduced** weights: `[1.0, 8.0, 4.0, 5.0]`
- Equal combination (lambda=1.0), matching nnU-Net default

### Label Smoothing (epsilon = 0.10)

```python
# Replace hard one-hot [0, 0, 1, 0] with smoothed [0.025, 0.025, 0.925, 0.025]
smoothed = (1 - epsilon) * one_hot + epsilon / num_classes
```

- Directly addresses atlas-projection label noise
- Karimi et al. (arXiv:2203.14962) validated this on ~270 fetal subjects with noisy atlas labels — same scenario as ours
- Can use PyTorch's `CrossEntropyLoss(label_smoothing=0.10)`

### Optional: Light HD Loss (late training only)

```python
# From epoch 30+, after tissue classifier has converged
L = L_DiceCE + 0.05 * L_HD95
```

- Only if label noise at boundaries is addressed first (label smoothing handles this)
- lambda_HD <= 0.05, do NOT combine with focal loss

## What Changed from Run 16/17

| Setting | Run 16/17 | New |
|---------|-----------|-----|
| Loss | Focal NLLLoss (gamma=2.0) | DiceCE |
| CE weights | [1, 25, 9, 10] | [1, 8, 4, 5] |
| Label smoothing | None | epsilon=0.10 |
| Focal | Yes (gamma=2.0) | **Removed** |
| HD loss | None | Optional, late, light |

## Why This Should Fix the Convergence Issue

1. No focal → no aggressive learning of noisy boundary pixels
2. Reduced CP weight (25→8) → 3x less amplification of label noise
3. Label smoothing → prevents overconfident learning of wrong labels
4. DiceCE → calibrated probability maps → better FiLM conditioning
5. Sequential training (Phase A freeze → Phase B) already addresses gradient conflict

## FiLM Conditioning Quality Ranking

Probability calibration matters because FiLM uses `gamma(tissue) * features + beta(tissue)` per-pixel. Calibration rank:

**WCE ≈ DiceCE > DSC++ > pure Dice > DiceFocal > Tversky ≈ Focal**

DiceCE + label smoothing is the sweet spot for both segmentation accuracy and FiLM conditioning quality.

## Key References

- nnU-Net (Isensee 2021, Nature Methods): DiceCE as default, won/competitive in 49 tasks
- arXiv:2111.00528: Dice produces overconfident outputs across 6 biomedical datasets
- arXiv:2203.14962 (Karimi et al.): Label smoothing for noisy atlas labels in fetal brain
- arXiv:2104.05788: Spatially-varying label smoothing improves boundary calibration
- FeTA 2021-2024: DiceCE or Dice+Focal were plurality approaches; CP consistently hardest class
- Lin et al. (arXiv:1708.02002): Focal loss originally for 2-class detection, not calibrated

## Related

- [[fetenh-net]] — Training history, Run 16/17 failure analysis
- [[fetenh-data-pipeline-plan]] — Phase A training uses this loss
- [[fetenh-inverse-alignment-pipeline]] — Source of tissue labels (zero registration error)
