---
title: "FetEnhNet -- Comprehensive Data Inventory"
type: reference
status: active
created: 2026-04-14
updated: 2026-04-14
tags: [fetenh-net, data, inventory, canonical-data]
related: [[fetenh-data-knowledge-graph]], [[fetenh-data-methodology]]
---

# FetEnhNet -- Comprehensive Data Inventory

> Combined audit of NFS CanonicalData + Excel QA spreadsheet (New MRI Pipeline Processing.xlsx).
> Generated 2026-04-14.

## Per-protocol detail

### Heterotaxy

| Source | Count |
|--------|-------|
| Excel subjects | 160 |
| Excel Processed | 121 |
| NFS CanonicalData (Case) | 37 |
| NFS complete (seg+atlas+raw+masks) | 31 |

- GA range: 21-37 weeks (mean 30.8)
- Recon quality: 63 good/very good, 48 fair, 38 bad
- Seg quality: 57 good, 37 fair, 13 bad, 12 very bad
- Processed by: Camila, Seungyoon, others
- Case/Control: Excel mixes Gender and Case/Control columns (data quality issue)
- NFS location: `CanonicalData/Heterotaxy/Case/BCH_fetal_HTX_###/VISIT_##/`

### CHD

| Source | Count |
|--------|-------|
| Excel CHD_TD_onlySP | 197 |
| Excel CHD_TD_onlySP_2 | 243 |
| Excel Case/Control split | 118 Control, 57 Case |
| NFS Data/ | 268 |
| NFS Data_NeSVoR/ | 124 |
| NFS complete with segs (Data/) | 116 |
| NFS complete with segs (Data_NeSVoR/) | 120 |
| In current training manifest | 93 |
| Training subjects with manual segs | 43 |

- GA range: 20.0-38.7 weeks (mean 29.8)
- Gender: 82 Male, 56 Female, 2 Unknown
- 155 subjects have multiple sessions (longitudinal)
- New Status (automatic process): 119 Processed, 1 Failed
- NFS location: `CanonicalData/CHD_protocol/Data/FCB###/session/`

### Segmentation Corrections (tracked separately)

33 subjects tracked for segmentation quality corrections. Processed by: Victoria (10), Daniel (3), Yair (2), Suzette (2). Located in `CanonicalData/CHD_protocol/Data_NeSVoR/`.

### ASD

| Source | Count |
|--------|-------|
| Excel subjects | 61 |
| Excel ASD confirmed | 52 yes, 4 likely, 4 no |
| Excel Processed | 54 |
| NFS CanonicalData | 58 |
| NFS complete with segs | 48 |
| In current training manifest | 6 |
| In Daniel's data/ dir | 18 |

- GA range: 19.1-38.4 weeks (mean 28.1)
- Gender: 43 Male, 17 Female (3.5:1 ratio, consistent with ASD prevalence)
- Recon quality: 15 good, 9 very good, 17 fair, 7 bad
- Multiple scans: 7 subjects with 2nd scan, 1 with 3rd, 1 with 4th
- NFS location: `CanonicalData/ASD/<MRN>/<session>/`

### Placenta

| Source | Count |
|--------|-------|
| Excel subjects | 42 |
| Excel Processed | 17 |
| Excel good quality (new model) | 10 |
| NFS Data/ | 269 |
| NFS Data_NeSVoR/ | 8 |
| NFS complete with segs | 6 |
| In current training manifest | 14 |

- GA range: 24.6-32.0 weeks (mean 29.0)
- Subject Group: 38 Control
- Fetuses: mostly Singleton
- NFS location: `CanonicalData/Placenta_protocol/Data_NeSVoR/<MRN>/<session>/`

### Hydrocephalus / Spina Bifida

| Source | Count |
|--------|-------|
| Excel subjects | 40 |
| Excel Processed | 10 |
| NFS SpinaBifida | 63 subjects, 0 with segs |
| NFS Victoria dir | 40 entries, 0 complete |

- GA range: 17.9-38.3 weeks (mean 23.3, younger cohort)
- Acquisition: HASTE
- High failure rate (17 Failed vs 10 Processed)
- Not usable for FetEnhNet tissue conditioning (no segs)

### dHCP

| Source | Count |
|--------|-------|
| Excel subjects | 155 |
| Excel correct (final decision) | 149 |
| T2 SVR QC | mean 3.8/4.0 |

- GA range: 21.1-32.0 weeks (mean 27.7)
- External dataset (Developing Human Connectome Project)
- Uses 87-label DrawEM segmentation scheme (NOT our 4-class atlas)
- Has diffusion data (bval/bvec), SNR, translation, rotation metrics
- Not directly compatible with our pipeline without label remapping

## Grand summary

### Available data

| Protocol | NFS subjects | Complete (seg+atlas+raw) | In training manifest | In training WITH segs |
|----------|-------------|--------------------------|---------------------|----------------------|
| CHD | 268 | 116 | 93 | 43 |
| ASD | 58 | 48 | 6 | ? |
| Heterotaxy | 37 | 31 | 0 | 0 |
| Placenta | 269 | 6 | 14 | ? |
| VM | 133+ | 0 segs | 51 | 0 |
| Normative | 127 | 0 segs | 47 | 0 |
| Hydrocephalus | 63 | 0 segs | 0 | 0 |
| dHCP | 155 | incompatible | 0 | 0 |
| DownSyndrome | small | 0 segs | 1 | 0 |
| **Total** | **~892** | **201** | **212** | **43** |

### Gap analysis

- 201 subjects have manual tissue segmentations in CanonicalData
- Current training manifest has 212 subjects but only 43 have manual segs
- 158 subjects with manual segs are NOT in the training set at all
- The training set uses only 15% of available data (136 of 892 subjects in Daniel's data/ dir)
- Ventriculomegaly (51 training subjects) and Normative (47 training subjects) have ZERO manual segs

### What this means

1. The training set can be expanded significantly by including subjects from CanonicalData that have segs but aren't in the manifest
2. The overfitting (memorization by epoch 12) is partly explained by using only 212 unique anatomies when 892 exist
3. Tissue conditioning can be applied to 201 subjects if registration succeeds, vs the current 43
4. VM and Normative protocols contribute 98 training subjects with NO tissue conditioning possible (no segs exist)

## QA spreadsheet details

Source: `/home/brmz/Downloads/New MRI Pipeline Processing.xlsx`

| Sheet | Purpose | Key columns |
|-------|---------|-------------|
| Heterotaxy | HTX processing tracker | Study ID, GA, Recon/Seg quality, Status, By |
| Hydrocephalus | SB/Hydro tracker | Sub, GA, Recon, Status |
| ASD | Clinical + processing | PATIENT, ASD confirmed, GA, Gender, Recon quality, Status |
| dHCP | External dataset QC | subject_id, t2_svr_qc, GA_scan, final decision |
| CHD_TD | Original CHD (small set) | Subject, Case/Control, Recon/Seg quality |
| CHD_TD_onlySP | CHD expanded (197 subj) | Subject, GA, Case/Control, Gender, Maternal age/education |
| CHD_TD_onlySP_2 | CHD largest (243 subj) | Subject, GA, Case/Control, Gender, Recon quality |
| Segmentation Corrections | NeSVoR seg QC | Subject, Group, NeSVoR status, By |
| Placenta_TD | Placenta tracker | MAP ID, BCH MRN, Subject Group, GA, Status |
| Sheet2 | Placenta extended | MRN, Subject Group, GA, Fetal sex, Status |
| Reference | Color coding legend | Status labels |
| Sheet6 | HTX subject list | BCH_fetal_HTX IDs |

## Raw stack counts (from NFS ls scan)

| Protocol | Subjects with raw | Total raw stacks | Has manual seg |
|----------|------------------|-----------------|----------------|
| CHD | 230/264 | 4,010 | 116 |
| Placenta | 169/269 | 1,641 | 6 |
| Normative | 120/120 | 1,426 | 0 |
| ASD | 53/56 | 837 | 48 |
| HBCD | 29/37 | 600 | 0 |
| SpinaBifida | 40/45 | 584 | 0 |
| Heterotaxy | 32/37 | 367 | 31 |
| TMC | 0/25 | 0 | 0 |
| **Total** | **673** | **9,465** | **201** |

Current training set uses ~1,300 unique stacks from 212 subjects. CanonicalData has 9,465 stacks from 673 subjects.

## Excel vs NFS gap analysis

| Protocol | Excel Processed | NFS Complete | Gap | Explanation |
|----------|----------------|-------------|-----|-------------|
| Heterotaxy | 138 | 31 | 107 | In researcher dirs (Camila, Seungyoon), not moved to CanonicalData |
| CHD | 119 | 116 | 3 | Nearly 1:1. 93 more went through pipeline but never manually segmented |
| ASD | 54 | 48 | 6 | Minor gap, probably "recheck" status |
| Placenta | 19 | 6 | 13 | Segs in non-standard locations (raw/ dir, old pipeline) |
| Hydrocephalus | 11 | 0 | 11 | Victoria's WIP, incomplete processing |
| dHCP | 149 | 0 | 149 | Incompatible 87-label DrawEM scheme |
| **Total** | **~391** | **201** | **~190** | |

Biggest recoverable gap: 107 Heterotaxy subjects processed per Excel but not in CanonicalData. These are likely in Camila's or Seungyoon's researcher directories.

## Excel vs NFS Deep Audit (Apr 25)

Cross-referencing `New MRI Pipeline Processing.xlsx` with actual `segmentation_to31_final.nii` on NFS. "Processed" in Excel means pipeline ran (mask+QA+recon), NOT that manual segmentation was completed.

### Heterotaxy gap: 104 "Processed" missing segs

Excel says 138 processed. CanonicalData has 34 with seg. Seungyoon's dir (`/neuro/.../seungyoon.jeong/Data/Heterotaxy/`) has 46 subjects (44 unique, 2 overlap) but only **7 have segmentation_to31_final.nii**. Abraham processed 82 subjects per Excel but most only went through the automated pipeline — manual seg was never done.

**Recoverable:** 7 from Seungyoon (TIER_A candidates).

### Placenta gap: 2 misplaced segs

Two Placenta subjects have `segmentation_to31_final.nii` in `raw/` instead of `recon_segmentation/`:
- `2159609/MR-EI_Fetal_Body-25064318-20171102/raw/`
- `5112581/MR-EI_Fetal_Body-25015739-20170905/raw/`

**Recoverable:** 2 (copy seg to correct location).

### ASD: mostly accounted for

Excel 54, NFS 48. Suzette's dir has 52 with seg but mostly overlap with CanonicalData.

### Summary of recoverable subjects for TIER_A

| Source | Additional subjects with seg |
|--------|----------------------------|
| Seungyoon HTX | 7 |
| Placenta misplaced | 2 |
| Seungyoon unique HTX (no seg yet but have recon) | 37 (need manual seg) |
| **Immediately recoverable** | **~9** |

## Related

- [[fetenh-data-knowledge-graph]] -- Directory structure and processing status
- [[fetenh-data-methodology]] -- Qualitative-first processing approach
- [[fetenh-data-pipeline-plan]] -- v4 pipeline plan with Phase 1-5 results
- [[fetenh-net]] -- Main project
