---
title: FetEnhNet — Fetal MRI Enhancement Network
type: project
status: active
created: 2026-03-23
tags: [bch, research, deep-learning, fetal-mri, enhancement]
---

# FetEnhNet — Fetal MRI Enhancement Network

## Overview

Two-stage spatially-varying tissue-conditioned enhancement for full-FOV fetal HASTE stacks (19–34 weeks GA). No skull-stripping required.

**Goal:** Enhance low-quality fetal brain MRI raw stacks using deep learning, conditioned on anatomical tissue information.

**PI:** Kiho Im (FNNDSC, Boston Children's Hospital / Harvard Medical School)
**Team:** Daniel Barreras Meraz, Yair Beltran, Hyeokjin Kwon, Quentin Moliterno, Kyeong Ho Kim

---

## Architecture

### Stage 1 — TissueClassifier (`src/model/tissue_classifier.py`)
- Lightweight 3-level U-Net (depth=3, base_filters=32)
- Input: `(B, 1, H, W)` normalized HASTE slice
- Output: `(B, n_classes, H, W)` soft tissue probability maps (softmax)
- 4 classes (derived from iBEAT v2 labels):
  - 0: background (maternal tissue, amniotic fluid, out-of-brain)
  - 1: cortical_plate (iBEAT labels 1+42)
  - 2: wm_subplate (iBEAT labels 160+161)
  - 3: csf_other (iBEAT label 18)
- Trained via gradient from enhancement loss (FiLM conditioning) + optional tissue CE loss with focal weighting
- Class weights: `[1.0, 25.0, 9.0, 10.0]` (sqrt median-frequency balancing, CP boosted for severe imbalance)

### Stage 2 — EnhancementNet (`src/model/enhancement_net.py`)
- 4-level ResU-Net (depth=4, base_filters=64) with ResBlocks
- Conditioned on Stage 1 tissue maps via **spatially-varying FiLM** at every decoder level
- FiLM (Perez et al. AAAI 2018): tissue map bilinearly resized → 1×1 Conv → per-pixel γ,β → `h_conditioned = γ * h + β`
- Output: enhanced slice via residual learning `clamp(input + residual, 0, 1)`
- No sigmoid — clamp preserves identity when residual ≈ 0

### Combined Model (`src/model/fetenh_net.py`)
- Forward: `x_deg → TissueClassifier → tissue_map → EnhancementNet(x_deg, tissue_map) → x_enh`
- Returns both `x_enh` and `tissue_map` (for auxiliary supervision)
- `enhance_only()` for inference (no grad)
- Brain mask mode (run18+): bypasses TissueClassifier, uses GT mask directly as 2-channel one-hot FiLM input

### Loss Functions (`src/training/losses.py`)
| Loss | Weight | Description |
|------|--------|-------------|
| L1 | λ_l1=0.7 | Pixel-wise MAE on paired data |
| SSIM | λ_ssim=0.3 | 1 - SSIM (11×11 Gaussian window) |
| Frequency | λ_freq=0.0-0.1 | FFT magnitude L1 for sharpness (optional) |
| Tissue CE | λ_tissue=0.3-1.0 | Weighted focal NLLLoss, ignore_index=255 for unlabeled |
| SURE | λ_sure=0.0-0.1 | Stein's Unbiased Risk Estimator (self-supervised, currently disabled) |

### Training (`src/training/trainer.py`)
- Phase 1 (warmup_epochs): supervised only (paired stacks)
- Phase 2 (remaining): supervised + SURE self-supervised (joint, if unpaired loader provided)
- AdamW optimizer, CosineAnnealingLR scheduler
- DataParallel for multi-GPU (auto-detected)
- Visualization callback every N epochs via subprocess
- Gradient clipping: max_norm=1.0

### Dataset (`src/training/dataset.py`)
- `PairedSliceDataset`: loads (clean, degraded) pairs with tissue labels and brain masks
  - Central 20-80% z-range to avoid blank boundary slices
  - Brain-preferential sampling: 85% chance of picking labeled brain slices
  - Percentile normalization [p1, p99] → [0,1] using DEGRADED image's range (critical for scale consistency)
  - Center-crop/pad to 256×256 (no interpolation)
  - Augmentation: random H/V flip (consistent across image, label, mask)
- `UnpairedLowDataset`: real LOW quality stacks for SURE loss (no GT needed)

---

## Server Location

All code and data on sejong (10.26.66.103):
```
/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/
├── projects/fetenh_net/              # Main training code
│   ├── src/
│   │   ├── model/                    # config.py, fetenh_net.py, tissue_classifier.py, enhancement_net.py
│   │   ├── training/                 # dataset.py, trainer.py, losses.py
│   │   └── eval/
│   ├── scripts/
│   │   ├── train.py                  # Main training entry point
│   │   ├── launch_run16.sh           # Run16 launcher (tissue conditioning, 3-GPU gangnam)
│   │   ├── launch_run18.sh           # Run18 launcher (brain mask conditioning)
│   │   ├── evaluate.py, visualize.py, visualize_real.py
│   │   ├── compare_runs.py           # Cross-run comparison figures
│   │   ├── project_labels.py         # NeSVoR label projection to raw stack space
│   │   ├── make_tissue_label_figures.py
│   │   └── *_gpu*.sh                 # Per-GPU reconstruction dispatchers (sejong, hanyang, gangnam)
│   ├── checkpoints/                  # run08 through run18
│   ├── logs/                         # Per-GPU reconstruction logs (sejong_gpu0/1/2, hanyang_gpu0/1, recon_chd/)
│   ├── presentation/                 # LaTeX slides, figs/
│   ├── results/run03_vs_run04/       # Historical comparison figures
│   ├── tests/test_model.py
│   └── requirements.txt
├── experiments/2024_2026_degradation_study/
│   ├── training_data/
│   │   ├── manifests/                # train.csv, val.csv, train_v2.csv (with brain_mask_path), val_v2.csv
│   │   ├── noise/, blur/, bias/, slice_corrupt/, mixed_nb/, mixed_nbs/  # Degraded stacks by type
│   │   └── tissue_labels/{CHD,ASD,DownSyndrome,Normative,Placenta,Ventriculomegaly}/
│   ├── scripts/                      # 36 Python scripts for degradation generation, visualization, metrics
│   ├── comparison_results/
│   ├── cohort_characterization/{CHD,ASD,DownSyndrome,Normative,Placenta,Ventriculomegaly}/
│   ├── low_quality_analysis/         # Quality classification, N4 comparison, categorized stacks
│   ├── multiprotocol_quality/
│   ├── presentation_figures/
│   └── quality_classification/
├── data/                             # Raw MRI data by protocol (local copies from mri.team)
│   ├── CHD_TD/FCBxxx/                # 43 CHD subjects — each has raw/, masks/, brain/, recon_segmentation/
│   ├── ASD/                          # 18 ASD subjects
│   ├── Normative/                    # 1 subject (most are at mri.team source)
│   ├── Placenta/                     # 19 subjects
│   ├── VM/                           # 55 subjects
│   ├── normative_for_recon/          # Normative subjects copied for reconstruction
│   ├── vm_for_recon/                 # VM subjects copied for reconstruction
│   ├── dHCP/                         # Developing Human Connectome Project
│   └── individual_subjects/, test_subjects/
├── repos/
│   ├── bme-x/                        # BME-X reference implementation (DenseUNet3D, PyTorch)
│   │   ├── Brain_MRI_Enhancement/    # Original adult brain enhancement
│   │   └── fetal_enhancement/        # Daniel's fetal adaptation scripts (65+ files)
│   ├── FetalSynthSeg/                # Fetal segmentation model
│   └── iguane_harmonization/         # IGUANE 2D harmonization experiments
├── projects/activ_sparse_slm/        # Separate project: activation-sparse small language model
├── code/                             # Git repo with analysis notebooks, utilities
├── docs/, results/, scratch/, logs/
├── environments/                     # Conda/micromamba environment configs
└── scripts/                          # Utility scripts (disk_audit.sh, auto_project_after_recon.sh)
```

**Raw data source** (read-only, referenced in manifests):
```
/neuro/users/mri.team/fetal_mri/Data/
├── CHD_protocol/Data/FCBxxx/         # CHD subjects with masks/, brain/, raw/, recon_segmentation/
├── Normative/Data/                   # Normative subjects
├── Placenta/Data/                    # Placenta subjects
├── VM/                               # Ventriculomegaly subjects
└── ASD/                              # ASD subjects
```

---

## Training Data

### Paired Dataset (Supervised)
- **1,476 training pairs** across `train.csv` (246 unique subjects × 6 degradation types)
- **156 validation pairs** across `val.csv` (26 unique subjects × 6 degradation types)
- **Degradation types:** noise, blur, bias, slice_corrupt, mixed_nb, mixed_nbs
- **Input size:** 256×256 (center-crop/pad from varying raw sizes)

### Protocols
| Protocol | Train Subjects | Val Subjects |
|----------|---------------|-------------|
| CHD | 92 | 11 |
| ASD | 28 | — |
| Normative | 47 | 6 |
| Placenta | 24 | 3 |
| Ventriculomegaly | 52 | 6 |
| DownSyndrome | 3 | — |

### Tissue Label Coverage (~83.5%)
Generated via NeSVoR reconstruction campaign (March 2026). Tissue labels projected from reconstructed 3D volumes to 2D raw stack slices. Stored in `training_data/tissue_labels/`.

### Brain Mask Coverage (for Run18)
Brain masks exist at the raw data source `<session>/masks/<stack_stem>_mask.nii` — binary NIfTI aligned to each raw HASTE stack.

| Split | Rows with Masks | Total Rows | Coverage |
|-------|----------------|------------|----------|
| train_v2.csv | 1,020 | 1,476 | 70% |
| val_v2.csv | 120 | 156 | 77% |

**By protocol (train):**
| Protocol | With Masks | Total | Coverage |
|----------|-----------|-------|----------|
| DownSyndrome | 3 | 3 | 100% |
| Normative | 47 | 47 | 100% |
| Ventriculomegaly | 52 | 52 | 100% |
| CHD | 53 | 92 | 58% |
| Placenta | 11 | 24 | 46% |
| ASD | 6 | 28 | 21% |

Subjects without masks get a zero-mask tensor — the model learns to handle both conditioned and unconditioned inputs.

---

## Run History

| Run | Key Changes | Best val_sup | Notes |
|-----|------------|-------------|-------|
| 08 | Boosted CP weight 15→25 | — | Class imbalance fix |
| 09 | — | — | — |
| 10-13 | Various tissue weight, lr tuning | — | Iterating on architecture |
| 14-15 | Tissue labels expanded 30%→83.5% | — | NeSVoR reconstruction campaign |
| 16 | λ_tissue=1.0, focal_gamma=2.0, SURE=0, 3-GPU gangnam | — | First run with expanded labels |
| 17 | Same config as 16, further tuning | **0.0790** | Latest completed run (100 epochs) |
| **18** | **Brain mask FiLM (n_classes=2), no tissue CE, λ_freq=0.1** | **0.0541** | 31.5% over run17 |
| 19 | Tissue 4-class FiLM (predicted), λ_tissue=0.3 | **0.0538** | Marginal gain vs run18 |
| **20** | **On-the-fly 61-deg expansion, SURE warmup, noise map input** | **pending** | **Current — see below** |

### Run17 Final Stats (Completed)
- 100 epochs, ~128s/epoch on gangnam (3× NVIDIA GPUs via DataParallel)
- Final losses: sup≈0.082, tissue≈0.133, total≈0.215
- Best val_sup: **0.0790** (achieved around epoch 50-60)
- Checkpoints: best.pt, epoch_010-100.pt, final.pt
- Visualization outputs at epochs 10, 20, ..., 100

### Run18 Config (Ready to Launch)
```bash
# scripts/launch_run18.sh
--paired_csv train_v2.csv    # Updated manifest with brain_mask_path column
--val_csv    val_v2.csv
--use_brain_mask             # NEW: bypass TissueClassifier, use GT masks
--lambda_tissue 0            # No tissue CE loss (mask is GT, not predicted)
--lambda_sure 0              # SURE still disabled
--lambda_freq 0.1            # NEW: frequency loss for sharpness
--epochs 100 --warmup 5 --batch 16 --lr 1e-4 --workers 8
```

**Code changes for run18 (completed 2026-03-23):**
| File | Change |
|------|--------|
| `src/model/config.py` | Added `use_brain_mask`, `brain_mask_classes=2`, `mask_weighted_loss` flags |
| `src/model/fetenh_net.py` | Added `forward_with_mask()` — converts binary mask to 2-ch one-hot, passes to EnhancementNet; `classifier=None` in mask mode; fixed `param_count()` |
| `src/training/dataset.py` | Added `_load_brain_mask_slice()`, loads mask from `brain_mask_path` column, augments consistently |
| `src/training/trainer.py` | Brain mask training path: passes mask from batch data (not model), skips tissue CE loss |
| `scripts/train.py` | Added `--use_brain_mask`, `--mask_weighted_loss` CLI flags |
| `scripts/launch_run18.sh` | New launch script |

**Run18 training (2026-03-24) — COMPLETED:**
- 972 train pairs, 108 val pairs (after filtering 372 missing files from NFS)
- 609 unpaired LOW slices (SURE disabled, λ_sure=0)
- 3× RTX A5000, ~19s/epoch after warmup, 100 epochs total
- **Best val_sup = 0.0541 at epoch 82 — 31.5% improvement over run17 (0.0790)**

**Evaluation results (test_synthetic, 144 pairs after NFS filtering):**
| Degradation | N | PSNR delta | SSIM delta | Run17 PSNR delta | Run17 SSIM delta |
|-------------|---|-----------|-----------|-----------------|-----------------|
| noise | 24 | **+5.10** | **+0.261** | +3.43 | +0.199 |
| blur | 24 | **+4.04** | **+0.128** | +0.32 | +0.017 |
| bias | 24 | +3.32 | +0.057 | +3.52 | +0.056 |
| mixed_nb | 24 | **+1.63** | **+0.163** | -0.42 | +0.101 |
| mixed_nbs | 24 | +3.43 | **+0.157** | +3.18 | +0.133 |
| slice_corrupt | 24 | -58.72 | -0.011 | -58.46 | -0.021 |
| **ALL** | **144** | **-6.87** | **+0.126** | -8.07 | +0.081 |

**Key improvements over run17:**
- Blur: +4.04 dB vs +0.32 dB (12.6× better)
- Noise: +5.10 dB vs +3.43 dB (49% better)
- Overall SSIM: +0.126 vs +0.081 (55% better)
- mixed_nb: flipped from negative (-0.42) to positive (+1.63)

**Data issues fixed during launch:**
- `ASD_protocol/Data/` paths in manifests don't exist (directory renamed to `ASD/`)
- Additional CHD/Normative files missing from NFS (permissions or deleted)
- Added init-time path validation: `os.path.isfile()` check on clean_path + degraded_path
- Added retry-on-exception in `__getitem__` for robustness

---

### Run20 / Run20a / Run20b — Three-Server Parallel Launch (2026-04-03)

**Goal:** Largest-possible synthetic dataset via on-the-fly degradation + SURE for real subjects. Three simultaneous runs form a free ablation study across the cluster.

#### Dataset (`train_v3.csv` / `val_v3.csv`)
- 265 subjects with valid clean paths (58 dropped — ASD_protocol/Data NFS paths broken)
- 212 train / 53 val subjects (80/20 by subject, seed=42 — no slice leakage)
- 61 degradation configs × 265 subjects = **12,932 manifest rows**
- ~30 brain slices per subject → **~388,000 effective (slice, degradation) training examples**
- On-the-fly generation — no pre-computed degraded NIfTIs needed
- LOW-quality pool: 317 real subjects in `test_real_backup.csv` (separate — SURE only)

#### Degradation grid (61 configs, rationale: dense parameter coverage of all MRI-realistic artifacts)
| Type | Configs | Noise map | Why |
|------|---------|-----------|-----|
| gaussian_noise | σ ∈ {0.02–0.30} ×10 | σ | Baseline additive noise |
| rician_noise | σ ∈ {0.02–0.30} ×10 | σ | MRI-realistic (magnitude image noise) |
| gaussian_blur | σ_blur ∈ {0.5–3.5} ×10 | 0 | Motion/PSF blurring |
| bias_field | order∈{1,2,3} × scale∈{0.2,0.4,0.6} ×9 | 0 | Coil inhomogeneity |
| blur_rician | blur_σ∈{0.8,1.2,1.8,2.5} × noise_σ∈{0.05–0.20} ×16 | noise_σ | Most common real HASTE degradation |
| bias_rician | bias_scale∈{0.2,0.4} × noise_σ∈{0.05,0.10,0.15} ×6 | noise_σ | Coil + noise combined |

**Dropped:** `slice_corrupt` — Run18 showed -58.72 dB (structural artifact, not learnable). Including it hurt the model.

#### Three parallel ablation runs

| Run | Server | GPUs | Epochs | SURE | Batch | Purpose |
|-----|--------|------|--------|------|-------|---------|
| **Run20** | sejong (10.26.66.103) | 0,1,2 | 1000 | warmup ep 51→200, target 0.01 | 48 | **Main** — full SURE, long convergence |
| **Run20a** | busan (10.88.88.2) | 0,1,2 | 300 | disabled | 48 | **Ablation** — isolates dataset expansion alone |
| **Run20b** | gangnam (10.72.8.45) | 0,1 | 300 | warmup ep 21→80, target 0.01 | 32 | **Ablation** — aggressive SURE warmup |

**Why three runs:** No GPU idling. busan and gangnam run supervised-only / early-SURE ablations; sejong runs the full 1000-epoch experiment. Together they answer: "How much of the gain comes from (1) more data alone, (2) SURE alone, (3) schedule?"

#### Model architecture changes (Run20 vs Run18)
- `in_channels` 1 → 2 when `--use_noise_map`: inputs `[degraded_slice, noise_map]`
- `enhancement_net.py` residual: `img[:, :1] + residual` — always 1-ch output regardless of input channels
- `fetenh_net.py`: `forward(x_deg, brain_mask, noise_map)` — noise_map optionally cat'd before encoder
- `config.py`: added `use_noise_map: bool = False`
- **Parameters:** 65,649,665 (same as run18 — noise map adds 0 params, only changes first conv weight shape)

#### Python environment (critical — do not change)
The shared `/neuro/labs/.../environment` Python has CPU-only torch (2.11.0+cpu). The correct environment for all training:
```
/neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/bmex_fetal/bin/python3
PyTorch 2.1.2+cu121, CUDA 12.1, Python 3.10
```
All 3 launch scripts hardcode this path in the `PYTHON=` line.

#### Bugs found and fixed during launch (2026-04-03)
| Bug | Root cause | Fix |
|-----|-----------|-----|
| `--lambda_l1`/`--lambda_ssim` unrecognized args | These flags were never added to `train.py` argparse — `config.py` defaults (0.7/0.3) are used | Removed from all launch scripts |
| `_val_epoch` crashes with `RuntimeError: expected input to have 2 channels, got 1` | `trainer.py:_val_epoch` called `model(deg, brain_mask=mask)` without `noise_map` — model expects 2-ch when `use_noise_map=True` | Patched `_val_epoch` to extract `batch['noise_map']` and forward it |

#### Confirmed launch status (2026-04-03 18:09 EDT)
| Run | Epoch 1 train_sup | Epoch 1 val_sup | s/epoch | Est. completion |
|-----|------------------|-----------------|---------|-----------------|
| Run20 (sejong) | 0.1329 | 0.1095 | 141s | ~39h (1000 ep) |
| Run20a (busan) | 0.1310 | 0.1078 | 135s | ~11h (300 ep) |
| Run20b (gangnam) | 0.1267 | 0.1042 | 182s | ~15h (300 ep) |

GPU utilization confirmed: sejong 68–92%, busan 17–100%, gangnam 87–100%.

#### Code changes for Run20 (2026-04-03)
| File | Change |
|------|--------|
| `scripts/build_expanded_manifest.py` | NEW — builds train_v3.csv/val_v3.csv from all_pairs.csv × 61 configs; merges brain_mask_path from train_v2.csv |
| `src/training/dataset.py` | Added `apply_degradation()` (6 types), `_make_bias_field()`, `OnTheFlyPairedDataset` |
| `src/model/fetenh_net.py` | `use_noise_map` → `in_channels=2`; `forward()` cats noise_map |
| `src/model/enhancement_net.py` | Fixed residual: `img[:, :1] + residual` (always 1-ch output) |
| `src/model/config.py` | Added `use_noise_map: bool = False` |
| `src/training/trainer.py` | SURE warmup schedule; `_val_epoch` fix (noise_map passed); `_train_epoch` passes noise_map |
| `src/utils/noise_estimator.py` | NEW — background-std + MP-PCA noise estimation for real subjects |
| `scripts/train.py` | Added `--use_onthefly`, `--use_noise_map`, `--lambda_sure_target/warmup_start/end` |
| `scripts/launch_run20_sejong.sh` | NEW — 1000ep, SURE warmup ep 51→200 |
| `scripts/launch_run20a_busan.sh` | NEW — 300ep, SURE disabled (supervised ablation) |
| `scripts/launch_run20b_gangnam.sh` | NEW — 300ep, SURE warmup ep 21→80 (aggressive) |

**Logs:** `logs/run20_sejong.log`, `logs/run20a_busan.log`, `logs/run20b_gangnam.log`

---

## Current Direction (2026-03-24)

### Track 1: Brain Mask Enhancement (Run18) — COMPLETED
Per Kiho's feedback on March 17 meeting minutes (email March 21):
- **Use existing ground truth brain masks as FiLM conditioning NOW**
- Brain mask FiLM (2-class) significantly outperforms tissue map FiLM (4-class)
- val_sup improved 31.5%, SSIM improved 55%, blur improved 12.6×

**Status:** Training complete. Eval complete. Results ready for presentation.

**Run18 vs Run17 summary:**
| Metric | Run18 (brain mask) | Run17 (tissue map) |
|--------|-------------------|-------------------|
| val_sup (best) | **0.0541** | 0.0790 |
| Overall SSIM delta | **+0.126** | +0.081 |
| Parameters | 65.6M | 67.6M |
| Conditioning | 2-class brain mask (GT) | 4-class tissue (predicted) |

### Track 2: NeSVoR Inverse Transform — FIRST TEST COMPLETED
Per Kiho's email exchange with Margherita Firenze (NeSVoR author, MIT) on 2026-03-23:
- Kiho asked Margherita how to extract per-slice transformation matrices from NeSVoR
- Margherita confirmed: use `--simulated-slices <folder>` to save extracted slices with affine matrices
- Stack-level transforms are harder — would need NeSVoR source modification
- Kiho asked Yair and Daniel to try this approach

**Status (2026-03-24):** First test completed on FCB080.
- Ran NeSVoR `reconstruct` with `--simulated-slices` on 15 T2_HASTE stacks + brain masks
- **Runtime:** 344s (5.7 min) on single RTX A5000
- **Output:** 400 simulated slices, each with unique 4×4 affine matrix
- **Reconstruction:** 94×110×94 at 0.8mm isotropic
- Affine matrices encode motion-corrected slice→world transforms in RAS+ space
- Label projection formula: `vol_voxels = inv(vol_affine) @ slice_affine @ slice_voxels`
- Full results at: `experiments/nesvor_simslices/FCB080/`
- See [[050-Knowledge/NeSVoR]] for detailed documentation

**Next steps:**
1. Write label projection script (use Python + nibabel)
2. Segment the reconstruction volume (run iBEAT or use manual segmentation)
3. Project labels back to raw slices via the affine chain
4. Validate alignment visually vs existing brain masks
5. If accurate, batch all training subjects

### Track 3: Yair's Brain Masking Model — LOWER PRIORITY
- Yair developing a classification model based on masking (from literature review)
- Goal: brain masking model that works reliably on low-quality images
- Lower priority per Kiho (we already have GT masks for most subjects)

### Open Problems
- **NFS file accessibility:** 28% of training manifest rows point to missing/inaccessible files on mri.team NFS
- **Inverse transform chain:** Per-slice affines obtained; need to complete label projection pipeline
- **Interpolation problem:** Raw stack slice spacing/orientation doesn't match reconstructed volume grid — nearest-neighbor may suffice for coarse labels
- **SURE loss:** Currently disabled (was "broken" per run16 notes — NeSVoR reconstruction errors)

---

## Key Configs

```python
# FetEnhNetConfig defaults
lr = 1e-4, weight_decay = 1e-5
lambda_l1 = 0.7, lambda_ssim = 0.3
lambda_freq = 0.0           # 0.1 in run18
lambda_tissue = 0.5          # 0 in run18 (mask mode)
lambda_sure = 0.1            # 0 in runs 16-18
sure_sigma = 0.15
focal_gamma = 0.0            # 2.0 in run16/17
batch_size = 16, total_epochs = 100
warmup_epochs = 5            # 10 in run16

# Brain mask mode (run18+)
use_brain_mask = True        # bypass TissueClassifier
brain_mask_classes = 2       # [background, brain] one-hot
mask_weighted_loss = False   # loss only inside brain region (optional)
```

## Environment

```bash
# Python environment (micromamba doesn't work in non-interactive SSH)
PYTHON=/neuro/labs/grantlab/research/MRI_processing/environment/bin/python3

# Interactive shell
eval "$(micromamba shell hook --shell bash)"
micromamba activate /neuro/labs/grantlab/research/MRI_processing/environment

# Launch training
cd /neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net
bash scripts/launch_run18.sh

# Monitor
tail -f checkpoints/run18_launch.log
```

## NeSVoR Slice-to-Volume Transform (Parallel Work)

Per Kiho's email exchange with Margherita Firenze (MIT, NeSVoR author) on 2026-03-23.
See [[050-Knowledge/NeSVoR]] for full NeSVoR documentation.

### FCB080 Test Results (2026-03-24)
- **Test dir:** `experiments/nesvor_simslices/FCB080/`
- **Outputs:** `recon.nii.gz` (94×110×94 @ 0.8mm), `model.pt`, `simulated_slices/` (400 NIfTI files)
- Each simulated slice: `(256, 256, 1)` with unique 4×4 affine matrix
- Affine encodes motion-corrected slice pose in RAS+ world coordinates
- Reconstruction and slices share the same world coordinate space

### Label Projection Pipeline (to implement)
```python
import nibabel as nib
import numpy as np

# 1. Load segmented reconstruction volume
vol = nib.load('labels_volume.nii.gz')
vol_data, vol_affine = vol.get_fdata(), vol.affine

# 2. For each simulated slice:
sl = nib.load('simulated_slices/42.nii.gz')
sl_affine, sl_shape = sl.affine, sl.shape

# 3. Build voxel grid → world → volume voxel mapping
i, j = np.meshgrid(np.arange(sl_shape[0]), np.arange(sl_shape[1]), indexing='ij')
voxels = np.stack([i.ravel(), j.ravel(), np.zeros_like(i.ravel()), np.ones_like(i.ravel())])
vol_voxels = np.linalg.inv(vol_affine) @ sl_affine @ voxels

# 4. Sample labels (nearest neighbor)
vi = np.clip(np.round(vol_voxels[0]).astype(int), 0, vol_data.shape[0]-1)
vj = np.clip(np.round(vol_voxels[1]).astype(int), 0, vol_data.shape[1]-1)
vk = np.clip(np.round(vol_voxels[2]).astype(int), 0, vol_data.shape[2]-1)
slice_labels = vol_data[vi, vj, vk].reshape(sl_shape[:2])
```

### NeSVoR on Cluster
- **Container:** `/neuro/labs/grantlab/research/Apptainer/nesvor:v0.6.0rc2.sif`
- **Pipeline wrapper:** `tools/seg_pipeline/src/segmentation/core/reconstruction.py`
- **Docs:** https://nesvor.readthedocs.io/en/latest/

## Label Projection Alignment — Known Limitations

Analysis of why projected tissue labels on raw HASTE slices are sometimes elongated, rotated, or spatially offset (observed 2026-04-03 during batch gallery generation for all 48 training subjects).

### 1. NeSVoR Pose Estimation Error (fundamental, irreducible)
NeSVoR jointly optimizes slice poses and the 3D reconstruction. Its estimated pose for slice `i` is approximate — not the true scanner geometry. The projected label is correct relative to the *estimated* pose, but the actual raw slice was acquired at the true (slightly different) pose. This is the core irreducible error and cannot be removed without perfect motion correction.

### 2. Pixel Spacing Mismatch (causes elongation — most fixable)
The projected label is rendered in NeSVoR's internal isotropic coordinate frame (e.g., 0.8mm³). The raw HASTE stack has its own pixel spacing (e.g., 1.09×1.09mm in-plane). When both are displayed as raw pixel grids without accounting for physical voxel sizes, shapes distort — a round brain in physical space appears elongated. **Fix:** resample both raw slice and projected label to a common physical coordinate space (e.g., 1mm isotropic) before display.

### 3. Stack Orientation vs Projected Label Orientation (causes rotation)
HASTE stacks are acquired in oblique orientations. The projected label geometry reflects NeSVoR's internal reconstruction coordinate system. When displaying `raw_vol[:,:,z]` in pixel space (acquisition frame) vs the label in NeSVoR's frame, obliquity mismatches appear as rotation.

### 4. Simulated Slice ≠ Raw Slice Content
NeSVoR's simulated slice is a synthetic rendering from its 3D model at the estimated pose, not the actual raw signal. The raw slice has noise, motion ghosts, bias field, and signal intensity that the model only partially captures. The projected label is correct relative to the synthetic rendering, which is itself an approximation.

### 5. Partial Volume / Thick-Slice Averaging
Raw HASTE slices are typically 3–5mm thick. The 3D segmentation has fine-grained tissue boundaries. When projected onto a thick slice, the label averages across multiple tissue types at slice boundaries — edge regions are inherently ambiguous.

### 6. Tissue Label Quality
Labels come from NeSVoR reconstructions which have their own artifacts, especially for low-quality subjects. Inaccurate labels in reconstruction space propagate directly to inaccurate projected labels.

### Implication for Training
For brain-region FiLM conditioning (Run18+), the current alignment quality is sufficient — the labels correctly identify the fetal brain region. For tissue-level conditioning (Run19+, 4-class FiLM), the residual distortion from issues 1–3 may degrade conditioning accuracy, especially for thin structures like cortical plate. The most impactful fix before Run20 would be correcting pixel spacing during overlay and projection (issue #2).

---

## Other Projects on Same Server

| Project | Path | Description |
|---------|------|-------------|
| activ_sparse_slm | `projects/activ_sparse_slm/` | Activation-sparse small language model (15 config versions, v11-v15 latest) |
| bme-x/fetal_enhancement | `repos/bme-x/fetal_enhancement/` | 65+ scripts for fetal BME-X adaptation, batch processing, cohort visualization |
| FetalSynthSeg | `repos/FetalSynthSeg/` | Fetal segmentation model (configs, src, weights) |
| iguane_harmonization | `repos/iguane_harmonization/` | IGUANE 2D harmonization experiments |

## Related Notes
- [[BCH-Meeting-Minutes]] — Weekly meeting minutes with Kiho's group
