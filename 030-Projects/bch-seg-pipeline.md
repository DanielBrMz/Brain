---
title: "Segmentation Pipeline — Fetal MRI Processing"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, research, bch, pipeline, segmentation, fetal-mri, grant-lab]
---

# Segmentation Pipeline — Fetal MRI Processing

> Shared tool at Grant Lab for end-to-end fetal brain MRI processing. Authored by Daniel Barreras Meraz.
> Location: `/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/`

---

## Overview

Takes a subject directory with raw HASTE stack NIfTI files and produces a segmented, atlas-aligned, bias-corrected 3D reconstruction with volume measurements. Used across all cohorts (CHD, ASD, Normative, VM, Placenta, Down Syndrome).

---

## Pipeline Steps (8 total)

The `PipelineRunner` class defines the ordered pipeline:

```
mask → nuc → qa → recon → align (two-step) → post_nuc → segment → vol_measure
```

### 1. Masking (`mask_func`)
- **Input:** Raw NIfTI stacks in subject directory
- **Output:** `raw/`, `masks/`, `brain/` subdirectories + `verify/` with cropped visualizations
- **Method:** `run_masking_pipeline()` from `core.masking_wo_dil` — brain extraction without dilation
- **Variant:** `remask_func` for re-extraction with `remask=True` flag (manual only, not in normal pipeline)

### 2. Non-Uniformity Correction (`nuc_func`)
- **Input:** `brain/` directory from masking
- **Output:** `nuc/` directory with bias-corrected stacks
- **Method:** `run_nuc_pipeline()` — N4 bias field correction on masked brain images

### 3. Quality Assessment (`qa_func`)
- **Input:** `nuc/` directory
- **Output:** `quality_assessment.csv` in subject directory
- **Method:** `run_qa_pipeline()` — scores each slice, writes CSV
- **Critical:** Slices with QA score < 0.4 are excluded from reconstruction. Need ≥3 images with QA > 0.4.

### 4. Reconstruction (`reconstruction_func`)
- **Input:** Subject directory with QA CSV + `nuc/` folder
- **Output:** `recon_segmentation/recon.nii` — 3D volumetric reconstruction
- **Method:** `run_reconstruction_pipeline()` — GPU-accelerated (configurable via `gpu_config`)
- **Threshold:** Default 0.4 (QA filter)

### 5. Two-Step Alignment (`two_step_alignment_func`)
This is the most complex step — 6 sub-operations:

1. **Initial alignment:** `run_alignment_pipeline()` on `recon.nii` → `recon_to31.nii` (aligned to GA-matched template)
2. **Initial post-NUC:** `run_post_processing_pipeline()` → `recon_to31_nuc.nii` (bias correction on aligned volume)
3. **Initial 4-label segmentation:** `run_segmentation_pipeline(segmentation_type="4label")` → `recon_to31_nuc_deep_agg.nii.gz`
4. **Brain masking:** `mri_mask` (FreeSurfer) creates `recon_to31init_nuc_mask.nii` using initial segmentation
5. **File preparation:** Renames initial files with `init` suffix, moves transformation matrices
6. **Template selection + final alignment:** `run_template_selection_pipeline()` — selects best-matching age template and re-aligns

### 6. Post Processing (`post_processing_func`)
- **Input:** Final `recon_to31.nii` from alignment
- **Output:** `recon_to31_nuc.nii` — N4 bias field correction on final aligned volume
- **Method:** `run_post_processing_pipeline(processing_type="full")`

### 7. Final Segmentation (`segmentation_func`)
- **Input:** Final `recon_to31_nuc.nii`
- **Output:** `recon_to31_nuc_deep_agg.nii.gz` — FINAL segmentation mask
- **Method:** `run_segmentation_pipeline(segmentation_type="full")` — deep learning segmentation via BOUNTI container
- **Container:** `BOUNTI_segmentation_general_auto_amd_12_2024.sif` (Apptainer)

### 8. Volume Measurement (`volume_measure_func`)
- **Input:** `recon_to31_nuc_deep_agg.nii.gz` + `recon_native.xfm`
- **Output:** `recon_segmentation/Volume_measures.txt`
- **Method:** `run_volume_measurement_pipeline()` — computes tissue-specific volumes using native-space transformation

---

## CLI Usage

```bash
# Full pipeline
python3 /neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py \
  -i /path/to/subject --all

# Individual steps
python3 cli.py -i /path/to/subject --masks      # masking only
python3 cli.py -i /path/to/subject --NUC         # NUC only
python3 cli.py -i /path/to/subject --QA          # QA only
python3 cli.py -i /path/to/subject --recon       # reconstruction only
python3 cli.py -i /path/to/subject --auto_seg    # segmentation only

# Range execution
python3 cli.py -i /path/to/subject --from-recon  # from reconstruction to end
python3 cli.py -i /path/to/subject --to-qa       # from start to QA
python3 cli.py -i /path/to/subject --from-nuc --to-recon  # range

# Options
--gpu 0          # specify GPU (default: auto)
--threshold 0.4  # QA threshold (default: 0.4)
--dry-run        # preview without executing
```

---

## Container System

The pipeline runs tools through Apptainer containers:

| Tool | Container | Purpose |
|------|-----------|---------|
| FSL (flirt, bet, etc.) | `fsl:6.0.4-cuda9.1.sif` | Registration, brain extraction |
| FreeSurfer (mri_mask, mris_convert) | `freesurfer:7.4.1.sif` | Brain masking, surface conversion |
| BOUNTI | `BOUNTI_segmentation_general_auto_amd_12_2024.sif` | Deep learning segmentation |

Containers are at `/neuro/labs/grantlab/research/Apptainer/`.

Helper functions:
- `run_fsl_command()` — runs FSL via container with `/neuro` and `/net` bind mounts
- `run_fs_cmd()` — runs FreeSurfer via container, handles MINC tools (`param2xfm`, `xfm2param`, `nii2mnc`)
- `find_container_image()` — resolves container path from env var or default location
- `extract_scales_from_avscale()` — extracts scaling factors from FSL `avscale` output

---

## Output File Naming

| File | Description |
|------|-------------|
| `recon.nii` | Raw 3D reconstruction |
| `recon_to31.nii` | Atlas-aligned reconstruction |
| `recon_to31_nuc.nii` | Bias-corrected aligned reconstruction |
| `recon_to31_nuc_deep_agg.nii.gz` | Auto segmentation (BOUNTI) |
| `segmentation_to31_final.nii` | **Manual segmentation** (gold standard) |
| `recon_native.xfm` | Native-space transformation matrix |
| `recon_to31.xfm` | Template alignment transformation |
| `quality_assessment.csv` | Per-stack QA scores |
| `Volume_measures.txt` | Tissue volumes |

---

## Source Structure

```
seg_pipeline/
├── cli.py                  # CLI entry point (argparse)
├── src/
│   ├── __init__.py
│   ├── helper_functions.py # timeit, verify, run_fsl_command, run_fs_cmd, CUDA checks
│   ├── logging_config.py   # Colored logging
│   └── segmentation/
│       ├── __init__.py
│       ├── main.py         # Pipeline step functions + PipelineRunner class
│       └── core/
│           ├── masking_wo_dil.py   # Brain extraction
│           ├── nuc.py              # N4 bias field correction
│           ├── qa.py               # Quality assessment scoring
│           ├── reconstruction.py   # 3D volume reconstruction (GPU)
│           ├── alignment.py        # Template alignment
│           ├── post_processing.py  # Post-alignment NUC
│           ├── segmentation.py     # BOUNTI deep learning seg
│           ├── template_selection.py # Age-matched template selection
│           └── volume_measurement.py # Regional volumes
```

Git branches: `main`, `stable`, `param2xfm`, `part2`

---

## Related Notes

- [[fetenh-net|FetEnhNet]] — uses pipeline outputs as training data
- [[bch-surface-pipeline|Surface Processing Pipeline]] — runs after manual segmentation
- [[../040-Roles/research-engineer-bch|Research Engineer Role]]
