# NeSVoR: Neural Slice-to-Volume Reconstruction

Created: 2026-03-24
Tags: #neuroimaging #fetal-mri #deep-learning #implicit-neural-representation #slice-to-volume

---

## Overview

NeSVoR (Neural Slice-to-Volume Reconstruction) is a GPU-accelerated deep learning package for slice-to-volume reconstruction (SVR) in MRI. It reconstructs a 3D isotropic high-resolution volume from a set of motion-corrupted low-resolution 2D slices, with primary application to fetal and neonatal brain MRI.

- **Repository:** https://github.com/daviddmc/NeSVoR
- **Documentation:** https://nesvor.readthedocs.io/en/latest/
- **Author:** Junshen Xu (MIT EECS PhD, now at FNNDSC/BCH)
- **License:** MIT
- **Docker Image:** `junshenxu/nesvor` (built with CUDA 11.7)

## Publications

| Paper | Venue | Year | Link |
|-------|-------|------|------|
| NeSVoR: Implicit Neural Representation for Slice-to-Volume Reconstruction in MRI | IEEE Transactions on Medical Imaging | 2023 | [IEEE](https://ieeexplore.ieee.org/document/10015091/), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10287191/) |
| SVoRT: Iterative Transformer for Slice-to-Volume Registration in Fetal Brain MRI | MICCAI 2022 / IEEE TMI 2023 | 2022-2023 | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10129054/), [arXiv](https://arxiv.org/abs/2206.10802) |
| A Robust and Efficient Framework for Slice-to-Volume Reconstruction (PhD thesis) | MIT EECS | 2023 | [DSpace](https://dspace.mit.edu/bitstream/handle/1721.1/151495/xu-junshen-phd-eecs-2023-thesis.pdf) |

**Authors:** Junshen Xu, Daniel Moyer, Borjan Gagoski, Juan Eugenio Iglesias, P. Ellen Grant, Polina Golland, Elfar Adalsteinsson

## Installation

### Docker (Recommended)
```bash
docker pull junshenxu/nesvor

# Interactive
docker run -it --gpus all --ipc=host junshenxu/nesvor nesvor -h

# With volume mounts
docker run --gpus all --ipc=host \
  -v /path/to/data:/data \
  junshenxu/nesvor nesvor reconstruct \
  --input-stacks /data/stack-*.nii.gz \
  --output-volume /data/output.nii.gz
```

### From Source
```bash
pip install nesvor
# or clone and install from GitHub
git clone https://github.com/daviddmc/NeSVoR.git
cd NeSVoR && pip install -e .
```

## Architecture (Technical)

### Core Idea: Implicit Neural Representation

NeSVoR models the underlying 3D volume as a **continuous function** of spatial coordinates using an implicit neural representation. Instead of reconstructing a discrete voxel grid directly, it learns a function `f(x, y, z) -> intensity` that can be queried at arbitrary resolution.

### Multi-Resolution Hash Grid Encoding

Inspired by Instant NGP (NVIDIA), NeSVoR uses a **multi-resolution hash grid** data structure:
- Coordinates are encoded via look-up and interpolation from the hash grid
- Low-level grids encode slowly varying features (e.g., bias field)
- High-level grids encode high-frequency details (e.g., edges, fine anatomy)
- Hash table structure compresses high-level grids for smaller memory footprint
- Key advantage over frequency encoding: **convergence in 1-2 minutes** (vs. much longer with frequency/positional encoding)

### Three-Head MLP Architecture

The coordinate encodings + slice embeddings are fed to **three separate MLPs** that regress:
1. **Volume intensity** -- the actual tissue signal
2. **Bias field** -- smooth multiplicative inhomogeneity
3. **Variance** -- pixel-wise and slice-wise noise variance (enables outlier detection + uncertainty visualization)

**Slice embeddings** are trainable vectors that capture slice-specific information (e.g., contrast variations between acquisitions).

### Slice Acquisition Model

NeSVoR uses a continuous and comprehensive forward model:

```
y_observed = B_k * PSF * T_k(f(x)) + noise
```

Where:
- `f(x)` = implicit neural representation of the volume
- `T_k` = rigid transformation for slice k (6 DOF: 3 rotation + 3 translation)
- `PSF` = point spread function (approximated via random sampling)
- `B_k` = bias field for slice k
- `noise` ~ variance estimated per-pixel and per-slice

**Training objective:** Minimize error between simulated pixel values (from the model) and actual acquired pixel values.

### SVoRT: Slice-to-Volume Registration Transformer

SVoRT handles the motion correction (registration) step:
- Models multiple stacks of MR slices as a **sequence** fed to a Transformer
- Attention mechanism detects relevance between slices across stacks
- Predicts transformation of each slice using information from other slices
- Alternates between estimating the 3D volume and updating slice transformations
- Trained on synthetically transformed data (68 training + 12 test high-quality fetal brain volumes, GA 20-35 weeks)
- Pretrained weights available for download

## Commands

Get help for any command: `nesvor <command> -h`

### `nesvor reconstruct`

Reconstructs a 3D volume (trains a NeSVoR model) from stacks or motion-corrected slices.

```bash
# From raw stacks (does segmentation + bias correction + registration + reconstruction)
nesvor reconstruct \
  --input-stacks stack-1.nii.gz stack-2.nii.gz stack-N.nii.gz \
  --thicknesses <thick-1> <thick-2> <thick-N> \
  --output-volume volume.nii.gz \
  --output-model model.pt \
  --output-slices slices_folder/ \
  --output-resolution 0.8 \
  --registration svort \
  --segmentation \
  --bias-field-correction

# From pre-registered slices (separation of registration and reconstruction)
nesvor reconstruct \
  --input-slices slices_folder/ \
  --output-volume volume.nii.gz \
  --output-model model.pt

# With deformable (non-rigid) motion correction (experimental)
nesvor reconstruct \
  --input-stacks stack-*.nii.gz \
  --output-volume volume.nii.gz \
  --deformable
```

**Key flags:**
- `--input-stacks` -- Input NIfTI stacks (.nii / .nii.gz)
- `--input-slices` -- Folder of motion-corrected slices (alternative to stacks)
- `--output-volume` -- Reconstructed 3D volume (NIfTI)
- `--output-model` -- Trained NeSVoR model checkpoint (.pt file)
- `--output-slices` -- Folder to save motion-corrected individual slices
- `--output-resolution` -- Isotropic output resolution in mm
- `--thicknesses` -- Slice thickness for each stack
- `--registration svort` -- Use SVoRT for motion correction
- `--segmentation` -- Run CNN brain segmentation on input stacks
- `--bias-field-correction` -- Run N4 bias field correction
- `--deformable` -- Enable deformable (non-rigid) motion (experimental)

### `nesvor register`

Registers stacks of slices using SVoRT or stack-to-stack registration.

```bash
nesvor register \
  --input-stacks stack-1.nii.gz stack-2.nii.gz \
  --stack-masks mask-1.nii.gz mask-2.nii.gz \
  --output-slices registered_slices_folder/ \
  --registration svort
```

### `nesvor sample-volume`

Samples a discretized volume from a trained NeSVoR model at any desired resolution.

```bash
nesvor sample-volume \
  --input-model model.pt \
  --output-volume volume_0.5mm.nii.gz \
  --output-resolution 0.5
```

### `nesvor sample-slices`

Simulates slices from a trained NeSVoR model at the locations of input slices. Used for reconstruction quality evaluation.

```bash
nesvor sample-slices \
  --input-slices slices_folder/ \
  --input-model model.pt \
  --simulated-slices simulated_slices_folder/
```

**What `--simulated-slices` outputs:**
- A folder of NIfTI files, one per input slice
- Each simulated slice is what the trained model predicts the slice "should" look like at that motion-corrected location
- Comparing input slices vs. simulated slices allows quality assessment of the reconstruction
- The NIfTI header of each slice contains the affine transformation encoding its position/orientation in world (RAS+) coordinates

### `nesvor segment-stack`

Generates brain masks for input stacks using a CNN.

```bash
nesvor segment-stack \
  --input-stacks stack-1.nii.gz stack-2.nii.gz \
  --output-stack-masks mask-1.nii.gz mask-2.nii.gz
```

### `nesvor correct-bias-field`

Bias field correction using the N4 algorithm.

### `nesvor assess`

Quality and motion assessment of input stacks. Evaluates image quality/motion to find template stacks or filter low-quality data.

### `nesvor svr`

Classical (non-neural) slice-to-volume registration/reconstruction method.

## Motion-Corrected Slices: Format and Transforms

### How Slices Are Stored

When NeSVoR outputs motion-corrected slices (via `--output-slices` on `reconstruct` or `register`), they are saved as:
- **Individual NIfTI files** in a folder
- Each file is a single 2D slice (or thin 3D slab with 1 slice in k-dimension)
- The **NIfTI affine matrix** (sform/qform) in each file's header encodes the rigid-body transformation placing that slice in world (RAS+) coordinate space

### NIfTI Affine Transform Format

Each slice's NIfTI header contains a **4x4 affine matrix** mapping voxel coordinates `(i, j, k)` to world coordinates `(x, y, z)` in RAS+ space:

```
| M11  M12  M13  tx |   | i |   | x |
| M21  M22  M23  ty | * | j | = | y |
| M31  M32  M33  tz |   | k |   | z |
|  0    0    0    1  |   | 1 |   | 1 |
```

Where:
- The 3x3 submatrix `M` encodes rotation and scaling (voxel size)
- The 3x1 vector `[tx, ty, tz]` encodes translation
- This is the **motion-corrected** position -- i.e., where the slice actually was in 3D space during acquisition, after correcting for fetal motion

### Coordinate Spaces

- **Input slices** have their original scanner-space affine (from DICOM-to-NIfTI conversion)
- **Motion-corrected slices** have an updated affine reflecting the estimated rigid-body pose (rotation + translation) of that slice in the canonical reconstruction space
- The **reconstructed volume** has its own affine mapping voxels to the same RAS+ world coordinate system
- All share the same world coordinate space after reconstruction

## Projecting Labels from Volume Back to Slices

To map labels/segmentations from the reconstructed volume back to individual raw slices, the workflow is:

1. **Obtain the motion-corrected slice transforms** from `--output-slices` (the NIfTI affine in each slice file)
2. **For each slice**, the affine tells you exactly which voxels in the reconstructed volume correspond to that slice's pixel locations
3. **Procedure:**
   ```python
   import nibabel as nib
   import numpy as np

   # Load reconstructed volume with labels
   vol = nib.load('labels_volume.nii.gz')
   vol_data = vol.get_fdata()
   vol_affine = vol.affine

   # For each motion-corrected slice:
   slice_nii = nib.load('slices_folder/slice_001.nii.gz')
   slice_affine = slice_nii.affine
   slice_shape = slice_nii.shape

   # Build coordinate grid in slice voxel space
   i, j, k = np.meshgrid(
       np.arange(slice_shape[0]),
       np.arange(slice_shape[1]),
       np.arange(slice_shape[2] if len(slice_shape) > 2 else 1),
       indexing='ij'
   )
   voxels = np.stack([i.ravel(), j.ravel(), k.ravel(), np.ones_like(i.ravel())])

   # Transform slice voxels -> world coordinates
   world_coords = slice_affine @ voxels

   # Transform world coordinates -> volume voxel coordinates
   vol_inv_affine = np.linalg.inv(vol_affine)
   vol_voxels = vol_inv_affine @ world_coords

   # Sample the label volume at these coordinates (nearest neighbor for labels)
   vi = np.round(vol_voxels[0]).astype(int)
   vj = np.round(vol_voxels[1]).astype(int)
   vk = np.round(vol_voxels[2]).astype(int)

   # Clip to volume bounds
   vi = np.clip(vi, 0, vol_data.shape[0]-1)
   vj = np.clip(vj, 0, vol_data.shape[1]-1)
   vk = np.clip(vk, 0, vol_data.shape[2]-1)

   slice_labels = vol_data[vi, vj, vk].reshape(slice_shape[:2])
   ```

4. The key insight: the **slice affine** and the **volume affine** share the same world coordinate system, so you can compose `inv(vol_affine) @ slice_affine` to get a direct voxel-to-voxel mapping.

## Typical Workflow

### All-in-One (simplest)
```bash
nesvor reconstruct \
  --input-stacks stack-1.nii.gz stack-2.nii.gz stack-3.nii.gz \
  --thicknesses 3 3 3 \
  --output-volume recon.nii.gz \
  --output-model model.pt \
  --output-slices corrected_slices/ \
  --output-resolution 0.8 \
  --registration svort \
  --segmentation \
  --bias-field-correction
```

### Two-Step (separate registration and reconstruction)
```bash
# Step 1: Register
nesvor register \
  --input-stacks stack-1.nii.gz stack-2.nii.gz \
  --output-slices registered_slices/

# Step 2: Reconstruct from registered slices
nesvor reconstruct \
  --input-slices registered_slices/ \
  --output-volume recon.nii.gz \
  --output-model model.pt
```

### Post-Reconstruction Analysis
```bash
# Sample volume at different resolution
nesvor sample-volume \
  --input-model model.pt \
  --output-volume recon_0.5mm.nii.gz \
  --output-resolution 0.5

# Simulate slices for quality evaluation
nesvor sample-slices \
  --input-slices corrected_slices/ \
  --input-model model.pt \
  --simulated-slices simulated_slices/
```

## Key Performance

- **2-10x faster** reconstruction than state-of-the-art algorithms
- Model converges to high-quality volume in **1-2 minutes** (hash grid encoding)
- Resolution-agnostic: can sample output at any resolution from a single trained model
- Robust to subject motion via comprehensive slice acquisition model
- Uncertainty visualization via estimated per-pixel variance

## ChRIS Integration

NeSVoR is available as a [ChRIS ds plugin](https://github.com/FNNDSC/pl-NeSVoR-reconstruct) (`pl-NeSVoR-reconstruct`) for deployment in the ChRIS research platform at Boston Children's Hospital / FNNDSC.

## BCH Cluster Setup

### Apptainer Containers (sejong)

```
/neuro/labs/grantlab/research/Apptainer/nesvor:v0.3.0.sif
/neuro/labs/grantlab/research/Apptainer/nesvor:v0.4.0.sif
/neuro/labs/grantlab/research/Apptainer/nesvor:v0.6.0rc1.sif
/neuro/labs/grantlab/research/Apptainer/nesvor:v0.6.0rc2.sif  ← current
```

### Invocation on sejong

```bash
CUDA_VISIBLE_DEVICES=2 apptainer exec \
  --nv \
  --env CUDA_VISIBLE_DEVICES=0 \
  --bind /neuro:/neuro \
  /neuro/labs/grantlab/research/Apptainer/nesvor:v0.6.0rc2.sif \
  nesvor reconstruct \
    --input-stacks stack1.nii stack2.nii \
    --stack-masks mask1.nii mask2.nii \
    --output-volume recon.nii.gz \
    --output-resolution 0.8 \
    --simulated-slices simulated_slices/ \
    --output-model model.pt \
    --svort-version v2
```

### Existing Pipeline Wrapper

`/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/src/segmentation/core/reconstruction.py` wraps NeSVoR with bind mounts for `/neuro` and `/net` filesystems.

## Experimental Results: `--simulated-slices` on FCB080 (2026-03-24)

Test run on subject FCB080 (CHD, 15 T2_HASTE stacks + brain masks):

- **Runtime:** 344s (5.7 min) on single RTX A5000
  - Data loading: 12s
  - SVoRT registration: 36s (similarity=0.677)
  - Reconstruction training: 285s (39 epochs)
  - Results saving: 11s
- **Output reconstruction:** 94×110×94 at 0.8mm isotropic
- **Simulated slices:** 400 individual NIfTI files (one per input slice across all 15 stacks)

### Simulated Slice Format (verified)

Each simulated slice is a NIfTI with shape `(256, 256, 1)` containing:
- **Data:** The model's prediction of what this slice should look like (float32, range 0-1)
- **Affine:** A unique 4×4 matrix encoding the motion-corrected pose of this slice in RAS+ world space

Example affine from slice `0.nii.gz`:
```
[[ 1.786e-01 -1.143e+00 -3.224e-01  1.234e+02]
 [ 1.076e+00  9.295e-02  7.763e-01 -1.558e+02]
 [-4.286e-01 -2.428e-01  1.815e+00  6.387e+01]
 [ 0.000e+00  0.000e+00  0.000e+00  1.000e+00]]
```

Voxel sizes vary by stack acquisition (e.g., 1.17×1.17×2.0mm for HASTE stacks).

### Implications for FetEnhNet

The per-slice affine transforms enable:
1. **Label projection:** Segment the reconstructed volume → use `inv(vol_affine) @ slice_affine` to map labels back to each raw slice
2. **Tissue conditioning:** Project 4-class tissue maps onto raw stacks for FiLM conditioning (the original runs 14-17 approach, now tractable)
3. **Quality:** Transforms are motion-corrected, so projected labels account for fetal motion between slices

### Next Steps

- Run on a subject that also has manual segmentation labels to verify projection accuracy
- Compare projected labels vs existing brain masks for alignment quality
- If accurate, batch-process all training subjects to generate tissue label overlays

## Related Tools & Alternatives

- **NiftyMIC** -- Classical SVR framework (Python)
- **SVRTK** -- SVR toolkit from King's College London
- **IRTK** -- Image Registration Toolkit
- **pyrecon** -- Python reconstruction tools

## See Also

- [[030-Projects/BCH-FetEnhNet]] -- FetEnhNet project using NeSVoR for tissue label projection
- [[030-Projects/BCH-Meeting-Minutes]] -- Group meeting context

---

*Sources: [GitHub](https://github.com/daviddmc/NeSVoR), [IEEE TMI](https://ieeexplore.ieee.org/document/10015091/), [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10287191/), [ReadTheDocs](https://nesvor.readthedocs.io/en/latest/), [MIT Thesis](https://dspace.mit.edu/bitstream/handle/1721.1/151495/xu-junshen-phd-eecs-2023-thesis.pdf)*
