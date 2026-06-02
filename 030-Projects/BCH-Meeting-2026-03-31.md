---
title: "FetEnhNet — March 31 Meeting Notes"
type: meeting
created: 2026-03-31
updated: 2026-03-31 (post-meeting update)
tags: [bch, fetenh-net, meeting, sure, tissue-labels, run19]
---

# FetEnhNet — March 31 Meeting

> Weekly with Kiho Im's group, FNNDSC / Boston Children's Hospital.

---

## 1. Progress Since March 24

### Tissue Label Projection — **157 subjects (rawstack mode)**

Post-meeting update: original 49-subject NeSVoR simslice approach had a fundamental geometry error discovered after the meeting.

**Root cause of misalignment (found post-meeting):** NeSVoR takes multiple HASTE stacks as input and generates one simulated slice per input slice across ALL stacks (~847 per subject). The simulated slice affines are completely different from the manifest's `clean_path` raw HASTE stack (256×256×66). The 770mm origin offset confirmed they live in different spaces — projected labels were not aligned with the actual training images.

**Fix: `--rawstack` mode added to `project_labels.py`.** Derives per-slice affine directly from the 3D raw HASTE stack affine:
```
sl_affine = stack_affine.copy()
sl_affine[:3, 3] = (stack_affine @ [0, 0, z, 1])[:3]  # origin shifts per z
```

This guarantees labels are in exact raw HASTE space. Alignment confirmed visually across all 4 protocols.

**New batch:** `experiments/projected_labels_rawstack/` — **157 subjects** (all with valid labels in manifest), **4 parallel workers, running on sejong**. Covers far more subjects than NeSVoR approach (was limited to 67 subjects with reconstructions).

**Key insight (diagram in `presentation/label_projection_pipeline.png`):**

```
Raw HASTE stack → NeSVoR reconstruction → manual/auto segmentation
        │                                            ↓
        │                          project_labels.py --rawstack (per-z affine)
        │                                            ↓
        └──────────────── Tissue labels in raw HASTE space ← TRAINING GT
```

Figures: `presentation/label_projection_pipeline.png` and `presentation/label_projection_gallery.png` now show actual raw HASTE images (noisy, full FOV including mother tissue) with tissue labels aligned directly on the fetal brain.

---

## 2. Why Run18 Noise Performance is Limited — SURE Diagnosis

Run18 training log showed `sure=0.0000` for all 100 epochs, meaning **SURE was never active** despite unpaired LOW data being loaded (609 real slices).

### Root Cause: Wrong SURE Formulation

Our prior implementation used a simplified scalar-σ formulation (Metzler 2018):
```
SURE = ||f(y)||² - 2σ²·div(f)(y)
```

This has two critical problems confirmed by Pfaff 2023 Fig. 5:
- **Scalar σ is wrong** for spatially variant HASTE noise — using averaged σ causes SURE to diverge (loss goes negative, training collapses)
- **Wrong fidelity term** — `||f(y)||²` instead of `||f(y)-y||²`

### Fix Applied (losses.py) — Pfaff 2023 Eq. 5–6

New formulation:
```
L_SURE = (1/D)(||f(y)-y||² - Σ_d σ_d² + 2·div_y(σ²⊙f(y)))

MC divergence (Eq. 6):
div_y(σ²⊙f(y)) ≈ b^T·(σ²⊙(f(y+εb)-f(y))/ε)   b~N(0,I)
```

Key properties:
- Per-pixel σ_map (B×1×H×W) replaces scalar σ
- Fidelity measures distance to noisy input, not output norm
- Divergence scaled by per-pixel σ² via element-wise multiply
- Falls back to scalar σ if no map provided (backward compat)

### Noise Map Generation Plan

For SURE to work, σ_map must match actual noise:

| Degradation type | σ_map source |
|-----------------|--------------|
| `noise` | Known σ from degradation params (uniform map) |
| `mixed_nb` | σ_base × bias_field_proxy (spatially variant) |
| `blur`, `bias` | Zero map (no additive noise, SURE skipped) |
| Real LOW stacks | Background statistics: Dietrich method with Rayleigh correction |

Script: `scripts/generate_noise_maps.py` — generates per-subject σ maps and adds `noise_map_path` column to manifests.

---

## 3. Run19 Plan

Builds on Run18 (brain mask baseline, val_sup=0.0541) with two additions:

### Track A: Tissue-Conditioned FiLM (vs Run18 brain mask)
- Use projected tissue labels (49 subjects, 4-class) as FiLM conditioning
- Same architecture as Run18 but `--lambda_tissue 0.5` active
- Tells us definitively: does proper tissue conditioning beat simple brain mask?

### Track B: SURE with Noise Maps (denoising focus)
- Start from Run18 best.pt (warm start)
- Enable SURE with generated σ maps on real LOW subjects
- `--lambda_sure 0.01` (conservative — calibrate up if stable)
- Targets: improve noise ΔPSNR beyond Run18's +5.10 dB

### Track C (if time): Tissue + SURE combined
- Once both tracks are stable, combine for Run20

**Launch command (Track A):**
```bash
micromamba activate bmex_fetal
cd $FNET
CUDA_VISIBLE_DEVICES=0,1,2 nohup python scripts/train.py \
  --paired_csv experiments/2024_2026_degradation_study/training_data/manifests/train_v2.csv \
  --out_dir checkpoints/run19 \
  --epochs 100 --batch 16 \
  --lambda_tissue 0.5 --lambda_sure 0.0 \
  --focal_gamma 2.0 \
  > logs/run19_launch.log 2>&1 &
```

**Post-meeting — dataset.py updated:** `_get_projected_labels_dir()` now checks `projected_labels_rawstack/{protocol}_{subject_id}/` first (correct geometry), falls back to legacy simslice dir, then `tissue_label_path` stack volume. Training will automatically use the correct per-slice rawstack projections as they complete.

---

## 4. Figures

- `presentation/label_projection_pipeline.png` — FCB003 pipeline: recon → 3D seg → raw HASTE slice + projected labels
- `presentation/label_projection_gallery.png` — CHD (FCB010, FCB003), ASD (5496460), Placenta (5536532) on actual raw HASTE images

---

## 5. Post-Meeting Status

| Item | Status |
|------|--------|
| `project_labels.py` rawstack fix | ✅ deployed |
| `dataset.py` rawstack proj priority | ✅ deployed |
| `losses.py` Pfaff 2023 SURE fix | ✅ deployed |
| `generate_noise_maps.py` | ✅ deployed, **running → `train_v2_noise.csv`** |
| Rawstack projection batch (157 subj) | ✅ **complete** — all 157 subjects in `projected_labels_rawstack/` |
| Run19 Track A | ✅ **complete** — 100 epochs, **best val_sup = 0.0538** (vs Run18: 0.0541) |

## 6. Next Steps

- [x] Rawstack batch complete — 157 subjects in `projected_labels_rawstack/`
- [x] Run19 Track A complete — best val_sup=0.0538, saved at `checkpoints/run19/best.pt`
- [ ] Check generate_noise_maps.py completion → `train_v2_noise.csv`
- [ ] Analyze Run19 per-degradation metrics vs Run18 — does tissue conditioning help?
- [ ] Launch Run19 Track B (SURE + noise maps) using `train_v2_noise.csv`
- [ ] Calibrate SURE λ on a smoke test before full Run19+SURE
- [ ] Symposium slides update — **deadline April 3**
- [ ] Puentes demo video — **deadline April 3**

---

## Related

- [[fetenh-net|FetEnhNet Project Note]]
- [[fetenh-net-codebase|Codebase Documentation]]
- [[BCH-Email-2026-03-24|March 24 Meeting Minutes]]
