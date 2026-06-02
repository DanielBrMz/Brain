---
title: "FetEnhNet vs BME-X — Complete Architecture Comparison"
type: reference
updated: 2026-05-11
tags: [fetenh, bme-x, comparison]
---

# FetEnhNet vs BME-X: Complete Architecture Comparison

Side-by-side analysis of every architectural and training decision. Goal: identify what to adopt from BME-X, what to keep from FetEnhNet, and what to change for the mirror implementation.

---

## 1. HIGH-LEVEL DESIGN PHILOSOPHY

| Dimension | FetEnhNet | BME-X |
|-----------|-----------|-------|
| **Core idea** | Tissue-conditioned enhancement via FiLM modulation | Tissue-guided enhancement via concatenation |
| **Conditioning** | Spatially-varying FiLM (γ,β per pixel per layer) | Concatenation at input only (tissue + image → conv → recon) |
| **Architecture** | 2-stage: TissueClassifier (3-level UNet) + EnhancementNet (4-level ResUNet) | 2-stage: DU-Net (seg) + DU-Net (recon), connected by Conv+BN+ReLU concat |
| **Dimensionality** | 2D slices (2.5D: 3 adjacent slices as channels) | 3D patches (40×40×40 voxels) |
| **Target domain** | Fetal HASTE stacks (raw 2D slices) | Postnatal 3D volumetric T1w/T2w (full lifespan) |
| **Framework** | PyTorch (modern) | Caffe (training) → PyTorch (inference) |

**Key philosophical difference:** FetEnhNet conditions the enhancement at EVERY decoder level via FiLM (deep integration). BME-X conditions only at the input via concatenation (shallow integration). FiLM theoretically allows the network to modulate features differently for each tissue type at each resolution level. BME-X's concatenation gives the network all information upfront but lets it decide how to use it.

---

## 2. TISSUE CLASSIFICATION

| Feature | FetEnhNet | BME-X |
|---------|-----------|-------|
| **Architecture** | 3-level U-Net (shallow) | DU-Net with dense connections |
| **Input** | 1ch (center slice only, 2D) | 1ch (3D patch) |
| **Output** | 4ch softmax: bg, cortical_plate, wm_subplate, csf | 4ch: bg, WM, GM, CSF (Caffe: logits+ReLU; PyTorch: softmax) |
| **Tissue classes** | Fetal-specific: cortical plate + WM/subplate | Postnatal: standard GM + WM |
| **Label source** | NeSVoR inverse alignment → iBEAT atlas projection | iBEAT V2.0 direct segmentation |
| **Training signal** | Auxiliary DiceCE + gradient from enhancement loss | CE loss (weight 1.0), primary training objective |
| **Class weights** | [1.0, 8.0, 4.0, 5.0] (heavy cortical plate emphasis) | Equal weights (ignore_label=-1) |
| **Parameters** | ~0.5M (shallow 32→64→128) | Caffe: ~2.5M (32ch/8 growth); PyTorch: ~16M (64ch/16 growth) |
| **Dropout** | 0.1 | 0.1 |

**Critical difference in tissue classes:** FetEnhNet uses fetal-specific labels (cortical plate instead of GM) because fetal brains don't have the same cortical gray matter layering as postnatal brains. The cortical plate is the precursor to cortical GM. BME-X uses standard postnatal tissue classes that don't apply to fetal anatomy.

**Critical difference in training signal:** In BME-X, classification is the PRIMARY training objective (CE loss weight 1.0, MSE weight 10⁻⁷). The classifier must be good because everything depends on it. In FetEnhNet, classification is AUXILIARY (weight 0.1) — the enhancement loss drives most of the training. The classifier learns mainly through gradient backflow from enhancement, plus optional DiceCE when GT labels are available.

---

## 3. ENHANCEMENT NETWORK

| Feature | FetEnhNet | BME-X |
|---------|-----------|-------|
| **Architecture** | 4-level ResU-Net with FiLM at each decoder level | DU-Net with dense connections (identical to classifier) |
| **Input** | 3ch (2.5D: prev + center + next slices) + 4ch tissue map via FiLM | 64ch (32ch from tissue Conv+BN+ReLU + 32ch from image Conv+BN+ReLU) |
| **Output** | 2ch → dual-path residual (additive + multiplicative) | 1ch → direct intensity (Conv+BN+ReLU) |
| **Conditioning** | FiLM: per-pixel γ,β at every decoder level (deep) | Concatenation at input only (shallow) |
| **Residual design** | (input + additive) × exp(multiplicative) — handles both additive noise and multiplicative bias | Direct prediction (no explicit residual) |
| **Output activation** | `torch.clamp(result, 0, 1)` | BN + ReLU (Caffe and PyTorch) |
| **Skip connections** | Standard U-Net concatenation skips | Dense concatenation (DenseNet-style) |
| **Parameters** | ~8M (64→128→256→512) | Caffe: ~2.5M; PyTorch: ~16M |
| **Depth** | 4 encoder + 4 decoder levels | 3 encoder + 3 decoder levels + bottleneck |

**Dual-path residual (FetEnhNet) vs Direct prediction (BME-X):**

FetEnhNet's output head:
```python
additive = out[:, 0:1]
mult_log = out[:, 1:2]
multiplicative = exp(clamp(mult_log, -1, 1))
result = clamp((input + additive) * multiplicative, 0, 1)
```

This design explicitly handles two types of artifacts:
- **Additive** (noise, ringing) → corrected by the additive path
- **Multiplicative** (bias field) → corrected by the multiplicative path

BME-X has no such decomposition — it predicts the final intensity directly. This is why BME-X's bias field correction comes from preprocessing (N4), not the model.

**FiLM vs Concatenation:**

FiLM at decoder level k:
```python
tissue_resized = interpolate(tissue_map, size=decoder_k_size)
params = Conv1x1(tissue_resized)  # → (B, 2C, H, W)
gamma, beta = params.chunk(2)
output = gamma * features + beta  # per-pixel affine
```

BME-X concatenation:
```python
tissue_processed = Conv3x3(tissue_logits) + BN + ReLU  # 4ch → 32ch
image_processed = Conv3x3(input_image) + BN + ReLU     # 1ch → 32ch
combined = cat(tissue_processed, image_processed)       # 64ch
# → feeds into reconstruction DU-Net as input
```

FiLM is richer: it modulates at every resolution level, with per-pixel spatial variation. Concatenation is simpler: all tissue information is provided once at the input.

---

## 4. LOSS FUNCTIONS

| Loss | FetEnhNet | BME-X |
|------|-----------|-------|
| **Pixel loss** | L1 (MAE), weight 0.6 | MSE (Caffe EuclideanLoss), weight 10⁻⁷ |
| **Structural** | SSIM, weight 0.3 | None |
| **Frequency** | FFT magnitude L1, weight 0.1 | None |
| **Perceptual** | VGG (optional), weight 0.05 | None |
| **Classification** | DiceCE (auxiliary), weight 0.1 | CE (primary), weight 1.0 |
| **Self-supervised** | SURE (Stein's Unbiased Risk Estimator), weight 0.01→0.1 | None |
| **Focal** | Optional (γ=2), disabled by default | None |

**FetEnhNet has 6 loss components; BME-X has 2.**

The loss weight distribution tells the story:
- **FetEnhNet:** Enhancement-focused (L1+SSIM+Freq = 1.0 combined weight) with auxiliary classification (0.1)
- **BME-X:** Classification-focused (CE weight 1.0) with negligible enhancement (MSE weight 10⁻⁷ ≈ 0)

**SURE loss (unique to FetEnhNet):** Enables training on REAL corrupted data without ground truth. Uses Stein's Unbiased Risk Estimator to estimate the MSE from the noisy observation alone. Requires an accurate per-pixel noise estimate (σ map), which the Rician noise degradation provides.

---

## 5. DEGRADATION / DATA AUGMENTATION

| Feature | FetEnhNet | BME-X |
|---------|-----------|-------|
| **Types** | 8: rician noise, gaussian blur, bias field, gibbs ringing, kspace spike, signal dropout, motion ghost, downsample | 2: motion simulation (view2Dmotion) + phase-shift blurring (artefact simulator) |
| **Physics accuracy** | High: complex signal model for noise, hard k-space truncation for Gibbs, PE-line zeroing for dropout | Moderate: external motion simulator (realistic trajectory) + phase-shift blurring |
| **Spatial augmentation** | Rotation, horizontal flip, vertical flip | None |
| **Intensity augmentation** | Gamma correction [0.8, 1.2] | None |
| **Combination** | 1-3 types randomly applied per sample | Motion + blur combined |
| **Deterministic** | Seeded per (subject, slice, epoch, type) | Random per sample |
| **Noise map output** | Yes (per-pixel σ for SURE loss) | No |

**FetEnhNet's degradation is far more comprehensive.** 8 physically-modeled artifact types vs 2 external tools. FetEnhNet also provides a noise map for self-supervised training — something BME-X doesn't have.

**BME-X has no augmentation at all** — no flips, rotations, scaling, gamma. FetEnhNet has both spatial and intensity augmentation. This is a significant difference for generalization.

---

## 6. TRAINING CONFIGURATION

| Parameter | FetEnhNet | BME-X |
|-----------|-----------|-------|
| **Optimizer** | AdamW (weight_decay=1e-5) | SGD (momentum=0.9, weight_decay=5e-4) |
| **Learning rate** | 1e-4 | 5e-3 |
| **LR schedule** | CosineAnnealing (eta_min=1e-6) | Step decay ×0.1 per epoch |
| **Epochs** | 100 | 5 LR steps (5M iterations total) |
| **Batch size** | 24 (16 supervised + 8 SURE) | 3 (effective 9 with iter_size=3) |
| **Mixed precision** | AMP (autocast + GradScaler) | No (Caffe doesn't support) |
| **Gradient clipping** | max_norm=1.0 | No |
| **Multi-GPU** | torchrun DDP | No (single GPU Caffe) |
| **Weight init** | PyTorch default (Kaiming) | Xavier (Caffe) |
| **Patch/crop size** | 256×256 (2D) | 40×40×40 (3D) |
| **Resolution** | Native HASTE (1.0-1.25mm in-plane, 2-3mm through-plane) | 0.8mm isotropic (resampled) |
| **Warmup** | 5 epochs (SURE: 10 epochs) | None |
| **Validation** | Per-epoch with best-model checkpointing | Not visible in code |
| **Instrumentation** | ModelMonitor + TrainingLogger | None |

**FetEnhNet uses modern training practices** (AdamW, cosine LR, AMP, grad clipping, DDP, warmup, validation). BME-X uses 2015-era Caffe practices (SGD, step LR, single GPU, no validation visible).

---

## 7. DATA AND PREPROCESSING

| Feature | FetEnhNet | BME-X |
|---------|-----------|-------|
| **Training data** | 538 fetal subjects, 6 protocols, 179K slices (NeSVoR-aligned) | 516 participants (52 fetal + 464 postnatal 0-6y), BCP |
| **Data format** | Raw HASTE .nii stacks + projected per-slice labels | HDF5 patches pre-extracted at 0.8mm |
| **Tissue labels** | NeSVoR recon → atlas → inverse alignment → per-slice projection | iBEAT V2.0 on artefact-free images |
| **Preprocessing** | Percentile normalization [1%, 99%] → [0, 1], center-crop 256² | iBEAT (N4 + skull strip + cerebellum removal) on training GT |
| **Inference preprocessing** | None (raw slice in, enhanced slice out) | 14-step pipeline (N4×2, histogram match×2, skull strip, resample, reverse hist match, composite) |
| **Age handling** | Single model for all gestational ages | 8 separate age-specific models |
| **Self-supervised data** | 317 real LOW stacks (SURE loss, no GT needed) | None |
| **Test data** | 20K slices, per-degradation evaluation | 2,448 synthesized + 10,963 in vivo |

**FetEnhNet's inference is clean** — raw slice in, enhanced slice out. No preprocessing pipeline. BME-X requires a 14-step pipeline that does most of the artifact correction before the model even runs.

**FetEnhNet has self-supervised capability** via SURE loss on real data. BME-X is purely supervised.

---

## 8. INFERENCE

| Feature | FetEnhNet | BME-X |
|---------|-----------|-------|
| **Input** | (3, 256, 256) — 2.5D: 3 adjacent slices | (1, 40, 40, 40) — 3D patch |
| **Output** | (1, 256, 256) — enhanced center slice | (1, 40, 40, 40) — enhanced + (4, 40, 40, 40) tissue labels |
| **Sliding window** | No — per-slice, full resolution | Yes — stride 18, margin 5 (center 30³ kept), overlap averaged |
| **Preprocessing** | Percentile normalize to [0,1] | N4, histogram match, skull strip, resample (14 steps) |
| **Postprocessing** | Denormalize | Reverse histogram match, skull compositing |
| **Speed** | ~50ms per slice (GPU) | ~3-5 min per 3D volume (GPU, with preprocessing) |
| **Memory** | ~1GB for 256² slice | ~10GB for 40³ sliding window on resampled volume |

---

## 9. WHAT FETENHNET SHOULD ADOPT FROM BME-X

1. **3D context** — BME-X's 3D patches give inter-slice context that FetEnhNet's 2.5D (3 slices) can't match. For NeSVoR reconstructions (isotropic 3D volumes), 3D processing is the natural choice.

2. **Preprocessing pipeline** — FetEnhNet currently has no inference preprocessing. Adding N4 bias correction and intensity standardization before the model would make inputs more consistent and reduce the burden on the model.

3. **Separate age-specific models** — FetEnhNet uses one model for all gestational ages. Fetal brain appearance changes dramatically from 21 to 36 weeks. BME-X's approach of age-specific models avoids learning contradictory tissue contrasts.

4. **Massive validation scope** — BME-X validates on 19 datasets, 10K+ images. FetEnhNet's validation is currently limited to its own test set.

5. **Downstream task evaluation** — BME-X shows improvements in segmentation, registration, parcellation, diagnosis. FetEnhNet currently only reports PSNR/SSIM.

## 10. WHAT FETENHNET SHOULD KEEP OVER BME-X

1. **FiLM conditioning** — deeper tissue integration than concatenation. FiLM at every decoder level is architecturally superior.

2. **Dual-path residual** — explicit additive + multiplicative correction handles more artifact types than direct prediction.

3. **Comprehensive degradation engine** — 8 physics-based artifact types vs 2. This gives much better robustness.

4. **SURE self-supervised loss** — enables training on real corrupted data. BME-X has no self-supervised capability.

5. **Modern training stack** — AdamW, cosine LR, AMP, DDP, gradient clipping, validation, model monitoring.

6. **Multi-loss training** — L1 + SSIM + Frequency + SURE + Tissue CE is a richer training signal than CE + negligible MSE.

7. **Fetal-specific tissue classes** — cortical plate + WM/subplate is correct for fetal anatomy. BME-X's GM/WM doesn't apply to fetuses.

8. **Clean inference** — no 14-step preprocessing pipeline needed.

## 11. WHAT TO CHANGE FOR THE MIRROR IMPLEMENTATION

1. **Extend to 3D** where data supports it (NeSVoR reconstructions) while keeping 2D capability for raw HASTE stacks
2. **Add optional N4 + intensity standardization** as preprocessing (can be toggled on/off)
3. **Consider age-stratified models** for different gestational age ranges (21-28w vs 28-36w)
4. **Add histogram matching** as optional preprocessing for cross-scanner consistency
5. **Increase classification loss weight** — BME-X's insight that classification quality drives everything is valid. FetEnhNet's 0.1 weight may be too low.
6. **Add sliding window inference** for 3D volumes with overlap averaging
7. **Keep FiLM, dual-path residual, comprehensive degradation, SURE, modern training**
