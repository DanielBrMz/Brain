---
title: "Surface Processing Pipeline — Cortical Surface Extraction"
type: project
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [project, research, bch, pipeline, surface, cortical, fetal-mri, grant-lab]
---

# Surface Processing Pipeline — Cortical Surface Extraction

> Extracts inner and outer cortical plate surfaces from manually segmented fetal brain reconstructions.
> Authors: Andrea Gondova (original), Sungmin You (modifications), Daniel (pipeline runner refactor)
> Location: `/neuro/labs/grantlab/research/MRI_processing/tools/surface_procesing_pipeline/`

---

## Overview

Takes a manually corrected segmentation (`segmentation_to31_final.nii`) and produces cortical surfaces, CSF skeleton, Laplacian field, outer surface, and morphometric measurements. This is the final step after the [[bch-seg-pipeline|segmentation pipeline]] and manual review.

---

## Pipeline Steps (6 total)

### 1. Relabel Segmentation
- Remap iBEAT labels to 5-class scheme for surface extraction
- Input: `segmentation_to31_final.nii`
- Output: `cp_manual_seg_5.nii`

### 2. Inner Cortical Plate Surface Extraction
- Extract white matter (inner CP) surfaces for both hemispheres **in parallel** using `ThreadPoolExecutor`
- Left hemisphere: label 160, Right hemisphere: label 161
- Taubin smoothing (default 15 iterations)
- Mesh subsampling to 81,920 vertices (configurable)
- Output formats: `.obj`, `.asc`, `.gii` (FreeSurfer GIFTI conversion via `mris_convert`)
- Files: `lh.wm_81920.{obj,asc,gii}`, `rh.wm_81920.{obj,asc,gii}`

### 3. CSF Skeletonization
- `run_csf_skeletonization()` — iterative thinning of CSF space
- Creates skeleton used to define outer boundary of cortical plate

### 4. Laplacian Field Computation
- `compute_laplacian_field()` — solves Laplace equation between inner and outer boundaries
- Produces smooth field used to expand inner surface to outer surface

### 5. Outer Surface Extraction
- `extract_outer_surface()` — deforms inner surface along Laplacian gradient
- Produces outer cortical plate surfaces

### 6. Surface Measurements
- `run_surface_measurements()` — cortical thickness, surface area, curvature
- Uses FreeSurfer tools for metric computation

---

## CLI Usage

```bash
# Standard usage (after manual segmentation)
python3 /neuro/labs/grantlab/research/MRI_processing/tools/surface_procesing_pipeline/app.py \
  --iSEGM /path/to/subject/recon_segmentation/segmentation_to31_final.nii \
  --outdir /path/to/subject/surfaces

# For young fetuses (GA < 28.5 weeks)
python3 app.py \
  --iSEGM /path/to/segmentation_to31_final.nii \
  --outdir /path/to/surfaces \
  --subsampling False

# Custom Taubin smoothing
python3 app.py \
  --iSEGM /path/to/segmentation_to31_final.nii \
  --outdir /path/to/surfaces \
  --taubin_itr_CP 20
```

---

## Prerequisites

- Manual segmentation must be done first in freeview:
  ```bash
  freeview ${subject}/recon_segmentation/recon_to31_nuc.nii \
           ${subject}/recon_segmentation/recon_to31_nuc_deep_agg.nii.gz:colormap=lut
  # Save as: segmentation_to31_final.nii
  ```

---

## Segment IDs

| ID | Structure |
|----|-----------|
| 1 | Left Cortical Plate |
| 42 | Right Cortical Plate |
| 160 | Left Inner (WM/Subplate) |
| 161 | Right Inner (WM/Subplate) |
| 18 | CSF |

---

## Critical Rules

1. **GA < 28.5 weeks:** Use `--subsampling False` — young brains are too small for 81,920 vertex meshes
2. Requires `segmentation_to31_final.nii` (manual correction), NOT the auto segmentation
3. Pipeline uses FreeSurfer container (`freesurfer:7.4.1.sif`) for surface operations

---

## Source Structure

```
surface_procesing_pipeline/
├── app.py                   # CLI entry point (argparse)
├── config.py                # BIC environment setup
├── src/
│   ├── main.py              # Step functions (inner_cp_extraction, etc.)
│   ├── pipeline_runner.py   # PipelineRunner class
│   ├── helper_functions.py  # run_fs_cmd, timeit_decorator
│   ├── logging_config.py
│   └── core/
│       ├── relabel_segmentation.py
│       ├── inner_cp_surface.py
│       ├── CSF_skeletonization_iteration.py
│       ├── laplacian_field.py
│       ├── outer_surface_extraction.py
│       └── surface_measures.py
```

---

## Related Notes

- [[bch-seg-pipeline|Segmentation Pipeline]] — runs before this pipeline
- [[fetenh-net|FetEnhNet]] — tissue labels from this pipeline used for FiLM conditioning
- [[../040-Roles/research-engineer-bch|Research Engineer Role]]
