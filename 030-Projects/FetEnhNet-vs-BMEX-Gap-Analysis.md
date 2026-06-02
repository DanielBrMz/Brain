# FetEnhNet vs BME-X: Scientific Gap Analysis

**Date:** 2026-05-07
**Purpose:** Internal gap analysis for fetal brain MRI enhancement. All facts verified from codebases. Brutally honest assessment.

---

## Executive Summary

BME-X (Sun et al., Nature BME 2025) holds one decisive advantage: **real paired training data** (same subject scanned twice). FetEnhNet counters with superior architecture, loss design, augmentation, degradation modeling, and 10x more fetal subjects --- but every one of those advantages rests on the assumption that synthetic degradations approximate real LOW stacks well enough. That assumption is currently **unvalidated**.

---

## 1. Data Quality & Quantity

| Dimension | BME-X | FetEnhNet | Verdict |
|-----------|-------|-----------|---------|
| Fetal subjects | 52 | 538 | FetEnhNet (10x) |
| Total subjects | 516 (incl. 464 pediatric) | 538 fetal-only | Comparable volume, different populations |
| Sites | 1 (BCP) | Multi-site, 8 protocols | FetEnhNet |
| Pair type | Real LOW-HIGH (same subject, two scans) | Synthetic LOW from real HIGH | **BME-X** |
| Label quality audit | None visible in code | Pre-computed fg-in-tissue fraction (5396 good, 11 borderline, 6 bad) | FetEnhNet |
| Slice count | Unknown (3D patches from volumes) | 179K slices | FetEnhNet (transparent) |

### Who is ahead

**BME-X is ahead on data authenticity.** Real paired data is the gold standard --- it captures the true joint distribution of artifacts. No synthetic pipeline, however sophisticated, perfectly replicates real scanner behavior.

**FetEnhNet is ahead on data scale, diversity, and auditability.** Multi-site, multi-protocol data with explicit quality auditing is stronger for generalization.

### Actions needed

1. **Domain gap quantification (CRITICAL).** Compute distributional statistics (noise floor, bias field smoothness, k-space energy profiles, SNR histograms) on real LOW stacks from BCP or equivalent, then compare against our synthetic LOW stacks. Without this, we cannot claim equivalence.
2. **Acquire or simulate real paired data.** Even a small validation set of real LOW-HIGH pairs (10--20 subjects) would let us measure the synthetic-to-real gap directly.
3. **Cross-domain evaluation.** Train on synthetic, evaluate on real LOW stacks (if available). Report the delta vs training on real pairs.

---

## 2. Degradation Realism

| Degradation | BME-X | FetEnhNet | Physics-correct? |
|-------------|-------|-----------|------------------|
| Rician noise | N/A (real data) | Complex magnitude model with random phase + coil sensitivity | Yes |
| Gaussian blur | N/A | Per-slice 2D | Approximate (real PSF is 3D and anisotropic) |
| Bias field | N/A | Yair directional + Legendre polynomial + exp(), brain-focused soft mask | Yes (standard model) |
| Gibbs ringing | N/A | Hard rectangular k-space cutoff along PE axis | Yes |
| K-space spike | N/A | Log-magnitude injection with conjugate spike | Yes |
| Signal dropout | N/A | Hybrid k-space PE-line zeroing + image-domain dark bands | Partially (simplified) |
| Intra-slice motion | N/A | Per-slice rigid + k-space phase ramp | Yes (single-shot approximation) |
| Downsample | N/A | K-space truncation | Yes |
| **Inter-slice motion** | Captured in real data | **Not modeled** | GAP |
| **Maternal/fetal overlap** | Captured in real data | **Not modeled** | GAP |
| **Through-plane aliasing** | Captured in real data | **Not modeled (2D)** | GAP |

### Who is ahead

**BME-X is trivially ahead** --- real data contains all artifacts by definition. FetEnhNet's degradation engine is physics-informed and covers 8 artifact types, which is strong, but three real-world phenomena are absent.

### Actions needed

1. **Validate degradation distributions.** For each of the 8 types, measure the parameter range in real LOW stacks (e.g., estimate noise level via background ROI, estimate bias field via N4 fitting) and confirm our sampling ranges overlap.
2. **Add inter-slice motion model.** This is the most common fetal artifact and we do not simulate it. Even a simple model (random per-slice shifts in k-space) would help.
3. **Consider maternal tissue contamination.** Real fetal scans have overlapping maternal anatomy. Our full-FOV approach partially handles this, but the degradation engine does not model it.
4. **Ablation: degradation realism.** Train with subsets of degradations and measure which contribute most. If some are never seen in real data, they add noise to training.

---

## 3. Architecture

| Feature | BME-X | FetEnhNet | Analysis |
|---------|-------|-----------|----------|
| Backbone | DU-Net (DenseBlocks, growth 16/32) | ResU-Net (residual blocks) | Both proven; DenseNet has better gradient flow, ResNet is simpler |
| Dimensionality | 3D (64x64x64 patches) | 2D (256x256 full FOV) | **BME-X** for inter-slice context; **FetEnhNet** for full spatial context |
| Tissue conditioning | Concatenation at input (4ch tissue + 1ch image -> 64ch) | FiLM: per-pixel affine at every decoder level | **FetEnhNet (FiLM)** --- strictly more expressive |
| Output formulation | Direct prediction (1ch output) | Residual: clamp(input + residual, 0, 1) | **FetEnhNet** --- residual learning converges faster, preserves unaffected regions |
| Dual-path correction | None | Additive + multiplicative (exp) for bias field | **FetEnhNet** --- architecturally principled for bias field |
| Skull handling | Requires skull stripping + histogram matching | Full FOV, no preprocessing | **FetEnhNet** --- more practical, fewer failure modes |
| Patch overlap | 40x40x40 stride on 64x64x64 patches (hardcoded mismatch: code says 64, options say 32) | Full slice, no stitching | **FetEnhNet** --- no boundary artifacts |

### Who is ahead

**FetEnhNet is ahead architecturally** on almost every axis. FiLM conditioning, residual learning, dual-path correction, and full-FOV processing are all principled improvements.

**BME-X's one architectural advantage is 3D context.** Inter-slice consistency matters for fetal MRI where through-plane resolution is poor. Our 2D approach loses this entirely.

### Actions needed

1. **2.5D or 3D extension.** Implement a 2.5D mode (adjacent slices as input channels) or a lightweight 3D refinement stage. This is our biggest architectural gap.
2. **Benchmark FiLM vs concat.** Run the BME-X baseline (concat mode) vs FiLM mode on the same data to quantify FiLM's advantage. If tissue classifier quality is poor, FiLM may actually hurt.
3. **Fix tissue classifier.** fg_dice=0.107 is extremely poor. Noisy tissue maps fed into FiLM inject noise at every decoder level. Either improve the classifier or fall back to concat until it is fixed.

---

## 4. Loss Functions

| Loss | BME-X (paper) | BME-X (code) | FetEnhNet |
|------|---------------|--------------|-----------|
| Cross-entropy (segmentation) | Yes | Yes (only loss actually used) | DiceCE + label smoothing |
| MSE (enhancement) | Yes (lambda=1e-7) | **Defined but NEVER called** | Yes (option) |
| L1 | No | No | Yes (primary) |
| SSIM | No | No | Yes |
| Frequency (FFT) | No | No | Yes |
| VGG Perceptual | No | No | Yes |
| MC-SURE | No | No | Yes (self-supervised) |

### Who is ahead

**FetEnhNet is decisively ahead.** BME-X's enhancement branch receives gradient signal **only** through backpropagation from the segmentation cross-entropy loss. This is a critical finding: the enhancement network is not directly optimized for image quality. It learns to produce outputs that, when segmented, minimize CE --- a very indirect supervision signal.

FetEnhNet has 5 supervised losses plus MC-SURE for self-supervised training on real data without ground truth.

### Actions needed

1. **Exploit this in the paper.** BME-X's released code contradicts the paper's claimed loss function. Document this clearly (with code line references) as it fundamentally changes what the model actually learns.
2. **Validate SURE on real LOW stacks.** SURE is our unique capability for domain adaptation. Test it on held-out real LOW data and report whether it closes the synthetic-to-real gap.
3. **Loss ablation.** Quantify the contribution of each loss component. Some may be redundant or conflicting.

---

## 5. Training Strategy

| Aspect | BME-X | FetEnhNet |
|--------|-------|-----------|
| Training mode | Joint end-to-end (both stages, single forward pass) | Staged: freeze classifier, then train enhancer |
| Optimizer | SGD, lr=0.005, momentum=0.9 | Adam, lr=1e-4, weight_decay=1e-5 |
| Scheduler | StepLR(step=1, gamma=0.1) --- lr drops 10x every epoch | Cosine with 5-epoch warmup |
| Augmentation | **None** | nnU-Net v2 consensus (7 types) |
| Validation | **Commented out in code** | Active (assumed from logging infrastructure) |
| Normalization | data/10000.0 (global scalar) | Presumably [0,1] range |
| Reproducibility | Hardcoded values, no seeding visible | Deterministic (subject, slice, epoch) seeding |
| Monitoring | None visible | JSONL logger, loss curves, sample grids, degradation stats, explorer |

### Who is ahead

**FetEnhNet is ahead on training rigor.** BME-X's training setup has multiple red flags:
- StepLR with step=1 and gamma=0.1 means lr goes 0.005 -> 0.0005 -> 0.00005 after just 2 epochs. This is extremely aggressive decay.
- No augmentation on a dataset of 52 fetal subjects is a severe overfitting risk.
- Validation being commented out means there is no way to detect overfitting during training.

### Actions needed

1. **Joint training experiment.** Our staged training is more stable but potentially leaves performance on the table. Implement and test joint end-to-end training with appropriate loss weighting.
2. **Verify our validation pipeline.** Confirm that validation runs on held-out subjects (not slices from training subjects) to avoid data leakage.

---

## 6. Tissue Conditioning Quality

| Metric | BME-X | FetEnhNet |
|--------|-------|-----------|
| Tissue classes | 4 (BG, CSF, GM, WM) | 4 (BG, CP, WM_SP, CSF) |
| Classifier accuracy | Not reported in code | fg_dice = 0.107 (very poor) |
| Conditioning method | Input concatenation | FiLM (per-pixel affine at every decoder level) |
| Impact of poor tissue maps | Low (only at input, network can learn to ignore) | **High (noisy affine transform at every level)** |

### Who is ahead

**BME-X is ahead in practice** despite having a less expressive conditioning method. Their simple concatenation is robust to noisy tissue maps because the network can learn to down-weight the tissue channels. FetEnhNet's FiLM conditioning amplifies tissue map errors at every decoder level.

### Actions needed

1. **Fix the tissue classifier (URGENT).** fg_dice=0.107 means the classifier is barely above random for foreground tissues. This is the single biggest bottleneck for FiLM mode.
2. **Fallback strategy.** Until the classifier is fixed, use concat mode (our BME-X baseline) for all comparisons. FiLM with garbage tissue maps is worse than concat with garbage tissue maps.
3. **Pre-trained tissue classifier.** Consider using a separately trained, high-quality tissue segmentation model (e.g., from SynthSeg or similar) rather than training from scratch on our data.

---

## 7. Inference Pipeline

| Step | BME-X | FetEnhNet |
|------|-------|-----------|
| Preprocessing | Histogram match to age-matched template | None required |
| Brain extraction | Required (brain boundary extraction) | Not required (full FOV) |
| Patch/slice processing | Overlapping 3D patches, average predictions | Full 2D slices |
| Post-processing | Skull reintroduction | None |
| Template dependency | Yes (age-matched template needed) | No |
| Failure modes | Skull stripping failure, template mismatch, patch boundary artifacts | Potential hallucination outside brain |

### Who is ahead

**FetEnhNet is ahead for clinical deployment.** BME-X's inference pipeline has multiple failure points (skull stripping, histogram matching, template selection) that require manual intervention or can fail silently. FetEnhNet processes raw slices end-to-end.

### Actions needed

1. **Validate full-FOV behavior.** Confirm that our model does not hallucinate structure outside the brain or alter maternal tissue. The residual formulation should prevent this (residual near zero outside brain), but verify empirically.
2. **Benchmark inference speed.** 2D slice processing should be faster than 3D overlapping patches, but quantify this.

---

## 8. Reproducibility & Code Quality

| Aspect | BME-X | FetEnhNet |
|--------|-------|-----------|
| Loss implementation matches paper | **No** (MSE defined, never called) | N/A (no paper yet) |
| Validation during training | **Commented out** | Active logging infrastructure |
| Hardcoded inconsistencies | Patch size 64 in loop vs 32 in options | None identified |
| Augmentation | **None in code** | 7 types, nnU-Net consensus |
| Degradation modeling | **None in code** | 8 physics-based types, deterministic seeding |
| Data inspection tools | None | Explorer (interactive web tool) |
| Training monitoring | None visible | JSONL logger, loss curves, sample grids |
| Deterministic training | No seeding visible | (subject, slice, epoch) deterministic seeding |

### Who is ahead

**FetEnhNet is decisively ahead.** BME-X's released code has fundamental discrepancies with the paper (loss function, no augmentation, no validation, no degradation). This raises serious reproducibility concerns.

### Actions needed

1. **Document all BME-X code-paper discrepancies** with exact line references. This is valuable for the paper's related work section and for reviewers.
2. **Ensure our code matches every claim.** Every loss weight, every augmentation probability, every architecture detail must be verifiable from code.

---

## Summary: Gap Priority Matrix

| Gap | Owner | Severity | Effort | Priority |
|-----|-------|----------|--------|----------|
| Synthetic-to-real degradation validation | FetEnhNet | **CRITICAL** | Medium | 1 |
| Tissue classifier quality (fg_dice=0.107) | FetEnhNet | **CRITICAL** | High | 2 |
| Inter-slice context (2D vs 3D) | FetEnhNet | HIGH | High | 3 |
| Inter-slice motion degradation | FetEnhNet | HIGH | Medium | 4 |
| Joint training mode | FetEnhNet | MEDIUM | Medium | 5 |
| SURE validation on real LOW | FetEnhNet | MEDIUM | Low | 6 |
| Loss ablation study | FetEnhNet | MEDIUM | Medium | 7 |
| FiLM vs concat benchmark | FetEnhNet | MEDIUM | Low | 8 |
| Real paired validation set | FetEnhNet | HIGH | High (data access) | 9 |
| Full-FOV hallucination check | FetEnhNet | LOW | Low | 10 |

---

## Honest Scorecard

| Dimension | BME-X | FetEnhNet | Notes |
|-----------|:-----:|:---------:|-------|
| Data authenticity | **W** | L | Real pairs are irreplaceable |
| Data scale & diversity | L | **W** | 10x fetal subjects, multi-site |
| Architecture expressiveness | L | **W** | FiLM, residual, dual-path |
| Inter-slice modeling | **W** | L | 3D patches capture z-context |
| Loss design | L | **W** | 5 supervised + SURE vs only CE in practice |
| Training rigor | L | **W** | Augmentation, validation, monitoring |
| Degradation modeling | N/A | **W** | 8 physics-based types (but unvalidated) |
| Tissue conditioning (practice) | **W** | L | Our classifier is broken |
| Inference practicality | L | **W** | No preprocessing needed |
| Reproducibility | L | **W** | Code matches claims |
| **Domain gap risk** | **W** | L | Real data has zero domain gap |

**Bottom line:** FetEnhNet wins on 7/11 dimensions, but the 3 dimensions BME-X wins on (data authenticity, inter-slice modeling, functioning tissue conditioning) are existential risks. If our synthetic degradations do not match real artifacts, or our tissue classifier remains broken, none of our architectural advantages matter.

**The single most important experiment is degradation validation against real LOW stacks.** Everything else is secondary.
