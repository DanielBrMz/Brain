---
title: "FetEnhNet — Option C: Scaled Conditioning Dataset"
type: project
status: active
created: 2026-04-13
updated: 2026-04-13
tags: [fetenh-net, dataset, registration, tissue-conditioning]
related: [[fetenh-label-projection-pipeline]], [[medical-image-registration]], [[fetenh-manual-registration-guide]]
---

# FetEnhNet — Option C: Scaled Conditioning Dataset

> Scaled-up version of the manual tissue seg projection pipeline, targeting ~50 high-quality subjects for Stage 2 FiLM conditioning instead of the original 15.

## Why Option C

After investigation, we discovered the full BCH dataset has **~300-450 subjects with manual segmentations** (not the 15 I initially estimated from a narrow directory search). Source: `/home/brmz/Downloads/New MRI Pipeline Processing.xlsx`.

Scale options considered:
- **A (3 subjects)**: current automated-only result
- **B (15 subjects)**: original target + manual for failing ones (~45 min user time)
- **C (~50 subjects, chosen)**: high-quality subset, automated-first + targeted manual (~2-3 days)
- **D (~150 subjects)**: all "good" + "very good" quality, ~10 hrs manual
- **E (~300 subjects)**: everything processed, ~20 hrs manual

Option C sweet spot: 15× more than current, manageable time cost, focuses on quality.

## Candidate list

Filtered from Excel to "good" or "very good" on both recon and segmentation quality:

| Protocol | Count | Notes |
|----------|-------|-------|
| Heterotaxy | 29 | Seungyoon/Camila dirs |
| CHD_TD | 18 | Camila dir (overlaps shared location for some) |
| ASD | 26 | 67 total subjects, 26 with good recon |
| Placenta | 10 | Own structure |
| **Total** | **83** | Before path verification |

## Path locations

The key discovery: **most processed data lives in individual researcher directories**, not the shared `/neuro/users/mri.team/fetal_mri/Data/` location:

```
/neuro/labs/grantlab/research/MRI_processing/camila.rodriguez/MRI_processing/
/neuro/labs/grantlab/research/MRI_processing/seungyoon.jeong/Data/Heterotaxy/
/neuro/labs/grantlab/research/MRI_processing/victoria.hopcohen/Hydrocephalus/
```

Each researcher uses slightly different directory structures. The manifest script normalizes these.

## Pipeline

```
For each candidate subject:
  1. Verify files: recon_to31_nuc.nii, segmentation_to31_final.nii, recon.nii, raw stacks, masks
  2. Stage scanner-space NeSVoR recon (if not already)
  3. Try all automated methods, pick best Dice:
     - Binary brain shape (MSE + Powell)
     - SynthMorph affine
     - ANTs multi-start (7 rotations)
  4. If Dice ≥ 0.85 → mark as production-ready
  5. If Dice < 0.85 → queue for manual alignment
  6. Build per-slice conditioning tensors for production-ready subjects
  7. Update master manifest CSV
```

## Output structure

```
/neuro/labs/.../fetenh_net/experiments/option_c_conditioning/
├── manifest.csv                   # subj, protocol, ga, dice, method, n_slices
├── transforms/
│   └── <subj>_best.lta
├── segs_in_scanner/
│   └── <subj>_seg_in_scanner.nii.gz
├── per_slice/
│   └── <subj>/stack_<nn>_z<nn>.npz
└── gallery/
    ├── top15_contact_sheet.png
    └── <subj>_6steps.png
```

## Gallery target

After automated pipeline completes, generate 6-step gallery for the top 15 subjects by Dice. Format matches the earlier `sixstep_gallery/` outputs: raw HASTE → NeSVoR → atlas → seg on NeSVoR → projected labels → seg on raw.

## Related

- [[fetenh-label-projection-pipeline]] — upstream label projection documentation
- [[medical-image-registration]] — theory of why this is hard
- [[fetenh-manual-registration-guide]] — Option C fallback for failing subjects
- [[bch_fetenh_net]] — project memory
