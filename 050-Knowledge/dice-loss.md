---
title: "Dice Loss & Dice Coefficient"
type: knowledge
updated: 2026-04-27
tags: [math, loss-function, segmentation, medical-imaging]
---

# Dice Loss & Dice Coefficient

## Definition

The Dice coefficient (Sorensen-Dice, F1 score) measures overlap between two sets:

    Dice(A, B) = 2|A intersect B| / (|A| + |B|)

Range [0, 1]. 1 = perfect overlap.

## Soft Dice (differentiable)

For network output probabilities pred_c and one-hot target_c:

    Dice(c) = (2 * sum(pred_c * target_c) + smooth) / (sum(pred_c) + sum(target_c) + smooth)

    L_dice = 1 - (1/C) * sum_c Dice(c)

The smooth term (epsilon, typically 1.0) prevents division by zero.

## Why Dice over Cross-Entropy?

- CE counts per-pixel errors -> dominated by majority class (background)
- Dice measures per-class overlap -> each class contributes equally (macro-averaging)
- For highly imbalanced data (ventricles = <5% of volume), Dice naturally handles the imbalance

## Combined: DiceFocalLoss

MONAI combines both:

    L = lambda_dice * DiceLoss + lambda_focal * FocalLoss

Used in: [[victoria-hydro-model]] (lambda_dice=0.5, lambda_focal=0.5, gamma=2.0)

## Combined: DiceCELoss

    L = DiceLoss + lambda_ce * CrossEntropyLoss

Used in: FetEnhNet TissueClassifier with label smoothing (epsilon=0.10) to handle noisy atlas-projected labels.

## Used In
- [[victoria-hydro-model]] — primary loss function
- [[fetenh-net]] — SoftDiceLoss + DiceCELoss for tissue classifier
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Milletari et al. "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation", 3DV 2016.
