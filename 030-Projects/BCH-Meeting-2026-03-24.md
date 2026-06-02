---
tags:
  - bch
  - meeting-prep
  - fetenh-net
---

# FetEnhNet Progress Update - March 24, 2026

## 1. Brain Mask Conditioning (Run18) - Completed

Replaced the 4-class tissue map FiLM conditioning with 2-class brain mask FiLM conditioning. Brain masks are already available in raw stack space so no inverse transform is needed for this approach.

Run18 trained for 100 epochs on sejong (3x RTX A5000). Best validation loss at epoch 82.

| Metric | Run17 (Tissue, 4-class) | Run18 (Brain Mask, 2-class) |
|--------|------------------------|-------------------------------|
| Best val_sup | 0.0790 | 0.0541 (31.5% lower) |
| Blur PSNR gain | +0.32 dB | +4.04 dB |
| Noise PSNR gain | +3.43 dB | +5.10 dB |
| Overall SSIM gain | +0.081 | +0.126 |

The tissue conditioning in run17 underperformed because the tissue labels were not accurately projected onto the raw stacks. The brain mask approach bypasses that problem entirely and sets a strong baseline.

### Synthetic Test Results (Run17 vs Run18)

![[fig_synthetic_run17_vs_run18.png]]

10 test pairs across 5 degradation types. Each row shows: degraded input, run17 enhanced, run18 enhanced, clean ground truth, and error map.

### Real Low-Quality Subject Gallery (Run18)

![[fig_run18_real_gallery.png]]

24 real low-quality subjects from the test set. Each pair shows the original input and the run18 enhanced output. These are not cherry-picked.

### Run17 vs Run18 on Real Data

![[fig_real_run17_vs_run18.png]]

8 real low-quality subjects comparing run17 and run18 enhancement side by side.

---

## 2. NeSVoR Inverse Transform Pipeline - In Progress

The goal is to get accurate tissue labels projected onto raw stack slices using NeSVoR's per-slice affine transforms. This would allow proper tissue-level FiLM conditioning in future runs.

### What was done

1. Ran NeSVoR with `--simulated-slices` on FCB080 as a test case. Each output slice has a unique 4x4 affine matrix encoding its motion-corrected pose in world space.

2. Wrote `project_labels.py` to project reconstruction volume data back to individual slice coordinates using the formula: `vol_voxels = inv(vol_affine) @ slice_affine @ slice_voxels`

3. Validated the projection visually. The projected intensity aligns well with the brain region in the simulated slices.

4. Launched batch processing across all 77 training subjects with raw stacks and brain masks. Running on 3 GPUs, roughly 5 minutes per subject. As of writing, 25+ CHD subjects are complete.

### Projection Validation (8 subjects)

![[fig_nesvor_compact_validation.png]]

Columns: simulated slice from NeSVoR, projected reconstruction intensity, overlay (green = projected region), and brain region zoom. The projection aligns consistently across subjects.

### Next Steps

- Finish batch processing (remaining subjects across ASD, Placenta, Normative protocols)
- Project actual tissue segmentation labels (not just intensity) using the same affine transforms
- Train a new run with properly projected tissue labels as FiLM conditioning
- Compare against run18 brain mask results to see if tissue-level conditioning adds value when done correctly
