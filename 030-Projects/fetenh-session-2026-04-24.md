---
title: "FetEnhNet — Session Summary Apr 23-24, 2026"
type: project
status: active
created: 2026-04-24
updated: 2026-04-24
tags: [fetenh-net, session-summary, victoria, hydrocephalus, data-pipeline]
related: [[fetenh-net]], [[fetenh-v4-dataset-strategy]], [[fetenh-data-pipeline-plan]], [[fetenh-tissue-classifier-loss]]
---

# Session Summary: Apr 23-24, 2026

## FetEnhNet Data Pipeline — Phases 1-5 Complete

### What was built
- 8-script pipeline in `projects/fetenh_net/data_pipeline/`
- Crawled ALL of CanonicalData + 15 researcher directories
- Quality classified 12,941 brain stacks
- Assigned cohorts and built manifests

### Results

| Metric | Old (v3) | New (v4) |
|--------|----------|----------|
| Train subjects | 254 | 422 |
| Synthetic pairs | 12,932 | 464,820 |
| Subjects with segs | 43 | 148 |
| Protocols | 6 | 9 |

### Key discoveries
- 848 total subjects across lab (was 673)
- 15,766 brain stacks (was 9,465)
- 250 subjects with segmentations (was 201)
- HBCD has 29 subjects with segs (previously thought 0)
- Researcher directories add 53 unique subjects

### Loss function decision
Switched from focal NLLLoss (gamma=2.0, weights [1,25,9,10]) to **DiceCE + label smoothing (ε=0.10)** with reduced weights [1,8,4,5]. See [[fetenh-tissue-classifier-loss]].

---

## Victoria's Hydrocephalus Project

### Model comparison (all kfold, fair comparison)

| Model | Mean Dice | Brain | Ventricles | HD95 Brain | HD95 Vent |
|-------|-----------|-------|------------|------------|-----------|
| **3D kfold** | **0.919** | 0.915 | 0.923 | 6.2 mm | 4.4 mm |
| 2D multiview kfold | 0.361 | 0.581 | 0.140 | 16.7 mm | 57.5 mm |
| 2D axial kfold | 0.408 | 0.602 | 0.215 | 14.2 mm | 37.7 mm |

**Conclusion:** 3D is the only approach that works with N=17. All 2D approaches fail with kfold despite appearing good on 80/10/10 splits. Andrea was right about limited generalization, but wrong to call it "memorization" — kfold proves the 3D model DOES generalize to held-out subjects.

### Why 2D fails
1. Can't learn 3D spatial priors (where ventricles sit in volumetric context)
2. Training instability (gradient explosions from DiceFocalLoss on sparse 2D slices)
3. No inter-slice consistency at inference (each slice predicted independently)
4. Overparameterized for N=17 (6.5M params on slices from 13 subjects)

### Key conversation with Victoria (Apr 24)
- **Hydrocephalus subjects in Victoria's personal dir are NOT in CanonicalData** — they required manual masking and QA to get usable reconstructions
- **Suzette's ASD folder has severe cases** (ventriculomegaly, ACC) — some are very abnormal, could be useful for FetEnhNet LOW cohort
- **Andrea says ventriculomegaly subjects could be added** — "miles" (thousands) potentially available
- **Victoria will investigate and add subjects**, including doing masks for severe cases
- Kiho wants the hydro model for a **grant application** — 3D kfold 0.919 is publishable as proof of concept

### Implications for FetEnhNet
1. **Victoria's hydro model could generate pseudo-labels** for severe pathology cases (brain + ventricle segmentation on subjects without tissue segs)
2. **Severe cases go into SURE training** — real LOW quality stacks for self-supervised loss
3. **Ventriculomegaly expansion** — 130 subjects already in CanonicalData with 0 segs; if Victoria/Andrea process them, massive expansion of training data with pathological anatomy
4. **Cross-project synergy** — Victoria processes severe cases → FetEnhNet uses them for robustness on extreme anatomy

---

## Files Created/Modified This Session

### On sejong (FetEnhNet)
- `data_pipeline/config.py` — All paths, 9 canonical + 15 researcher protocols
- `data_pipeline/01_crawl_canonical.py` — Crawls all data sources
- `data_pipeline/02_quality_classify.py` — Computes quality metrics per stack
- `data_pipeline/04_assign_cohorts.py` — Assigns TIER_A/B/SURE/MEDIUM
- `data_pipeline/07_build_manifest.py` — Builds final train/val/test manifests
- `data_pipeline/outputs/catalog.csv` — 18,054 rows (all stacks)
- `data_pipeline/outputs/quality_metrics.csv` — 12,941 brain stacks classified
- `data_pipeline/outputs/cohort_assignments.csv` — 776 subjects assigned
- `data_pipeline/outputs/manifest_train.csv` — 464,820 synthetic pairs
- `data_pipeline/outputs/manifest_val.csv` — 53,497 val pairs
- `data_pipeline/outputs/manifest_test_synth.csv` — 51,911 test pairs

### On hanyang (Victoria's hydro)
- `visualize_kfold.py` — Generates kfold figures (bar charts, boxplots, overlays)
- `train_2d_kfold.py` — 2D axial kfold training
- `train_2d_multiview_kfold.py` — 2D multiview kfold training
- `TRAINING_RUNS.md` — Corrected (outputs_2d was multiview, not axial)
- `outputs_kfold/figures/` — 21 figures (4 summary + 17 overlays)
- `outputs_2d_kfold/` — Axial kfold results (Mean Dice 0.408)
- `outputs_2d_multiview_kfold/` — Multiview kfold results (Mean Dice 0.361)

### In vault (Brain/)
- `030-Projects/fetenh-data-pipeline-plan.md` — Pipeline plan + Phase 1-5 results
- `030-Projects/fetenh-tissue-classifier-loss.md` — Loss function research
- `030-Projects/fetenh-v4-dataset-strategy.md` — Complete v4 dataset proposal
- `030-Projects/fetenh-session-2026-04-24.md` — This file

### In memory
- `bch_fetenh_net.md` — Updated with pipeline status and loss decision
- `bch_toor_access.md` — toor password and procedure

---

## Next Steps

### FetEnhNet (critical path)
1. **SURE split fix** — merge v3's 317 LOW stacks + freeview review of 239 MEDIUM subjects
2. **Phase 4a: NeSVoR re-run** on 148 TIER_A subjects (3-5 day GPU, run this weekend)
3. **Phase 4b: Inverse alignment** batch on NeSVoR outputs
4. **Degradation grid redesign** — drop Gaussian noise, calibrate to real LOW distribution, add triple combo
5. **Phase A: Train TissueClassifier** with DiceCE + label smoothing
6. **Phase B: Train EnhancementNet** with frozen tissue FiLM
7. **Phase 6: Characterization figures** for Kiho

### Victoria's hydro (her responsibility, we assist)
- Show Kyeong Ho the 3D kfold results (0.919) for grant application
- Investigate adding ventriculomegaly subjects (Andrea's suggestion)
- Process severe cases from Suzette's ASD folder
- We run any training she needs on hanyang

### Cross-project
- Once Victoria processes more hydro/VM subjects → add to FetEnhNet SURE split
- Victoria's brain+ventricle model could generate pseudo-labels for FetEnhNet on severe cases
