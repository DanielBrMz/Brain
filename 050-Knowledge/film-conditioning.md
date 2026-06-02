---
title: "FiLM — Feature-wise Linear Modulation"
type: knowledge
updated: 2026-04-27
tags: [math, architecture, conditioning, deep-learning]
---

# FiLM — Feature-wise Linear Modulation

## Core Idea

Modulate neural network features based on external conditioning information:

    FiLM(x) = gamma * x + beta

where gamma (scale) and beta (shift) are learned functions of a conditioning input.

## In FetEnhNet

The tissue probability map (4 classes: bg, cortical plate, WM/subplate, CSF) conditions the enhancement decoder:

    gamma, beta = Conv1x1(tissue_map)     # (B, 2*C, H, W) -> split
    output = gamma * features + beta

This is **spatially-varying**: each pixel gets its own gamma/beta based on what tissue is there. The enhancement network applies different strategies per tissue (aggressive denoising in CSF, gentle sharpening in cortical plate).

## Implementation

```
tissue_map -> bilinear resize to feature map dims -> 1x1 Conv -> split into gamma, beta
features -> gamma * features + beta -> ReLU
```

Applied in every decoder block of the EnhancementNet U-Net.

## Teacher Forcing vs. Classifier Predictions

- **Training (teacher forcing):** Use GT tissue labels from NeSVoR/manual segmentation
- **Inference:** Use TissueClassifier predictions (Stage 1 output)
- Gap between GT and predicted tissue maps is the "classifier quality" problem (fg_dice=0.099)

## Why FiLM over Concatenation?

- Concatenation: tissue info enters only at the input -> may be lost in deep layers
- FiLM: tissue info applied at EVERY decoder level -> persistent conditioning
- FiLM is multiplicative + additive -> can scale features up/down, not just add

## Used In
- [[fetenh-net]] — core conditioning mechanism
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Perez et al. "FiLM: Visual Reasoning with a General Conditioning Layer", AAAI 2018.
