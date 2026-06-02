---
title: "BCH Fetal MRI Processing Pipeline — Complete Reference"
type: infrastructure
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [bch, neuroimaging, pipeline, fetal-mri, segmentation, surface-extraction, tools]
---

# BCH Fetal MRI Processing Pipeline

> Complete reference for all tools, models, containers, and processing steps on the FNNDSC NFS cluster.
> For cluster infrastructure see [[bch-cluster|BCH Cluster]].

## The Problem

Fetal MRI has extreme motion artifacts. The fetus moves during acquisition, so radiologists acquire brain images in 3 directions (axial, coronal, sagittal) separately. Each set shows one direction clearly but the other two appear blurry. For research, we need one clean 3D volume from these motion-corrupted 2D slices.

## Pipeline Overview

Two main pipelines run sequentially:

```
Script 1: Seg Pipeline (Volume Processing)
  raw scans → mask → NUC → QA → reconstruct → align → segment → volumes

Script 2: Surface Pipeline (Surface Processing)
  segmentation → inner surface → CSF skeleton → Laplacian → outer surface → measures
```

After Script 1 produces `segmentation_to31_final.nii` (with manual corrections), Script 2 extracts cortical surfaces and computes morphometric measurements.

---

## Script 1: Segmentation Pipeline (`seg_pipeline/`)

**Location:** `/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/`
**Entry point:** `python3 cli.py -i ${file} --all`
**Version:** 0.0.1a (current volume processing v2.1, based on manual v2.0 folder structure)

### Environment Setup

```bash
eval "$(micromamba shell hook --shell bash)"
micromamba activate /neuro/labs/grantlab/research/MRI_processing/environment
```

### Usage

```bash
# Full pipeline
python3 cli.py -i ${file} --all

# Individual steps
python3 cli.py -i ${file} --masking
python3 cli.py -i ${file} --remask        # After manual mask correction
python3 cli.py -i ${file} --NUC
python3 cli.py -i ${file} --QA
python3 cli.py -i ${file} --recon --GPU 0 --threshold 0.4
python3 cli.py -i ${file} --alignment
python3 cli.py -i ${file} --post_nuc
python3 cli.py -i ${file} --segment
python3 cli.py -i ${file} --vol_measure

# Flow control: start from a step and continue
python3 cli.py -i ${file} --from_recon
python3 cli.py -i ${file} --from_alignment

# Stop at a step
python3 cli.py -i ${file} --to_recon
```

### Steps in Detail

#### Step 1: Masking (`--masking`)
- **What:** Automated brain extraction from raw fetal MRI scans
- **Model:** Singularity container `brain_mask_wo_dil_2024.sif` (U-Net trained on fetal brain masks, without dilation post-processing)
- **Container:** `sungmin.you/MRI_SIF/brain_mask_wo_dil_2024.sif`
- **Input:** `${file}/raw/*.nii` (raw HASTE scans from scanner)
- **Output:**
  - `${file}/masks/*_mask.nii` — binary brain masks
  - `${file}/brain/*_brain.nii` — masked brain regions with enhanced colormap
  - `${file}/verify/*.png` — verification images for visual QC
- **How it works:** The container runs a deep learning model that segments the brain region from surrounding tissue (skull, maternal tissue). The mask delimits the ROI for motion correction.

#### Step 2: Remask (`--remask`)
- **What:** Re-apply masking after manual mask corrections in FreeView
- **When:** After reviewing masks in `verify/` and correcting errors in `masks/` using FreeView
- **Input:** Manually corrected masks in `${file}/masks/`
- **Output:** Updated `${file}/brain/` with corrected extractions

#### Step 3: Non-Uniformity Correction (`--NUC`)
- **What:** Correct MRI intensity inhomogeneity (bias field)
- **Tool:** ANTs N4BiasFieldCorrection (via Apptainer container)
- **Container:** `Apptainer/freesurfer:7.4.1.sif` (FreeSurfer container that includes N4)
- **Input:** `${file}/brain/*_brain.nii`
- **Output:** `${file}/nuc/*_brain.nii` (same filenames, corrected intensities)
- **Why:** In MRI, tissue intensity varies smoothly across the image due to RF coil inhomogeneity and biased magnetic field. N4 models this as a smooth multiplicative field and divides it out, making tissue intensities uniform for reliable downstream processing.
- **Reference:** Tustison et al., "N4ITK: Improved N3 Bias Correction" (IEEE TMI 2010)

#### Step 4: Quality Assessment (`--QA`)
- **What:** Score each scan's image quality and select best stacks
- **Model:** `sungmin.you/MRI_SIF/fetal_brain_QA.sif` (quality assessment container)
- **Input:** `${file}/nuc/` (NUC-corrected brain scans)
- **Output:**
  - `${file}/quality_assessment.csv` — filename, quality score (0.0–1.0), slice thickness
  - `${file}/Best_Images_Crop/` — cropped high-quality stacks (score ≥ threshold)
- **Scoring:** Volumes classified as good (1.0), fair (0.5), bad (0.0) based on image quality
- **Threshold:** Default 0.4 (configurable via `--threshold`). At least 3 images must pass.

#### Step 5: Reconstruction (`--recon`)
- **What:** Create a single high-resolution 3D volume from multiple motion-corrupted 2D slice stacks
- **Tool:** **NeSVoR** (Neural Slice-to-Volume Reconstruction)
- **Container:** `Apptainer/nesvor:v0.6.0rc2.sif`
- **Input:** NUC-corrected stacks that passed QA threshold
- **Output:** `${file}/recon_segmentation/recon.nii` (0.5mm isotropic resolution)
- **GPU:** Required. Auto-detected by default, configurable via `--GPU 0|1|2|cpu`
- **How NeSVoR works internally:**
  1. **Slice-to-volume registration:** Iteratively estimates the 3D position/orientation of each 2D slice using a neural implicit representation
  2. **Neural implicit reconstruction:** Represents the 3D volume as a continuous function parameterized by a neural network (coordinate-based MLP)
  3. **Joint optimization:** Simultaneously optimizes slice transforms and the neural volume representation
  4. **Super-resolution:** The continuous representation naturally provides super-resolution — outputs at any desired resolution (default 0.5mm)
  - Key advantage over classical SVR: no explicit regularization needed; the neural network acts as an implicit regularizer
- **Reference:** [NeSVoR docs](https://nesvor.readthedocs.io/en/latest/)

#### Step 6: Alignment (`--alignment`)
- **What:** Two-stage alignment to standardize brain orientation
- **Tools:** FSL FLIRT (via container), FreeSurfer mri_mask
- **Container:** `Apptainer/fsl:6.0.4-cuda9.1.sif`
- **Process (two-step):**
  1. **First alignment:** Linear registration (FLIRT, 7 DOF) to gestational-age-matched fetal brain templates (23–32 weeks) at `/neuro/users/mri.team/fetal_mri/templates_for_alginment/original/`
  2. **Initial segmentation:** Quick 4-label CP segmentation to create brain mask
  3. **Brain masking:** Use initial segmentation to mask out non-brain tissue (FreeSurfer `mri_mask`)
  4. **Second alignment:** Re-align masked brain to template for cleaner registration (template selection based on best fit)
- **Output:**
  - `${file}/recon_segmentation/recon_to31.nii` — aligned reconstruction
  - `${file}/recon_segmentation/recon_native.xfm` — transformation matrix (native ↔ template space)
  - `${file}/recon_segmentation/alignment_temp/` — intermediate files

#### Step 7: Post-NUC (`--post_nuc`)
- **What:** Second N4 bias field correction on the aligned reconstruction
- **Why:** Reconstruction can reintroduce subtle intensity inhomogeneity
- **Output:** `${file}/recon_segmentation/recon_to31_nuc.nii`

#### Step 8: Segmentation (`--segment`)
- **What:** Automatic cortical plate (CP) segmentation using deep learning
- **Models (Singularity containers):**
  - **Full (5-label):** `sungmin.you/MRI_SIF/fetal_CP_CSF5.sif` — segments CP + CSF (5 tissue classes)
  - **4-label:** `sungmin.you/MRI_SIF/fetal_cp_seg_0.5.sif` — 4-label CP segmentation
- **Architecture:** 3-view attention U-Net (axial + coronal + sagittal predictions aggregated)
- **Output:** `${file}/recon_segmentation/recon_to31_nuc_deep_agg.nii.gz`
- **Labels:**
  | Value | Structure |
  |-------|-----------|
  | 1 | Right cortical plate (CP) |
  | 42 | Left cortical plate (CP) |
  | 160 | Left inner (WM + ventricles + deep gray) |
  | 161 | Right inner (WM + ventricles + deep gray) |

#### Manual Segmentation Correction (between Script 1 & 2)
- **Tool:** FreeView (FreeSurfer visualization)
- **Process:** Open `recon_to31_nuc.nii` (grayscale) + `recon_to31_nuc_deep_agg.nii.gz` (labels, opacity ~0.4, Lookup Table colormap)
- **Correction order:** Sagittal → Coronal → Axial
- **Save as:** `segmentation_to31_final.nii`
- **Tip:** In Edit → Preferences, enable right-click to erase voxels

#### Step 9: Volume Measurement (`--vol_measure`)
- **What:** Compute regional brain volumes from segmentation
- **Input:** `recon_to31_nuc_deep_agg.nii.gz` + `recon_native.xfm`
- **Output:** `${file}/recon_segmentation/Volume_measures.txt`
- **Measures:** Total GM, total WM, left/right GM volumes (in native space using transformation matrix)

---

## Script 2: Surface Processing Pipeline (`surface_procesing_pipeline/`)

**Location:** `/neuro/labs/grantlab/research/MRI_processing/tools/surface_procesing_pipeline/`
**Entry point:** `python3 app.py --iSEGM <segmentation> --outdir <output_dir>`
**Version:** 4.0 (refactored as ChRIS plugin template, parallelized, ~45% performance boost)

### Usage

```bash
# Full surface pipeline
python3 app.py --iSEGM ${file}/recon_segmentation/segmentation_to31_final.nii \
               --outdir ${file}/surfaces

# For subjects < 28.5 weeks gestational age
python3 app.py --iSEGM ... --outdir ... --subsampling False

# Inner surface only (for quick segmentation check)
python3 app.py --iSEGM ... --outdir ... --inner_only
```

### Steps in Detail

#### Step 1: Inner CP Surface Extraction
- **What:** Extract the inner cortical plate (white matter) surface
- **Container:** `docker://fnndsc/pl-fetal-cp-surface-extract` (via Apptainer)
- **Process:**
  1. Convert segmentation to MINC format (`nii2mnc`)
  2. Extract specific label (160=left WM, 161=right WM) using `mincmath`
  3. Run marching cubes surface extraction inside container with `--adapt_object_mesh 0,100,0,0` and `--mincmorph-iterations 1`
  4. Optional: WM subsampling for subjects ≥ 28.5 weeks (`--subsample`)
  5. Check and remove self-intersections (`check_self_intersect`, `mris_remove_intersection`)
  6. Resample to standard mesh format (81,920 vertices) via Perl script
  7. Apply Taubin smoothing (100 iterations default)
- **Output:** `lh.smoothwm.to31_81920.obj/.asc`, `rh.smoothwm.to31_81920.obj/.asc`

#### Step 2: CSF Skeletonization + CLASP Relabeling
- **What:** Iterative CSF skeletonization to create CLASP-format segmentation for outer surface extraction
- **Process:** 10 iterations of morphological skeletonization of CSF space between inner surface and outer boundary
- **Output:** CLASP segmentation with labels: 1=WM, 2=GM (cortical plate), 3=CSF

#### Step 3: Laplacian Field Computation
- **What:** Compute smooth gradient field between inner and outer cortical boundaries
- **Tool:** Perl script `laplace_CSF.pl` (solves Laplace's equation on the CLASP segmentation)
- **Output:** Laplacian map (`.mnc`) — smooth scalar field from 0 (inner) to 1 (outer)

#### Step 4: Outer CP Surface Extraction
- **What:** Expand inner surface outward along Laplacian gradient to create pial surface
- **Container:** `Apptainer/pl-civet_2.1.1.4.sif` (CIVET surface tools)
- **Tool:** `expand_from_white_fetal_MNI.pl` — iterative mesh deformation
- **Parameters:**
  - Stretch weight (default 1.0) — prevents excessive mesh deformation
  - Laplacian weight (default 1.0) — guides expansion along gradient field
  - Normal mode: 3,500 iterations; fast mode: 1,750 iterations
- **Output:** `lh.pial.to31_81920.obj/.asc`, `rh.pial.to31_81920.obj/.asc`

#### Step 5: Cleanup
- Copy final `.wm` and `.pial` surfaces to output directory, remove temp files

#### Step 6: Surface Registration & Measurements
- **Registration targets:** 3 templates
  - `/neuro/users/mri.team/fetal_mri/Surface_template/template-29/` (29 GW)
  - `/neuro/users/mri.team/fetal_mri/Surface_template/template-31/` (31 GW)
  - `/neuro/users/mri.team/fetal_mri/Surface_template/template-adult/`
- **Registration tool:** `bestsurfreg.pl` (CIVET container)
- **Surface measures computed:**

| Measure | Tool | Description |
|---------|------|-------------|
| **Cortical thickness** | `cortical_thickness -tlink` | Distance between WM and pial surfaces |
| **Sulcal depth** | `ADT_subvoxel_final3` | Approximate Distance Transform from brain hull |
| **Surface area** | `depth_potential -area_voronoi` | Voronoi-based vertex area |
| **Mean curvature** | `depth_potential -mean_curvature` | Local surface curvature |
| **Gyrification index** | pial area / smooth hull area | Cortical folding complexity |
| **Volume** | From segmentation labels | GM/WM tissue volumes |

- All vertex measures smoothed with 5mm kernel (`depth_potential -smooth 5`)
- **Output files:**
  - `surfaces/Area_Depth_aMC.rsl.s5.txt` — L/R area, depth, absolute mean curvature
  - `surfaces/GI_info_final.txt` — L/R/whole gyrification indices
  - `surfaces/template-*/` — resampled surfaces and measures per template

---

## Additional Processing: Brain Age Estimation

Not part of standard pipeline — run separately after QA.

```bash
# Environment
micromamba activate /neuro/labs/grantlab/research/MRI_processing/sungmin.you/conda_env/brain_age2

# Setup
cp -r ./${file}/best_images_crop/ ./${file}/estimated_brain_age/

# Preprocessing
python3 .../sungmin.you/MRI_codes/make_verify_single2.py ./${file}/estimated_brain_age/
python3 .../sungmin.you/MRI_codes/resample_inplane.py ./${file}/estimated_brain_age/

# Prediction (Singularity container)
singularity run --no-home -B ${file}/estimated_brain_age:/data --nv \
  /neuro/labs/grantlab/research/MRI_processing/sungmin.you/MRI_SIF/fetal_brain_Andrea.sif

# Mode calculation
python3 .../sungmin.you/MRI_codes/mode_brain_age_fix.py ./${file}/estimated_brain_age/pred_age.txt
```

**Output:** `pred_age_mode.txt` (mode estimated brain age), `pred_age.txt` (per-slice ages)

---

## Data Acquisition: Pulling from ChRIS/PACS

```bash
# SSH to ChRIS PACS server
ssh chris-local@titan  # pw: chris1234
# Then type "v" (fish shell by Rudolph)

# Search for patient
px-find --aet CHRISV3 --serverIP 134.174.12.21 --serverPort 104 \
  --PatientID <MRN> --Modality MR \
  --db /neuro/users/chris/PACS/log --verbosity 1 \
  --then retrieve,status --withFeedBack --json

# Data lands in: /neuro/users/chris/PACS/data/<MRN-name-date>/<Accession>/

# Convert DICOM to NIfTI (filters HASTE, BRAIN, Uterus, T2)
python3 /neuro/labs/grantlab/research/HyukJin_MRI/code/dicom2nii_chris.py <INPUT> <OUTPUT>

# For diffusion (DTI) data
python3 /neuro/labs/grantlab/research/HyukJin_MRI/code/dicom2nii_chris_DTI.py <INPUT> <OUTPUT>
```

---

## Apptainer/Singularity Containers

All containers live in `/neuro/labs/grantlab/research/Apptainer/` (shared) and `/neuro/labs/grantlab/research/MRI_processing/sungmin.you/MRI_SIF/` (lab-specific models).

**Runtime:** Apptainer 1.4.3

### Containers Used by Pipeline

| Container | Location | Used By | Purpose |
|-----------|----------|---------|---------|
| `brain_mask_wo_dil_2024.sif` | sungmin/MRI_SIF/ | Masking | Brain extraction (U-Net, no dilation) |
| `fetal_brain_QA.sif` | sungmin/MRI_SIF/ | QA | Image quality scoring |
| `nesvor:v0.6.0rc2.sif` | Apptainer/ | Recon | NeSVoR slice-to-volume reconstruction |
| `fsl:6.0.4-cuda9.1.sif` | Apptainer/ | Alignment | FSL FLIRT linear registration |
| `freesurfer:7.4.1.sif` | Apptainer/ | NUC, tools | N4, mri_mask, mris_remove_intersection |
| `fetal_CP_CSF5.sif` | sungmin/MRI_SIF/ | Segmentation | 5-label CP+CSF segmentation |
| `fetal_cp_seg_0.5.sif` | sungmin/MRI_SIF/ | Segmentation | 4-label CP segmentation (alignment step) |
| `pl-fetal-cp-surface-extract` | Docker Hub | Inner surface | Marching cubes + MINC morphology |
| `pl-civet_2.1.1.4.sif` | Apptainer/ | Outer surface | CIVET surface deformation tools |
| `fetal_brain_Andrea.sif` | sungmin/MRI_SIF/ | Brain age | Brain age estimation model |
| `BOUNTI_segmentation_general_auto_amd_12_2024.sif` | tools/ | Alt. seg | BOUNTI segmentation (alternative) |

### Other Available Containers (Apptainer/)

| Category | Containers |
|----------|-----------|
| **FreeSurfer** | 7.2.0, 7.3.2, 7.4.1, 8.1.0, infant-8.1.0, neurodesk-8.1.0 |
| **FSL** | 5.0.11, 6.0.4-cuda8.0, 6.0.4-cuda9.1, 6.0.5.1-cuda9.1 |
| **NeSVoR** | v0.3.0, v0.4.0, v0.6.0rc1, v0.6.0rc2 |
| **Segmentation** | babyseg, BOUNTI, malpem, ibeat_v2 (200, 208) |
| **Surface** | pl-fetal-surface-extract (2.0.2), pl-bichamfer, pl-gifit, pl-smoothness-error |
| **Reconstruction** | svrtk, pl-irtk-reconstruction |
| **Tractography** | dsistudio, ukftractography |
| **FastSurfer** | fastsurfer-gpu |
| **Infant** | infantfs, pl-infantfs (7.1.1.1, 7.1.1.2) |
| **Utilities** | dcm2mha_cnvtr, minc-toolkit, pl-n4biasfieldcorrection, robex, irtk, tensorflow:1.15.5-gpu |

### Sungmin's Model Zoo (MRI_SIF/)

| Container | Purpose |
|-----------|---------|
| `brain_mask*.sif` (5 variants) | Brain masking models (various versions/configs) |
| `fetal_cp_seg*.sif` (6 variants) | CP segmentation models (attention, 0.5mm, JS version) |
| `fetal_CP_CSF5*.sif` (3 variants) | 5-label CP+CSF segmentation |
| `fetal_CP_Label7.sif` | 7-label CP segmentation |
| `fetal_CP_aug_Label5.sif` | Augmented 5-label CP |
| `fetal_anomaly_detection*.sif` (2) | Anomaly detection models |
| `fetal_BA_*.sif` (2) | Brain age estimation (BF, CHD-ND variants) |
| `fetal_brain_QA.sif` | Quality assessment |
| `fetal_brain_TMC.sif` | TMC-specific brain model |
| `fetal_parcellation.sif` | Brain parcellation |

---

## Installed Software on NFS

### `/neuro/arch/Linux64/packages/`

| Tool | Versions | Purpose |
|------|----------|---------|
| **FreeSurfer** | dev, dev-centos, stable 5.1/5.2/5.3, stable-6.0, infant | Cortical surface analysis, brain segmentation, visualization (FreeView) |
| **FSL** | Current (+ fsl419, fsl-old) | FLIRT registration, BET brain extraction, FAST segmentation, eddy current correction |
| **ANTs** | 1.9.v4 + current | N4BiasFieldCorrection, SyN registration, brain extraction |
| **AFNI** | Current | fMRI analysis, image processing |
| **ITK-SNAP** | 2.4, 3.2, 4.4 | Interactive segmentation editor |
| **3D Slicer** | 3, 4, 5 | Medical image visualization and analysis |
| **dcm2niix** | Current | DICOM to NIfTI conversion |
| **DCMTK** | Current | DICOM toolkit |
| **BrainSuite** | Current | Brain surface/volume analysis |
| **MATLAB** | Current | Scientific computing |
| **TrackVis** | Current | Diffusion tractography visualization |
| **NeSVoR** | via containers | Slice-to-volume reconstruction |
| **CUDA** | Current | GPU compute libraries |

### Key FSL Commands Used

| Command | Pipeline Step | Purpose |
|---------|-------------|---------|
| `flirt` | Alignment | Linear registration (6/7/12 DOF) |
| `convert_xfm` | Alignment | Combine/invert transformation matrices |
| `avscale` | Alignment | Extract scale from transformation |
| `fslmaths` | Various | Image arithmetic, thresholding |
| `fslstats` | Volume | Image statistics |
| `bet` | (optional) | Brain extraction |

### Key FreeSurfer Commands Used

| Command | Pipeline Step | Purpose |
|---------|-------------|---------|
| `mri_mask` | Alignment | Apply binary mask to volume |
| `mris_remove_intersection` | Surface | Fix self-intersecting mesh |
| `freeview` | Manual QC | Interactive visualization and editing |
| `nii2mnc` / `mnc2nii` | Surface | Format conversion |
| `mincmath` | Surface | Voxelwise math on MINC files |

### CIVET Tools (via container)

| Command | Purpose |
|---------|---------|
| `adapt_object_mesh` | Taubin mesh smoothing |
| `check_self_intersect` | Detect mesh self-intersections |
| `obj2asc` / `asc2obj` | Surface format conversion |
| `cortical_thickness -tlink` | Thickness between WM and pial |
| `depth_potential` | Area, curvature, depth, smoothing |
| `ADT_subvoxel_final3` | Approximate Distance Transform (sulcal depth) |
| `transform_objects` | Apply transformations to surfaces |
| `bestsurfreg.pl` | Surface registration |
| `expand_from_white_fetal_MNI.pl` | Outer surface expansion |

---

## Templates

### Alignment Templates
**Location:** `/neuro/users/mri.team/fetal_mri/templates_for_alginment/`

| Directory | Content |
|-----------|---------|
| `original/` | GA-matched templates (23–32 weeks) at original resolution (0.86mm) |
| `0.5mm/` | Upsampled to 0.5mm isotropic |
| `0.25mm/` | Upsampled to 0.25mm isotropic |

### Surface Templates
**Location:** `/neuro/users/mri.team/fetal_mri/Surface_template/`

| Template | Purpose |
|----------|---------|
| `template-24` through `template-31` | GA-specific surface templates |
| `template-adult` | Adult brain surface template |
| `xfm/` | Inter-template transformation matrices |
| `verify/` | Template verification images |

---

## Container Environment Variables

The seg pipeline checks these environment variables before falling back to default paths:

```bash
# Override default container paths
export FREESURFER_CONTAINER=/path/to/freesurfer.sif
export FSL_CONTAINER=/path/to/fsl.sif
```

This allows testing different container versions without code changes.

---

## Deploying New Models as Containers

From the manual — steps to containerize a new deep learning model:

1. **Prepare:** trained weights (`.h5`), inference code (`.py`), `requirements.txt`, any template files
2. **Create definition file** (`container.def`) with `%files`, `%environment`, `%post`, `%runscript` sections
3. **Build:** `sudo singularity build <name>.sif container.def` (requires sudo, do on local machine)
4. **Deploy:** Copy `.sif` to `/neuro/labs/grantlab/research/MRI_processing/sungmin.you/MRI_SIF/` or `/neuro/labs/grantlab/research/Apptainer/`
5. **Install Apptainer** (if needed): `sudo dpkg -i apptainer_*.deb && sudo patch /etc/apptainer/apptainer.conf < .../bind_grantlab.patch`

---

## Version History

### Volume Processing (seg_pipeline)
| Version | Changes |
|---------|---------|
| 1.0 | Alex's masking model, Ivan's QA (docker://fnndsc/pl-fetal-brain-assessment:1.3.0), SVR recon, Fernanda's alignment, 0.86mm templates |
| 1.1 | Moved recon_native.xfm from surfaces/ to recon_?/ |
| 1.2 | Added per-step flags (--segment, etc.) |
| 1.3 | Error messages, termination on missing files, reprocess flag |
| 2.0 | New folder structure (recon_segmentation/) |
| 2.1 | Changed alignment templates path to mri.team |

### Surface Processing (surface_procesing_pipeline)
| Version | Changes |
|---------|---------|
| 1.0 | Marching cube inner extraction, registration to 28-31 templates |
| 3.0 | Added adult template, 10mm smoothing kernel |
| 3.2 | Changed inner extraction options, added subsampling + Taubin |
| 3.3 | Python-based volume measures (replaced fslstats) |
| 3.4 | --all_young flag (no subsampling for young fetuses) |
| 4.0 | **Major refactor:** ChRIS plugin template, parallelism (+45%), robust error handling, modular codebase |

---

## Related

- [[bch-cluster|BCH Cluster Infrastructure]]
- [[../030-Projects/fetenh-net|FetEnhNet — Fetal MRI Enhancement]]
- [[../030-Projects/sparse-slm|ActivSparse-SLM]]
