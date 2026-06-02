---
title: "FetEnhNet — Fetal MRI Enhancement"
type: project
status: active
created: 2026-03-20
updated: 2026-05-07
tags: [project, research, bch, fetal-mri, deep-learning, pytorch, enhancement, grant-lab]
---

# FetEnhNet — Tissue-Conditioned Deep Learning Enhancement of Fetal MRI Raw Stacks

> Main research project at BCH/HMS FNNDSC Grant Lab. Supervisor: Kiho Im.

---

## Goal

Enhance fetal MRI raw HASTE stack images (2D slices) using deep learning. NOT reconstructed volumes — works on individual slices with Rician noise and physics-based degradations.

---

## Architecture

### Stage 1: TissueClassifier
- 3-level U-Net → 4-class soft tissue probability maps
- Classes: 0=background, 1=cortical_plate, 2=wm_subplate, 3=csf_other
- Labels from iBEAT v2: {1,42}→1, {160,161}→2, {18}→3

### Stage 2: EnhancementNet
- 4-level ResU-Net + **FiLM conditioning** at every decoder level
- FiLM: `γ(tissue) · features + β(tissue)` — per-pixel, spatially-varying
- `Conv2d(4→2C, k=1)` on bilinear-resized tissue_map
- Output: `clamp(input + residual, 0, 1)` (residual learning)

### Loss Function
```
L = L_sup + λ_tissue × L_tissue + λ_sure × L_sure
L_sup = 0.7 × L1 + 0.3 × (1 - SSIM)
```

---

## Dataset v2 (Complete)

- **1,914 pairs**: 319 HIGH subjects × 6 degradation types
- Degradations: noise, blur, bias, slice_corrupt, mixed_nb, mixed_nbs
- **Splits:** train=1530 (254 subj), val=186 (31), test_synthetic=198 (32), test_real=317 LOW
- Manifests: `experiments/2024_2026_degradation_study/training_data/manifests/`
- **CRITICAL:** use `training_data/` NOT `training_data_v2/`

---

## Training History

| Run | Config | Result |
|-----|--------|--------|
| **run06** | No tissue (λ=0) | CHAMPION baseline: noise+5.71, blur+5.07, bias+5.90 dB |
| run10 | λ_tissue=0.5, 81 labels, 100ep | val_sup=0.0515, bias best (+6.31dB) |
| **run11** | Warm from run10, 50ep, 1566 pairs | **CURRENT BEST** val_sup=0.0500 |
| run12 | λ_sure=0.1 | ABANDONED ep20 — SURE too aggressive |
| run13 | λ_sure=0.01, from run11 | Completed 100ep |
| run15 | Cosine LR, 100ep | val_sup oscillated 0.06-0.09 |
| run16 | 83.5% coverage, λ_tissue=1.0 | WORSE than run11 (~+1.6dB) |
| run17 | 83.5% coverage, λ_tissue lower | WORSE than run11 (~+2.0dB) |
| **run18** | Brain mask FiLM (2-class), 100ep, best ep82 | **NEW CHAMPION** val_sup=0.0541, blur+4.04dB, noise+5.10dB, SSIM+0.126 |

### run11 Results (Current Best)
| Degradation | ΔPSNR | ΔSSIM |
|-------------|-------|-------|
| noise | +5.70 dB | — |
| blur | +4.29 dB | — |
| bias | +5.29 dB | — |
| mixed_nb | +2.79 dB | — |
| mixed_nbs | +4.34 dB | — |
| **Mean (excl. slice_corrupt)** | **+4.48 dB** | **+0.161** |

### Why run11 > run16/17 (more tissue labels)
1. **Warm start:** run11 inherits run10 weights (sup=0.063 ep1 vs 0.115 fresh)
2. **Multi-task gradient conflict:** 83.5% coverage → tissue CE dominates gradients, pulls FiLM γ/β toward tissue discrimination instead of enhancement
3. **Tissue classifier never converges** (bad iBEAT labels on noisy stacks) → noisy FiLM conditioning
4. SURE adds a third competing signal

**Fix:** Train TissueClassifier to convergence first, freeze it, then train EnhancementNet alone.

**Run18 key insight:** Brain mask (2-class, already in raw stack space) outperforms tissue map (4-class, requires inverse transform). No projection needed = no registration error = cleaner conditioning signal. Use as baseline to compare against properly projected tissue labels.

**Run21 (latest, Apr 2026):** SURE self-supervised training with brain mask FiLM. Run21_sup: +3.36 dB PSNR, +0.119 SSIM on synthetic test. Run21_sure: SURE active from ep 32+, training complete.

**SURE plan (post March 24 meeting):** Reintroduce SURE loss (λ_sure calibrated, ~0.01) once tissue conditioning is stable. Reference: Pfaff et al., 2023 (https://www.nature.com/articles/s41598-023-49023-2). Prior runs (12, 13) failed because SURE was combined with an unstable tissue classifier.

**Dataset expansion plan (post March 24 meeting):** Significantly increase training data by generating synthetic images across the full range of degradation parameter values — full coverage of degradation space rather than sampled parameter sets.

### Current Training Strategy (as of Run 21)

**What runs now:** EnhancementNet only, with brain mask FiLM (2-class).
- Loss: `L_sup + λ(t) * L_SURE` (no tissue classification loss)
- `L_sup = 0.7 * L1 + 0.3 * (1 - SSIM)` on 12,932 synthetic pairs
- `L_SURE`: MC-SURE on 317 real LOW stacks, warmup from ep 30→200
- Brain mask already in raw stack space → no registration error

**Why tissue conditioning is not active:**
- Joint training (runs 16-17) failed: tissue CE dominated gradients, pulled FiLM away from enhancement
- TissueClassifier never converged on noisy iBEAT labels → noisy FiLM conditioning

**Planned sequential training (enabled by inverse alignment pipeline):**
1. Phase A: Train TissueClassifier alone with **DiceCE + label smoothing (ε=0.10)** vs inverse-aligned atlas labels → convergence → freeze. See [[fetenh-tissue-classifier-loss]] for full analysis.
2. Phase B: Train EnhancementNet with frozen 4-class tissue FiLM + L_sup + L_SURE
3. Compare tissue FiLM vs brain mask FiLM

**Loss decision (Apr 23):** Switched from focal NLLLoss (gamma=2.0, weights [1,25,9,10]) to DiceCE (weights [1,8,4,5]) + label smoothing (ε=0.10). Focal was mining noisy boundary pixels from atlas projection; high CP weight amplified label noise 25x. See [[fetenh-tissue-classifier-loss]].

**Data pipeline (Apr 23):** Phase 1 crawl complete — 795 subjects, 14,818 stacks (12,941 brain), 236 with segs. See [[fetenh-data-pipeline-plan]].

### Inverse Alignment Pipeline (Apr 21, Yair)

**SOLVED:** Atlas segmentation → raw HASTE stack space with zero registration error. 4-step pipeline using NeSVoR's `--extract-slice-transforms`. 100% success rate vs 73% with registration. See [[fetenh-inverse-alignment-pipeline]] for full details.

This eliminates the need to email Margherita about NeSVoR transforms and supersedes the registration-based `project_labels.py` approach.

---

## Degradation Engine v3-opt (May 6-7, 2026)

Physics-based rewrite of training + explorer degradation engines. 8 types with correct HASTE MRI physics:

| Type | Algorithm | Key Change from v2 |
|------|-----------|-------------------|
| Rician noise | Complex magnitude model with random phase + coil sensitivity | Was Gaussian, now physically correct |
| Gaussian blur | Per-slice 2D sigma | Unchanged |
| Bias field | Yair directional gradient + Legendre poly + exp(), brain-focused | Now constrained to brain via soft mask |
| Gibbs ringing | HARD rectangular k-space cutoff along PE axis | Tukey window removed (it suppressed ringing) |
| K-space spike | Log-magnitude injection + conjugate spike | New in v3 |
| Signal dropout | Hybrid k-space PE-line zeroing + image-domain dark bands | Bands positioned within brain extent |
| Intra-slice motion | Per-slice rigid transform (Yair) + k-space phase ramp | Was N/2 ghosting (wrong for single-shot HASTE) |
| Downsample | K-space truncation | Was interpolation zoom |

Key findings: Yair uses custom scipy/numpy (NO MONAI). BME-X has zero degradations/augmentation. scipy.fft gives 2-5x speedup.

## Tissue Labels Pipeline

- Script: `scripts/project_labels.py`
- Method: stack_voxel → A_stack → world → recon_to31.xfm (4×4 affine) → A_seg⁻¹ → label
- NN interpolation (`np.round`). Manual seg > iBEAT automated seg.
- Coverage after reconstruction campaign (Mar 2026): **83.5% train, ~77% val, ~75% test**

---

## Reconstruction Campaign (Mar 2026, ~90% complete)

| Cohort | Server | Status |
|--------|--------|--------|
| CHD (39 subj) | gangnam GPU 0 | 31/39 done, 8 pending |
| VM (42 subj) | sejong | ALL DONE |
| ASD (33 subj) | hanyang | ALL DONE |
| Normative (33 subj) | — | Mostly done |
| Placenta (24 subj) | hanyang | DONE |
| DS (3 subj) | hanyang | DONE |

**CHD pending:** FCB005, FCB014, FCB018, FCB071, FCB076, FCB086, FCB121, FCB160

---

## Key Files & Commands

### Pipeline
```bash
# Full pipeline
python3 /neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py \
  -i ${file} --all

# Manual segmentation
freeview ${file}/recon_segmentation/recon_to31_nuc.nii \
         ${file}/recon_segmentation/recon_to31_nuc_deep_agg.nii.gz:colormap=lut
# save as: segmentation_to31_final.nii

# Surface extraction (after manual seg)
python3 /neuro/labs/grantlab/research/MRI_processing/tools/surface_procesing_pipeline/app.py \
  --iSEGM ${file}/recon_segmentation/segmentation_to31_final.nii \
  --outdir ${file}/surfaces
# Add --subsampling False for GA < 28.5 weeks
```

### Training
```bash
eval "$(micromamba shell hook --shell bash)"
micromamba activate /neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/bmex_fetal
cd /neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net
python -m pytest tests/ -v  # 14/14 pass
```

---

## File Naming Conventions

| File | Purpose |
|------|---------|
| `recon_to31_nuc.nii` | Reconstruction |
| `recon_to31_nuc_deep_agg.nii.gz` | Auto segmentation |
| `segmentation_to31_final.nii` | Manual segmentation (gold standard) |
| `quality_assessment.csv` | QA scores |

**Segment IDs:** 1=Left CP, 42=Right CP, 160=Left Inner, 161=Right Inner, 18=CSF

---

## Symposium

- **Event:** FNNDSC Symposium Spring 2026
- **Format:** 3-minute talk, 5+title slides
- **Abstract submitted:** March 18, 2026
- **PDF slides due:** April 3, 2026
- **Title:** "FetEnhNet: Tissue-Conditioned Deep Learning Enhancement of Fetal MRI Raw Stacks"

---

## Critical Rules

1. Work on brain images (`Best_Images_Crop/`), NOT raw (except degradations project)
2. Need ≥3 images with QA > 0.4 for reconstruction
3. Delete old `recon_to31*` before rerunning reconstruction
4. GA < 28.5 weeks: `--subsampling False` for surface extraction
5. Never use interactive git (`-i` flag)

---

## Workspace Structure (live from sejong, 2026-03-20)

```
/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/
├── ARCHIVE_OLD_PROJECTS/   199M
├── code/                   181K
├── data/                   333G  ← MRI datasets (CHD_TD, ASD, VM, Placenta, Normative, etc.)
├── docs/                   0
├── environments/           17K
├── experiments/            31G   ← degradation study, training data, manifests
├── logs/                   12M
├── models/                 0
├── papers/                 418M  ← literature reviews + PDFs
├── projects/               115G  ← fetenh_net, activ_sparse_slm, puentes docs
└── scripts/                      ← auto_project_after_recon.sh, disk_audit.sh
```

### FetEnhNet Project Tree
```
projects/fetenh_net/
├── checkpoints/    run10–run17, smoke_test
├── configs/
├── figs/
├── figures/        tissue_labels_for_hyeokjin/
├── logs/           recon logs per server (hanyang_gpu0, sejong_gpu0, etc.)
├── presentation/   symposium materials
├── results/        run03_vs_run04 comparisons
├── scripts/        train.py, evaluate.py, visualize.py, project_labels.py, etc.
├── src/
│   ├── model/      tissue_classifier.py, enhancement_net.py, config.py
│   ├── training/   trainer.py, dataset.py, losses.py
│   └── eval/
└── tests/          14 tests (all pass)
```

### Mamba Environments on sejong
`analysis`, `bmex_fetal`, `brmz`, `fetal_pipeline`, `fetalsynthseg`, `iguane`, `neuronscope`

### GPU Status (sejong, 2026-03-20 09:25)
All 3× RTX A5000 **idle** (0% util, 38°C, ~9 MiB used). Available for training.

---

## Related Notes

### Pipelines & Methods
- [[fetenh-inverse-alignment-pipeline|Inverse Alignment Pipeline (Apr 21, solved)]] — 4-step atlas→raw projection via NeSVoR transforms
- [[fetenh-label-projection-pipeline|Label Projection Pipeline (registration-based, superseded)]] — binary shape registration, Dice 0.8985
- [[fetenh-manual-registration-guide|Manual Registration Guide]] — step-by-step FSL flirt approach
- [[bch-seg-pipeline|Segmentation Pipeline (8 steps)]]
- [[bch-surface-pipeline|Surface Processing Pipeline]]
- [[../020-Infrastructure/bch-processing-pipeline|BCH Processing Pipeline — Tools, Models, Containers]]

### Training & Experiments
- [[FetEnhNet-Run20-Plan|Run 20 Plan]]
- [[FetEnhNet-Run21-Plan|Run 21 Plan]]
- [[fetenh-overfitting-analysis|Overfitting Analysis — 6 causes]]
- [[fetenh-tissue-classifier-loss|Tissue Classifier Loss Research (Apr 23)]]

### Data
- [[fetenh-data-inventory|Data Inventory]] — CHD/ASD/Heterotaxy/Placenta/VM subject counts
- [[fetenh-data-methodology|Data Methodology]]
- [[fetenh-data-knowledge-graph|Data Knowledge Graph]]
- [[fetenh-data-pipeline-plan|Complete Data Pipeline Plan (Apr 23-24)]]
- [[fetenh-v4-dataset-strategy|v4 Dataset Strategy (complete proposal)]]
- [[fetenh-option-c-dataset|Option C Dataset]]

### Planning & Sessions
- [[fetenh-nesvor-rerun-plan|NeSVoR Re-Run & Inverse Alignment Plan]]
- [[fetenh-session-2026-04-24|Session Summary Apr 23-24]]
- [[fetenh-net-codebase|Codebase Documentation]]

### Meetings
- [[BCH-Meeting-Minutes|BCH Meeting Minutes (full log)]]
- [[BCH-FetEnhNet|BCH-FetEnhNet Notes]]
- [[BCH-Email-2026-03-24|March 24 Meeting Email (draft)]]

### Other Projects
- [[../040-Roles/research-engineer-bch|Research Engineer Role]]
- [[../020-Infrastructure/servers-index|Server Inventory]]
- [[neuronscope|NeuroNScope]]
- [[sparse-slm|ActivSparse-SLM]]
