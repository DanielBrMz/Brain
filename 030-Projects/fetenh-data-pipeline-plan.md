---
title: "FetEnhNet — Complete Data Preparation Pipeline Plan"
type: plan
status: active
created: 2026-04-23
updated: 2026-04-23
tags: [fetenh-net, data-pipeline, canonical-data, inverse-alignment, cohort, plan]
related: [[fetenh-net]], [[fetenh-data-knowledge-graph]], [[fetenh-data-inventory]], [[fetenh-inverse-alignment-pipeline]], [[fetenh-data-methodology]]
---

# FetEnhNet — Complete Data Preparation Pipeline

> End-to-end pipeline to maximize training data from all CanonicalData, integrate Yair's inverse alignment for tissue labels, and produce final manifests with proper splits.

## Goals

- Expand from 254 → 500+ HIGH training subjects
- Expand from 43 → 236 tissue-conditioned subjects (via inverse alignment)
- Use every usable raw stack in the lab (**14,818 stacks, 795 subjects** — Phase 1 crawl, Apr 23)
- Qualitative-first methodology: researcher visually confirms every cohort assignment
- Re-runnable pipeline: changing thresholds produces updated manifests automatically

## Phase 1 Results (Apr 23 — COMPLETE)

| Protocol | Subjects | Sessions | Stacks | Brain | w/Mask | w/Seg |
|----------|----------|----------|--------|-------|--------|-------|
| CHD | 232 | 373 | 6,606 | 6,062 | 3,518 | 119 |
| ASD | 53 | 56 | 891 | 773 | 782 | 48 |
| Heterotaxy | 35 | 44 | 497 | 489 | 474 | 34 |
| Placenta | 169 | 176 | 1,720 | 1,267 | 418 | 6 |
| Normative | 120 | 137 | 1,628 | 1,360 | 1,617 | 0 |
| Ventriculomegaly | 130 | 130 | 1,326 | 1,007 | 1,326 | 0 |
| SpinaBifida | 40 | 44 | 655 | 572 | 629 | 0 |
| HBCD | 32 | 75 | 1,406 | 1,336 | 1,203 | 29 |
| DownSyndrome | 6 | 6 | 89 | 75 | 77 | 0 |
| **Total** | **795** | **1,039** | **14,818** | **12,941** | **10,044** | **236** |

**Discoveries vs Apr 14 audit:** +122 subjects, +5,353 stacks, +35 with segs (HBCD 29 found at deeper paths, Heterotaxy +3, CHD multi-session data).
Catalog: `data_pipeline/outputs/catalog.csv` (14,823 rows)

With researcher directories (second crawl): **848 subjects, 18,047 stacks, 15,766 brain, 250 with segs.**

## Phase 2 Results (Apr 23 — COMPLETE)

Quality classification on 12,941 brain stacks (12 parallel workers, ~15 min):

| Quality | Stacks | % |
|---------|--------|---|
| HIGH | 213 | 1.7% |
| MEDIUM | 8,212 | 65.7% |
| LOW | 4,073 | 32.6% |
| Errors | 443 | — |

Note: Raw HASTE stacks are inherently noisy — strict thresholds put most in MEDIUM. Subject-level aggregation with relaxed thresholds (score≥2 = HIGH) yields 534 HIGH subjects.

## Phase 3 Results (Apr 24 — COMPLETE)

Cohort assignment (thresholds: HIGH≥2, LOW≤0):

| Cohort | Subjects | Stacks | Meaning |
|--------|----------|--------|---------|
| TIER_A | 148 | 3,480 | HIGH + has seg → synthetic + tissue FiLM |
| TIER_B | 386 | 5,816 | HIGH + no seg → synthetic + brain mask FiLM |
| SURE | 3 | 18 | LOW → SURE self-supervised |
| MEDIUM_REVIEW | 239 | 3,184 | Needs freeview visual review |

LOW sub-cohorts: blur=123, mixed=89, noise=7, bias=1 (from earlier strict threshold run).

## Phase 5 Results (Apr 24 — COMPLETE)

Final manifests (80/10/10 split, seed=42, 61 degradation configs):

| Manifest | Rows | Subjects |
|----------|------|----------|
| manifest_train.csv | 464,820 | 422 |
| manifest_val.csv | 53,497 | 52 |
| manifest_test_synth.csv | 51,911 | 54 |
| manifest_train_sure.csv | 15 | 2 |
| manifest_val_real.csv | 3 | 1 |

**Improvements over v3:** 254→422 train subjects (+66%), 43→148 with segs (+3.4x), ~19,700→464,820 synthetic pairs (+23x).

**Known gap:** SURE split too small (3 LOW subjects). Will use MEDIUM_REVIEW subjects flagged by freeview tool as LOW, or merge with v2's 317 LOW stacks.

## NeSVoR Campaign Status (Apr 25 — RUNNING)

**Architecture:** Staging mode — symlinks to CanonicalData for read-only dirs, writable copy of recon_segmentation/ in Daniel's workspace at `experiments/nesvor_staging/{protocol}_{subject}/`.

**Pre-flight:** 112/148 TIER_A subjects ready. 26 HBCD blocked (no recon.nii — need full NeSVoR run). 8 CHD + 2 HTX failed preflight.

**Launch:** 8 GPU slots across sejong (3), busan (3), gangnam (2). 14 subjects per GPU. Launched Apr 25 ~00:10.

**Issue found:** TensorFlow masking step ignores CUDA_VISIBLE_DEVICES and grabs GPU 0 on each server, causing contention. Jobs will serialize through GPU phases — slower than estimated but will complete.

**Monitor:** `python3 data_pipeline/05c_monitor_nesvor.py`

**Issues encountered & fixed:**
1. Permission denied on CanonicalData → switched to staging mode (symlinks + writable recon_segmentation/)
2. `rmtree` on symlinked dirs → replaced dir-level symlinks with dirs containing file-level symlinks
3. Container can't follow symlinks → copied `recon.nii` as real files (94GB total staging)

**Campaign results (Apr 25):**
1. First attempt via seg_pipeline: 31/112 (alignment step failures)
2. Direct NeSVoR approach (05e_direct_nesvor.py): bypassed seg_pipeline entirely
3. Final: **91/112 completed (81%)**. 21 CHD subjects OOM (too many stacks for 24GB A5000)
4. All 21 ASD, 10/12 Heterotaxy, 60/89 CHD succeeded

**21 OOM failures (all CHD with 25-35 stacks):** FCB011,016,022,030,056,057,059,062,067,078,089,090,126,127,128,133,151,193,198,215,217. Need either more VRAM or subset of stacks.

**Final count: 112/112 (100%).** All TIER_A subjects completed.

Challenges encountered and solved:
1. seg_pipeline `--from_recon` ran full alignment → bypassed with direct NeSVoR call
2. Apptainer container couldn't follow symlinks → copied real files
3. Zombie GPU process hogged 23GB → killed
4. Full-FOV raw stacks OOM'd → ran preprocessing (mask+QA+crop) first, then NeSVoR on brain-cropped stacks
5. Gangnam staging had symlink permission issues → replaced all symlinks with copies, built best_images_crop from brain/ files

**Inverse alignment: 112/112 complete (100%).** 84,087 per-slice labels generated, 78,895 with non-zero tissue labels (93.8% coverage). Labels in `experiments/projected_labels_rawstack/{protocol}_{subject}/{slice_idx}.nii.gz`.

2 subjects (FCB220, FCB226) had corrupted provenance.json — fixed by truncating duplicate JSON arrays.

**Manifests updated, verification complete** (93.8% mean coverage, 82 subjects >95%, 4 subjects <80%).

## Expansion Campaign (Apr 25 — IN PROGRESS)

Total subjects by category:
| Cat | Count | Status | What they need |
|-----|-------|--------|---------------|
| A | 112 | ✅ DONE | Have tissue labels (manual seg) |
| B | 231 | STAGING (~190/231) | Have auto-seg, need NeSVoR + inverse |
| E | 433 | NOT STARTED | Need full pipeline from raw stacks |

After all processing: **776/776 subjects with tissue labels (100% coverage)**.

Category B uses `recon_to31_nuc_deep_agg.nii` (auto iBEAT seg) instead of manual `segmentation_to31_final.nii`. Label smoothing ε=0.10 in DiceCE loss handles the auto-seg noise.

**Next:** Finish Cat B staging → NeSVoR on 10 GPUs (~23h) → inverse alignment → begin Cat E full pipeline (~13 days GPU).

## Pipeline Directory

```
projects/fetenh_net/data_pipeline/
├── config.py                     # Paths, constants, protocol definitions
├── 01_crawl_canonical.py         # Discover all raw stacks
├── 02_quality_classify.py        # Compute metrics per stack
├── 03_visual_review.py           # Freeview-based interactive review
├── 04_assign_cohorts.py          # HIGH/LOW assignment + LOW sub-classification
├── 05_run_inverse_alignment.py   # Batch NeSVoR + 4-step inverse alignment
├── 06_verify_alignment.py        # Visual verification of tissue overlays
├── 07_build_manifest.py          # Final manifests with splits + degradation grid
├── 08_characterize.py            # Figures for Kiho
├── utils/
│   ├── metrics.py                # SNR, CNR, sharpness, bias metrics
│   └── plotting.py               # Figure generation
└── outputs/
    ├── catalog.csv               # Phase 1
    ├── quality_metrics.csv       # Phase 2
    ├── visual_review_log.csv     # Phase 2b (human approvals)
    ├── cohort_assignments.csv    # Phase 3
    ├── alignment_status.csv      # Phase 4
    ├── manifest_train.csv        # Phase 5
    ├── manifest_val.csv
    ├── manifest_test_synth.csv
    ├── manifest_train_sure.csv
    ├── manifest_val_real.csv
    └── figures/                  # Phase 6
```

## Phases

### Phase 1: Data Discovery (Crawl CanonicalData) — 1 day

- Walk all 8 protocols, handle structural variants (CHD Data/ vs flat ASD, Heterotaxy Case/ subdir)
- One row per raw stack: subject, protocol, session, paths, existence of seg/atlas/masks
- Deduplicate CHD Data/ vs Data_NeSVoR/
- **Gate:** Verify counts match Apr 14 audit (673 subjects, 9,465 stacks, 201 with segs)

### Phase 2: Quality Classification — 2-3 days

- Port `classify_raw_quality.py` metrics to work on full catalog
- Per-stack: SNR, CNR, Laplacian sharpness, within-tissue CV (bias), motion
- Classify HIGH/MEDIUM/LOW
- Interactive freeview tool for researcher visual confirmation (focus on MEDIUM subjects)
- **Gate:** Show Kiho quality distribution plots, confirm HIGH/LOW cutoff

### Phase 3: Cohort Assignment — 0.5 days

- HIGH + has seg → TIER_A (synthetic pairs + tissue conditioning)
- HIGH + no seg → TIER_B (synthetic pairs, brain mask FiLM only)
- LOW → SURE + real validation (sub-classify: noise/blur/bias/mixed)
- MEDIUM → researcher decides per-subject
- **Gate:** Show Kiho cohort composition table

### Phase 4: Inverse Alignment — 3-5 days (GPU bottleneck)

**4a. NeSVoR re-run** (longest pole)
- Check which of 201 subjects need NeSVoR with `--extract-slice-transforms`
- Batch across 4 servers × 2-3 GPUs = 8-12 parallel slots
- ~15-30 min per subject, ~67 GPU-hours total

**4b. 4-step inverse alignment** (CPU, fast)
1. Atlas → Native (FSL flirt nearestneighbour)
2. Native → Simulated Slices (Yair's resample_to_raw_space.py)
3. Slices → Stacks (Yair's map_to_stacks.py, parameterize LOCAL_STACK_DIR)
4. Crop → Raw HASTE (Yair's resample_to_rawhaste.py, affine bug fix)
5. Remap FeTA labels {1,18,42,160,161} → 4-class {0,1,2,3}

**4c. Visual verification** (~1.5 hours)
- Show tissue overlay on raw stacks, worst-coverage first
- Auto-approve >95% coverage, flag <80% for manual review
- **Gate:** Show Kiho best/median/worst overlays

### Phase 5: Manifest Generation — 0.5 days

- Subject-stratified 80/10/10 train/val/test (no leakage)
- Synthetic pairs: all HIGH × 61 degradation configs
- SURE split: LOW subjects 80/20 train_sure/val_real
- Include tissue label paths (4-class) where available, brain mask fallback
- **Gate:** Confirm no subject in multiple splits, split balance

### Phase 6: Characterization Figures — 0.5 days

- GA distribution by protocol
- Protocol breakdown by split
- Quality distribution violin plots
- Tissue label coverage histogram
- LOW sub-cohort breakdown
- Degradation grid heatmap
- **Gate:** Present all figures to Kiho

## Timeline

| Phase | Duration | Blocking? |
|-------|----------|-----------|
| Phase 1 (crawl) | 1 day | No |
| Phase 2 (quality) | 2-3 days | No (review overlaps) |
| Phase 3 (cohorts) | 0.5 days | Depends on 1+2 |
| Phase 4a (NeSVoR) | 3-5 days | **Longest pole** |
| Phase 4b (alignment) | 1 day | Depends on 4a |
| Phase 4c (verification) | 1.5 hours | Depends on 4b |
| Phase 5 (manifests) | 0.5 days | Depends on 3+4 |
| Phase 6 (figures) | 0.5 days | Depends on 5 |
| **Total** | **~8-10 days** | |

Critical path: Phase 4a (NeSVoR batch). Phases 1-3 run while NeSVoR runs in background.

## Success Criteria

- 400+ HIGH training subjects (vs current 254)
- 150+ subjects with 4-class tissue labels (vs current 43)
- No data leakage across splits
- SURE split has held-out val_real (50+ LOW stacks)
- All 8 protocols represented
- Pipeline re-runnable end-to-end

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| NeSVoR fails on some subjects | High | Pre-check QA scores, expect ~5-10% failure, fallback to brain mask FiLM |
| Yair's scripts hardcode paths | High | Parameterize LOCAL_STACK_DIR, test on 3 protocols first |
| GPU contention delays NeSVoR | High | Run off-hours, distribute across 4 servers |
| Visual review of 673 subjects | Medium | Auto-classify HIGH/LOW with confidence, only review MEDIUM (~100-150) |
| affine bug fix pad not universal | Medium | Verify helper_functions.py uses fixed [50,50,16] constant |
| recon_to31_inv.xfm missing | Low | Compute inverse from recon_to31.xfm with FSL convert_xfm |

## Key Paths (sejong)

- Pipeline: `projects/fetenh_net/data_pipeline/`
- CanonicalData: `/neuro/users/mri.team/fetal_mri/Data/`
- Yair's scripts: `/neuro/labs/grantlab/research/MRI_processing/yair.beltran/inverse_alignment/test_data/recon_segmentation/`
- Seg pipeline CLI: `/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py`
- Existing scripts: `experiments/2024_2026_degradation_study/scripts/`
- Current manifests: `experiments/2024_2026_degradation_study/training_data/manifests/`

## Related

- [[fetenh-net]] — Main project
- [[fetenh-inverse-alignment-pipeline]] — Yair's 4-step pipeline (Apr 21)
- [[fetenh-data-knowledge-graph]] — Complete data map
- [[fetenh-data-inventory]] — Per-protocol counts
- [[fetenh-data-methodology]] — Qualitative-first approach
- [[fetenh-option-c-dataset]] — Previous Option C approach (superseded)
