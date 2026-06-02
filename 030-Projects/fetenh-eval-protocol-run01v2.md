---
title: "FetEnhNet BME-X Mirror Run 01 v2 — Complete Evaluation Protocol"
type: protocol
created: 2026-05-15
tags: [fetenh, bch, eval, bmex, protocol]
---

# Evaluation Protocol: BME-X Mirror Run 01 v2

> Checkpoint: `checkpoints/bmex_run01/best.pt` (BMEXMirror2d, 30 epochs, best val=0.4812)
> Model outputs: `seg_logits` (4-class: bg, CP, WM, CSF) + `recon` (1-ch enhanced)

---

## 1. DL RESEARCHER: PSNR/SSIM Computation Specification

### 1.1 PSNR Definition

```python
# Data range: MAX = 1.0 (crops are [0,1] normalized)
# Per-SLICE PSNR, then average across slices

def psnr_slice(clean: np.ndarray, enhanced: np.ndarray) -> float:
    """
    clean, enhanced: 2D arrays, float32, range [0,1], shape (192,192)
    """
    mse = np.mean((clean.astype(np.float64) - enhanced.astype(np.float64)) ** 2)
    if mse < 1e-12:
        return 60.0  # cap at 60 dB to avoid inf
    return float(10.0 * np.log10(1.0 / mse))  # MAX=1.0, so MAX^2=1.0
```

**Critical decisions:**
- `MAX = 1.0` because crops are normalized to [0,1] during preprocessing. This is the dynamic range of the data the model sees.
- Compute per-slice, then **arithmetic mean** across slices. NOT aggregate MSE then log. Rationale: per-slice averaging is standard in enhancement literature (DnCNN, EDSR, SwinIR all do this). Aggregating MSE biases toward high-error slices.
- Use `float64` accumulation to avoid precision loss on 192x192 crops.
- Cap at 60 dB. Any PSNR above ~55 dB is measurement noise, not signal.

**DELTA-PSNR (the primary metric):**
```python
delta_psnr = psnr_slice(clean, enhanced) - psnr_slice(clean, degraded)
```
This is the improvement FROM the degraded input. Positive = model helped. This is how every enhancement paper reports results (SwinIR, Restormer, NAFNet).

### 1.2 SSIM Definition

```python
from skimage.metrics import structural_similarity as ssim

def ssim_slice(clean: np.ndarray, enhanced: np.ndarray) -> float:
    """
    Use scikit-image SSIM with standard parameters.
    data_range=1.0 because [0,1] normalized.
    """
    return ssim(clean, enhanced, data_range=1.0, win_size=7,
                gaussian_weights=True, sigma=1.5, K1=0.01, K2=0.03)
```

**Critical decisions:**
- `win_size=7` (standard for 192x192; default 11 is fine for 256+ but 7 is more sensitive at our resolution). Actually, 7 is the scikit-image default. Keep it.
- `gaussian_weights=True` — matches Wang et al. 2004 original SSIM paper.
- `data_range=1.0` — must match our normalization.
- Do NOT use the hand-rolled global-mean SSIM from `model_inference.py` (that computes a single scalar mean/var over the whole image — it is NOT structural similarity, it is a luminance-contrast approximation). Use `skimage.metrics.structural_similarity` which computes the proper sliding-window version.

**DELTA-SSIM:**
```python
delta_ssim = ssim_slice(clean, enhanced) - ssim_slice(clean, degraded)
```

### 1.3 Test Set Size and Determinism

```
Test set: 232 stacks, 8,233 slices (from DB, verified May 14)
Pre-computed crops: experiments/precomputed/test/clean.npy, labels.npy
```

For eval, we need **per-degradation** application to each test crop.

**Deterministic seeding protocol:**
```python
# Each (slice_index, degradation_id) pair gets a unique, reproducible seed
seed = hash((slice_global_index, degradation_id)) % (2**31)
rng = np.random.RandomState(seed)
```

This ensures:
- Same degradation instance every time we re-run eval
- Different random realization per slice (not all slices get identical noise pattern)
- Different degradation types on the same slice get independent randomness

**Sample counts per metric row:**
- Each of 33 degradation presets: all 8,233 test slices
- Total forward passes: 33 x 8,233 = 271,689
- At ~71 img/s (batch=32, AMP, single A5000): ~64 minutes

### 1.4 Brain-Masked Metrics (mandatory secondary)

Metrics computed only within the brain region, not the black background:

```python
def psnr_masked(clean, enhanced, mask):
    """mask: binary, True where brain tissue exists."""
    brain_clean = clean[mask].astype(np.float64)
    brain_enh = enhanced[mask].astype(np.float64)
    mse = np.mean((brain_clean - brain_enh) ** 2)
    if mse < 1e-12:
        return 60.0
    # MAX is still 1.0 (the value range within brain)
    return float(10.0 * np.log10(1.0 / mse))
```

Rationale: brain crops are ~50-70% brain tissue, rest is black background. An enhancement model that does nothing to background but fixes brain gets penalized by full-image PSNR. Brain-masked PSNR isolates the signal of interest.

Brain mask derivation: `labels > 0` (any non-background class in the ground truth segmentation).

---

## 2. MRI PHYSICIST: BME-X Quality Index (TCT/QI) Computation

### 2.1 What TCT Actually Is

From BME-X replication plan (confirmed against container code):

```
TCT = |mu_tissue_A - mu_tissue_B| / sqrt(sigma_A^2 + sigma_B^2)
```

This is the **Tissue Contrast-to-Noise Ratio** — a standard MRI quality metric (sometimes called CNR). It measures how well two tissue classes are distinguishable given their intensity overlap.

BME-X computes this for **all tissue pairs** and takes the mean. With 4 classes (bg, CSF, GM, WM), there are C(3,2) = 3 foreground tissue pairs:
- CP vs WM
- CP vs CSF
- WM vs CSF

(Background excluded — it is air/zero-padding, not tissue.)

**NOTE on class naming:** BME-X uses bg/CSF/GM/WM. Our model uses bg/CP/WM/CSF (cortical plate instead of gray matter — fetal brain has cortical plate, not mature gray matter). The mapping is: CP <-> GM (both are the cortical/gray tissue class).

### 2.2 TCT Computation on 2D Crops

```python
def compute_tct(image_2d: np.ndarray, label_2d: np.ndarray) -> float:
    """
    image_2d: (192,192) float32 [0,1]
    label_2d: (192,192) int, classes {0=bg, 1=CP, 2=WM, 3=CSF}

    Returns mean TCT across all foreground tissue pairs.
    """
    tissue_classes = [1, 2, 3]  # CP, WM, CSF
    pairs = [(1,2), (1,3), (2,3)]  # CP-WM, CP-CSF, WM-CSF

    tct_values = []
    for c_a, c_b in pairs:
        mask_a = (label_2d == c_a)
        mask_b = (label_2d == c_b)

        # Skip if either class has < 10 pixels (unreliable statistics)
        if mask_a.sum() < 10 or mask_b.sum() < 10:
            continue

        mu_a = image_2d[mask_a].mean()
        mu_b = image_2d[mask_b].mean()
        sigma_a = image_2d[mask_a].std()
        sigma_b = image_2d[mask_b].std()

        denom = np.sqrt(sigma_a**2 + sigma_b**2)
        if denom < 1e-8:
            continue

        tct = abs(mu_a - mu_b) / denom
        tct_values.append(tct)

    if len(tct_values) == 0:
        return float('nan')
    return float(np.mean(tct_values))
```

### 2.3 QI Computation

```python
def compute_qi(tct_original: float, tct_enhanced: float) -> float:
    """
    BME-X definition: QI = TCT_original / TCT_enhanced

    QI < 1 means enhancement IMPROVED tissue contrast (enhanced has higher TCT).
    QI > 1 means enhancement DEGRADED tissue contrast.
    QI = 1 means no change.

    NOTE: BME-X container writes QI to {stem}-QI.txt. Their reported range
    was 0.45-0.81 for fetal data, meaning enhancement improved contrast by
    ~1.2x to ~2.2x.
    """
    if tct_enhanced < 1e-8:
        return float('nan')
    return tct_original / tct_enhanced
```

### 2.4 Is TCT Meaningful on 2D Crops with Synthetic Degradation?

**Yes, with caveats:**

1. **Noise degradation**: TCT is DIRECTLY sensitive to this. Adding noise increases sigma_A and sigma_B, which decreases TCT. If the model denoises, TCT goes up. This is the most informative case.

2. **Blur degradation**: Blur increases overlap between tissue distributions (blurs boundaries, mixes intensities). TCT should decrease. Enhancement that sharpens should partially restore TCT.

3. **Bias field**: Bias field shifts mu_A and mu_B spatially, but the global mean ratio may not change much. TCT is LESS sensitive here. Report but note caveat.

4. **On 2D crops**: Perfectly valid. TCT is a statistical measure over pixel intensities — it does not require 3D structure. Each 192x192 crop contains all 3 tissue classes (verified: 98.1% of training stacks have Dice >= 0.95 for label coverage).

5. **Using GT labels for both original and enhanced**: We use the SAME ground truth label map (from clean data) to define tissue regions in both the degraded and enhanced images. This is correct — we are measuring how well the enhancement restores tissue discriminability, not whether it changes the segmentation.

### 2.5 TCT on Real Data (Eval Pool)

For real degraded data (eval pool, 4,087 stacks), we do NOT have clean references. Use the MODEL'S OWN segmentation output to define tissue regions:

```python
def compute_tct_with_predicted_labels(image_2d, seg_logits):
    """Use model's argmax segmentation to define tissue regions."""
    label_2d = np.argmax(seg_logits, axis=0)  # (H,W)
    return compute_tct(image_2d, label_2d)
```

This is EXACTLY how BME-X does it — their TCT uses the model's own tissue classification. For the QI metric on real data:
- TCT_original: computed on the raw input using the model's predicted segmentation of that input
- TCT_enhanced: computed on the enhanced output using the model's predicted segmentation of the output

Report QI separately for real data with a caveat that both numerator and denominator depend on model predictions.

---

## 3. ML ENGINEER: Eval Script Specification

### 3.1 Script: `scripts/eval_bmex_run01v2.py`

```python
#!/usr/bin/env python3
"""
Complete evaluation of BME-X Mirror Run 01 v2.

Usage:
    python eval_bmex_run01v2.py \
        --checkpoint checkpoints/bmex_run01/best.pt \
        --test_crops experiments/precomputed/test/clean.npy \
        --test_labels experiments/precomputed/test/labels.npy \
        --output_dir eval_results/bmex_run01v2/ \
        --device cuda:0 \
        --batch_size 32 \
        --seed 42

Outputs:
    eval_results/bmex_run01v2/
    ├── metrics.json              # All numbers, machine-readable
    ├── metrics_summary.txt       # Human-readable summary table
    ├── per_degradation.csv       # One row per degradation preset
    ├── per_slice.parquet         # One row per (slice, degradation) pair
    ├── segmentation_dice.csv     # Per-class Dice, one row per slice
    ├── qi_synthetic.csv          # QI per (slice, degradation) pair
    ├── figures/
    │   ├── delta_psnr_barplot.pdf
    │   ├── delta_ssim_barplot.pdf
    │   ├── dice_boxplot.pdf
    │   ├── qi_histogram.pdf
    │   ├── psnr_vs_degradation_severity.pdf
    │   ├── visual_grid_noise.pdf
    │   ├── visual_grid_blur.pdf
    │   ├── visual_grid_bias.pdf
    │   ├── visual_grid_combined.pdf
    │   ├── visual_grid_all_types.pdf
    │   └── tissue_overlay_examples.pdf
    └── config.json               # Exact eval config for reproducibility
```

### 3.2 Pseudocode: Main Eval Loop

```python
import numpy as np
import torch
import json
import pandas as pd
from pathlib import Path
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm

# --- PHASE 1: Load model and data ---

model = load_bmex_mirror(checkpoint_path, device)
model.eval()

clean_crops = np.load(test_crops_path)     # (N, 192, 192) float32 [0,1]
label_crops = np.load(test_labels_path)    # (N, 192, 192) int64 {0,1,2,3}
N = clean_crops.shape[0]

# Import the CANONICAL degradation catalog from src/degradation.py
from src.degradation import apply_degradation, DEGRADATION_CATALOG

# Save exact config
config = {
    "checkpoint": str(checkpoint_path),
    "test_crops": str(test_crops_path),
    "n_slices": N,
    "crop_size": 192,
    "data_range": 1.0,
    "psnr_cap": 60.0,
    "degradation_catalog_len": len(DEGRADATION_CATALOG),
    "batch_size": batch_size,
    "seed": seed,
    "eval_timestamp": datetime.now().isoformat(),
}
json.dump(config, open(output_dir / "config.json", "w"), indent=2)

# --- PHASE 2: Per-degradation eval (synthetic) ---

records = []  # per-(slice, degradation) records

for deg in tqdm(DEGRADATION_CATALOG, desc="Degradations"):
    deg_id = deg["id"]

    batch_degraded = []
    batch_clean = []
    batch_labels = []
    batch_indices = []

    for i in range(N):
        # Deterministic seed per (slice, degradation)
        deg_seed = hash((i, deg_id)) % (2**31)
        degraded = apply_degradation(clean_crops[i], deg_id, seed=deg_seed)

        batch_degraded.append(degraded)
        batch_clean.append(clean_crops[i])
        batch_labels.append(label_crops[i])
        batch_indices.append(i)

        # Process in batches
        if len(batch_degraded) == batch_size or i == N - 1:
            # Stack and run model
            deg_tensor = torch.from_numpy(
                np.stack(batch_degraded)[:, None]  # (B, 1, 192, 192)
            ).float().to(device)

            with torch.no_grad(), torch.amp.autocast('cuda'):
                seg_logits, recon = model(deg_tensor)

            seg_np = seg_logits.cpu().numpy()   # (B, 4, 192, 192)
            enh_np = recon[:, 0].cpu().numpy()  # (B, 192, 192)

            for j in range(len(batch_degraded)):
                c = batch_clean[j]
                d = batch_degraded[j]
                e = np.clip(enh_np[j], 0, 1)  # clip model output to valid range
                lab = batch_labels[j]
                brain_mask = lab > 0

                # --- Full-image metrics ---
                psnr_deg = psnr_slice(c, d)
                psnr_enh = psnr_slice(c, e)
                ssim_deg = ssim(c, d, data_range=1.0)
                ssim_enh = ssim(c, e, data_range=1.0)

                # --- Brain-masked metrics ---
                psnr_deg_brain = psnr_masked(c, d, brain_mask)
                psnr_enh_brain = psnr_masked(c, e, brain_mask)

                # --- Segmentation Dice ---
                seg_pred = np.argmax(seg_np[j], axis=0)  # (192,192)
                dice_per_class = {}
                for cls_id, cls_name in [(1,"CP"), (2,"WM"), (3,"CSF")]:
                    pred_mask = (seg_pred == cls_id)
                    gt_mask = (lab == cls_id)
                    intersection = (pred_mask & gt_mask).sum()
                    union = pred_mask.sum() + gt_mask.sum()
                    dice = 2 * intersection / max(union, 1)
                    dice_per_class[cls_name] = float(dice)

                # --- TCT / QI ---
                tct_clean = compute_tct(c, lab)
                tct_degraded = compute_tct(d, lab)
                tct_enhanced = compute_tct(e, lab)
                qi = compute_qi(tct_degraded, tct_enhanced)

                records.append({
                    "slice_idx": batch_indices[j],
                    "degradation_id": deg_id,
                    "degradation_type": deg["type"],
                    "degradation_level": deg.get("level", ""),
                    "psnr_degraded": psnr_deg,
                    "psnr_enhanced": psnr_enh,
                    "delta_psnr": psnr_enh - psnr_deg,
                    "ssim_degraded": ssim_deg,
                    "ssim_enhanced": ssim_enh,
                    "delta_ssim": ssim_enh - ssim_deg,
                    "psnr_degraded_brain": psnr_deg_brain,
                    "psnr_enh_brain": psnr_enh_brain,
                    "delta_psnr_brain": psnr_enh_brain - psnr_deg_brain,
                    "dice_CP": dice_per_class["CP"],
                    "dice_WM": dice_per_class["WM"],
                    "dice_CSF": dice_per_class["CSF"],
                    "dice_mean_fg": np.mean(list(dice_per_class.values())),
                    "tct_clean": tct_clean,
                    "tct_degraded": tct_degraded,
                    "tct_enhanced": tct_enhanced,
                    "qi": qi,
                })

            batch_degraded, batch_clean, batch_labels, batch_indices = [], [], [], []

# --- PHASE 3: Aggregate and save ---

df = pd.DataFrame(records)
df.to_parquet(output_dir / "per_slice.parquet")

# Per-degradation summary
agg = df.groupby("degradation_id").agg({
    "delta_psnr":       ["mean", "std", "median"],
    "delta_ssim":       ["mean", "std", "median"],
    "delta_psnr_brain": ["mean", "std", "median"],
    "dice_CP":          ["mean", "std"],
    "dice_WM":          ["mean", "std"],
    "dice_CSF":         ["mean", "std"],
    "dice_mean_fg":     ["mean", "std"],
    "qi":               ["mean", "std", "median"],
}).round(4)
agg.to_csv(output_dir / "per_degradation.csv")

# Top-level summary
summary = {
    "overall_delta_psnr_mean": float(df["delta_psnr"].mean()),
    "overall_delta_psnr_std":  float(df["delta_psnr"].std()),
    "overall_delta_ssim_mean": float(df["delta_ssim"].mean()),
    "overall_delta_ssim_std":  float(df["delta_ssim"].std()),
    "overall_delta_psnr_brain_mean": float(df["delta_psnr_brain"].mean()),
    "overall_dice_CP_mean":  float(df["dice_CP"].mean()),
    "overall_dice_WM_mean":  float(df["dice_WM"].mean()),
    "overall_dice_CSF_mean": float(df["dice_CSF"].mean()),
    "overall_qi_mean":       float(df["qi"].mean()),
    "n_slices": N,
    "n_degradations": len(DEGRADATION_CATALOG),
    "n_records": len(df),
}
json.dump(summary, open(output_dir / "metrics.json", "w"), indent=2)
```

### 3.3 Phase 4: No-Reference Eval on Real Data (Eval Pool)

```python
# --- PHASE 4: Real degraded data (no clean reference) ---
# Load eval pool from DB: stacks with role='eval'
# For each stack, load all slices, crop to 192x192 brain region

eval_records = []

for stack in eval_pool_stacks:
    for slice_2d in load_stack_slices(stack):
        # Normalize to [0,1]
        normed = normalize_to_01(slice_2d)
        crop = brain_crop_192(normed)  # same cropping as training

        # Run model
        tensor = torch.from_numpy(crop[None, None]).float().to(device)
        with torch.no_grad():
            seg_logits, recon = model(tensor)
        enhanced = recon[0, 0].cpu().numpy()
        seg_pred = seg_logits[0].cpu().numpy()

        # No-reference metrics
        tct_input = compute_tct_with_predicted_labels(crop, seg_pred)

        # For enhanced, re-run segmentation or use same labels
        # Using SAME predicted labels (from input) is fairer — avoids
        # circular reasoning where better enhancement -> better seg -> higher TCT
        tct_enhanced = compute_tct(enhanced, np.argmax(seg_pred, axis=0))

        qi = compute_qi(tct_input, tct_enhanced)

        # Sharpness (Laplacian variance — no-reference)
        laplacian_var_input = np.var(
            cv2.Laplacian(crop, cv2.CV_64F)
        )
        laplacian_var_enh = np.var(
            cv2.Laplacian(enhanced, cv2.CV_64F)
        )

        # SNR estimate (brain mean / background std)
        brain_mask = np.argmax(seg_pred, axis=0) > 0
        if brain_mask.sum() > 0 and (~brain_mask).sum() > 10:
            snr_input = crop[brain_mask].mean() / max(crop[~brain_mask].std(), 1e-8)
            snr_enh = enhanced[brain_mask].mean() / max(enhanced[~brain_mask].std(), 1e-8)
        else:
            snr_input = snr_enh = float('nan')

        eval_records.append({
            "stack_id": stack.id,
            "slice_idx": slice_idx,
            "protocol": stack.protocol,
            "quality_label": stack.quality,  # from explorer annotations
            "tct_input": tct_input,
            "tct_enhanced": tct_enhanced,
            "qi": qi,
            "laplacian_input": laplacian_var_input,
            "laplacian_enhanced": laplacian_var_enh,
            "delta_sharpness": laplacian_var_enh - laplacian_var_input,
            "snr_input": snr_input,
            "snr_enhanced": snr_enh,
        })
```

### 3.4 Reproducibility Guarantees

1. **Exact degradation catalog**: import from `src/degradation.py` (the unified source). Do NOT use the old explorer-local `degradations.py` — it has different parameter names and missing presets.

2. **Deterministic seeding**: `hash((slice_idx, degradation_id)) % 2**31` for each degradation application. Document this in `config.json`.

3. **Model determinism**: `torch.backends.cudnn.deterministic = True` and `torch.backends.cudnn.benchmark = False` at script start.

4. **Exact normalization**: crops loaded from `clean.npy` are ALREADY [0,1] normalized (done during `precompute_crops.py`). Do NOT re-normalize.

5. **Output clipping**: `np.clip(enhanced, 0, 1)` on model output before computing metrics. The model has ReLU on recon head but could theoretically output slightly > 1 due to floating point.

6. **Save everything**: per-slice parquet enables post-hoc analysis (stratify by brain size, by protocol, by degradation severity). Never discard per-sample data.

### 3.5 Runtime Estimate

| Phase | Samples | Batch | Time (single A5000) |
|-------|---------|-------|---------------------|
| Synthetic eval (33 degs x 8,233 slices) | 271,689 | 32 | ~64 min |
| Segmentation Dice (computed in same pass) | — | — | +0 min |
| Real data eval (~50K slices from 4,087 stacks) | ~50,000 | 32 | ~12 min |
| Figure generation | — | — | ~5 min |
| **Total** | | | **~81 min** |

Run on hanyang (2x A5000, both free). Can parallelize by splitting degradation catalog across GPUs.

---

## 4. PEER REVIEWER: Required Tables and Figures

### 4.1 Table 1: Per-Degradation Enhancement Results (PRIMARY)

This is the money table. Format matches enhancement literature (DnCNN Table 1, SwinIR Table 2).

```
+----------------------------+--------+--------+---------+---------+---------+
| Degradation                | DPSNR  | DSSIM  | DPSNR   | Dice    | QI      |
|                            | (dB)   |        | (brain) | (fg)    |         |
+----------------------------+--------+--------+---------+---------+---------+
| Rician noise (low, s=0.05) | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Rician noise (med, s=0.10) | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Rician noise (high, s=0.20)| +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gaussian blur (low, s=0.8) | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gaussian blur (med, s=1.5) | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gaussian blur (high, s=2.5)| +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Bias field (low)           | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Bias field (med)           | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Bias field (high)          | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Intra-slice motion (low)   | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Intra-slice motion (med)   | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Intra-slice motion (high)  | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Signal dropout (low)       | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Signal dropout (med)       | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Signal dropout (high)      | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gibbs ringing (low)        | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gibbs ringing (med)        | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Gibbs ringing (high)       | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| K-space spike (low)        | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| K-space spike (med)        | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| K-space spike (high)       | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Downsample (low)           | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Downsample (med)           | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Downsample (high)          | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Combined (noise+blur)      | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
| Combined (all)             | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
+----------------------------+--------+--------+---------+---------+---------+
| OVERALL (all 33 presets)   | +X.XX  | +0.XXX | +X.XX   | 0.XXX   | 0.XXX   |
+----------------------------+--------+--------+---------+---------+---------+
```

Report mean +/- std in the supplementary. Main table shows mean only (cleaner).

### 4.2 Table 2: Per-Class Segmentation Dice

```
+--------------------+-------+-------+-------+-------+
| Degradation Type   |  CP   |  WM   |  CSF  |  Mean |
+--------------------+-------+-------+-------+-------+
| Clean (no degrad)  | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Noise (all levels) | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Blur (all levels)  | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Bias (all levels)  | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Motion (all)       | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Dropout (all)      | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Gibbs (all)        | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| K-spike (all)      | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Downsample (all)   | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
| Combined           | 0.XXX | 0.XXX | 0.XXX | 0.XXX |
+--------------------+-------+-------+-------+-------+
```

**Must also include a "clean" row** — Dice on undegraded crops. This shows the baseline segmentation quality when the input is already perfect. If Dice on clean is low, the problem is the segmentation head, not degradation robustness.

### 4.3 Table 3 (Supplementary): Comparison with Run 01 (FetEnhNet)

Side-by-side with Run 01 results (already published in slides):

```
+----------------------------+-----------+-----------+-----------+-----------+
| Degradation                | Run01 FE  | Run01v2   | Run01 FE  | Run01v2   |
|                            | DPSNR     | DPSNR     | DSSIM     | DSSIM     |
+----------------------------+-----------+-----------+-----------+-----------+
| Noise (low)                | +3.76     | +X.XX     | +0.012    | +0.XXX    |
| Noise (med)                | +7.14     | +X.XX     | +0.067    | +0.XXX    |
| ...                        | ...       | ...       | ...       | ...       |
+----------------------------+-----------+-----------+-----------+-----------+
```

### 4.4 Required Figures

#### Figure 1: DPSNR Bar Plot (per degradation type, grouped by severity)

```
[Grouped bar chart]
X-axis: degradation types (8 groups)
Bars within group: low / med / high
Y-axis: DPSNR (dB)
Color: blue gradient (light=low, dark=high)
Error bars: +/- 1 std
Horizontal line at y=0 (no improvement)
```

**What makes it convincing:** Error bars show variance is small relative to effect size. Horizontal zero line makes it obvious which degradations the model helps vs hurts.

**What makes it suspicious:** If ALL bars are identical height (model applying a fixed filter regardless of input). If std is larger than mean for any bar (unreliable).

#### Figure 2: Visual Comparison Grid (THE most scrutinized figure)

```
4 columns: Degraded | Enhanced | Clean (GT) | Difference (|Enhanced - Clean|)
6+ rows: one per degradation TYPE (pick the medium severity)
Each cell: 192x192 crop, same colormap, same window/level

Bottom row: tissue overlay — argmax segmentation painted on enhanced, side by side with GT labels on clean
```

**What makes it convincing:**
- Same window/level across all panels (normalize globally, not per-panel)
- Difference map uses a perceptually uniform colormap (viridis or magma), NOT jet
- Include a FAILURE case (one row where the model makes things worse, e.g., bias field)
- Tissue overlay shows spatial accuracy, not just Dice number
- Choose slices with ALL 3 tissue classes clearly visible (not edge slices)

**What makes it suspicious:**
- Cherry-picked success cases only
- Different window/level per panel (hides artifacts)
- Jet colormap on difference (hides structure in yellow-green)
- Only showing noise degradation (the easiest case)

#### Figure 3: Dice Box Plot

```
Box-and-whisker per tissue class (CP, WM, CSF)
Grouped by: clean vs degraded (all types pooled)
Shows: median, IQR, outliers
```

#### Figure 4: QI Distribution

```
Histogram of QI values across all synthetic test pairs
Vertical line at QI=1 (no change)
Separate panels or overlaid histograms per degradation type
```

#### Figure 5: Real Data Enhancement Gallery (Eval Pool)

```
3x6 grid:
Columns: Original | Enhanced | Tissue Overlay
Rows: 6 real degraded slices from eval pool, chosen to span:
  - 2 good quality (model should not make worse)
  - 2 medium quality (visible improvement expected)
  - 2 low quality (hardest cases, most improvement expected)

Each row labeled with: protocol, quality annotation, QI value
```

**What makes it convincing:** Showing real MRI data (not synthetic) proves generalization. Including good-quality inputs where the model should be near-identity shows it does not hallucinate on clean data.

#### Figure 6: PSNR vs Degradation Severity Curve

```
Line plot.
X-axis: degradation parameter value (e.g., noise sigma: 0.05, 0.10, 0.20)
Y-axis: DPSNR
One line per degradation TYPE
```

Shows that improvement scales with degradation severity (expected behavior: more degraded -> more room to improve -> higher DPSNR). If this relationship is NOT monotonic, something is wrong.

### 4.5 Mandatory Sanity Checks (reviewer will look for these)

1. **Identity test**: Run clean (undegraded) crops through the model. PSNR should be very high (>35 dB), SSIM > 0.95. If the model degrades clean inputs, it is not usable. Report this as row 0 in Table 1.

2. **Negative DPSNR count**: How many individual slices have DPSNR < 0 (model made it worse)? Report as: "X% of slices showed negative DPSNR for degradation Y." If > 20% for any degradation type, the model is unreliable for that artifact.

3. **Dice on clean vs degraded**: If Dice drops significantly with degradation, the segmentation head is not robust. This is expected (same as BME-X observation that classification is robust to corruption), but quantify it.

4. **Statistical significance**: For the comparison with Run 01 (Table 3), compute paired t-test or Wilcoxon signed-rank test on per-slice DPSNR. Report p-value. With N=8,233, even tiny differences will be significant, so also report effect size (Cohen's d).

5. **Distribution plots**: At minimum, show the DISTRIBUTION of DPSNR (histogram or violin), not just mean/std. A bimodal distribution (some slices massively improved, others degraded) tells a very different story than a tight unimodal one.

### 4.6 Red Flags a Reviewer Will Catch

| Red Flag | Mitigation |
|----------|------------|
| Reporting PSNR with wrong MAX value (e.g., MAX=255 for [0,1] data) | Explicitly state MAX=1.0 in methods |
| Global SSIM instead of sliding-window | Use `skimage.metrics.structural_similarity` |
| No variance/confidence intervals | Report std and show box plots |
| Only synthetic eval, no real data | Include eval pool results (Phase 4) |
| Dice computed on clean inputs only | Show Dice on degraded inputs too |
| QI computed with GT labels on real data | Use predicted labels; disclose this |
| Cherry-picked visual examples | Include failure cases; state selection criteria |
| Comparing to BME-X Run 01 without noting architecture differences | Separate table, note conditioning method difference |

---

## 5. EXECUTION CHECKLIST

```
[ ] 1. Verify test crops exist: experiments/precomputed/test/{clean,labels}.npy
[ ] 2. Verify checkpoint loads: checkpoints/bmex_run01/best.pt
[ ] 3. Run identity test first (clean crops through model, no degradation)
[ ] 4. Run full synthetic eval (33 presets x 8,233 slices)
[ ] 5. Run real data eval (eval pool ~4,087 stacks)
[ ] 6. Generate all figures
[ ] 7. Compute Table 1, Table 2, Table 3
[ ] 8. Sanity checks: negative DPSNR %, identity PSNR, Dice on clean
[ ] 9. Save everything to eval_results/bmex_run01v2/
[ ] 10. Update vault context: _fetenh-context.md with results summary
```

---

## 6. KEY FORMULAS SUMMARY

| Metric | Formula | Range | Good Value |
|--------|---------|-------|------------|
| PSNR | `10*log10(1/MSE)` | 0-60 dB | >30 dB |
| DPSNR | `PSNR(clean,enh) - PSNR(clean,deg)` | any | >0 dB |
| SSIM | Wang et al. 2004 (sliding window) | 0-1 | >0.85 |
| DSSIM | `SSIM(clean,enh) - SSIM(clean,deg)` | any | >0 |
| Dice | `2*|A^B| / (|A|+|B|)` | 0-1 | >0.7 |
| TCT | `|mu_A - mu_B| / sqrt(s_A^2 + s_B^2)` | 0-inf | higher=better |
| QI | `TCT_degraded / TCT_enhanced` | 0-inf | <1 = improved |
| Laplacian var | `var(Laplacian(img))` | 0-inf | higher=sharper |
