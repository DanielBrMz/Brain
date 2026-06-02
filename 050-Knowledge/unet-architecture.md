---
title: "U-Net Architecture"
type: knowledge
updated: 2026-05-14
tags: [architecture, segmentation, deep-learning, medical-imaging]
---

# U-Net Architecture

## Core Idea

Encoder-decoder with skip connections for dense prediction. The encoder captures *what* is in the image (semantic features), the decoder recovers *where* (spatial precision). Skip connections bridge the two.

```
Input -> [Enc1] -> [Enc2] -> [Enc3] -> [Enc4] -> [Bottleneck]
            |         |         |         |
            v         v         v         v        (skip connections)
         [Dec4] <- [Dec3] <- [Dec2] <- [Dec1] -> Output
```

## Encoder (Contracting Path)

Each level: Conv -> BN -> ReLU -> Conv -> BN -> ReLU -> MaxPool(2)
- Spatial dims halved, channels doubled at each level
- Captures increasingly abstract features
- Receptive field grows exponentially with depth

## Decoder (Expanding Path)

Each level: Upsample(2) -> Concat(skip) -> Conv -> BN -> ReLU -> Conv -> BN -> ReLU
- Spatial dims doubled, channels halved
- Skip connections concatenate encoder feature maps → precise localization

## Skip Connections: Why They Matter

Without them, upsampled features lack spatial precision (blurry boundaries). Skips provide:
- High-resolution spatial info (edges, boundaries) from encoder
- Combined with deep semantic features from decoder
- Essential for precise segmentation — the entire reason U-Net works for medical imaging

## Key Variants

### Dense U-Net (BME-X / CaffeDenseUNet2d)
- Dense connections within each encoder/decoder block (like DenseNet)
- 32ch init, growth rates 8 (enc) / 16 (dec), 3 stages
- 2.5M params per network (seg + recon = ~5.5M total)
- Transition layers between stages: BN -> ReLU -> 1x1 Conv -> Pool
- Trained at 192x192 crop size on 2D HASTE slices
- **Dual-head**: segmentation (4ch softmax) + reconstruction (1ch)
- Connection: softmax(seg) -> Conv+BN+ReLU + image -> Conv+BN+ReLU -> concat(64ch) -> recon decoder
- The seg head guides recon by providing tissue-awareness

### FiLM-Conditioned U-Net (FetEnhNet)
- Feature-wise Linear Modulation: gamma*features + beta at each decoder level
- Conditioning signal: tissue class probabilities from a separate classifier
- Allows the enhancer to apply different processing per tissue type
- ResBlocks instead of plain conv blocks
- channels (32, 64, 128, 256), 2D per-slice

### 3D U-Net (MONAI / Hydro)
- spatial_dims=3, processes volumetric patches
- 128^3 patches with sliding window inference
- Critical for 3D structures (ventricles) — 2D misses shape prior
- Result: 3D Dice 0.919 vs 2D Dice 0.166

### V-Net
- 3D variant with residual connections and Dice loss
- PReLU instead of ReLU, strided convolutions instead of max pool

### Attention U-Net
- Attention gates on skip connections — learns to suppress irrelevant features
- Useful when target is small relative to FOV (e.g., lesions)

## Training Considerations for Medical Imaging

### Loss Functions
- **CE** for segmentation (with class weights for imbalanced tissue types)
- **Dice loss** for overlap optimization (handles class imbalance better than CE alone)
- **MSE / L1** for reconstruction / enhancement
- **SURE** for self-supervised denoising (no clean reference needed)
- Joint loss: L = CE(seg) + lambda * MSE(recon) — the lambda balance is critical

### Data Augmentation
- Spatial: rotation, flip, shift, scale
- Intensity: gamma, brightness, contrast
- **Synthetic degradation**: the key to training enhancement models — apply noise, blur, bias field, motion artifacts to clean images, train model to undo them
- Must match real artifact physics (Rician noise, not Gaussian; per-slice motion, not volumetric)

### Practical Lessons (from BME-X mirror training)
- **NFS memmap + shuffled DataLoader = disaster** — always RAM-load
- **DDP may SIGSEGV on some GPU setups** — test single-GPU first
- **lambda_recon too small (1e-7) = model ignores reconstruction** — use 0.01-0.1
- **AMP halves VRAM** — enables batch=32 on 24GB GPUs
- **CosineAnnealingLR >> StepLR** for slow epochs (StepLR kills LR too fast)

## Used In
- [[BME-X-Deep-Analysis]] — CaffeDenseUNet2d architecture
- [[fetenh-net]] — FiLM-conditioned 2D U-Net for enhancement
- [[bch-victoria-hydro]] — 3D/2D UNet for hydrocephalus segmentation

## References
- Ronneberger et al. "U-Net: Convolutional Networks for Biomedical Image Segmentation", MICCAI 2015
- Huang et al. "Densely Connected Convolutional Networks" (DenseNet), CVPR 2017
- Perez et al. "FiLM: Visual Reasoning with a General Conditioning Layer", AAAI 2018
- Milletari et al. "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation", 3DV 2016
