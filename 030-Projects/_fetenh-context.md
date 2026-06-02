---
title: "FetEnhNet — Quick Context"
type: context
updated: 2026-05-10
tags: [fetenh, bch, context]
---

# FetEnhNet — Quick Context

> One-read context file for Claude. Load this first for any FetEnhNet/BCH work.

## What is it
Deep learning enhancement of fetal MRI raw HASTE stacks. Tissue-conditioned U-Net (FiLM) that improves SNR and sharpness of individual 2D slices without reconstruction. Research project at BCH/HMS FNNDSC Grant Lab.

## People
- **Kiho Im** — PI, supervisor. Wants step-by-step verification, intermediate results shared.
- **Hyeokjin Kwon** — senior researcher, discuss alternatives with him before trying
- **Yair Beltran** — solved inverse alignment pipeline (Apr 21), brain masking model
- **Victoria Hop Cohen** — hydrocephalus ventricle segmentation model, meeting minutes before Daniel
- **Daniel (you)** — model architecture, training, data pipeline, meeting minutes

## Server
- **busan** (10.88.88.2) — PRIMARY for training (CUDA driver 580, PyTorch 2.11+cu130 compatible), 3× RTX A5000
- **hanyang** (10.26.67.148) — also compatible (driver 580), 2× RTX A5000, but often occupied
- **sejong** (10.26.66.103) — workstation, 3× RTX A5000 — driver 580 (upgraded Apr 28), DDP SIGSEGV issue (single-GPU works)
- **gangnam** (10.72.8.45) — 2× RTX A5000 — driver 580 (upgraded Apr 28)
- Work dir: `/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/`
- Python env: `/neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/fetal_pipeline/bin/python`
- VPN required: WireGuard `wg-quick@bch`
- SSH: passphrase-protected key, use ControlMaster sockets at `~/.ssh/ctl/`

## Current Status (2026-05-18)

### Active: TWO runs training in parallel
- **Run 03a** (CE+L1, no detach): sejong GPUs 0+1, epoch 8, ΔPSNR=+2.34, sharpness=0.811
- **Run 03b** (CE+L1+detach): sejong GPU 2 (sharing with Hyeokjin), epoch 0, L1=0.087
- **NLM baseline**: DONE on busan (-0.23 dB, classical denoising fails)
- **Rolling QA**: 23 live flags, shared blacklist (symlinked), auto-masking active
- **All 3 GPUs utilized**: 03a on 0+1, 03b on 2 alongside Hyeokjin
- Clean dataset: 117K train (2,456 automated + 23 live QA excluded), 16K val, 8K test
- Master plan: both finish overnight → eval → paper by May 22

### Live QA Flags (23 total, 3 categories)
- Wrong/bad labels: 8 (labels don't match tissue boundaries)
- No brain in crop: 9 (crop at edge of brain volume or failed detection)
- Misaligned NeSVoR/reverse transform: 4 (composite target doesn't align with raw)
- All auto-masked via rolling QA (seg_valid=False, recon_skip where corr<0.5)

### Run History (BME-X Mirror)
| Run | Loss | ΔPSNR | Sharpness | Status |
|-----|------|-------|-----------|--------|
| 01 | CE+MSE (synthetic) | -18 dB | — | Failed (data gap) |
| 02a | CE+MSE (NeSVoR) | +2.57 | 0.72 | COMPLETE |
| 02b | L1+SSIM+Lap | diverged | — | FAILED ×4 |
| 03a | CE+L1 (NeSVoR) | +2.03 (ep3) | 0.74 | RUNNING |
| 03b | CE+L1+detach | — | — | PLANNED |

### Key Discovery: Data > Architecture > Loss
The 20 dB swing (Run 01 → 02a) proves data quality is the dominant factor. Same model, same loss, different data. This is the paper's headline finding.

### Dataset (nesvor_pairs_v3)
- Train: 117,054 pairs, 101,121 seg-valid (86.4%), 116,654 recon-valid (99.7%)
- Val: 15,924 pairs, 12,675 seg-valid, 15,868 recon-valid
- Test: 7,639 pairs, 6,655 seg-valid, 7,606 recon-valid
- QA: automated (Dice<0.15 + corr<0.3) + rolling live flagging

### Explorer Features (May 18)
- Per-row flag buttons with notes → rolling QA auto-masks seg_valid/recon_skip
- Full inference pipeline (crop→model→paste back)
- Training Monitor with live loss/sample/blacklist
- Run comparison table in Model Validation
- SQLite DB for metadata (adding runs + metrics tables)

### Paper Target
- MICCAI workshop (PIPPI/FETUS), 8 pages
- Deadline: May 22 (Daniel's last day at BCH)
- "Reference Methods" (BM3D + pretrained DnCNN) with caveat framing

---

## Historical Status (2026-05-07)

### Complete File System Map

All data on persistent NFS under `/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/` (abbreviated as `$PROJ` below).

#### Source Data (read-only, CanonicalData)
```
/neuro/users/mri.team/fetal_mri/Data/
├── CHD_protocol/Data/{FCBnnn}/            264 subjects
├── ASD/{MRN}/                              56 subjects
├── Heterotaxy/Case/{BCH_fetal_HTX_nnn}/    37 subjects
├── SpinaBifida/{MRN}/                      45 subjects
├── Placenta_protocol/Data_NeSVoR/{MRN}/     6 subjects (+ 165 in other Placenta dirs)
├── Normative/Data/{MRN}/                  120 subjects
├── Ventriculomegaly/{MRN}/                130 subjects
├── HBCD/{MRN}/                              8 subjects
└── DownSyndrome/                            0 subjects
```

#### Project Data (Daniel's work dir)
```
$PROJ/
├── checkpoints/                           Model weights (NEVER /tmp)
│   ├── foundational_run01/best.pt         Epoch 92, 1-ch GT FiLM, +4.29 dB
│   ├── foundational_run03/best.pt         Epoch 199, 1-ch SURE, val=0.096
│   ├── foundational_run04/best.pt         Epoch 1, dry run
│   └── tissue_classifier/best.pt          Epoch 1, dry run
├── experiments/
│   ├── inverse_alignment/                 Yair pipeline working dirs (673 dirs)
│   │   ├── {proto}_{subject}/             Per-subject NeSVoR + alignment
│   │   │   ├── raw/                       Copies of raw HASTE stacks
│   │   │   ├── best_images_crop/          Brain-extracted crops
│   │   │   ├── brain/                     Brain masks
│   │   │   └── recon_segmentation/
│   │   │       ├── recon.nii              NeSVoR 3D reconstruction
│   │   │       ├── provenance.json        Per-slice transforms (CRITICAL)
│   │   │       ├── simulated_slices/      NeSVoR re-projected 2D slices
│   │   │       ├── segmentation_native.nii.gz  Atlas seg in native space
│   │   │       ├── segmentation_raw_slices/    Per-slice segs (Step 2)
│   │   │       └── stack_space/           Per-stack 3D segmentations
│   │   │           ├── stack_NN_segmentation.nii.gz  Brain stacks
│   │   │           └── stack_NN_seg_rawhaste.nii.gz  Crop→raw HASTE
│   │   ├── dataset_report.json            Full dataset characterization
│   │   ├── campaign_*.log                 Batch processing logs
│   │   └── auto_rebuilder.log             Auto label builder log
│   ├── annotations.json                   Quality annotations (explorer, 795 subjects)
│   ├── projected_labels_rawstack/         Per-slice labels for explorer
│   │   └── {proto}_{subject}/             {global_idx}.nii.gz per slice
│   └── seg_native_cache/                  Cached native segmentations
├── explorer/                              FetEnhNet Explorer web app
│   ├── server/app.py                      FastAPI backend (port 8787)
│   ├── dist/                              Built React frontend
│   ├── connect.sh                         SSH tunnel script
│   └── server.log                         Server log
├── data_pipeline/
│   └── outputs/                           18 pipeline CSVs
├── scripts/
│   ├── batch_full_campaign2.py            CURRENT CAMPAIGN — handles all protocols, resumable queue
│   ├── run_alignment_direct.py            /tmp — bypass session lookup, run steps 1-5 directly
│   ├── batch_inverse_alignment_proper.py  Yair pipeline batch (--from_recon, needs CanonicalData session)
│   ├── batch_full_pipeline.py             Full seg_pipeline batch (--all)
│   ├── fast_inverse_alignment.py          Direct resampling (needs recon in CanonicalData)
│   └── fix_labels_to_rawhaste.py          Label format converter
└── src/model/
    ├── fetenh_net.py                      Joint model (classifier + enhancer)
    ├── enhancement_net.py                 Stage 2: tissue-conditioned U-Net
    ├── tissue_classifier.py               Stage 1: tissue classifier
    └── config.py                          Model configs (EnhancementNetConfig etc.)
```

#### Reference: Yair's Pipeline
```
/neuro/labs/grantlab/research/MRI_processing/yair.beltran/inverse_alignment/test_data/recon_segmentation/
├── resample_to_raw_space.py               Step 2: Native → simulated slices
├── map_to_stacks.py                       Step 3: Slices → stack volumes
├── resample_to_rawhaste.py                Step 4: Crop → raw HASTE space
└── provenance.json                        Reference FCB002 provenance
```

#### Key External Tools
```
/neuro/labs/grantlab/research/MRI_processing/tools/seg_pipeline/cli.py     Seg pipeline CLI
/neuro/labs/grantlab/research/Apptainer/nesvor:v0.6.0rc3_provenance.sif   NeSVoR container
/neuro/labs/grantlab/research/Apptainer/fsl:6.0.5.1-cuda9.1.sif           FSL container
```

### Dataset Alignment Review (May 10 — verified)

| Status | Count | Description |
|--------|-------|-------------|
| **Correct** | 488 | Properly aligned inverse alignment labels |
| **Partial** | 48 | Correct where labels exist, some stacks uncovered |
| **Wrong** | 23 | Unfixable (bad atlas XFM, mostly SpinaBifida Chiari II) |
| **No Data** | 236 | No reconstruction available |
| **Usable** | **536** | correct + partial, 164K brain slices |

### Training Dataset (May 5 — BUILT)
- `$PROJ/experiments/training_data/train.h5` — 179,601 slices (55 GB)
- `$PROJ/experiments/training_data/val.h5` — 24,356 slices (7.5 GB)
- `$PROJ/experiments/training_data/test.h5` — 20,547 slices (6.3 GB)
- Split: stratified by protocol, seed=42

### Degradation Engine v3-opt (May 6-7 — DEPLOYED)

Complete physics-based rewrite of training + explorer degradation engines. 8 types:

1. **Bias field**: Yair's directional gradient + Legendre poly + exp(). Brain-focused via soft mask
2. **Rician noise**: Complex model with random phase + coil sensitivity. Renamed from "Gaussian Noise"
3. **Gibbs ringing**: HARD rectangular k-space cutoff along PE axis (Tukey suppresses ringing)
4. **K-space spike**: Log-magnitude injection with conjugate spike
5. **Signal dropout**: Hybrid k-space PE-line zeroing + image-domain dark bands
6. **Intra-slice motion**: Yair's per-slice rigid transform (NOT N/2 ghosting — HASTE is single-shot). Renamed from "Motion Ghost"
7. **Downsample**: K-space truncation
8. **Gaussian blur**: Per-slice 2D

Key corrections:
- **Yair does NOT use MONAI** — all custom scipy/numpy
- **BME-X has zero degradations** — trains on real paired BCP data only
- scipy.fft used throughout for 2-5x speedup
- Brain mask auto-detected, degradations constrained to brain region

Explorer: training recommendation panel (TRAIN/SURE/VALIDATE/FIX LABELS), label quality metric (label-in-tissue fraction), updated slider ranges.

**DONE (May 8)**: Label quality pre-computed for 536 subjects → `$PROJ/experiments/label_quality_cache.json`. Results: 5,396 good / 11 borderline / 6 bad. Explorer serves cached values.

**Model Monitor (May 8)**: `src/training/model_monitor.py` — gradient norms, weight distributions, activation stats, dead neuron detection. Auto-generates during training. 7 explorer endpoints for live inspection.

**Augmentation Preview (May 8)**: `/api/slice/.../augment-preview` (manual) and `/api/slice/.../augment-random` (pipeline-realistic). 3-panel PNG output.

**Gap Analysis (May 8)**: `~/Brain/030-Projects/FetEnhNet-vs-BMEX-Gap-Analysis.md` — FetEnhNet wins 7/11 dimensions. Critical gaps: synthetic-to-real validation, tissue classifier quality, 2.5D.

### BME-X Baseline Approach (May 5)
- Concatenation mode (not FiLM) for baseline — matches BME-X paper
- MSE loss for enhancement (BME-X uses MSE, not L1)
- Bias field upgraded to Legendre polynomial (MONAI algorithm)
- Augmentation: flip, rotation +/-15, scale 0.8-1.2, crop 192, gamma, brightness
- 5 loss variants: MSE, L1, SSIM, perceptual (VGG), frequency (FFT)
- SURE self-supervised finetune after best combo selected

### BME-X Complete Analysis (May 10 — Deep Dive)
- Full audit: `~/Brain/030-Projects/BME-X-Paper-vs-Code-Audit.md` (claim-by-claim with code citations)
- Ground truth: memory `bmex_code_analysis.md`
- Container code extracted to `$PROJ/references/bmex_container/` (53 files from Docker v1.0.5)
- **Key findings:**
  - Caffe training DOES use both CE (weight=1) + EuclideanLoss/MSE (weight=10⁻⁷) — joint training confirmed
  - Patch size IS 40³ (confirmed in container `BME_X_enhanced.py`, stride=18, margin=5). GitHub `test_model.py` (32³) is outdated.
  - N4 bias correction applied TWICE (full head + skull-stripped brain) — undisclosed
  - Histogram matching to age template BEFORE enhancement, then REVERSE histogram matching AFTER — undisclosed, largely explains "harmonization" result
  - Fetal resolution is 0.75mm (not 0.8mm) — undisclosed
  - PyTorch model is 6.6× larger than Caffe training model (64ch/16 growth vs 32ch/8 growth)
  - PyTorch feeds softmax probs to connection; Caffe feeds ReLU'd logits — different information content
  - ReLU on recon output IS in Caffe too (in-place operation)
  - Three separate codebases in repo: Caffe training, PyTorch inference, unrelated ViT+registration model
  - Age required at inference (crashes without JSON sidecar specifying units)
  - Docker CPU test running locally, Apptainer SIF building on BCH for GPU test

### Handoff Documentation
- Google Docs: https://docs.google.com/document/d/15HY0uoVDPJefQi6aX41XVYc4aFkmWuahr3LXGHOHxHY/edit
- DOCX: `~/Downloads/FetEnhNet_Project_Documentation.docx`

#### Full Pipeline Campaign v2 (May 2, running on sejong GPUs 0-2)

Script: `$PROJ/scripts/batch_full_campaign2.py`
Queue file: `$PROJ/experiments/inverse_alignment/campaign_queue.json`
Logs: `$PROJ/experiments/inverse_alignment/campaign_logs/campaign_gpu{0,1,2}.log`

**Check status:**
```bash
python3 -c "
import json; from collections import Counter
q = json.load(open('experiments/inverse_alignment/campaign_queue.json'))
c = Counter(s['status'] for s in q)
print(dict(c))
"
# or tail logs:
tail -f experiments/inverse_alignment/campaign_logs/campaign_gpu0.log
```

**Restart campaign** (e.g. after server reboot):
```bash
PYTHON=/neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/fetal_pipeline/bin/python
SCRIPT=$PROJ/scripts/batch_full_campaign2.py
# resets running-gpu* back to pending automatically on next run
for gpu in 0 1 2; do
  nohup $PYTHON $SCRIPT --gpu $gpu > $PROJ/experiments/inverse_alignment/campaign_logs/campaign_gpu${gpu}.log 2>&1 &
done
```

**Queue state (as of May 10 — verified):**
| Status | Count |
|--------|-------|
| OK (done) | 319 |
| pending | 1 |
| running (stale) | 7 |
| FAIL:realign | 14 |
| FAIL:pipeline | 41 |
| **Total** | **382** |

**Subject breakdown:**
| Protocol | Total | Notes |
|----------|-------|-------|
| CHD | 28 | 6 FAIL, rest alignment-only (most needed --from_recon first) |
| Normative | 127 | 89 done already (had recon in CanonicalData) |
| Ventriculomegaly | 133 | flat dir structure, symlinked Best_Images_crop |
| SpinaBifida | 29 | session-based structure |

**Pipeline logic per subject:**
1. If `segmentation_native.nii.gz` exists → **skip** (done)
2. If `recon_to31_nuc_deep_agg.nii.gz` exists but no `simulated_slices/` → run `seg_pipeline --from_recon --extract-slice-transforms` then steps 1-5
3. If only `recon_to31_nuc_deep_agg.nii.gz` + `simulated_slices/` → run steps 1-5 directly
4. If no recon at all → `setup_working_dir` (symlink from CanonicalData) + `seg_pipeline --all --extract-slice-transforms` + steps 1-5

**Steps 1-5 (inverse alignment):**
1. Atlas→Native: FSL flirt with inverse xfm → `segmentation_native.nii.gz`
2. Native→SimSlices: `yair.beltran/resample_to_raw_space.py` → `segmentation_raw_slices/`
3. SimSlices→StackSpace: `yair.beltran/map_to_stacks.py` → `stack_space/`
4. Crop→RawHASTE: `yair.beltran/resample_to_rawhaste.py` → `stack_NN_seg_rawhaste.nii.gz`
5. Per-slice labels: → `projected_labels_rawstack/{proto}_{subj}/{N}.nii.gz`

**Accessing busan/hanyang from sejong:** requires SSH agent forwarding (`-A`). Cannot SSH without it. To launch on all servers from local machine:
```bash
# From local machine (has SSH agent):
ssh -A daniel.barrerasmeraz@sejong.tch.harvard.edu '
  for gpu in 0 1 2; do
    ssh -o StrictHostKeyChecking=no busan \
      "nohup $PYTHON $SCRIPT --gpu $gpu > $LOGS/campaign_busan_gpu${gpu}.log 2>&1 &"
    ssh -o StrictHostKeyChecking=no hanyang \
      "nohup $PYTHON $SCRIPT --gpu $gpu > $LOGS/campaign_hanyang_gpu${gpu}.log 2>&1 &"
  done
'
```

**ETA (all 10 GPUs — sejong 3 + busan 3 + hanyang 2 + gangnam 2):**
- 177 subjects remaining as of ~08:30 May 2
- ~20 alignment-only (fast, ~15 min each with --from_recon) + ~157 full-pipeline (~50 min each)
- 157 full-pipeline ÷ 10 GPUs ≈ 16 per GPU × 50 min ≈ **~14 hours** → done by ~22:30 May 2
- Campaign is resumable — just rerun with same `--gpu N` flags, queue tracks state

**Explorer SSH tunnel** (local port 8787 → sejong):
```bash
ssh -fNL 8787:localhost:8787 \
    -o IdentityFile=~/.ssh/id_ed25519 \
    daniel.barrerasmeraz@sejong.tch.harvard.edu
# Then open: http://localhost:8787
```

### Inverse Alignment Pipeline (Yair's 4-Step)

Prerequisite: NeSVoR `--extract-slice-transforms` → `provenance.json` + `simulated_slices/`

1. **Atlas → Native** — FSL flirt, nearestneighbour, inverse xfm
2. **Native → Simulated Slices** — resample 3D seg to each slice's affine
3. **Map to Stacks** — group by provenance stack_index, place in 3D volumes
4. **Crop → Raw HASTE** — affine resample with [50,50,16] pad correction + brain mask

Label conversion: `seg_rawhaste` 3D volumes → per-slice `{global_idx}.nii.gz` files
- Global indexing must match explorer's stack order (all sessions, cumulative)
- Multi-session subjects: query explorer API for exact stack list
- Stem matching: exact → scan_key (strip VISIT prefix) → shape-based fuzzy

### Completed Runs (Apr 29 — audited)

Checkpoint base: `/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/checkpoints/`

| Run | Config | val_sup | ΔPSNR | Checkpoint | Status |
|-----|--------|---------|-------|------------|--------|
| 01 | 1-ch, GT FiLM | — | +4.29 (9 types) | `foundational_run01/best.pt` (epoch 92) | On disk |
| 03 | 1-ch + SURE | 0.0912 | — | `foundational_run03/best.pt` (epoch 199) | On disk |
| 04 | 2.5D + dual-path | 0.0813 | — | `foundational_run04/best.pt` (epoch 1, dry run only) | On disk |
| **05** | **2.5D + SURE** | **0.0785** | +3.14 | **LOST** — was in hanyang `/tmp`, wiped by reboot | Needs retrain |
| 06 | 1-ch + SURE 500ep | — | — | **LOST** — was training on gangnam+sejong | Unknown |
| 07 | 2.5D + perceptual | 0.0860 | +3.35 | **LOST** — was in `/tmp` | Needs retrain |
| Classifier | 2.5D, DiceCE | fg=0.107 | — | `tissue_classifier/best.pt` (epoch 1, dry run) | On disk |

### GPU Cluster (all 4 servers driver 580, CUDA 13.0)
- busan: 3× A5000, FREE
- hanyang: 2× A5000, FREE
- gangnam: 2× A5000, Run 06
- sejong: 3× A5000, Run 06 on GPU 0 (DDP SIGSEGV, GPUs 1+2 idle)

### Code Changes (Apr 28)
- `train_tissue_25d.py` — DDP support
- `train_foundational.py` — `--perceptual_loss`, `--out_channels`, SURE channel expansion, input slicing
- `eval_foundational.py` — `--in_channels`, `--out_channels` for 2.5D
- `losses.py` — VGGPerceptualLoss
- `enhancement_net.py` — single/dual path forward

### Presentation
- `~/Downloads/fetenh_apr28_slides.pdf` (12 pages)
- Source: `~/Downloads/apr28_figures/fetenh_apr28_slides.tex`
- Figures: `~/Downloads/apr28_figures/*.pdf`

### Previous Status (2026-04-27)

### Foundational Model — TRAINED (Run 01)
Trained from scratch with GT tissue FiLM teacher forcing. 100 epochs, 58 min on busan 3× A5000.

**Results (test set, 80 stacks × 3 slices × 11 degradation types):**

| Degradation | ΔPSNR (dB) | ΔSSIM |
|-------------|-----------|-------|
| Noise low (σ=0.05) | +3.76 | +0.012 |
| Noise med (σ=0.10) | +7.14 | +0.067 |
| Noise high (σ=0.20) | +10.18 | +0.258 |
| Blur low (σ=0.8) | +1.04 | +0.002 |
| Blur med (σ=1.5) | +3.26 | +0.014 |
| Blur high (σ=2.5) | +3.08 | +0.029 |
| Bias field | -0.84 | -0.001 |
| Motion ghost | +0.40 | +0.003 |
| Signal dropout | +0.16 | +0.007 |
| Combined (noise+blur) | +5.35 | +0.054 |
| Combined (noise+blur+motion) | +4.42 | +0.030 |
| **OVERALL** | **+3.45** | **+0.043** |

**Checkpoint:** `checkpoints/foundational_run01/best.pt` (busan)

**Key design decisions:**
- GT tissue labels as FiLM conditioning (teacher forcing) — not classifier predictions
- Comprehensive degradation: 7 types (noise, blur, anisotropic blur, bias, motion ghost, signal dropout, Gibbs ringing)
- Frequency loss enabled (lambda_freq=0.1) — anti-blur
- TissueClassifier trained as auxiliary task (DiceCE, not used for conditioning during training)
- From scratch, NOT warm-started from Run 18

### Data Pipeline — COMPLETE
- **363/383 subjects with tissue labels** (up from 112 at start of Apr 26)
- **179,234 labeled slices** across 6 protocols (92.4% coverage)
- **364/383 provenance** (NeSVoR reconstruction, 95%)

### Previous Champion
- **Run 18:** Brain mask FiLM (2-class), +4.04 dB blur, +5.10 dB noise, +0.126 SSIM

### TissueClassifier (Phase A)
- Run02 best: fg_dice=0.099 (cp=0.014, wm=0.190, csf=0.109)
- Weights [1,25,12,15], no boundary erosion, degradation augmentation 70%
- Checkpoint: `checkpoints/tissue_run02/best.pt`

## Known Weaknesses (next improvements)
1. **Bias field** (-0.84 dB) — needs multiplicative correction branch, not additive residual
2. **Motion ghosting** (+0.40 dB) — needs k-space-aware loss or adversarial training
3. **Signal dropout** (+0.16 dB) — needs 2.5D context or generative prior (inpainting problem)
4. **Classifier quality** (fg_dice=0.099) — at inference, classifier predictions replace GT labels
5. **No SURE yet** — self-supervised loss on real data would improve generalization

## Immediate Next Steps
1. **Show Kiho** — these are publishable results. Prepare 5-slide summary.
2. **Train Run 02** — 200 epochs + SURE self-supervised on real LOW stacks
3. **Architectural fix for bias** — multiplicative correction branch
4. **For paper** — 3-seed cross-validation, comparison with BM3D/NLM/DnCNN

## Key Scripts Created (Apr 26-27)
- `data_pipeline/05f_mask_and_nesvor.py` — brain mask + crop + NeSVoR for full-FOV subjects
- `data_pipeline/05g_align_and_segment.py` — alignment + segmentation for subjects with recon
- `data_pipeline/08_build_tissue_manifest.py` — tissue train/val/test manifests
- `src/training/foundational_degradation.py` — 7-type comprehensive degradation engine
- `src/training/tissue_trainer.py` — standalone TissueClassifier trainer
- `src/training/losses.py` — added SoftDiceLoss + DiceCELoss
- `scripts/train_foundational.py` — foundational training with GT tissue FiLM
- `scripts/train_tissue.py` — Phase A tissue classifier training
- `scripts/eval_foundational.py` — per-degradation evaluation

## Critical Rules

### NEVER save to /tmp
All checkpoints, outputs, and artifacts MUST be saved to persistent NFS paths under:
`/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net/`
Server `/tmp` gets wiped on reboot. Run 05 (best model, val=0.0785) was lost this way after hanyang's driver upgrade reboot on Apr 28. Always use `--out_dir checkpoints/<run_name>`.

### Always include full paths in documentation
When referencing checkpoints, scripts, data, or outputs in vault notes or context files, always include the full NFS path so it can be found later. Example:
- Good: `checkpoints/foundational_run01/best.pt` (epoch 92, val=0.096)
- Bad: "the best checkpoint"

## Kiho's Process Requirements
1. Step-by-step verification
2. Share intermediate results
3. Discuss with Hyeokjin before trying alternatives
4. Never miss meetings

## Victoria's Hydrocephalus Model

Separate project: 3-class fetal brain segmentation (background/brain/ventricles) for hydrocephalus subjects.
- **Code:** `.../victoria.hopcohen/Code/unit_model_hydrocephalus/`
- **Data:** 17 hydrocephalus subjects with NeSVoR recons + manual brain & ventricle segs
- **Best model:** 3D UNet 5-fold CV — Mean Dice 0.919, Brain 0.915, Ventricle 0.923
- **2D models failed:** 2D axial (0.408) and 2D multiview (0.361) — ventricle Dice collapses
- **Improved 2D (May 8, busan):** COMPLETE — brain=0.293, vent=0.039, mean=0.166. Context radius=1 (3 slices), DiceFocalLoss, 3x ventricle oversample. Still far worse than 3D. **2D confirmed non-viable for this task.**
- **Kiho approved** adding ventriculomegaly subjects (Apr 27) — will expand from 17
- **Daniel contributed:** `train_2d_kfold.py`, `train_2d_multiview_kfold.py`, `improved_train2d_axial_kfold.py`, `compare_models.py`, `visualize_kfold.py`, `TRAINING_RUNS.md`, `data_list.csv`
- **Python env:** `/neuro/users/victoria.hopcohen/.local/share/mamba/envs/hydrocephalus`
- See [[victoria-hydro-model]] for full details

### Unified Codebase + SQLite DB (May 13-14 — COMPLETE)

**Major restructure:** single degradation engine, SQLite database, explorer UX overhaul.

#### Architecture
- `src/degradation.py` — single source of truth for all degradations (33 catalog presets)
- `src/db.py` — SQLite CRUD (subjects, stacks, annotations, training, review tracking)
- `src/training/db_loader.py` — training pipeline reads splits from DB
- `explorer/server/degradations.py` — re-export shim → `src/degradation.py`
- `explorer/server/app.py` — all endpoints DB-backed
- Old `foundational_degradation.py` — archived (895 lines, replaced)
- 38 dead scripts moved to `scripts/_archived/`

#### Database: `experiments/explorer.db` (~9MB, WAL mode)
- 776 subjects, 12,949 stacks, 927 annotations, 12,943 training assignments
- Review tracking: quality_reviewed, split_reviewed, degradations_reviewed per stack
- All characterization cached → instant load (no more "Analyzing..." delay)

#### Explorer UX (http://10.26.66.103:8787)
- Amazon-style inline zoom (click image → 2.5x scale inside container, mouse-pan)
- Role badges on thumbnails: TRAIN/EVAL/SURE/EXCLUDED with review dots
- Training role card in quality panel with review checklist
- Drop Labels toggle (DB flag, files kept on disk)
- Exclude/Re-include toggle (instant UI update)
- Quality/Split/Role filters in filter bar
- Pipeline 1 QA score in quality panel
- Collapsible Degradation Explorer (lazy load)
- No annotator tracking — just reviewed/not-reviewed flags
- Victoria's feedback: zoom + QA score in quality window

#### Dataset Verification (May 14 — FULLY VERIFIED)

```
Supervised train:  2,216 stacks, 79,781 slices, 387 subjects
  Dice >= 0.95: 2,174 (98.1%)  |  0.90-0.95: 27  |  0.80-0.90: 14  |  0.70-0.80: 1
Supervised val:      450 stacks, 15,201 slices,  53 subjects
Supervised test:     232 stacks,  8,233 slices,  34 subjects
Eval pool:         4,087 stacks (real degraded data)
SURE pool:         4,921 stacks (self-supervised candidates)
Excluded:            516 stacks
```

All checks PASS:
- 0 bad quality in train, 0 unlabeled, 0 bad Dice, 0 SNR=0
- 0 subject leakage between splits (was 327, fixed)
- 0 unscored Dice in train (was 595, batch-computed)
- 521 ghost-labeled stacks found (DB said labels, files didn't exist) → moved to SURE

#### Dataset Rules (enforced)
1. Manual QA overrides pipeline QA
2. bad/LOW quality → eval only (never supervised train)
3. Only good/fair/MEDIUM/HIGH + labels → supervised train
4. All stacks from one subject → same split (no leakage)
5. 0-1 slice stacks → auto-excluded
6. Dice < 0.70 → labels dropped, stack moved to SURE

#### Next: Run 1
1. Regenerate pre-computed crops from 2,216 verified train stacks
2. Launch on hanyang: unified degradation, λ_recon=0.1, CosineAnnealingLR, 30 epochs

## Detailed Notes
- [[fetenh-foundational-model]] — Run 01 results and analysis
- [[fetenh-net]] — main hub with all sub-notes linked
- [[BCH-Meeting-Minutes]] — weekly meeting log
- [[fetenh-data-pipeline-plan]] — 8-script pipeline spec
- [[fetenh-inverse-alignment-pipeline]] — solved pipeline docs
- [[fetenh-data-inventory]] — subject counts per cohort
- [[victoria-hydro-model]] — Victoria's hydrocephalus segmentation model
- [[BME-X-Deep-Analysis]] — full 3-part paper vs code analysis
- [[unet-architecture]] — U-Net variants and practical lessons
