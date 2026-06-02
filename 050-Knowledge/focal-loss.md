---
title: "Focal Loss"
type: knowledge
updated: 2026-04-27
tags: [math, loss-function, class-imbalance, segmentation]
---

# Focal Loss

## The Problem

In medical image segmentation, background dominates (>90% of voxels). Standard cross-entropy is overwhelmed by easy, correctly-classified background pixels. The network never learns to segment small structures.

## Definition

    FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t)

where p_t is the model's predicted probability for the ground truth class.

## The Modulation Factor

(1 - p_t)^gamma is the key:

| p_t (confidence) | gamma=0 (CE) | gamma=2 (focal) |
|-------------------|--------------|------------------|
| 0.9 (easy)        | 1.0          | 0.01             |
| 0.5 (moderate)    | 1.0          | 0.25             |
| 0.1 (hard)        | 1.0          | 0.81             |

With gamma=2, easy examples contribute ~100x less than hard examples. The network focuses learning budget on the hard, informative cases (ventricle boundaries, small structures).

## Combined with Dice (DiceFocalLoss)

MONAI's implementation:

    L = lambda_dice * DiceLoss + lambda_focal * FocalLoss

Both lambda=0.5, gamma=2.0 in the hydro model. Dice handles class-level balance; focal handles instance-level difficulty.

## Used In
- [[victoria-hydro-model]] — DiceFocalLoss (primary loss)
- [[dice-loss]] — combined formulations
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Lin et al. "Focal Loss for Dense Object Detection", ICCV 2017.
