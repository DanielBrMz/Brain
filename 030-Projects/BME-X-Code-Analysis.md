---
title: "BME-X Code Analysis & Gap Assessment"
type: reference
updated: 2026-05-06
tags: [fetenh, bch, bmex, architecture]
---

# BME-X Code Analysis

> Complete analysis of https://github.com/DBC-Lab/Brain_MRI_Enhancement
> Sun et al., Nature Biomedical Engineering, Vol 9, Apr 2025, pp 521-538

## Architecture: DUNet3D_seg_recon_softmax.py (740 lines)

Single class containing TWO identical U-Nets in one forward pass:

### Stage A: Segmentation Network (~32 conv layers)

```
Input: (B, 1, 32, 32, 32) single-channel 3D patch

Encoder Level 1 (32^3):
  Conv3d(1->64) + BN + ReLU
  Conv3d(64->64) + BN + ReLU
  Dense block: 3 layers, Conv3d(->16) + Dropout(0.1), concatenated (64->80->96->112)
  Transition: Conv3d(112->64) + BN + ReLU + MaxPool3d(stride=2)

Encoder Level 2 (16^3):
  Conv3d(64->64) + BN + ReLU
  Dense block: 3 layers x Conv3d(->32) + Dropout, concat (64->96->128->160)
  Transition: Conv3d(160->128) + BN + ReLU + MaxPool3d(stride=2)

Bottleneck (8^3):
  Conv3d(128->128) + BN + ReLU + MaxPool(stride=2) -> 4^3
  ConvTranspose3d(128->128, stride=2) back to 8^3
  Cat with level 2 skip -> 256ch

Decoder Level 1 (8^3 -> 16^3):
  Conv(256->256) + Dense block (3x32: 256->288->320->352)
  ConvTranspose(352->128, stride=2)
  Cat with level 1 skip -> 256ch

Decoder Level 2 (16^3 -> 32^3):
  Conv(256->256) + dense blocks (two: 3x32 each)
  ConvTranspose(352->64, stride=2)
  Cat with input skip -> 128ch

Output head:
  Conv(128->128) + dense (3x16: 128->144->160->176)
  Conv(176->64) + dense (3x16: 64->80->96->112)
  Conv(112->4) + BN + ReLU -> Softmax -> 4 tissue classes
```

### Connection Layer (3 lines of code)

```python
tissue_probs = Softmax(seg_output)            # (B, 4, 32, 32, 32)
tissue_features = Conv3d(4->32) + BN + ReLU   # tissue branch
image_features = Conv3d(1->32) + BN + ReLU    # image branch
concatenated = cat([tissue_features, image_features], dim=1)  # -> 64 channels
```

No FiLM, no attention, no gating. Just Conv+BN+ReLU on each, then concat.

### Stage B: Enhancement Network (identical architecture)

Same encoder-bottleneck-decoder as Stage A, but:
- Input: 64 channels (concatenated tissue + image)
- Output: 1 channel (enhanced image)

### DenseBlock implementation

```python
# First iteration: Conv3d(in->hidden, 1x1x1) -> BN -> ReLU -> Conv3d(hidden->out, 3x3x3) -> BN -> ReLU
# Repeating: Conv3d(out->hidden, 3x1x1) -> BN -> ReLU -> Conv3d(hidden->out, 3x3x3) -> BN -> ReLU
# Output is concatenated (not added) with input at each step
```

Growth rate: 16 (level 1) or 32 (level 2+). Hidden channels: 128.

## Training (trainer.py)

### Loss

```python
# DEFINED:
mse = nn.MSELoss()                           # Enhancement loss
loss_func = nn.CrossEntropyLoss(reduction='none')  # Segmentation loss

# ACTUALLY USED (line 187-188):
loss_matrix = loss_func(logits, in_label.squeeze().long())
loss = torch.mean(torch.mul(loss_matrix, in_weight))  # Weighted CE only

# CRITICAL: MSE loss is defined but NEVER CALLED in the training loop.
# Paper says L = L1 + lambda*L2 (CE + 1e-7*MSE), but code only does CE.
# The reconstruction branch gets gradients only through the shared backbone,
# NOT through a dedicated reconstruction loss.
```

### Training specifics

- Batch: 3 samples x 3 iterations x 100 sub-batches per loader step
- Patch size: 64^3 (hardcoded in loop, NOT the 32 from options)
- Normalization: data = data / 10000.0
- Optimizer: SGD, momentum=0.9, lr=0.005
- Scheduler: StepLR(step_size=1, gamma=0.1) -- lr drops 10x every epoch
- Checkpoint: every 1000 steps + every epoch
- Validation: COMMENTED OUT in released code
- No augmentation in training loop

### Inference (BME_X_enhanced.py)

1. Load NIfTI, histogram match to age-matched template
2. Find brain boundary with margins
3. Extract overlapping 40x40x40 patches, stride 18
4. Forward pass each patch -> seg + enhanced
5. Average overlapping predictions
6. Reassemble, reintroduce skull: `brain_mask * enhanced + (1-brain_mask) * original`

## Dependencies

```
torch==1.13.1, monai==0.7.0, SimpleITK==2.4.0, tensorboardX
numpy, scipy, einops, nipype, pybids
```

---

# Gap Analysis: BME-X vs Our FetEnhNet

## What BME-X does that we replicate

| BME-X Feature | Our Implementation | Status |
|---|---|---|
| DU-Net (dense U-Net) | ResU-Net (residual blocks) | Different backbone |
| 4 tissue classes (BG, CSF, GM, WM) | 4 classes (BG, CP, WM/SP, CSF) | Done, fetal-specific |
| Tissue concatenation at input | `use_film=false` mode | Implemented |
| Cross-entropy seg loss | DiceCE loss | Improved (Dice + CE) |
| MSE enhancement loss | MSE + L1/SSIM/freq/perceptual/SURE variants | Extended |
| 3D patch-based (40x40x40) | 2D slice-based (256x256) | Design choice |
| Caffe original, PyTorch port | PyTorch native | Modern |
| Histogram matching preprocess | Not used (direct raw HASTE) | Different |
| Skull stripping required | Full-FOV, no skull strip needed | Advantage |

## What BME-X does that we DON'T

| BME-X Feature | Gap | Priority |
|---|---|---|
| Joint end-to-end training (both stages) | We train staged (freeze stage 1) | Medium - could try joint |
| Spatial importance weighting (in_weight) | Not implemented | Low |
| 3D dense concatenation (DenseNet) | We use residual blocks (ResNet) | Architecture choice |
| Age-stratified models (fetal, 0-24mo, adult) | Single model for fetal only | N/A for our scope |
| Histogram matching to template | Not needed for raw HASTE | N/A |
| Overlapping 3D patch inference | 2D slice inference | Design choice |
| Motion simulation (k-space phase shifts) | Dropped per Hyeokjin | Intentional |

## What we do that BME-X DOESN'T

| Our Feature | BME-X Equivalent | Advantage |
|---|---|---|
| FiLM conditioning (per-pixel gamma/beta at every decoder level) | Simple concatenation at input | More expressive |
| SURE self-supervised loss (train on real LOW without GT) | None | Domain adaptation |
| Frequency loss (FFT magnitude L1) | None | Anti-blur |
| VGG perceptual loss | None | High-level features |
| Legendre polynomial bias field | Raw polynomial | More realistic |
| Data augmentation (nnU-Net v2 consensus) | No augmentation | Robustness |
| QA-based quality tiers | None | Targeted training |
| FetEnhNet Explorer (interactive web tool) | None | Data management |
| Residual learning (clamp not sigmoid) | No explicit residual | Better PSNR |
| 2D full-FOV (no skull strip) | 3D patch (requires skull strip) | Practical |

## Critical discrepancy: Released code vs paper

The paper claims `L = L1 + lambda*L2` with lambda=1e-7, where L1 is cross-entropy and L2 is MSE. But in the released `trainer.py`:
- MSE is defined (`mse = nn.MSELoss()`) but **never called** in the training loop
- Only weighted cross-entropy loss drives backpropagation
- The reconstruction branch learns only through gradients from the segmentation loss propagating back through the shared encoder, NOT through a dedicated reconstruction loss
- Validation is completely commented out

This means the enhancement network is NOT directly supervised with MSE in the released code. It learns to produce enhanced outputs solely through the classification gradient signal flowing through the concatenation layer. This is a significant finding.

## Data gap

| Dimension | BME-X | FetEnhNet |
|---|---|---|
| Subjects | 52 fetal + 464 pediatric | 538 fetal only |
| Age range | Fetal to 6 years | 19-34 weeks GA |
| Patches/image | 2,000 (40x40x40) | All brain slices (256x256) |
| Total training samples | ~1M patches | 179,601 slices |
| Tissue labels | iBEAT V2.0 (auto) | iBEAT V2.0 (auto, inverse-projected) |
| Degradation | Motion sim + k-space + blur | Noise + blur + bias + downsample |
| Template matching | Yes (per age group) | No |
| QA scoring | Not mentioned | Per-stack, integrated |
| Protocols | BCP (single site) | 8 protocols, multi-site |
