---
title: "FetEnhNet -- Data Knowledge Graph"
type: reference
status: active
created: 2026-04-14
updated: 2026-04-14
tags: [fetenh-net, data, dataset, canonical-data, cohorts, knowledge-graph]
related: [[fetenh-net]], [[fetenh-label-projection-pipeline]], [[fetenh-option-c-dataset]]
---

# FetEnhNet -- Data Knowledge Graph

> Complete map of all data available for FetEnhNet training, from source through cohort assignment to final validated conditioning dataset. Every subject passes through human-supervised visual confirmation before inclusion.

---

## 1. Data sources

### 1.1 CanonicalData (primary)

Location: `/neuro/labs/grantlab/research/MRI_processing/CanonicalData/`

**Verified counts (2026-04-14, ls-based scan):**

| Protocol | Subjects in Data/ | Has seg | Complete (seg+atlas+raw+masks) | Structure |
|----------|-------------------|---------|-------------------------------|-----------|
| CHD_protocol | 266 | 116 | **116** | Data/FCB###/session/recon_segmentation/ |
| Heterotaxy | 37 (Case only) | 33 | **31** | Case/BCH_fetal_HTX_###/VISIT_##/ |
| Placenta_protocol | 269 | 6 | **6** | Data/MRN/session/ |
| Normative | 127 | 0 | 0 | Has Data/ but no segs yet |
| HBCD | 61 | 0 | 0 | Has Data/ but no segs yet |
| ASD | ~65 (flat) | 48 | **48** | Flat: MRN/session/recon_segmentation/ (no Data/ subdir) |
| dHCP | complex | 0* | 0* | External dataset, different structure |
| TMC_data | 32 | 0 | 0 | |
| **Total actionable** | | **203** | **201** | |

*SpinaBifida has 63 subjects but 0 segs. Hydrocephalus (Victoria's dir) has 40 entries but non-standard structure. dHCP has segs but in non-standard structure.

**201 unique subjects (first-session only) are immediately processable** via standard `recon_segmentation/` path.

**Deep scan (find-based, all sessions, all depths) reveals more:**

| Protocol | Complete sessions (find) | Notes |
|----------|------------------------|-------|
| CHD | 1,371 | Multiple sessions per subject (155 subjects have >1) |
| Placenta | 316 | Segs in non-standard subdirs (not in `recon_segmentation/`) |
| HBCD | 108 | Segs at deeper paths |
| Backup | 81 | Old data, may overlap with active protocols |
| ASD | 65 | Includes multi-session |
| Heterotaxy | 38 | Includes multi-visit |
| Normative | 13 | At deeper paths |
| dHCP | 0 complete (424 seg-only) | Has segs but no raw+masks in same tree |

**Correction (2026-04-14 deep audit):** The find-based counts were inflated:
- **HBCD 108**: FALSE. Structure is flat (no session layer). `recon_segmentation/` exists but contains no `segmentation_to31_final.nii`. Zero usable segs.
- **Placenta 316**: MOSTLY FALSE. Inflated by segs in `raw/` (misplaced files) and duplicates across Data/ and Data_NeSVoR/. Actual usable: still 6 in Data_NeSVoR/.
- **CHD 1,371**: Inflated by multiple sessions per subject and segs in Data_NeSVoR/ (120 subjects). Real unique: ~160 subjects (116 Data/ + ~44 unique in Data_NeSVoR/).
- **Backup 81**: Old/duplicate copies. Should not be used (risk of stale data).

**True count remains ~201 unique complete subjects.**

### 1.2 Researcher directories (secondary)

Data processed by individual researchers, may overlap with CanonicalData:

| Location | Researcher | Protocols | Status |
|----------|-----------|-----------|--------|
| `/neuro/labs/.../camila.rodriguez/MRI_processing/` | Camila Rodriguez | CHD, Heterotaxy | Active, some subjects not in CanonicalData |
| `/neuro/labs/.../enrique.mondragon/morton_lab/abraham.urena/heterotaxy/` | Abraham Urena | Heterotaxy controls | 28 subjects with segs |
| `/neuro/labs/.../fernanda.elizondo/MRI_processing/` | Fernanda Elizondo | CHD | Some unique subjects |
| `/neuro/labs/.../victoria.hopcohen/Hydrocephalus/` | Victoria Hop Cohen | Hydrocephalus | 11 processed |
| `/neuro/labs/.../seungyoon.jeong/Data/` | Seungyoon Jeong | Heterotaxy, SpinaBifida | Processing data |

### 1.3 Shared pipeline data

Location: `/neuro/users/mri.team/fetal_mri/Data/`

| Protocol | Subjects | Notes |
|----------|----------|-------|
| CHD_protocol/Data | ~264 | Mirrors CanonicalData but different path, has recon_segmentation/ |
| ASD_protocol/Data | ~67 | ASD subjects with clinical metadata |

### 1.4 QA spreadsheet

Location: `/home/brmz/Downloads/New MRI Pipeline Processing.xlsx`

Sheets: Heterotaxy, Hydrocephalus, ASD, dHCP, CHD_TD, Segmentation Corrections, CHD_TD_onlySP, CHD_TD_onlySP_2, Placenta_TD

Contains: subject IDs, GA, recon quality ratings, segmentation quality ratings, processing status, paths.

---

## 2. Data preparation methodology: qualitative-first, human-supervised

### Philosophy

The researcher (Daniel) is the primary decision maker at every stage. Automation assists but never decides. Quantitative metrics document what the human approved, they do not replace visual inspection.

### Stage A: Subject selection and cohort assignment

**Human decides:**
- Which subjects to include (from QA spreadsheet + CanonicalData listing)
- Which cohort each belongs to (CHD control, CHD case, Heterotaxy, Placenta, Normative, etc.)
- Whether the QA ratings are trustworthy (recon quality, seg quality)

**Inputs:** QA spreadsheet, CanonicalData directory listing
**Output:** Selected subject list with cohort labels

### Stage B: Raw data quality verification

**Human decides:**
- Are the raw HASTE stacks usable? (sufficient brain coverage, acceptable motion)
- Does the brain mask exist and look reasonable?
- Is the atlas seg anatomically correct for this subject?

**Inputs:** Raw .nii files, mask .nii files, segmentation_to31_final.nii
**Output:** Verified subject list (subset of Stage A)

### Stage C: Alignment

**Automation proposes:**
- NeSVoR scanner-space reconstruction
- Binary brain shape registration + 8-flip search
- Proposed overlay with Dice score

**Human decides:**
- Does the proposed overlay match the anatomy?
- If yes: approve, move to Stage D
- If no: manual correction via GUI, then re-inspect

**Inputs:** Scanner-space NeSVoR recon, atlas seg, proposed transform
**Output:** Approved transform per subject

### Stage D: Quantitative confirmation

**Automation computes:**
- Dice vs brain mask for each raw stack
- Per-slice brain coverage metrics
- Overlay images for documentation

**Human reviews:**
- Are the Dice values consistent with the visual assessment?
- Any stacks with unexpectedly low Dice? (may indicate a bad stack, not a bad registration)

**Output:** Per-subject Dice scores, per-stack quality flags

### Stage E: Manifest generation

**Automation builds:**
- CSV with (subject, cohort, stack, slice, dice, brain_voxels, approved_by, approval_date)
- Per-slice .npz conditioning tensors

**Human reviews:**
- Final count per cohort
- Distribution of GA, quality, and Dice across the dataset
- Any cohort imbalances that need addressing

**Output:** The final training manifest

---

## 3. Per-protocol processing status

### CHD_protocol (primary, 116 complete)

- 266 subjects in Data/, 124 in Data_NeSVoR/
- 116 with seg + atlas + raw + masks (ready to process)
- 209 have recon_segmentation/ but 93 lack the seg file
- Scanner-space NeSVoR completed: ~46 subjects (need ~70 more)
- Automated registration completed: 25 (Dice >= 0.80)
- Visually confirmed: 0 (pending human review)

### Heterotaxy (31 complete)

- 37 Case subjects in CanonicalData/Heterotaxy/Case/
- 31 complete with seg + atlas + raw + masks
- No Control directory in CanonicalData (controls are in researcher dirs)
- Registration completed: ~20 from Option C batch
- Visually confirmed: 0

### Placenta_protocol (6 complete)

- 269 subjects in Data/, only 6 with segs
- Large pool of subjects but very few have been segmented
- NeSVoR: 8 subjects
- Registration: not yet attempted on these 6

### ASD (48 complete)

- ~65 subjects in flat MRN/session/ structure (no Data/ subdir)
- 48 complete with seg + atlas + raw + masks in standard recon_segmentation/
- Flat structure: `CanonicalData/ASD/<MRN>/<session>/recon_segmentation/`
- No NeSVoR runs yet

### dHCP (needs investigation)

- External dataset, different acquisition protocol
- 424 segs found but in non-standard structure
- Needs compatibility check: same 31-week atlas? Same label convention?

### Normative (no segs yet)

- 127 subjects in Data/, 0 with segs
- Could be processed if manual segmentation is done upstream

### HBCD (no segs yet)

- 61 subjects in Data/, 0 with segs in standard location
- Needs investigation

---

## 4. Full content audit per protocol

### CHD_protocol

Top-level: `Data/`, `Data_NeSVoR/`, `Data_IRTK/`, `Genetic_data/`, `older/`

**Data/** (266 subjects, 155 with multiple sessions):
Per session contains: `raw/`, `masks/`, `brain/`, `nuc/`, `verify/`, `recon_segmentation/`, `quality_assessment.csv`

- `raw/`: Raw HASTE .nii stacks (~10-25 per session)
- `masks/`: Brain masks per stack (`*_mask.nii`)
- `brain/`: Brain-extracted versions (`*_brain.nii`)
- `nuc/`: Non-uniformity corrected + `Best_Images_crop/`
- `verify/`: Cropped brain + verification PNGs
- `quality_assessment.csv`: Per-stack quality scores + slice thickness
- `recon_segmentation/`: Pipeline outputs (see structure below)

**Data_NeSVoR/** (124 subjects): Same session structure as Data/ but processed through NeSVoR pipeline. Contains `surfaces/` in addition.

**Data_IRTK/** (259 entries): Legacy IRTK reconstructions. Contains scripts and old-format data. Not directly usable.

**older/**: Spreadsheets, failed/pending processing logs, old alignments. Archive material.

### ASD

Flat structure: `<MRN>/<session>/`. No `Data/` subdirectory. 58 subjects, 6 with multiple sessions.

Per session: `raw/`, `masks/`, `brain/`, `nuc/`, `verify/`, `recon_segmentation/`, `quality_assessment.csv`, `best_images_crop/`, plus DTI-related `.bval`/`.bvec` files at session root and `Json/`, `TRUFSIP/` dirs.

48 subjects have complete seg + atlas + raw + masks.

### Heterotaxy

Structure: `Case/<BCH_fetal_HTX_###>/<VISIT_##>/`. Only Case dir exists (37 subjects, no Control dir in CanonicalData; controls are in researcher dirs).

Per visit: Same structure as CHD (raw, masks, brain, nuc, verify, recon_segmentation, quality_assessment.csv). Also has `surfaces/` and `temp/`.

31 complete subjects.

### Placenta_protocol

Top-level: `Data/`, `Data_NeSVoR/`, `Data_IRTK/`, `old_placenta_work/`, `scripts/`, `Twin/`

**Data/** (269 subjects): Most have only `raw/` dir. Very few have been through the full pipeline. 2 subjects have segs in `raw/segmentation_to31_final.nii` (non-standard location).

**Data_NeSVoR/** (8 subjects): 6 have complete pipeline (seg + atlas + raw). These are the 6 processable Placenta subjects.

**Twin/** (6 entries): Corrected/Done/Failed/Pending/Raw subdirs. Twin pregnancies, separate processing.

### SpinaBifida

63 subjects in flat `<MRN>/<session>/` structure. Sessions contain mostly `.json` sidecar files at root level. Has `raw/` with .nii files and `recon_segmentation/` with pipeline output BUT **no segs** (`segmentation_to31_final.nii` absent). Has atlas recon (`recon_to31_nuc.nii`) in some. The pipeline was run but manual segmentation was never done.

### Hydrocephalus (Victoria's dir)

40 entries, most suffixed `_test`. Flat `<MRN_test>/<session>/` structure. Has `recon_segmentation/` for some but no segs and no raw/masks directories. These are test/WIP processing, not finished subjects.

### Normative

127 subjects in `Data/<MRN>/<session>/`. Sessions have legacy AFNI files (`afni_recon+acpc.BRIK`, `.HEAD`), `brain/`, `Best_Images_crop/`, `.mnc` files. No `segmentation_to31_final.nii` found. These subjects were processed with an older pipeline and never manually segmented.

### dHCP

External dataset. Complex structure with subdirectories for recons, labels, hemisphere masks, atlas data. Uses 87-label DrawEM segmentation scheme (different from our 4-class atlas). Subject dirs like `sub-CC00861XX12_ses-43210/`. Not directly compatible with our pipeline without label remapping investigation.

### HBCD

61 subjects in `Data/`. Structure needs deeper audit. No segs in standard location.

### Other empty/archive protocols

- `Abnormal_postnatally_confirmed/`, `Ali_Lana/`, `Ashok_data/`, `Brain_age/`, `CHP_data/`, `Clinical_data/`, `Denver/`, `EarlyMR_data/`, `FeTA_data/`, `FetalPost_AbnormalBrain_longitudinal/`, `Longitudinal_Sungmin/`, `NICU_GRADS/`, `Public_data/`, `TMC_data/`, `VGH_data/`: No processable data for our pipeline (no seg + atlas + raw combinations).

- `Brain_malformation/`: Contains CSV metadata and subdirs by pathology type (Lissencephaly, Macrocephaly, Microcephaly, Polymicrogyria). Potentially interesting for future work but no standard pipeline output.

- `Backup_or_unused/`: Contains dated backups, FeTA_data copies, old longitudinal data, processing logs.

- `Camilo_CDH/`: Congenital diaphragmatic hernia. Has atlas recons (207) but no segs.

---

## 5. Directory structure per subject

Standard layout in CanonicalData:

```
CanonicalData/<protocol>/Data/<subject_id>/<session>/
├── raw/                           # Raw HASTE stacks
│   ├── T2_HASTE_*.nii
│   └── CERVIX_T2_HASTE_*.nii
├── masks/                         # Brain masks per stack
│   ├── T2_HASTE_*_mask.nii
│   └── CERVIX_T2_HASTE_*_mask.nii
└── recon_segmentation/            # Pipeline outputs
    ├── recon.nii                  # Pipeline reconstruction (NOT scanner coords)
    ├── recon_to31_nuc.nii         # Atlas-aligned reconstruction
    ├── recon_to31.xfm             # Pipeline-to-atlas transform (4x4 affine)
    └── segmentation_to31_final.nii # Manual tissue segmentation in atlas space
```

NeSVoR outputs (generated by us):

```
fetenh_net/experiments/nesvor_simslices/<protocol>_<subject>_scanner_space/
└── recon.nii.gz                   # Scanner-space NeSVoR reconstruction
```

---

## 5. Cohort definitions for FetEnhNet

| Cohort | Source protocols | Purpose | Expected N |
|--------|-----------------|---------|------------|
| CHD_control | CHD_protocol (controls) | Primary training + validation | ~100 |
| CHD_case | CHD_protocol (cases) | Training + case-specific evaluation | ~100 |
| Heterotaxy | Heterotaxy | Training supplement | ~40 |
| Placenta | Placenta_protocol | Training supplement | ~30 |
| Normative | Normative | Validation reference | ~18 |
| ASD | ASD | Training supplement (if compatible) | ~30 |
| dHCP | dHCP | External validation (if compatible) | TBD |

Case/control assignment comes from the QA spreadsheet column "Is this baby a case or control?"

---

## 6. Current FetEnhNet training dataset (v3)

| Split | Source | Subjects | Pairs/stacks | Purpose |
|-------|--------|----------|-------------|---------|
| train_v3 | Synthetic (HIGH degraded) | 254 | 12,932 pairs | Supervised loss |
| val_v3 | Synthetic (HIGH degraded) | 31 | 3,233 pairs | Supervised validation |
| test_synth | Synthetic (HIGH degraded) | 32 | 198 pairs | Final synthetic eval |
| train_sure | Real LOW stacks | 250 | 250 stacks | SURE loss (Run22 split) |
| val_real | Real LOW stacks | 67 | 67 stacks | SURE validation (Run22 split) |

Conditioning supplement (tissue labels):
- 25 subjects with automated registration (Dice >= 0.80)
- 0 subjects with visual confirmation (pending)
- Target: 50-100+ after CanonicalData processing

---

## 7. Next steps (sequential, human-paced)

1. Complete CanonicalData scan (unique subjects with complete data per protocol)
2. Daniel reviews QA spreadsheet and selects first batch (e.g., 20 CHD subjects)
3. Visual inspection of raw data quality for selected batch
4. Run automated alignment pipeline on selected batch
5. Daniel visually confirms each overlay
6. Manual correction for failures
7. Quantitative confirmation (Dice scores)
8. Manifest generation for confirmed subjects
9. Repeat for next batch until target coverage reached

---

## Related

- [[fetenh-net]] -- Main project
- [[fetenh-label-projection-pipeline]] -- Registration pipeline details
- [[fetenh-option-c-dataset]] -- Option C batch results
- [[fetenh-overfitting-analysis]] -- Why more data matters
- [[fetenh-manual-registration-guide]] -- Manual alignment workflow
- [[medical-image-registration]] -- Registration theory
