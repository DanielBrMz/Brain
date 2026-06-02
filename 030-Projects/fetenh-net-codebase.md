---
title: "FetEnhNet — Codebase Documentation"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, research, bch, fetal-mri, codebase, deep-learning, pytorch, grant-lab]
---

# FetEnhNet — Codebase Documentation

> Detailed code documentation for the FetEnhNet model. For project overview, training history, and status see [[fetenh-net|FetEnhNet — Main]].

---

## Model Architecture (src/model/)

### config.py — `FetEnhNetConfig`

Dataclass configuration for the full model:

```
FetEnhNetConfig
├── tissue: TissueClassifierConfig
│   ├── tissue_classes: ["background", "cortical_plate", "wm_subplate", "csf_other"]
│   ├── in_channels: 1 (grayscale HASTE)
│   ├── base_filters: 32
│   ├── depth: 3
│   └── dropout: 0.1
├── enhance: EnhancementNetConfig
│   ├── in_channels: 1
│   ├── out_channels: 1
│   ├── base_filters: 64
│   ├── depth: 4
│   ├── use_film: True
│   └── dropout: 0.1
├── lr: 1e-4, weight_decay: 1e-5
├── lambda_l1: 0.7, lambda_ssim: 0.3, lambda_freq: 0.0
├── lambda_sure: 0.1, sure_sigma: 0.15
├── lambda_tissue: 0.5, focal_gamma: 0.0
├── warmup_epochs: 5, total_epochs: 100, batch_size: 16
```

**iBEAT label mapping:** {0→0, 1→1 (CP), 42→1 (CP), 160→2 (WM), 161→2 (WM), 18→3 (CSF)}

---

### tissue_classifier.py — `TissueClassifier` (Stage 1)

3-level shallow U-Net producing soft tissue probability maps.

**Architecture:**
- Encoder: 3× `EncoderBlock(Conv→BN→ReLU → Conv→BN→ReLU → Dropout → MaxPool)`
- Channel progression: 1 → 32 → 64 → 128
- Bottleneck: 128 → 256 → 256
- Decoder: 3× `DecoderBlock(ConvTranspose → Concat(skip) → Conv → Conv)`
- Head: `Conv2d(32→4, k=1)` → `softmax(dim=1)`

**Input:** `(B, 1, H, W)` normalized HASTE slice
**Output:** `(B, 4, H, W)` soft tissue probabilities

**Training signal:** No independent loss — trained via gradient from enhancement loss through FiLM layers. When `lambda_tissue > 0`, also receives direct CE supervision from projected iBEAT labels.

---

### enhancement_net.py — `EnhancementNet` (Stage 2)

4-level ResU-Net with spatially-varying FiLM conditioning at every decoder level.

**Architecture:**
- Encoder: 4× `EnhEncoderBlock(Conv→BN→ReLU → ResBlock → Dropout → MaxPool)`
- Channel progression: 1 → 64 → 128 → 256 → 512
- Bottleneck: 512 → 1024 (2× ResBlocks)
- Decoder: 4× `FiLMDecoderBlock(ConvTranspose → Concat(skip) → Conv → ResBlock → FiLM → ReLU)`
- Head: `Conv2d(64→32, k=3) → ReLU → Conv2d(32→1, k=1)`

**FiLM Mechanism (`FiLMLayer`):**
1. Tissue map `(B, 4, H_full, W_full)` bilinearly resized to decoder feature map dimensions `(H_k, W_k)`
2. `Conv2d(4→2C, k=1)` projects tissue channels to `γ` and `β` (each `(B, C, H_k, W_k)`)
3. Applied element-wise: `h_conditioned[b,c,h,w] = γ[b,c,h,w] * h[b,c,h,w] + β[b,c,h,w]`
4. Every spatial location gets its own scale+shift based on local tissue composition

**Output:** `torch.clamp(img + residual, 0, 1)` — residual learning with clamp (NOT sigmoid, to preserve identity when residual ≈ 0).

---

### fetenh_net.py — `FetEnhNet` (Full Model)

```python
class FetEnhNet(nn.Module):
    def forward(self, x_deg):
        tissue_map = self.classifier(x_deg)           # (B, 4, H, W)
        x_enh      = self.enhancer(x_deg, tissue_map) # (B, 1, H, W)
        return x_enh, tissue_map

    def enhance_only(self, x_deg):  # Inference shortcut
        with torch.no_grad():
            x_enh, _ = self.forward(x_deg)
        return x_enh
```

---

## Training (src/training/)

### dataset.py

Two dataset classes:

**`PairedSliceDataset`** (supervised):
- CSV columns: `clean_path`, `degraded_path`, `n_slices`, `degradation_type`, `tissue_label_path`
- Slice sampling: random from central 20-80% z-range
- Brain-preferential sampling: 85% chance of picking a slice with brain tissue (>100 labeled pixels)
- **Critical normalization:** Both clean and degraded normalized using DEGRADED image's [p1, p99] percentiles (same scale at inference)
- Spatial: center-crop/pad to 256×256 (no interpolation)
- Augmentation: random horizontal + vertical flip (applied consistently to image + label)
- Returns: `{clean, degraded, tissue_label, subject_id, cohort}`

**`UnpairedLowDataset`** (self-supervised SURE):
- CSV columns: `stack_path`, `n_slices`, `subject_id`
- 3 slices sampled per stack per epoch
- Returns: `{noisy, subject_id}`

### losses.py — `FetEnhNetLoss`

5 loss components combined:

| Loss | Class | Purpose |
|------|-------|---------|
| L1 | `L1Loss` | Pixel-wise MAE |
| SSIM | `SSIMLoss` | Structural similarity (11×11 Gaussian window) |
| Frequency | `FrequencyLoss` | FFT-magnitude L1 for sharpness |
| SURE | `SURELoss` | Stein's Unbiased Risk Estimator (self-supervised, no GT) |
| Tissue CE | `TissueCELoss` | Weighted CE or Focal on tissue classifier |

**SURE implementation:**
```
SURE(f) = ||f(y)||² - 2σ²·div(f)(y)
div(f) ≈ (1/ε)·b^T·(f(y+εb) - f(y))  where b ~ N(0,I)
```
σ=0.15 (Rician noise estimate), ε=1e-2 perturbation magnitude.

**Tissue class weights:** `[1.0, 25.0, 9.0, 10.0]` (sqrt median-frequency balancing, CP boosted to 25 for imbalance)

**Combined loss:**
```
L_sup    = λ_l1 * L1 + λ_ssim * (1-SSIM) + λ_freq * FreqLoss
L_tissue = λ_tissue * CE(tissue_map, tissue_label)  [only for labeled subjects]
L_self   = λ_sure * SURE(f, y_noisy)                [only for real LOW stacks]
Total    = L_sup + L_tissue + L_self
```

### trainer.py

Standard PyTorch training loop with:
- AdamW optimizer
- Warmup phase (supervised only for first N epochs)
- Mixed precision (AMP)
- Checkpoint saving (best validation + periodic)
- History tracking (per-epoch losses)

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/train.py` | Training CLI — takes config YAML, runs trainer |
| `scripts/evaluate.py` | Evaluate checkpoint on test_synthetic.csv (198 pairs), reports PSNR/SSIM per degradation |
| `scripts/compare_runs.py` | Compare multiple checkpoints — bar charts + visual panels |
| `scripts/visualize.py` | Generate enhancement visualization panels |
| `scripts/visualize_real.py` | Visualize on real LOW stacks (no GT) |
| `scripts/project_labels.py` | Project 3D iBEAT labels to 2D stack space (NN interpolation via affine chain) |
| `scripts/make_tissue_label_figures.py` | Generate tissue label figures for Hyeokjin |

---

## Evaluation Metrics

Custom implementations (no external dependency):
- **PSNR:** `10 * log10(1 / MSE)`
- **SSIM:** Wang et al. 2004, separable Gaussian convolution, C1=0.01², C2=0.03²

---

## Tests

14 tests (all passing). Located in `tests/`. Run with:
```bash
python -m pytest tests/ -v
```

---

## Related Notes

- [[fetenh-net|FetEnhNet — Project Overview]] — training history, results, status
- [[bch-seg-pipeline|Segmentation Pipeline]] — produces data for this model
- [[bch-surface-pipeline|Surface Pipeline]] — uses tissue labels
- [[neuronscope|NeuronScope]] — visualization of model activations
