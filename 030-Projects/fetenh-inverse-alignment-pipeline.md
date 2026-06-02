---
title: "FetEnhNet — Inverse Alignment Pipeline"
type: reference
status: active
created: 2026-04-21
updated: 2026-04-21
tags: [project, research, bch, fetal-mri, alignment, segmentation, nesvor, inverse-alignment]
---

# Inverse Alignment Pipeline: Atlas Segmentation → Raw HASTE Stack Space

> Built by Yair Beltran (Apr 20-21, 2026). Tested on 1 subject (MR-Fetal_Neuro_Indications-23047787-20140428). Replaces the registration-based `project_labels.py` approach.

---

## Why This Exists

FetEnhNet needs per-pixel tissue labels on raw HASTE slices for FiLM conditioning. Previous approach used binary brain shape registration (73% success, Dice >= 0.80 on 25/43 subjects). This pipeline uses NeSVoR's own slice geometry instead — **zero registration error, 100% success rate**.

---

## Prerequisite: NeSVoR with `--extract-slice-transforms`

The entire pipeline depends on NeSVoR producing simulated slices with per-slice affines and a provenance file. Run via the updated `seg_pipeline/cli.py`:

```bash
python3 /neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py \
  --from_recon --extract-slice-transforms -i /path/to/subject/
```

This adds three args to `nesvor reconstruct`:
- `--seed 42` — reproducible reconstruction
- `--simulated-slices recon_segmentation/simulated_slices/` — 2D NIfTIs with spatial affines
- `--output-provenance recon_segmentation/provenance.json` — slice→stack mapping

**Outputs:**
- `simulated_slices/0.nii.gz` ... `N.nii.gz` — re-simulated 2D slices, each with a 4x4 affine
- `provenance.json` — N-entry array: `{stack_name, stack_index, source_slice_index, transform_axisangle}`

---

## 4-Step Pipeline

### Step 1: Atlas → Native Space

Inverse-register atlas segmentation back to native reconstruction space.

```bash
apptainer exec \
  --bind $(pwd):/data \
  /neuro/labs/grantlab/research/Apptainer/fsl:6.0.5.1-cuda9.1.sif \
  flirt -in /data/recon_to31_nuc_deep_agg.nii \
        -ref /data/recon.nii \
        -init /data/alignment_temp/recon_to31_inv.xfm \
        -applyxfm \
        -interp nearestneighbour \
        -out /data/segmentation_native.nii
```

**Key:** `-interp nearestneighbour` preserves discrete label values.

### Step 2: Native → Simulated Slice Space

**Script:** `resample_to_raw_space.py`

Resamples 3D native segmentation into each NeSVoR simulated slice's 2D voxel space using the affine stored in each `simulated_slices/NNN.nii.gz`.

- Uses `recon.nii` affine as reference (not `segmentation_native` — fixes small FSL flirt origin offset)
- NIfTI convention: `[i, j, k, 1]` = `[y, x, z, 1]` (row, col, slice)
- Nearest-neighbor interpolation for categorical labels

**Output:** `segmentation_raw_slices/seg_raw_NNNN.nii.gz` (1478 2D label images for test subject)

### Step 3: Simulated Slices → Stack Space

**Script:** `map_to_stacks.py`

Uses `provenance.json` to reassemble 2D slices into 3D volumes matching each input stack's geometry.

- Groups provenance entries by `stack_index`
- Loads source stack from `best_images_crop/` for shape + affine
- Handles determinant-based flip: `if det(affine) < 0: flipud(slice)`
- Pads smaller simulated slices into target stack dimensions

**Output per stack in `stack_space/`:**
- `stack_XX_raw.nii.gz` — symlink to source stack
- `stack_XX_simulated.nii.gz` — NeSVoR simulated slices in stack geometry
- `stack_XX_segmentation.nii.gz` — segmentation in stack geometry

**Note:** `LOCAL_STACK_DIR` in `map_to_stacks.py` is hardcoded to Yair's local path. Must be updated per-user.

### Step 4: Crop Stack → Raw HASTE Space (stacks 18-35 only)

**Script:** `resample_to_rawhaste.py`

Resamples crop-space segmentations into full 256x256xN raw HASTE geometry.

**Critical bug fix:** `auto_crop_image()` in `fetal_segmentation_pipeline/src/helper_functions.py` pads by `[50, 50, 16]` voxels before bbox detection but uses the **unpadded** affine for origin. Corrected:
```python
PAD = np.array([50, 50, 16])
corrected_affine[:3, 3] = seg_img.affine[:3, 3] + seg_img.affine[:3, :3] @ (-PAD)
```

Brain mask applied after resampling to remove boundary artifacts.

**Output:** `stack_space/stack_XX_seg_rawhaste.nii.gz` (uint8 labels in raw HASTE space)

---

## Output Summary

| Stack range | Source type | Use this file |
|---|---|---|
| 00-17 | `_brain.nii` (full FOV = raw) | `stack_XX_segmentation.nii.gz` |
| 18-35 | `_brain_crop.nii.gz` (cropped) | `stack_XX_seg_rawhaste.nii.gz` |

All label files: uint8. Labels: `[1, 18, 42, 160, 161]` (FeTA tissue classes).

---

## Test Subject Results (Apr 21)

- 36/36 stacks processed
- 1478 simulated slices
- All 5 tissue labels preserved
- Consistent ~140k labeled voxels per stack (lower for body-coil stacks 14-17, 32-35)
- Tissue proportions balanced between brain and crop→raw stacks

---

## File Tree (test subject)

```
recon_segmentation/
├── recon.nii                          # NeSVoR reconstruction (native space)
├── recon_to31_nuc_deep_agg.nii        # Segmentation (atlas space) — Step 1 input
├── segmentation_native.nii.gz         # Step 1 output
├── segmentation_raw_slices/           # Step 2 output (1478 2D label images)
├── simulated_slices/                  # NeSVoR simulated slices (with spatial affines)
├── provenance.json                    # NeSVoR provenance: slice→stack mapping
├── stack_space/                       # Steps 3 & 4 outputs
│   ├── stack_XX_raw.nii.gz            # Symlink to source input stack
│   ├── stack_XX_simulated.nii.gz      # Simulated slices in stack geometry
│   ├── stack_XX_segmentation.nii.gz   # Segmentation in crop/brain space
│   └── stack_XX_seg_rawhaste.nii.gz   # Segmentation in raw HASTE space (crops 18-35)
├── resample_to_raw_space.py           # Step 2
├── map_to_stacks.py                   # Step 3
└── resample_to_rawhaste.py            # Step 4
```

---

## Yair's Notes

- FreeView was broken during development; tested with napari
- `combine_slices_to_nifti.py` adds center-padding for napari visualization — utility only, not in main pipeline
- `group_simulated_slices.py` groups slices by shape for debugging
- The NeSVoR container and pipeline CLI were updated by Yair to support `--extract-slice-transforms`

---

## Comparison with Previous Approach

| | Registration-based (`project_labels.py`) | Inverse alignment (this pipeline) |
|---|---|---|
| Method | Binary brain shape reg + 8-flip search | NeSVoR's own slice geometry |
| Success rate | 73% (25/43 subjects, Dice >= 0.80) | **100%** of reconstructed subjects |
| Registration error | Non-zero (registration approximation) | **Zero** (uses exact NeSVoR affines) |
| Per-subject tuning | flip_k selection, Dice threshold | None needed |
| Requires | NeSVoR --scanner-space re-run | NeSVoR --extract-slice-transforms |
| Margherita email | Was needed for step 2 questions | **No longer needed** |

---

## Server Paths

- Yair's test data: `/neuro/labs/grantlab/research/MRI_processing/yair.beltran/inverse_alignment/test_data/recon_segmentation/`
- Yair's scripts: same directory (`resample_to_raw_space.py`, `map_to_stacks.py`, `resample_to_rawhaste.py`)
- Pipeline CLI: `/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py`
- NeSVoR container: updated by Yair (Apptainer on cluster)

---

## Next Steps

1. Run pipeline on full training set (~250 subjects)
2. Generate tissue labels in raw stack space for all stacks
3. Train TissueClassifier alone (Phase A) on these labels → convergence → freeze
4. Train EnhancementNet (Phase B) with frozen 4-class tissue FiLM
5. Compare tissue FiLM vs brain mask FiLM

---

## Presentation

- `~/Downloads/alignment_plots/fetenh_apr21_slides.pdf` — 16-slide presentation
- `~/Downloads/alignment_plots/*.png` — pipeline diagram, overlay grid, coverage stats, tissue distribution, rawhaste overlays

---

## Related Notes

- [[fetenh-net|FetEnhNet — Main Project]]
- [[fetenh-label-projection-pipeline|Label Projection Pipeline (registration-based, superseded)]]
- [[fetenh-overfitting-analysis|Overfitting Analysis]]
- [[bch-seg-pipeline|Segmentation Pipeline (8 steps)]]
