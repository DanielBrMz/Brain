---
title: "FetEnhNet — Label Projection Pipeline (Registration-Based)"
type: reference
status: superseded
created: 2026-04-09
updated: 2026-04-21
tags: [project, research, bch, fetal-mri, alignment, segmentation, nesvor]
---

# FetEnhNet — Manual Segmentation → Raw Stack Overlay Pipeline (Registration-Based)

> **SUPERSEDED 2026-04-21** by [[fetenh-inverse-alignment-pipeline|Inverse Alignment Pipeline]] which uses NeSVoR's own geometry (100% success, zero registration error) instead of binary brain shape registration (73% success, Dice >= 0.80).

> How to project manual tissue segmentations from atlas space onto raw HASTE stack slices.
> Debugged 2026-04-09/10 on subject FCB033. **SOLVED 2026-04-10 — Dice 0.8985.**

---

## Problem

We need tissue labels on raw HASTE stack slices for FiLM conditioning visualization and presentation figures. Manual segmentations (`segmentation_to31_final.nii`) live in the 31-week atlas space. Raw stacks live in scanner space. Getting labels from one to the other requires a chain of transforms.

---

## Pipeline Steps

### Step 1 — Raw HASTE Stack (scanner input)
- Individual 2D HASTE slices acquired during fetal MRI scan
- Each stack is a 3D NIfTI where z-slices are independently acquired 2D images
- Located: `<subject>/<session>/raw/*.nii`

### Step 2 — Volume Reconstructions (THREE separate coordinate systems!)

| Reconstruction | File | Resolution | Coordinate System |
|---|---|---|---|
| Pipeline recon | `recon_segmentation/recon.nii` | 0.5 mm iso | **Pipeline's own frame** (NOT scanner coords!) |
| Atlas recon | `recon_segmentation/recon_to31_nuc.nii` | 0.5 mm iso | 31-week atlas space |
| NeSVoR recon | `nesvor_simslices/<subject>/recon.nii.gz` | 0.8 mm iso | NeSVoR's atlas-aligned frame |

**Critical discovery (2026-04-09):** The pipeline recon (`recon.nii`) is **NOT in scanner coordinates**. Checkerboard comparison between pipeline recon resampled into raw stack grid shows mismatched anatomy — coronal brain in raw blocks, sagittal in recon blocks. The pipeline reconstruction process creates its own coordinate frame.

### Step 3 — Atlas Space (perfect alignment) ✅
- `recon_to31_nuc.nii` and `segmentation_to31_final.nii` share the same affine → perfect overlay
- Labels: 1/42 → cortical plate, 160/161 → WM/subplate, 18 → CSF

### Step 4 — Seg in NeSVoR Space (SimpleITK registration) ✅
- Register NeSVoR recon → atlas `recon_to31_nuc.nii` using SimpleITK affine
- Inverse-resample seg into NeSVoR space
- **Verified correct** — labels align with NeSVoR recon anatomy
- Transform saved: `presentation/debug_overlay_FCB033/nesvor_to_atlas_tx.tfm`

### Step 5 — Labels on Simulated Slices ✅
- Project `seg_in_nesvor` onto each sim-slice using `inv(A_nesvor) @ A_simslice`
- **Verified correct** — labels align with sim-slice anatomy
- 661/686 sim-slices have brain label content

### Step 6 — Labels on Raw HASTE Slices ✅ SOLVED (Dice 0.8985)

**WORKING SOLUTION (2026-04-10):**

```
atlas seg → (inv binary-brain-reg TX) → scanner-NeSVoR space → flip_k → (inv_A_nesvor @ A_raw) → raw voxels
```

**Step 6 implementation:**
1. Load saved transform: `scanner_nesvor_to_atlas_tx.tfm` (binary brain shape registration)
2. Inverse-resample atlas seg into scanner-NeSVoR space (nearest-neighbor)
3. Apply `flip_k` correction: `seg_in_nesvor[:,:,::-1]` — fixes 180° rotation ambiguity from binary brain registration
4. For each raw stack: compute `T = inv(A_nesvor) @ A_raw`, meshgrid raw voxels, map through T, sample `seg_in_nesvor` via `map_coordinates(order=0)`
5. Mask out-of-bounds voxels (outside NeSVoR FOV)

**Results across all 20 raw stacks:**

| Stack type | Dice range |
|---|---|
| `T2_HASTE_for_SVS__ax_to_fetal_brain` (best) | **0.8985** |
| `CERVIX_T2_HASTE_fullFOV` | 0.862–0.884 |
| `T2_HASTE_CAT4_lowSAR` | 0.845–0.865 |
| `T2_HASTE_CAT4_lowSAR_S14_ND` | 0.865 |

**Why flip_k?** The binary brain registration finds a rotationally-ambiguous solution because the brain is roughly symmetric. It correctly places the seg but rotates it 180° in k. The flip recovers the correct orientation.

**Historical failures:**

| # | Approach | Dice | Issue |
|---|----------|------|-------|
| 1 | `recon_to31.xfm` applied to NeSVoR coords | — | Wrong XFM (12mm z-offset) |
| 2 | Direct affine (raw→NeSVoR world) | — | NeSVoR world ≠ scanner world |
| 3 | Cumulative index (sim-slice i → raw slice i) | — | Pixel grids differ |
| 4 | Direct voxel mapping (raw→default-NeSVoR) | — | Different coord systems |
| 5–9 | nibabel/XFM/mask-guided registration | 0.22–0.90 | Wrong anatomical view |
| 10–13 | Pipeline recon chain, 2D per-slice | 0.036–0.594 | Pipeline NOT in scanner coords |
| 14 | Binary brain shape registration, no flip | ~0.89 | Correct position, 180° rotated |

**Root cause (resolved):** The scanner-space NeSVoR re-run (`--scanner-space` flag) put the NeSVoR recon in scanner coordinates. Binary brain registration bridged atlas ↔ scanner-NeSVoR. `flip_k` resolved the rotational ambiguity. Direct voxel mapping then works because both are in scanner coords.

---

## NeSVoR Coordinate System (researched from source code)

1. **NeSVoR uses its own atlas-aligned frame** — SVoRT zeros out scanner rotation: `transform_ax[:, :-1] = 0`
2. **Simulated slices are in NeSVoR frame** — resampled to 1mm, motion-corrected orientations
3. **1:1 cumulative index** between sim-slices and input raw slices exists, but pixel grids differ
4. **`--scanner-space` flag** would keep outputs in scanner coords — was NOT used for FCB033

---

## Next Steps

1. **Batch process all 15 subjects with manual segs**
   - Re-run NeSVoR with `--scanner-space` for each subject (FCB005, FCB014, FCB018, FCB033✅, FCB040, FCB056, FCB068, FCB094, FCB105, FCB160, FCB193, FCB215, FCB242, 5437158, 5761642)
   - For each subject: run binary brain registration, apply flip_k, generate step4/6 outputs
   - Script: `/tmp/final_pipeline_flipk.py` — parameterize by subject

2. **Validate flip_k generalization**
   - flip_k was chosen visually for FCB033 — need to confirm same flip works for all subjects
   - If not, may need per-subject flip test or a more principled orientation fix

3. **Integration into FetEnhNet training pipeline**
   - These projected labels are the FiLM conditioning target for visualization
   - Feed step 6 outputs into the presentation figure pipeline

---

## Debug Gallery (FCB033)

```
.../projects/fetenh_net/presentation/debug_overlay_FCB033/
├── step1_raw_haste.png                # Raw HASTE input
├── step2_reconstructions.png          # Pipeline recon vs NeSVoR recon (checkerboard)
├── step3_atlas_space.png              # Atlas overlay (PERFECT)
├── step4_nesvor_seg_overlay.png       # Seg in scanner-NeSVoR space, flip_k ✅
├── step5_simslice_projection.png      # Labels on NeSVoR sim-slices ✅
├── step6_raw_overlay.png              # Seg on raw HASTE — diagnostic 5-col ✅ Dice=0.8985
├── step6_clean.png                    # Seg on raw HASTE — clean 3-col overlay ✅
├── flip_test_3d.png                   # 8 flip combinations (user chose flip_k = #3)
└── scanner_nesvor_to_atlas_tx.tfm     # Binary brain shape registration transform (KEY FILE)
```

## Working Scripts

All scripts persisted at `.../fetenh_net/scripts/` on sejong:

| Script | Purpose |
|--------|---------|
| `final_pipeline_flipk.py` | **FINAL WORKING SCRIPT** — full pipeline with flip_k |
| `numpy_chain.py` | Binary brain shape registration (generates the TX) |
| `flip_seg.py` | 8-flip visual test that determined flip_k |
| `chain_old_new.py` | Two-stage registration via old atlas-aligned NeSVoR (deprecated) |
| `fix_step4_scanner.py` | Multi-strategy registration sweep (deprecated) |
| `direct_scanner.py` | Direct scanner-space mapping (intermediate approach) |

---

## Key Lessons

| Lesson | Detail |
|--------|--------|
| Pipeline recon ≠ scanner coords | Confirmed via checkerboard — sagittal output for coronal raw input |
| NeSVoR default ≠ scanner coords | SVoRT zeros scanner rotation → direct voxel mapping fails |
| `--scanner-space` flag is essential | Re-run NeSVoR with this flag to get scanner-aligned recon |
| Binary brain shape reg > intensity reg | Intensity MI fails when coordinate frames differ by >30°; shape is rotation-invariant |
| flip_k required | Symmetric brain → binary reg finds two valid solutions differing by 180° k-flip |
| Seg looks coarser on raw stacks | Resolution chain: 0.5mm atlas → 0.8mm NeSVoR → 3mm raw; NN interpolation at each step — not a bug |
| Best stack ≠ most common stack | `T2_HASTE_for_SVS__ax_to_fetal_brain` has tightest brain FOV → highest Dice |

---

## Manual Seg Availability

15/78 subjects have `segmentation_to31_final.nii`:
- CHD: FCB005, FCB014, FCB018, FCB033, FCB040, FCB056, FCB068, FCB094, FCB105, FCB160, FCB193, FCB215, FCB242
- ASD: 5437158, 5761642

---

## Related Notes

- [[fetenh-net|FetEnhNet — Main Project]]
- [[FetEnhNet-Run21-Plan|Run21 Plan]]
- [[BCH-Meeting-2026-04-07|Apr 7 Meeting — alignment feedback]]
- [[medical-image-registration|Medical Image Registration — Theory and Practice]] — deep dive on why classical registration fails for cross-subject fetal MRI and how SynthMorph solves it
