---
title: "FetEnhNet — NeSVoR Re-Run & Inverse Alignment Plan"
type: plan
status: active
created: 2026-04-24
updated: 2026-04-24
tags: [fetenh-net, nesvor, inverse-alignment, compute-plan, data-pipeline]
related: [[fetenh-data-pipeline-plan]], [[fetenh-v4-dataset-strategy]], [[fetenh-inverse-alignment-pipeline]], [[fetenh-net]]
---

# NeSVoR Re-Run & Inverse Alignment — Detailed Plan

## 1. Current Data Flow Architecture

### Where does training data LIVE?

There are **three layers** of data on NFS:

```
LAYER 1: CanonicalData (read-only source of truth)
  /neuro/labs/grantlab/research/MRI_processing/CanonicalData/
  = /neuro/users/mri.team/fetal_mri/Data/  (same path, symlink)
  Contains: raw stacks, masks, recon_segmentation (atlas recon + manual seg)
  Owned by: mri.team / various researchers
  We NEVER write here.

LAYER 2: Daniel's data/ (working copy of selected subjects)
  /neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/data/
  Contains: CHD_TD (43), ASD (18), Placenta (19), Normative (1) = 81 subjects
  These are COPIES of CanonicalData subjects selected for training.
  Same directory structure (raw/, masks/, recon_segmentation/)
  This is what the v3 manifest points to via mri.team symlink paths.

LAYER 3: Daniel's experiments/ (pipeline outputs)
  /neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/experiments/
  ├── nesvor_simslices/           # 124 subjects, 79 with simulated_slices/, 0 with provenance.json
  ├── projected_labels_rawstack/  # empty (never populated)
  ├── option_c_conditioning/      # Option C outputs (old approach)
  └── subject_previews/           # 4 preview PNGs
```

### Key finding: NO subjects have provenance.json

The existing 79 NeSVoR runs used the OLD `seg_pipeline/cli.py` without `--extract-slice-transforms`. They have `simulated_slices/` but no `provenance.json`. The inverse alignment pipeline requires BOTH. **All 148 TIER_A subjects need a NeSVoR re-run with the updated CLI.**

### Where does the training code read from?

The v3 manifest uses `/neuro/users/mri.team/fetal_mri/Data/...` paths (= CanonicalData via symlink). The new v4 manifest uses `/neuro/labs/grantlab/research/MRI_processing/CanonicalData/...` paths directly. Both resolve to the same NFS location.

The training code (`dataset.py`) reads:
1. **Raw stacks:** from `stack_path` in manifest (CanonicalData)
2. **Brain masks:** from `mask_path` in manifest (CanonicalData)
3. **Tissue labels:** from `projected_labels_rawstack/{protocol}_{subject}/` in Daniel's experiments dir (Layer 3)
4. **Fallback tissue labels:** from `tissue_label_path` in manifest (3D volume in CanonicalData's recon_segmentation/)

**Strategy:** Read raw data from CanonicalData (Layer 1). Write ALL pipeline outputs to Daniel's experiments dir (Layer 3). Never write to CanonicalData.

---

## 2. Where to Save NeSVoR Re-Run Outputs

### Option A (chosen): Write to CanonicalData's recon_segmentation/

The `seg_pipeline/cli.py` writes outputs INTO the subject's `recon_segmentation/` directory by default. The new flags add:
- `recon_segmentation/simulated_slices/` — per-slice NIfTIs with spatial affines
- `recon_segmentation/provenance.json` — slice→stack mapping

**Pros:** Everything stays co-located with the subject data. The inverse alignment scripts (Steps 2-4) expect to find these adjacent to `recon.nii` and `segmentation_to31_final.nii`.

**Cons:** We write to CanonicalData, which is shared. Other researchers could be affected if we overwrite existing recon.nii. **Mitigation:** The `--from_recon` flag skips reconstruction and only generates simulated slices from the existing recon. It does NOT overwrite recon.nii.

### Option B (alternative): Write to Daniel's experiments/

Copy subject data to `experiments/nesvor_inverse_alignment/{protocol}_{subject}/` and run there.

**Pros:** Isolated, no risk to shared data.
**Cons:** 148 subjects × ~2GB each = ~300GB of copies. The inverse alignment scripts need paths adjusted per-subject.

### Decision: Option A with `--from_recon --extract-slice-transforms`

This only ADDS `simulated_slices/` and `provenance.json` to existing `recon_segmentation/` dirs. It does not modify any existing files. The `--from_recon` flag means it reads the existing `recon.nii` and re-simulates slices from it — no new reconstruction.

### Where to save inverse alignment outputs (Steps 1-4)

After NeSVoR produces `simulated_slices/` and `provenance.json`, the 4-step inverse alignment runs and produces:
- `segmentation_native.nii.gz` (Step 1)
- `segmentation_raw_slices/seg_raw_NNNN.nii.gz` (Step 2)
- `stack_space/stack_XX_{raw,simulated,segmentation,seg_rawhaste}.nii.gz` (Steps 3-4)

**These go into the subject's recon_segmentation/ directory** in CanonicalData (same as NeSVoR outputs). The files are new — they don't overwrite anything.

### Where to save final 4-class per-slice labels for training

After inverse alignment + label remapping, the per-slice 4-class labels go to Daniel's experiments dir:

```
projects/fetenh_net/experiments/projected_labels_rawstack/{protocol}_{subject_id}/
  ├── 0.nii.gz    # slice 0, uint8, values {0,1,2,3}
  ├── 1.nii.gz    # slice 1
  └── ...
```

This is where `dataset.py` already looks for them (the `_RAWSTACK_PROJ_BASE` constant).

---

## 3. Prerequisites Check

### What each TIER_A subject needs before inverse alignment

| Requirement | File | Location | Status |
|-------------|------|----------|--------|
| Reconstruction | `recon.nii` | `recon_segmentation/` | Must exist (from original pipeline run) |
| Atlas segmentation | `segmentation_to31_final.nii` | `recon_segmentation/` | Must exist (manual seg) |
| Atlas transform | `recon_to31.xfm` | `recon_segmentation/` | Must exist (or compute inverse) |
| NeSVoR simulated slices | `simulated_slices/` | `recon_segmentation/` | **NEEDS RE-RUN** (0/148 have it with provenance) |
| Provenance | `provenance.json` | `recon_segmentation/` | **NEEDS RE-RUN** (0/148 have it) |
| Raw stacks | `raw/*.nii` | session dir | Must exist |
| Brain masks | `masks/*_mask.nii` | session dir | Must exist |

### Pre-flight check script needed

Before launching NeSVoR, verify for each of the 148 TIER_A subjects:
1. `recon.nii` exists
2. `segmentation_to31_final.nii` exists
3. `recon_to31.xfm` exists (or can compute inverse from `recon_to31.xfm`)
4. At least 3 raw stacks with brain masks exist
5. `quality_assessment.csv` exists and has stacks with QA > 0.4

---

## 4. Compute Plan: 4 Servers

### Available GPUs

| Server | GPUs | VRAM | Notes |
|--------|------|------|-------|
| sejong | 3× RTX A5000 | 24GB each | Primary workstation, 14 users |
| busan | 3× RTX A5000 | 24GB each | Usually idle |
| hanyang | 2× RTX A5000 | 24GB each | Victoria may use for training |
| gangnam | 2× RTX A5000 | 24GB each | K8s master, usually idle |
| **Total** | **10 GPUs** | | |

### Job distribution strategy

NeSVoR reconstruction (with `--from_recon --extract-slice-transforms`) takes ~15-30 min per subject on one GPU. With 148 subjects and 10 GPUs:

- **148 subjects ÷ 10 GPUs = ~15 subjects per GPU**
- **15 subjects × 25 min avg = ~6 hours per GPU**
- **Wall clock: ~6-8 hours** (accounting for load imbalance)

### Job assignment

```
sejong GPU 0:  subjects 001-015 (15)
sejong GPU 1:  subjects 016-030 (15)
sejong GPU 2:  subjects 031-045 (15)
busan GPU 0:   subjects 046-060 (15)
busan GPU 1:   subjects 061-075 (15)
busan GPU 2:   subjects 076-090 (15)
hanyang GPU 0: subjects 091-105 (15)
hanyang GPU 1: subjects 106-118 (13)
gangnam GPU 0: subjects 119-133 (15)
gangnam GPU 1: subjects 134-148 (15)
```

### Execution plan

1. Generate per-GPU shell scripts: `run_nesvor_sejong_gpu0.sh`, etc.
2. Each script:
   ```bash
   export CUDA_VISIBLE_DEVICES=0  # or 1, 2
   for SUBJECT_DIR in <list of subject session paths>; do
     echo "[$(date)] Starting $SUBJECT_DIR"
     python3 /neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py \
       --from_recon --extract-slice-transforms \
       -i "$SUBJECT_DIR"
     echo "[$(date)] Done $SUBJECT_DIR"
   done
   ```
3. Launch all 10 scripts via SSH with nohup
4. Monitor via shared status CSV or log files

### Timing

- **Best case:** Friday evening → Saturday morning (overnight, all GPUs free)
- **Check `nvidia-smi`** on all 4 servers before launching
- **Do NOT use hanyang GPU 1** if Victoria is training

---

## 5. After NeSVoR: Inverse Alignment Batch

Once NeSVoR completes (simulated_slices/ + provenance.json exist), run the 4-step pipeline:

### CPU-only, can run on sejong with 12 workers

Steps 1-4 are CPU operations (FSL flirt, numpy resampling). No GPU needed. Can parallelize across CPU cores.

**Estimated time:** ~2 min per subject × 148 subjects ÷ 12 workers = ~25 minutes

### Step-by-step per subject

```python
for subject in tier_a_subjects:
    session_path = subject["session_path"]
    recon_seg = session_path / "recon_segmentation"

    # Step 1: Atlas → Native (FSL flirt)
    run_fsl_flirt(
        input=recon_seg / "recon_to31_nuc_deep_agg.nii",  # or segmentation_to31_final.nii
        ref=recon_seg / "recon.nii",
        init=recon_seg / "alignment_temp/recon_to31_inv.xfm",  # compute if missing
        interp="nearestneighbour",
        output=recon_seg / "segmentation_native.nii"
    )

    # Step 2: Native → Simulated Slices (Yair's script)
    resample_to_raw_space(
        segmentation=recon_seg / "segmentation_native.nii",
        recon=recon_seg / "recon.nii",
        simulated_slices_dir=recon_seg / "simulated_slices/",
        output_dir=recon_seg / "segmentation_raw_slices/"
    )

    # Step 3: Simulated Slices → Stacks (Yair's script)
    map_to_stacks(
        raw_slices_dir=recon_seg / "segmentation_raw_slices/",
        provenance=recon_seg / "provenance.json",
        stack_dir=session_path / "best_images_crop/",  # or raw/ depending on stack type
        output_dir=recon_seg / "stack_space/"
    )

    # Step 4: Crop → Raw HASTE (Yair's script, with affine bug fix)
    resample_to_rawhaste(
        stack_space_dir=recon_seg / "stack_space/",
        output: stack_XX_seg_rawhaste.nii.gz
    )

    # Step 5: Remap FeTA labels → 4-class
    remap_labels(
        input: recon_seg / "stack_space/stack_XX_segmentation.nii.gz",  # or seg_rawhaste
        mapping: {1:1, 42:1, 160:2, 161:2, 18:3},  # FeTA → 4-class
        output: experiments/projected_labels_rawstack/{proto}_{subject}/{slice_idx}.nii.gz
    )
```

---

## 6. Validation After Pipeline

For each subject, verify:
1. `simulated_slices/` has N files matching raw stack slice count
2. `provenance.json` has entries for all simulated slices
3. `stack_space/` has one segmentation per input stack
4. Tissue labels have all 4 classes present (at least in some stacks)
5. Coverage: >80% of brain voxels have non-zero labels

Automated check + visual spot-check on 10% of subjects.

---

## 7. Summary: What Goes Where

| Data | Location | Read/Write | Shared? |
|------|----------|-----------|---------|
| Raw stacks, masks | CanonicalData (Layer 1) | Read only | Yes |
| Manual segmentations | CanonicalData recon_segmentation/ | Read only | Yes |
| NeSVoR simulated_slices + provenance | CanonicalData recon_segmentation/ | **Write (new files only)** | Yes |
| Inverse alignment intermediates | CanonicalData recon_segmentation/ | **Write (new files only)** | Yes |
| Per-slice 4-class labels | Daniel's experiments/ | Write | No (Daniel only) |
| Training manifests | Daniel's data_pipeline/outputs/ | Write | No |
| Model checkpoints | Daniel's projects/fetenh_net/checkpoints/ | Write | No |

---

## Related

- [[fetenh-inverse-alignment-pipeline]] — Yair's 4-step pipeline details
- [[fetenh-data-pipeline-plan]] — Overall pipeline phases
- [[fetenh-v4-dataset-strategy]] — How the outputs feed into training
- [[fetenh-net]] — Main project
