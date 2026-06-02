---
title: "FetEnhNet — BME-X Replication Plan"
type: reference
created: 2026-04-28
tags: [fetenh, bch, bmex, training-plan]
---

# BME-X Replication Plan

> Reference: Sun et al., "A foundation model for enhancing magnetic resonance images and downstream segmentation, registration and diagnostic tasks", Nature BME 9, 521-538 (April 2025). DOI: 10.1038/s41551-024-01283-7

## BME-X Architecture

**Two-stage pipeline:**
1. **Classification model** — DU-Net (DenseNet encoder-decoder), predicts tissue class probabilities (background, CSF, GM, WM). Loss: cross-entropy (L1). Labels from iBEAT V2.0.
2. **Enhancement model** — DU-Net, takes **concatenation** of [low-quality image + classification output] as input. Loss: **MSE (L2)**. Outputs the high-quality image directly (not residual).

**Total loss:** `L = L1_ce + lambda * L2_mse` where lambda = 1e-7, jointly trained.
**Optimizer:** SGD, LR=0.005, decayed by 0.1 per epoch, 5 epochs total.
**Init:** Xavier.
**Framework:** Caffe 1.0.0-rc3 (we use PyTorch).
**Patch size:** 40x40x40 voxels, 2000 patches per training image.
**Split:** 95% train / 5% val.

### Key differences from FetEnhNet (current)

| Aspect | BME-X | FetEnhNet (current) |
|--------|-------|---------------------|
| Conditioning | Concatenation (classifier output + input) | FiLM (feature-wise linear modulation) |
| Enhancement loss | MSE (L2) only | L1 + SSIM + Frequency |
| Backbone | DU-Net (DenseNet-based) | ResU-Net |
| Training | Joint (classifier + enhancer) | Sequential (freeze classifier, then enhancer) |
| Self-supervised | None | SURE loss on real LOW stacks |
| Input | 2D patches (40x40x40 at 0.8mm) | 2.5D (3 adjacent slices) |
| Tissue labels | iBEAT V2.0 automated | Manual segmentations (inverse-aligned atlas) |

**NOTE:** We keep our manual segmentations (inverse-aligned atlas labels) instead of iBEAT automated labels. This is a deliberate improvement over BME-X.

## BME-X Degradation Types (exact parameters)

### 1. Motion artefacts
- Tool: MRI-Motion-Artifact-Simulation-Tool (view2Dmotion)
- Simulated rotation, periodic/continuous/sudden motion
- BCP params: TR=2400ms, TE=2.2ms, phase-encoding=anterior-posterior, res 0.8x0.8x0.8mm3
- Random motion amplitude = [0.01, 2.5], frequency hz = [0, 0.0075] x TR
- 3 severity levels:
  - Minor: amp=1, hz=0.12 x TR
  - Moderate: amp=2, hz=0.18 x TR
  - Severe: amp=3, hz=0.42 x TR
- Then further blurred via artefact simulator (Fourier + random phase shift per k-space readout)
- For non-BCP testing: severe periodic motion (amp=3, hz=0.42 x TR)

### 2. Downsampling (super-resolution)
- From 0.8mm3 isotropic to lower resolutions
- Through-plane thickening: 1.6, 2.4, 3.2, 4.0, 4.8 x 0.8 x 0.8 mm3

### 3. Gaussian noise
- Standard deviation sigma = {0.01, 0.03, 0.05, 0.08}

### 4. Rician noise
- Percentage of signal: {5%, 9%, 13%, 17%}

### 5. Gaussian smoothing (contrast/blur)
- Sigma = {0.6, 0.8, 1.0, 1.2}

### Robustness evaluation (Supp Fig 2)
- Motion: 3 levels (minor/moderate/severe) x 3 resolutions = 9 conditions per image
- Downsampling: 4 levels (2.4, 3.2, 4.0, 4.8 mm through-plane)
- Gaussian noise: 4 levels (sigma 0.01, 0.03, 0.05, 0.08)
- Rician noise: 4 levels (5%, 9%, 13%, 17%)
- Gaussian smooth: 4 levels (sigma 0.6, 0.8, 1.0, 1.2)

## Training Strategy (age-specific)
- BME-X trains separate models per age group: 0, 3, 6, 9, 12, 18, 24+ months
- For participants aged 24+ months to 100 years, same 24+ model used
- Rationale: brain images within each age group are representative and relatively consistent

## Hyeokjin's Clarification (Apr 28 email)

**BME-X motion/k-space degradations do NOT apply to fetal HASTE raw stacks.**
BME-X motion simulation (phase-encode ghosting, k-space corruption) targets reconstructed postnatal T1w volumes. Fetal HASTE artifacts are inter-slice motion, not intra-slice k-space corruption. Do not include these.

**Degradation types for FetEnhNet (confirmed):**
1. Noise (Gaussian + Rician) -- already have
2. Smoothing/blur -- already have
3. Bias field (intensity inhomogeneity) -- discuss with Victoria & Suzette, simulate from real LOW data
4. Down-sampling (optional) -- simulate "small brain" (few voxels), e.g. 1x1 -> 1.5x1.5

## New Training Campaign Plan

### Phase 0: Preparation
- [ ] Brain crop + padding to fixed canvas
- [ ] Rewrite degradation engine: noise, smoothing, bias field, (optional) down-sampling -- NO motion/k-space
- [ ] Discuss bias field with Victoria & Suzette, review real LOW data with intensity inhomogeneity
- [ ] Add tissue classifier visualization to all eval outputs

### Phase 1: Individual Loss Baselines
All with same degradation types (noise + smoothing + bias field), same architecture:
- [ ] Run A: MSE only
- [ ] Run B: L1 only
- [ ] Run C: L1 + SSIM (0.7/0.3)
- [ ] Run D: L1 + SSIM + Frequency
- [ ] Run E: L1 + SSIM + Perceptual (VGG)
- [ ] Run F: SURE only (self-supervised)

### Phase 2: Analysis
- Compare all baselines on matched eval set
- Understand each loss's effect on the model
- Choose combinations informed by individual results

## Evaluation Metrics (matching BME-X)
- MSE
- PSNR
- SSIM
- MS-SSIM
- UQI
- VIF
- TCT (tissue contrast, for in vivo: |mu_wm - mu_gm| / sqrt(sigma_wm^2 + sigma_gm^2))

## Code/Data References
- BME-X source: https://github.com/DBC-Lab/Brain_MRI_Enhancement.git
- Motion sim tool: https://github.com/Yonsei-MILab/MRI-Motion-Artifact-Simulation-Tool
- Artefact simulator: https://ieeexplore.ieee.org/abstract/document/8759167
- iBEAT V2.0: http://www.ibeat.cloud
