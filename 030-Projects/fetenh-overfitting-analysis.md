---
title: "FetEnhNet -- Overfitting Root Cause Analysis"
type: analysis
status: active
created: 2026-04-14
updated: 2026-04-14
tags: [fetenh-net, overfitting, training, analysis]
related: [[fetenh-net]], [[fetenh-label-projection-pipeline]]
---

# FetEnhNet -- Overfitting Root Cause Analysis

> Why Run21 overfits and what Run22 must fix.

## Evidence

- Run21_sup: best val_sup = 0.0705 at epoch 12, rises to 0.0799 by epoch 300
- Run21_sure: best val_sup = 0.0716 at epoch 17, rises to 0.091 by epoch 210
- Train loss keeps decreasing through all 300 epochs (memorization)

## Rationale-level causes

### 1. Small effective dataset

12,932 synthetic pairs come from only 254 unique HIGH subjects multiplied by 6 degradation types. The network sees the same 254 brain anatomies repeatedly. By epoch 12 it has memorized what each subject's brain looks like and stops generalizing. The degradation variation adds input diversity but not enough anatomical diversity.

### 2. Synthetic-to-real domain gap

The supervised loss trains on synthetic degradations (Gaussian noise, Gaussian blur, bias field, mixed). Real LOW stacks have scanner-specific noise characteristics: Rician distribution, spatially varying coil sensitivity, motion artifacts, inter-slice intensity inconsistency. The model learns to perfectly undo synthetic artifacts (train loss drops) but this capability does not fully transfer to real noise patterns (val loss rises).

SURE was designed to bridge this gap by training directly on real LOW stacks. However, due to the checkpoint selection bug (#6), SURE's effect was never properly evaluated.

### 3. Misaligned tissue conditioning labels

Before the April 9-14 projection pipeline work, the tissue labels projected onto raw slices were incorrectly aligned. The model learned to condition on labels that did not match the actual anatomy at each pixel. During validation on different subjects, the mismatch pattern is different, contributing to generalization failure.

As of April 14, 25 subjects now have correctly aligned tissue labels (Dice >= 0.80 vs brain mask). This removes a major source of train/val distribution mismatch for the conditioning pathway.

## Implementation-level causes

### 4. No regularization

Run21 used no weight decay, no dropout, and no data augmentation beyond the degradation pipeline. The enhancement network has approximately 5M parameters. Training on 254 unique anatomies without regularization is a classic recipe for memorization.

### 5. No early stopping

Run21 trained for 300 epochs. Best validation loss occurred at epoch 12. The remaining 288 epochs were pure overfitting. Training should have stopped at epoch 20-30 with a patience of 10.

### 6. Checkpoint selection bug

For Run21_sure, best.pt was saved at epoch 17, before SURE activated at epoch 32. The "best" SURE checkpoint has zero SURE exposure. The checkpoint selection criterion (minimize val_sup) is inherently biased toward the pre-SURE regime because SURE adds stochastic gradient noise that temporarily increases val_sup even when it improves real-image quality.

## What fixes what

| Fix | Addresses | Expected impact |
|-----|-----------|-----------------|
| More subjects (25+ tissue labels, 300+ available) | #1 anatomy diversity | Largest single win. 2x more unique anatomies delays memorization. |
| Correctly aligned tissue labels | #3 conditioning quality | Removes systematic conditioning error. |
| SURE on real stacks with correct sigma | #2 domain gap | Adds real noise gradient signal. Must evaluate post-SURE checkpoint. |
| Weight decay 1e-4 | #4 regularization | Standard practice. Prevents extreme weight growth. |
| Dropout 0.1 in enhancement path | #4 regularization | Forces distributed representations. |
| Data augmentation (flips, rotations, intensity jitter) | #1, #4 | Multiplies effective dataset size by 4-8x. |
| Early stopping at val_sup plateau | #5 memorization | Saves compute. Best model found earlier. |
| Post-SURE checkpoint selection via CNR/SNR | #6 evaluation | Evaluates SURE benefit on real images, not synthetic val. |

## Priority for Run22

1. Regularization (weight decay + dropout + augmentation) -- cheapest to implement, immediate effect
2. Correctly aligned tissue labels -- done (25 subjects, scaling to 50+)
3. Early stopping -- trivial implementation
4. More data -- scaling pipeline in progress (CanonicalData directory has 300+ candidates)
5. SURE with fixed checkpoint selection -- requires training to complete before evaluation
6. Post-SURE no-reference metric evaluation -- needs implementation

## Validation Gap: No Held-Out Set for SURE

Current split:
- train_v3: 254 HIGH subjects (supervised, synthetic pairs)
- val_v3: 31 HIGH subjects (held out, synthetic pairs) -- validates supervised performance
- test_synth: 32 HIGH subjects (held out)
- real LOW: 317 subjects (ALL used for SURE training)

**Problem:** All 317 LOW stacks go into SURE training. When we evaluate on real stacks using CNR/SNR, we are evaluating on the same data SURE trained on. Any improvement could be memorization of specific noise patterns, not generalization.

**Fix for Run22:** Split the 317 LOW stacks:
- 267 for SURE training
- 50 held out for real-image validation (val_real)

Two independent validation signals:
1. val_sup (31 synthetic subjects): does supervised enhancement still work?
2. val_real (50 LOW subjects, never-seen): does SURE improve real image quality?

Metric for val_real: CNR and noise sigma (no-reference, since no clean reference exists for these subjects).

## Related

- [[fetenh-net]] -- Main project doc
- [[fetenh-label-projection-pipeline]] -- Tissue label alignment (fixes cause #3)
- [[medical-image-registration]] -- Why registration is hard (background for cause #3)
