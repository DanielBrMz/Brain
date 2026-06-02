---
title: "FetEnhNet — v4 Dataset Strategy (Complete Proposal)"
type: reference
status: active
created: 2026-04-24
updated: 2026-04-24
tags: [fetenh-net, dataset, degradation, splits, training-strategy, v4]
related: [[fetenh-data-pipeline-plan]], [[fetenh-net]], [[fetenh-tissue-classifier-loss]], [[fetenh-inverse-alignment-pipeline]], [[fetenh-data-inventory]]
---

# FetEnhNet v4 Dataset Strategy

> Complete specification for the final training dataset. Covers data sources, degradation physics, split logic, SURE integration, tissue conditioning, and the training pipeline.

---

## 1. Data Sources

### 1.1 Raw data (from Phase 1 crawl, Apr 23)

| Source | Subjects | Brain Stacks | With Seg |
|--------|----------|-------------|----------|
| CanonicalData (9 protocols) | 795 | 12,941 | 236 |
| Researcher directories | +53 unique | +2,825 | +14 |
| **Total** | **848** | **15,766** | **250** |

### 1.2 What a "subject" gives us

Each subject has one or more sessions. Each session has:
- `raw/*.nii` — 8-25 raw HASTE stacks (2D multi-slice acquisitions, each ~8-70 slices)
- `masks/*_mask.nii` — per-stack binary brain masks (not all stacks have masks)
- `recon_segmentation/` — pipeline outputs: `recon.nii`, `recon_to31_nuc.nii`, `segmentation_to31_final.nii` (manual tissue seg in atlas space), `recon_to31.xfm` (atlas transform)

**Per-slice yield:** A typical subject with 15 brain stacks × 30 brain slices per stack = ~450 unique 2D training slices. With 422 training subjects, that's ~190,000 unique anatomical slices before degradation augmentation.

### 1.3 Stack spatial properties

Raw HASTE stacks come in 7 spatial shapes: 192×192, 224×224, 232×256, 256×256, 320×320, 448×372, 512×512. The dataset loader handles this via center-crop-then-zero-pad to 256×256 — no resampling, no interpolation artifacts.

Voxel sizes: typically 1.17×1.17×3.0mm (in-plane × slice thickness). Some protocols use 0.8mm or 1.5mm in-plane.

---

## 2. Synthetic Degradation Strategy

### 2.1 Physics of fetal MRI degradation

Real LOW-quality HASTE stacks suffer from three independent physical mechanisms:

**Rician noise** — The dominant noise source in MRI magnitude images. NOT Gaussian. The magnitude signal follows a Rice distribution: `|S + n|` where `S` is the true signal and `n` is complex Gaussian noise. At low SNR, this produces a positive bias (noise floor) and non-linear distortion that pure Gaussian noise cannot replicate. Our Rician simulation is physically correct: we generate random phase, add Gaussian noise to real and imaginary channels independently, then take the magnitude.

**Blur (within-slice)** — Caused by intra-acquisition fetal motion (the fetus moves DURING the ~500ms HASTE readout), T2* decay during the echo train, and coil sensitivity roll-off. This is a 2D phenomenon — each slice is acquired independently, so blur happens within each slice plane, not across slices. Our simulation applies per-slice 2D Gaussian blur with `sigma=[σ, σ, 0]` (zero along the slice axis).

**B1+ bias field** — Caused by radiofrequency coil inhomogeneity. The transmit B1 field is not uniform across the imaging volume, creating smooth spatial intensity variations. This is a property of the coil geometry, so it's approximately constant across slices (same 2D pattern applied to every slice). Our simulation generates a polynomial 2D field of configurable order (1-3) and strength, smoothed by a Gaussian filter, then multiplies every slice by this field.

### 2.2 Degradation grid (61 configurations)

Each HIGH-quality clean stack is paired with 61 degraded versions:

| Type | Count | Parameters | Physics |
|------|-------|-----------|---------|
| Gaussian noise | 10 | σ ∈ {0.02, 0.04, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.30} | Simplified noise model (not Rician) — useful for training robustness to additive noise |
| **Rician noise** | 10 | σ ∈ same range | Physically correct MRI noise — primary noise degradation |
| Gaussian blur | 10 | σ ∈ {0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5} | Per-slice 2D blur — simulates intra-slice motion |
| Bias field | 9 | order ∈ {1,2,3} × scale ∈ {0.2, 0.4, 0.6} | 2D polynomial B1+ inhomogeneity |
| Blur + Rician | 16 | blur_σ ∈ {0.8, 1.2, 1.8, 2.5} × noise_σ ∈ {0.05, 0.10, 0.15, 0.20} | Combined degradation — most realistic |
| Bias + Rician | 6 | bias_scale ∈ {0.2, 0.4} × noise_σ ∈ {0.05, 0.10, 0.15} | Combined degradation |
| **Total** | **61** | | |

**σ is relative to mean signal intensity** — `σ_actual = σ_fraction × mean(image[image > 0])`. So σ=0.10 means noise at 10% of the mean brain signal, giving output SNR ≈ 10.

### 2.3 Why on-the-fly vs pre-generated

Degradations are applied **on-the-fly during training**, not pre-generated to disk. The manifest specifies `(clean_path, degradation_type, degradation_params)` and the dataloader applies the degradation at load time. Benefits:
- No disk storage for 464,820 degraded stacks (~50TB if pre-generated)
- Different random seed each epoch → slightly different noise realization → implicit augmentation
- Easy to add new degradation types without regenerating data

The manifest rows define the degradation schedule; the dataloader executes it.

### 2.4 Normalization strategy (critical detail)

Both clean and degraded slices are normalized using the **degraded image's** percentile range `[p1, p99] → [0, 1]`. This is intentional: at inference time, only the degraded image is available, so the model must operate in the degraded image's intensity space. Using separate normalizations would create a scale mismatch between training and inference.

---

## 3. Split Strategy

### 3.1 Subject-stratified splits (no leakage)

All stacks from one subject go to the same split. Multi-session subjects: all sessions in same split. No slice from a training subject ever appears in validation or test.

```
848 total subjects
 ├── 534 HIGH quality (score ≥ 2)
 │    ├── 148 TIER_A (has seg) ─── tissue FiLM conditioning
 │    └── 386 TIER_B (no seg)  ─── brain mask FiLM only
 ├── 239 MEDIUM ──────────────── pending freeview visual review
 └── 75  LOW ─────────────────── SURE + real validation
      ├── blur (dominant)
      ├── noise
      ├── bias
      └── mixed
```

### 3.2 Supervised splits (HIGH subjects)

| Split | Subjects | Purpose | Metric |
|-------|----------|---------|--------|
| **Train** | 422 (80%) | L_sup: learn to reverse degradations | Training loss |
| **Val synthetic** | 52 (10%) | Model selection, early stopping, LR scheduling | PSNR/SSIM on known degradations with known clean target |
| **Test synthetic** | 54 (10%) | Final controlled benchmark | PSNR/SSIM per degradation type |

Val synthetic is valid because we have the ground truth clean image — we can measure exactly how much quality the model recovers. These are never-seen subjects with known degradation parameters.

### 3.3 SURE splits (LOW + MEDIUM-flagged subjects)

| Split | Subjects | Purpose | Metric |
|-------|----------|---------|--------|
| **Train SURE** | 60 (80% of LOW) | L_SURE: self-supervised denoising on real degraded images | SURE loss value |
| **Val real** | 15 (20% of LOW) | Generalization check on real clinical images | No-reference metrics (NIQE, BRISQUE), visual assessment |

**SURE gap:** Current Phase 3 found only 3 LOW subjects with strict thresholds. Solution:
1. Merge v3's existing 317 real LOW stacks (from `test_real.csv`) — these are already validated
2. After freeview visual review, move MEDIUM subjects with genuinely poor quality to SURE
3. Target: 75+ SURE subjects (60 train + 15 val)

### 3.4 What each split teaches the model

```
                    ┌─────────────────────────────────────────┐
                    │           TRAINING                       │
                    │                                          │
                    │  L_sup (supervised):                     │
                    │    422 subjects × 61 degradations        │
                    │    = 464,820 (clean, degraded) pairs     │
                    │    Loss: 0.7*L1 + 0.3*(1-SSIM)          │
                    │    Teaches: how to reverse known          │
                    │    degradations on high-quality anatomy   │
                    │                                          │
                    │  L_SURE (self-supervised):               │
                    │    60 subjects, real LOW stacks           │
                    │    Loss: MC-SURE (Stein's unbiased est)  │
                    │    Teaches: denoise real images without   │
                    │    clean reference — adapts to real       │
                    │    noise statistics that synthetic        │
                    │    degradations may not perfectly match   │
                    │                                          │
                    │  L_tissue (Phase A only):                │
                    │    148 TIER_A subjects                    │
                    │    Loss: DiceCE + label smoothing ε=0.10 │
                    │    Teaches: predict tissue class per-pixel│
                    │    for FiLM conditioning                 │
                    └─────────────────────────────────────────┘

                    ┌─────────────────────────────────────────┐
                    │           VALIDATION                     │
                    │                                          │
                    │  Val synthetic (52 subjects):            │
                    │    Known clean target → PSNR/SSIM        │
                    │    Used for: early stopping, LR schedule │
                    │    model checkpoint selection             │
                    │                                          │
                    │  Val real (15 subjects):                 │
                    │    No clean reference                    │
                    │    Used for: generalization sanity check  │
                    │    no-reference quality metrics           │
                    │    visual inspection                     │
                    └─────────────────────────────────────────┘

                    ┌─────────────────────────────────────────┐
                    │           TEST (final, never seen)       │
                    │                                          │
                    │  Test synthetic (54 subjects):           │
                    │    Controlled benchmark with PSNR/SSIM   │
                    │    Report per-degradation-type results   │
                    │                                          │
                    │  Test real (from v3 + freeview):         │
                    │    Clinical images, visual assessment    │
                    │    Before/after comparison panels        │
                    └─────────────────────────────────────────┘
```

---

## 4. Tissue Conditioning Strategy

### 4.1 Two conditioning tiers

| Tier | Subjects | FiLM input | Quality |
|------|----------|-----------|---------|
| **TIER_A** | 148 | 4-class tissue probability map (bg, CP, WM, CSF) | Best — spatially-varying enhancement per tissue type |
| **TIER_B** | 386 | 2-class brain mask (bg, brain) | Good — inside/outside brain distinction |

Both tiers train together. The FiLM module receives either a 4-class or 2-class conditioning map and produces per-pixel γ/β. Subjects without any conditioning (no mask, no seg) are excluded from training.

### 4.2 Tissue label source (TIER_A)

**Inverse alignment pipeline** (Yair, Apr 21):
1. Atlas segmentation → Native space (FSL flirt, nearest-neighbour)
2. Native → NeSVoR simulated slices (per-slice affines from `--extract-slice-transforms`)
3. Simulated slices → Stack space (provenance.json grouping)
4. Crop → Raw HASTE space (affine bug fix for auto_crop_image padding)

**Zero registration error, 100% success rate** on tested subjects. Labels in raw HASTE stack space, pixel-aligned with the training images.

Label remapping: FeTA `{1,42}→1 (cortical_plate), {160,161}→2 (wm_subplate), {18}→3 (csf), else→0 (bg)`

### 4.3 TissueClassifier training (Phase A)

Before the main enhancement training, we train the TissueClassifier alone:

- **Architecture:** 3-level U-Net → 4-class softmax
- **Loss:** DiceCE + label smoothing (ε=0.10) — see [[fetenh-tissue-classifier-loss]]
  - CE weights: [1, 8, 4, 5] (bg, CP, WM, CSF) — reduced from [1, 25, 9, 10]
  - NO focal loss (focal mines noisy atlas boundary pixels)
- **Data:** 148 TIER_A subjects, all their brain stacks, inverse-aligned labels
- **Output:** Frozen 4-class probability maps that feed into FiLM
- **Convergence criterion:** val Dice plateau for ≥20 epochs

### 4.4 EnhancementNet training (Phase B)

After TissueClassifier is frozen:

- **Architecture:** 4-level ResU-Net + FiLM conditioning at every decoder level
- **FiLM:** `γ(tissue) · features + β(tissue)` where tissue = frozen softmax output from TissueClassifier
- **Loss:** `L = L_sup + λ_sure(t) * L_SURE`
  - `L_sup = 0.7 * L1 + 0.3 * (1 - SSIM)` on synthetic pairs
  - `L_SURE`: MC-SURE on real LOW stacks, warmup from epoch 30→200
  - No L_tissue — classifier is frozen, no gradient flows through it
- **Output:** `clamp(input + residual, 0, 1)` — residual learning

---

## 5. SURE Self-Supervised Component

### 5.1 What SURE does

Stein's Unbiased Risk Estimate allows training a denoiser without clean reference images. For an image corrupted by noise with known variance σ², SURE provides an unbiased estimate of MSE(denoised, clean) using only the noisy image and the denoiser's output.

**Why we need it:** Synthetic degradations approximate real degradations but don't perfectly match them. SURE training on actual LOW-quality clinical images bridges this domain gap — it teaches the model to handle real noise statistics, real motion patterns, and real bias fields that our simplified physics models may not capture.

### 5.2 SURE data requirements

- Real LOW-quality stacks (genuinely degraded, not synthetically)
- Brain masks (for computing SURE only within the brain region)
- Noise variance estimate per stack (from background std or from the quality metrics SNR)
- No clean reference needed

### 5.3 SURE schedule

SURE loss is ramped in during training:
- Epochs 1-30: `λ_sure = 0` (supervised only, establish baseline)
- Epochs 30-200: `λ_sure` linearly ramps from 0 to target (e.g., 0.01)
- This prevents SURE from destabilizing early training when the model is still learning basic enhancement

---

## 6. Comparison: v3 vs v4

| Metric | v3 (current) | v4 (this proposal) | Improvement |
|--------|-------------|---------------------|-------------|
| Train subjects | 212 | 422 | +99% |
| Train synthetic pairs | 12,932 | 464,820 | +36x |
| Degradation configs | 6 types (sampled) | 61 configs (full grid) | +10x coverage |
| Subjects with tissue segs | 43 | 148 | +3.4x |
| Tissue label accuracy | 73% success, Dice-based | 100% success, zero reg error | perfect |
| Protocols in training | 6 | 9 (+HBCD, SpinaBifida, HTX) | +3 new |
| SURE val split | none (all 317 used for SURE) | 15 held-out real stacks | proper eval |
| Tissue classifier loss | Focal + CE(weight=25) | DiceCE + label smoothing | stable convergence |
| Val strategy | Synthetic only | Synthetic + real | generalization check |

### What stayed the same
- Degradation physics (Rician, blur, bias implementations unchanged)
- EnhancementNet architecture (ResU-Net + FiLM)
- TissueClassifier architecture (3-level U-Net)
- Supervised loss (0.7*L1 + 0.3*(1-SSIM))
- SURE loss (MC-SURE with warmup)
- Slice sampling (central 20-80% z-range, random slice per call)
- Normalization (degraded image's [p1, p99] → [0,1])
- Augmentation (random H/V flip, consistent across image/label/mask)

---

## 7. Remaining Work

| Task | Status | Blocking? |
|------|--------|-----------|
| Phase 1: Crawl CanonicalData | ✅ DONE | — |
| Phase 2: Quality metrics | ✅ DONE | — |
| Phase 3: Cohort assignment | ✅ DONE | — |
| Phase 5: Manifest generation | ✅ DONE | — |
| Freeview visual review (MEDIUM subjects) | TODO | Blocks SURE expansion |
| Merge v3 LOW stacks into SURE split | TODO | Quick |
| Phase 4a: NeSVoR re-run on 148 TIER_A | TODO | **GPU bottleneck (3-5 days)** |
| Phase 4b: Inverse alignment batch | TODO | Depends on 4a |
| Phase 4c: Visual verification | TODO | Depends on 4b |
| Phase 6: Characterization figures | TODO | Depends on all above |
| Phase A: Train TissueClassifier | TODO | Depends on 4b |
| Phase B: Train EnhancementNet | TODO | Depends on Phase A |

**Critical path:** NeSVoR re-run (Phase 4a) → inverse alignment (4b) → TissueClassifier training (Phase A) → EnhancementNet training (Phase B).

Phases 1-3 and 5 are done. Can start training Phase B immediately with brain mask FiLM (TIER_B subjects) while tissue labels are being generated for TIER_A.

---

## Related

- [[fetenh-data-pipeline-plan]] — Pipeline implementation details and Phase 1-5 results
- [[fetenh-tissue-classifier-loss]] — Loss function research (DiceCE + label smoothing)
- [[fetenh-inverse-alignment-pipeline]] — Yair's 4-step pipeline
- [[fetenh-net]] — Main project, training history
- [[fetenh-data-knowledge-graph]] — Complete NFS data map
- [[fetenh-data-methodology]] — Qualitative-first approach
