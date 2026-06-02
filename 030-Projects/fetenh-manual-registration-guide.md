---
title: "FetEnhNet — Manual Registration Guide (Option C)"
type: guide
status: active
created: 2026-04-13
updated: 2026-04-13
tags: [fetenh-net, registration, itk-snap, manual, guide]
related: [[fetenh-label-projection-pipeline]], [[medical-image-registration]]
---

# Manual Registration Guide — Atlas → Scanner-NeSVoR

> Fallback for subjects where automated registration (SynthMorph, ANTs multi-start) fails to produce Dice ≥ 0.85 for the FetEnhNet training conditioning pipeline.

## Goal

Produce a **correct** 4×4 affine matrix that maps a subject's atlas-space segmentation (`segmentation_to31_final.nii`) onto the scanner-space NeSVoR recon (`CHD_TD_<subj>_scanner_space/recon.nii.gz`) for use as FiLM conditioning in the final FetEnhNet training run.

## Why manual

When orientation differences between atlas and scanner frames exceed the convergence radius of automated methods, we need human initialization. ITK-SNAP's "Registration" panel provides interactive nudging — you click and drag to roughly align, and the underlying optimizer refines.

## Tools

- **ITK-SNAP 4.0+** (recommended) — on Arch: `yay -S itk-snap-bin` or download from [itksnap.org](http://www.itksnap.org)
- **Alternative**: `fsleyes` (FSL), `slicer` (3D Slicer) — all support manual registration

## Subjects list (after all automated methods tried, 2026-04-13)

Subjects ready without manual work (best-of-3 automated approach):
- ✅ **FCB033** (Binary+flip_k, Dice=0.90)
- ✅ **FCB215** (Binary+flip_k, Dice=0.88)
- ✅ **FCB242** (ANTs, Dice=0.87)
- ⚠️ **FCB094** (ANTs, Dice=0.69) — borderline, may want manual refinement

Subjects that need manual registration (all automated methods failed):

| Subject | Best auto Dice | Notes |
|---------|---------------|-------|
| FCB014  | 0.0003 | all three methods fail |
| FCB018  | 0.06 | all three fail |
| FCB040  | 0.02 | all three fail |
| FCB056  | 0.28 | all three low |
| FCB068  | 0.16 | all three low |
| FCB105  | — | SynthMorph OOB, ANTs untested |
| FCB160  | — | SynthMorph OOB, ANTs untested |
| FCB193  | — | SynthMorph OOB, ANTs untested |

**Priority order** (by data importance):
1. FCB014, FCB018, FCB040, FCB056, FCB068 — these have clean NeSVoR recons; manual work should succeed
2. FCB105, FCB160, FCB193 — need investigation first (may have data quality issues)
3. FCB094 — optional refinement to get Dice > 0.85

## File paths on sejong

```
/neuro/users/mri.team/fetal_mri/Data/CHD_protocol/Data/<SUBJ>/<SESS>/recon_segmentation/
  ├── recon_to31_nuc.nii              # atlas recon (MOVING image for registration)
  ├── segmentation_to31_final.nii     # manual seg (to be warped)
  └── recon_to31.xfm                  # known pipeline↔atlas transform

/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/experiments/nesvor_simslices/
  └── CHD_TD_<SUBJ>_scanner_space/recon.nii.gz   # scanner-space NeSVoR (FIXED image)
```

Session name for each subject in `~/Brain/030-Projects/fetenh-label-projection-pipeline.md`.

## Workflow per subject

### Step 1: Copy files locally

```bash
# Copy both recons to a local working dir so ITK-SNAP isn't slow over NFS
mkdir -p ~/fetenh_manual/FCB014
rsync -av sejong:/neuro/users/mri.team/fetal_mri/Data/CHD_protocol/Data/FCB014/<sess>/recon_segmentation/{recon_to31_nuc.nii,segmentation_to31_final.nii} ~/fetenh_manual/FCB014/
rsync -av sejong:/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/experiments/nesvor_simslices/CHD_TD_FCB014_scanner_space/recon.nii.gz ~/fetenh_manual/FCB014/
```

### Step 2: Open ITK-SNAP

```bash
itk-snap -g ~/fetenh_manual/FCB014/recon.nii.gz
# Then: Tools → Registration → Load Moving → select recon_to31_nuc.nii
```

### Step 3: Interactive alignment

In ITK-SNAP's Registration panel:

1. **Switch to interactive mode** (Registration tab → Interactive)
2. **Use the 3D crosshair** to identify corresponding landmarks:
   - Centroid of the brain in both images
   - Approximate AP axis (brain stem direction)
   - L/R orientation (which side has which features)
3. **Rotate the moving image** with left-click drag on each orthogonal view until it roughly overlays the fixed image
4. **Translate** with middle-click drag to fine-tune position
5. Aim for visually-close overlap — doesn't need to be perfect

### Step 4: Automated refinement

1. **Switch to Automatic mode** (Registration tab → Automatic)
2. **Transformation model**: Affine (12 DoF)
3. **Similarity metric**: Mutual Information
4. **Multi-resolution**: 4 levels
5. Click **Run**
6. Wait ~30-60 seconds for convergence
7. **Review** — check 3 orthogonal views for good alignment

### Step 5: Save the transform

```
Registration panel → Save Transform → ITK transform file (.txt)
Save as: FCB014_atlas_to_scanner_manual.txt
```

### Step 6: Validate the transform

Upload back to sejong and apply to seg:

```bash
scp ~/fetenh_manual/FCB014/FCB014_atlas_to_scanner_manual.txt sejong:/neuro/labs/grantlab/.../presentation/manual_transforms/

# On sejong, apply to seg with SimpleITK (Python):
# See apply_manual_transform.py script in scripts/
```

Check the output seg's Dice vs. brain mask. Target: ≥ 0.85.

If below 0.85, re-open in ITK-SNAP and refine further. Usually 2-3 iterations gets you there.

## Tips for hard cases

- **Fetal brains are small** — zoom in close for fine-tuning
- **Use the linked cursors** — ITK-SNAP keeps crosshairs in sync across windows
- **Try Rigid first, then Affine** — if the automated MI registration oscillates, save the rigid result, load as initial for affine
- **Brain masks help** — you can load brain masks as overlays to visually guide alignment
- **GA matters** — if the brain in the recon looks very different from the 31-week atlas (e.g., subject is 25 weeks), expect more work; the shape is genuinely different

## Output format

For FetEnhNet training integration, each subject needs:

```
<PROJ>/experiments/manual_seg_conditioning/
├── FCB014/
│   ├── transform.txt              # the validated affine transform
│   ├── seg_in_scanner.nii.gz      # warped seg in scanner space
│   ├── dice_per_stack.json        # Dice vs brain mask for each raw stack
│   └── per_slice/
│       ├── stack_001_z010.npz     # seg projection per brain-containing slice
│       └── ...
├── FCB018/
│   └── ...
```

Manifest: `experiments/manual_seg_conditioning/manifest.csv` with columns:
`subject, stack, slice_z, dice, n_brain_voxels, validated`

Only rows with `validated=True AND dice >= 0.85` go into training.

## Time budget

- Per subject: 15-30 minutes (mostly interactive alignment)
- ~6 failing subjects → 1.5-3 hours total
- Alternative: batch in evening sessions, 2-3 subjects per sitting

## Related

- [[fetenh-label-projection-pipeline]] — overall label projection pipeline
- [[medical-image-registration]] — theory of why automated methods fail
- [[bch_fetenh_net]] (memory) — FetEnhNet project context
