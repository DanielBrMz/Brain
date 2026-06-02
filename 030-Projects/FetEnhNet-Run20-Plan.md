---
title: FetEnhNet — Run20+ Expansion Plan
type: project-plan
created: 2026-04-03
tags: [bch, research, deep-learning, fetal-mri, enhancement, planning]
---

# FetEnhNet Run20+ — Full Expansion Plan

Goal: build the most robust fetal raw stack enhancement model possible by (1) massively expanding synthetic training data, (2) correctly implementing SURE loss with noise maps, and (3) conditioning on brain masks for precise spatial awareness.

---

## What We Have (Baseline: Run18/19)

| Component | Current State |
|-----------|--------------|
| Model | TissueClassifier (U-Net 3-lvl) + EnhancementNet (ResU-Net 4-lvl) with brain mask FiLM |
| Best val_sup | 0.0541 (Run18, brain mask), 0.0538 (Run19, tissue 4-class) |
| Training pairs | ~1,476 pairs, 6 degradation types, 246 subjects |
| Unpaired real subjects | 317 LOW quality subjects (SURE disabled currently) |
| Coverage | 83.5% tissue labels, ~70% brain masks |
| Weak point | slice_corrupt: -58 dB (not a learned degradation — structural corruption); bias field underperforms |

---

## Phase 1 — Massive Synthetic Dataset Expansion

### 1.1 Principle
Apply every usable degradation parameter value to every brain-containing raw slice. This replaces the current coarse "6 degradation type per subject" scheme with a dense parameter grid per slice.

### 1.2 Source Slices
- For each subject with a brain mask, enumerate only z-slices where `mask[:,:,z].sum() > 0`
- This gives approximately **400,000–600,000 unique brain-containing slices** across all protocols
- Use the already-computed `projected_labels/` (from NeSVoR simslices) as tissue conditioning labels
- Use existing `masks/<stem>_mask.nii` as brain mask conditioning

### 1.3 Degradation Parameter Grid

**Gaussian Noise** (additive, σ in normalized [0,1] image space):
- σ ∈ {0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.30}
- 10 levels × all slices

**Rician Noise** (MRI-realistic, same σ values):
- σ ∈ {0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.30}
- 10 levels × all slices

**Gaussian Blur** (σ in pixels):
- σ ∈ {0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5}
- 10 levels × all slices

**Bias Field** (smooth multiplicative field):
- Polynomial order ∈ {1, 2, 3} × intensity scale ∈ {0.2, 0.4, 0.6} = 9 combinations
- Use SimpleITK N4-style bias simulation (random polynomial coefficients per slice)

**Combined: Blur + Rician Noise** (most realistic fetal HASTE degradation):
- blur_σ ∈ {0.8, 1.2, 1.8, 2.5} × noise_σ ∈ {0.05, 0.10, 0.15, 0.20} = 16 combinations
- Most practically important combination for real low-quality subjects

**Combined: Bias + Rician Noise**:
- bias_scale ∈ {0.2, 0.4} × noise_σ ∈ {0.05, 0.10, 0.15} = 6 combinations

**Total degradation classes:** ~61 parameter settings per slice

### 1.4 Storage Strategy
Do NOT store all 61 × 500K = 30M NIfTI files on disk. Instead:
- Store **only clean slices** as NIfTI (already exists, ~500K brain slices)
- Store a **manifest CSV** with columns: `clean_path, z, subject, protocol, degradation_type, degradation_params, brain_mask_path, tissue_label_path, noise_variance`
- Apply degradations **on-the-fly in the DataLoader** using a deterministic seed (reproducible)
- This keeps dataset portable and allows parameter tuning without regenerating data

### 1.5 Noise Variance Column (Critical for SURE)
For every synthetic degraded sample, store `noise_variance = σ²` (Gaussian/Rician σ²) directly in the manifest. This is the exact noise level the SURE loss needs. For bias + blur, set `noise_variance = 0` (SURE only applies to noise degradation).

### 1.6 Segmentation for Degraded Images
**Do NOT rerun iBeat on degraded images.** The tissue labels come from the NeSVoR reconstruction of the clean high-quality stacks. Since degradation is applied to the raw slice pixel values only (not the geometry), the spatial correspondence between the clean slice and the degraded slice is identical. Use the **same `projected_labels/i.nii.gz`** for both clean and degraded versions of slice `i`.

### 1.7 Brain Mask for Degraded Images
Identical reasoning — the brain mask geometry is unchanged by intensity degradation. Use the **same `masks/<stem>_mask.nii`** for all degraded variants of a given slice.

---

## Phase 2 — SURE Loss with Noise Maps

### 2.1 Why SURE
317 real low-quality subjects have no clean ground truth. SURE provides a provably unbiased estimator of the MSE purely from the noisy observation, enabling self-supervised denoising on these subjects without paired data.

SURE formula (for Gaussian noise with known σ²):
```
SURE(f, y, σ²) = ||y - f(y)||² / N - σ² + (2σ²/N) * div(f)(y)
```
where `div(f)(y) = Σᵢ ∂fᵢ/∂yᵢ` is the network's divergence.

### 2.2 Monte Carlo Divergence Estimator
Computing exact divergence is O(N×M) where N = pixels, M = parameters. Use Monte Carlo:
```python
def mc_divergence(net, y, sigma2, epsilon=0.01):
    b = torch.randn_like(y)                    # random probe vector
    y_perturbed = y + epsilon * b
    f_y = net(y)
    f_y_eps = net(y_perturbed)
    div_estimate = (b * (f_y_eps - f_y)).sum() / (epsilon * y.numel())
    return div_estimate

def sure_loss(net, y, sigma2):
    f_y = net(y)
    mse_term = ((y - f_y) ** 2).mean()
    div_term = mc_divergence(net, y, sigma2)
    return mse_term - sigma2 + 2 * sigma2 * div_term
```
Reference: Metzler et al., "Unsupervised Learning with Stein's Unbiased Risk Estimator", Sci Rep 2023.

### 2.3 Noise Map Input (Channel 3)
Rather than a scalar σ², provide a **per-pixel noise map** as an additional input channel. This allows the model to handle spatially-varying noise (common in HASTE: noise varies by distance from receive coil).

Input channels: `[degraded_slice (1ch), brain_mask_onehot (2ch), noise_map (1ch)]` → 4 channels total.

For synthetic data: `noise_map = σ * ones(H, W)` (uniform, since degradation is applied uniformly).
For real data: estimate noise map from local statistics in background + masked brain tissue.

### 2.4 Noise Estimation for Real Low-Quality Subjects
Two options (use both as ensemble):
- **Background estimation:** compute local std in regions outside the brain mask
- **Marchenko-Pastur:** estimate noise σ from the singular values of image patches (MP-PCA method)

Implement a `NoiseEstimator` module that runs on each real slice before feeding to SURE.

### 2.5 SURE Only for Noise Degradations
SURE is theoretically valid only for Gaussian noise. For Rician noise it is approximately valid when SNR > 2 (common in good brain tissue). For blur and bias, SURE does not apply — use supervised loss only.

Strategy:
- Supervised loss on ALL synthetic paired samples (all 61 degradation types)
- SURE loss on real low-quality subjects (noise contribution only)
- λ_sure schedule: start at 0.001, warm up to 0.01 over 20 epochs (avoid instability from runs 12-13)

---

## Phase 3 — Model Architecture Updates

### 3.1 Input Channel Change
Current: `(B, 1, H, W)` → degraded slice only (brain mask passed separately for FiLM)
New: `(B, 2, H, W)` → `[degraded_slice, noise_map]` concatenated

Brain mask still passed as FiLM conditioning (unchanged from Run18 — keep what works).

### 3.2 Noise-Adaptive FiLM (Optional, Run21+)
If noise map input alone is insufficient, add a second FiLM branch conditioned on a scalar noise level embedding:
```
noise_embed = MLP(σ) → (γ_noise, β_noise) → modulate decoder at top level only
```
This is additive to the brain mask FiLM. Try only if Run20 shows noise map input is not enough.

### 3.3 Keep TissueClassifier
Run19 showed tissue conditioning marginally helps (0.0538 vs 0.0541). Keep the classifier active — it provides anatomical priors that are valid regardless of the noise map. With the massive expanded dataset the classifier will get much more training signal.

### 3.4 No Slice Corrupt
Drop `slice_corrupt` from the training degradations entirely. Run18 showed -58.72 dB on this category — it is not a learnable enhancement in the current architecture (structural/geometric artifact, not intensity degradation). Including it actively hurts the model. Focus entirely on: noise, blur, bias, and their combinations.

---

## Phase 4 — Training Configuration (Run20)

### 4.1 Dataset Construction
```
Step 1: For each subject in nesvor_simslices/ (48 subjects with projected_labels):
  - Find raw/, masks/ directories
  - Build mask-nonzero cumulative index
  - For each brain slice i: record (raw_path, z, subject, protocol, label_path_i, mask_path)

Step 2: Cross with 61 degradation configs:
  - For each slice × degradation: add row to manifest with degradation_type, params, noise_variance

Step 3: Add 317 real LOW quality subjects as UnpairedLowDataset rows (noise_variance=None → estimated at runtime)

Step 4: 80/20 train/val split by subject (not by slice) to prevent data leakage
```

### 4.2 Training Schedule
```
Phase 1 (epochs 1-10):  supervised only, λ_sure=0, λ_tissue=0.3, λ_freq=0.1, lr=1e-4
Phase 2 (epochs 11-30): supervised + SURE warmup, λ_sure linearly 0→0.005, lr cosine decay
Phase 3 (epochs 31-100): supervised + SURE full, λ_sure=0.01, continue cosine
```

### 4.3 Hyperparameters
```yaml
batch_size: 16
lr: 1e-4
optimizer: AdamW (weight_decay=1e-4)
scheduler: CosineAnnealingLR (T_max=100, eta_min=1e-6)
gradient_clip: 1.0
lambda_l1: 0.7
lambda_ssim: 0.3
lambda_freq: 0.1
lambda_tissue: 0.3
lambda_sure: 0.0 → 0.01 (warmed up)
noise_map_input: True
```

---

## Phase 5 — Evaluation Protocol

### 5.1 Synthetic Test Set
- Hold-out subjects (not in training) × all 61 degradation types
- Report PSNR, SSIM per degradation category
- Compare Run18 vs Run20 on each category

### 5.2 Real Low-Quality Gallery
- Pick 30 representative real subjects (noise-dominant, blur-dominant, mixed)
- Run model in inference mode (noise_map estimated from background)
- Visual comparison: original vs enhanced, with and without brain mask visible

### 5.3 SURE Ablation
- Run20a: no SURE (supervised only, new dataset)
- Run20b: SURE λ=0.001
- Run20c: SURE λ=0.01 (full)
- Compare all three on real subjects (no GT) via qualitative gallery + FID/perceptual metric

---

## Implementation Order

1. ✅ **`scripts/build_expanded_manifest.py`** — 265 subjects × 61 degradations → `train_v3.csv` (12,932 rows), `val_v3.csv` (3,233 rows). Merges `brain_mask_path` from `train_v2.csv`. 2026-04-03.
2. ✅ **`src/training/dataset.py`** — Added `apply_degradation()` (6 types), `_make_bias_field()`, `OnTheFlyPairedDataset`. Returns `noise_map` tensor + `noise_variance` scalar. 2026-04-03.
3. ✅ **`src/training/losses.py`** — `SURELoss` with MC divergence estimator already implemented (spatially-variant, Pfaff 2023 formulation).
4. ✅ **`src/utils/noise_estimator.py`** — background-std + MP-PCA noise estimation. Verified: σ_bg=0.0997, σ_mp=0.0996 on synthetic σ=0.10 test. 2026-04-03.
5. ✅ **`src/model/fetenh_net.py`** — `use_noise_map=True`: concat `[degraded, noise_map]` → in_channels=2. Fixed `enhancement_net.py` residual to `img[:, :1] + residual` (always 1-ch output). 2026-04-03.
6. ✅ **`src/model/config.py`** — Added `use_noise_map: bool = False`. 2026-04-03.
7. ✅ **`scripts/train.py`** — Added `--use_onthefly`, `--use_noise_map`, `--lambda_sure_target`, `--lambda_sure_warmup_start/end`. SURE warmup in trainer. 2026-04-03.
8. ✅ **`scripts/launch_run20.sh`** — full launch config with SURE 3-phase warmup schedule. 2026-04-03.

**Integration test passed 2026-04-03:** dataset → model (2-ch input) → loss. All 6 degradation types verified. pred.shape=(B,1,H,W) confirmed. SURE loss computes. Noise estimator accurate.

**STATUS: ALL 3 RUNS LIVE — 2026-04-03 18:09 EDT**

---

## Launch Fixes Applied (2026-04-03)

Two bugs surfaced during the first launch attempt and were fixed before epoch 1 completed:

### Bug 1: Wrong Python environment
- `/neuro/labs/.../environment/bin/python3` → `torch 2.11.0+cpu`, CUDA disabled
- Fix: use `/neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/bmex_fetal/bin/python3` (torch 2.1.2+cu121)
- Updated `PYTHON=` line in all 3 launch scripts

### Bug 2: `--lambda_l1` / `--lambda_ssim` not in argparse
- Launch scripts passed `--lambda_l1 0.7 --lambda_ssim 0.3` but `train.py` never registered these flags
- These values are already the defaults in `config.py` (`lambda_l1=0.7`, `lambda_ssim=0.3`)
- Fix: removed both flags from all launch scripts — defaults apply automatically

### Bug 3: `_val_epoch` missing noise_map
- `trainer.py:_val_epoch` called `self.model(deg, brain_mask=brain_mask)` — 1-channel input
- Model trained with `use_noise_map=True` expects 2-channel input `[degraded, noise_map]`
- Crash: `RuntimeError: expected input to have 2 channels, got 1 channels`
- Fix: patched `_val_epoch` to load `batch['noise_map']` and pass it to model (both with/without brain_mask cases)

All fixes are in-place on NFS — all 3 servers see the corrected code immediately.

---

## Confirmed Epoch 1 Results

| Run | Server | train_sup | val_sup | s/epoch |
|-----|--------|-----------|---------|---------|
| Run20 (SURE, 1000ep) | sejong | 0.1329 | 0.1095 | 141s |
| Run20a (supervised, 300ep) | busan | 0.1310 | 0.1078 | 135s |
| Run20b (early SURE, 300ep) | gangnam | 0.1267 | 0.1042 | 182s |

Baseline (Run18 best): `val_sup = 0.0541`. These epoch-1 values are expected to drop significantly during training.
GPU utilization confirmed healthy: sejong 68–92%, busan up to 100%, gangnam 87–100%.

---

## Expected Outcomes

| Metric | Run18 (baseline) | Run20 (target) |
|--------|-----------------|----------------|
| Noise PSNR gain | +5.10 dB | +6–7 dB (SURE on real + denser training) |
| Blur PSNR gain | +4.04 dB | +5–6 dB (more blur levels in training) |
| Bias PSNR gain | +3.32 dB | +4–5 dB (full bias parameter grid) |
| Mixed PSNR gain | +1.63 dB | +3–4 dB (combined degradation training) |
| Real subject quality | subjective improvement | measurable via SURE loss ↓ + visual gallery |

---

## Open Questions

1. **On-the-fly vs pre-generated:** On-the-fly degradation requires more CPU per batch. With 8 workers and simple degradation ops (Gaussian filter, additive noise) this should be fine. Benchmark first.
2. **Noise map accuracy for real subjects:** If background estimation is too noisy (pun intended), switch to MP-PCA which is more robust but slower. Decide after checking a few real subjects.
3. **SURE for Rician noise:** The reference Sci Rep paper (Metzler 2023) shows SURE works well for Rician in practice for SNR > 2. Our noise levels are in this range for the brain region. Acceptable approximation.
4. **Tissue label completeness:** 48 subjects have projected_labels. The remaining ~200 subjects without NeSVoR reconstructions only have brain masks (no tissue labels). They can still be used for training with tissue CE loss disabled for those rows.

---

## Related Notes
- [[BCH-FetEnhNet]] — main project note, architecture, run history
- [[BCH-Meeting-Minutes]] — weekly group meetings
