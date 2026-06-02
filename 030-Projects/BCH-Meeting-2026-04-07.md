# BCH Meeting Minutes — 2026-04-07

**Date:** 2026-04-07
**Project:** FetEnhNet Run21 — Progress Presentation
**Attendees:** Daniel Barreras Meraz + Grant Lab team

---

## Presented

Run21 progress slides covering:
- Motivation and challenge (fetal HASTE MRI low quality cases)
- Method: FetEnhNet architecture + MC-SURE self-supervised loss
- Training curves: Run21_sup (done ep 300) and Run21_sure (ep ~220/300, ongoing)
- Results: Run21_sup synthetic evaluation (PSNR +3.36 dB, SSIM +0.119) and real stack gallery

---

## Feedback Received

### 1. Difference map visualization
- Current approach (amplified signed diff × 5, RdBu_r colormap, absolute values) is not comparable across subjects because the intensity normalization differs per stack
- **Action:** Replace with a metric that is comparable across subjects — e.g., z-score normalized difference, or difference as % of input dynamic range, or PSNR-equivalent pixel error

### 2. Alignment figures needed
- Show figures demonstrating the alignment work — the lab is working on a generalizable alignment method across the different software pipelines used to process subjects (different cohorts processed with different tools)
- **Action:** Generate and add alignment overlay figures to next presentation

### 3. Model specifics — deeper explanation needed
- Audience needs more explanation of:
  - The supervised loss $\mathcal{L}_{\text{sup}}$: what it is, what it measures, why it going down is good
  - The SURE loss $\mathcal{L}_{\text{SURE}}$: the math, what the divergence estimator is doing, why sigma matters
- **Action:** Add a dedicated "Loss Functions" slide to the next presentation with plain-language and math

### 4. Overfitting investigation
- Model appears to be overfitting — val_sup is climbing while train loss keeps going down
- **Confirmed:** Both Run21_sup and Run21_sure show classic overfitting:
  - Run21_sure: best val_sup = 0.0716 at ep 17 (before SURE activates at ep 32), climbs to ~0.090 by ep 220
  - Run21_sup: best val_sup = 0.0705 at ep 12, climbs to 0.0799 by ep 300
  - Train loss: 0.0638 → 0.0565 (still going down = model memorizing training pairs)
- **Critical implication:** best.pt for Run21_sure was saved at ep 17, BEFORE SURE activated — the "best" checkpoint by val_sup criterion has zero SURE benefit. Need a different checkpoint selection strategy
- **Action:** Investigate overfitting causes (regularization, dropout, weight decay, data augmentation). Fix mask alignment first as that may be contributing to train/val distribution mismatch

### 5. Fix mask alignment before next training attempt
- Brain masks used for FiLM conditioning must be properly aligned with the image stacks before launching Run22
- Misaligned masks would cause the model to apply tissue-aware conditioning to wrong spatial regions, degrading generalization
- **Action:** Verify and fix mask-to-image alignment across all manifests before next run

### 6. Colorbar / difference metric
- Current colorbar is "absolute signed difference of normalized [0,1] intensity" — not comparable across subjects
- A diff of 0.05 in one stack means something different than 0.05 in another if normalization differs
- **Action:** Change to a subject-comparable metric (e.g., percent change relative to input range, or standardized by background noise sigma)

### 7. Explain loss functions formally
- Add to presentation or methods: formal definition of $\mathcal{L}_{\text{sup}}$ and $\mathcal{L}_{\text{SURE}}$
- $\mathcal{L}_{\text{sup}}$: pixel-wise reconstruction loss (L1 or L2) between $f(x_{\text{deg}})$ and $x_{\text{clean}}$
- $\mathcal{L}_{\text{SURE}}$: Monte Carlo Stein estimator — measures expected risk on noisy observations without needing clean reference

---

## Action Items (priority order)

| # | Item | Owner | Notes |
|---|------|-------|-------|
| 1 | Fix mask alignment across all manifests | Daniel | Before Run22 launch |
| 2 | Investigate overfitting — regularization strategy | Daniel | Consider early stopping, weight decay, dropout |
| 3 | Replace difference map colorbar with cross-subject comparable metric | Daniel | % change or sigma-normalized |
| 4 | Add alignment figures to next presentation | Daniel | Show cross-software alignment |
| 5 | Add loss function slide (formal + plain language) | Daniel | L_sup and L_SURE math |
| 6 | Re-evaluate Run21_sure checkpoint strategy | Daniel | best.pt is pre-SURE — need post-SURE selection criterion |

---

## Key Technical Note — Overfitting and val_sup Gap

The increasing gap between Run21_sure val_sup and Run21_sup val_sup is **not primarily** due to SURE's domain shift — it is primarily overfitting, amplified by SURE's stochastic gradient noise. Both models' val_sup is worse at ep 200+ than at ep 12–17.

The implication for Run21_sure: the checkpoint that minimizes val_sup (best.pt, ep 17) is also the checkpoint with the least SURE exposure. Evaluating best.pt will not show SURE's benefit. For the paper, the correct comparison is:
- Run21_sup: latest stable checkpoint (ep 300)
- Run21_sure: latest stable post-SURE checkpoint, selected by real-image no-reference metric (SNR/CNR), not val_sup

---

## Context

- Run21_sure training ongoing: ep ~220/300, ~12h remaining
- Once complete: run evaluate_real.py on busan comparing both models on 317 real LOW stacks
- Gallery of 1352 diff-panel images already generated for Run21_sup (on busan)
- Presentation: `/home/brmz/Downloads/fetenh_run21_slides.pdf`
- Presenter script: `/home/brmz/Downloads/fetenh_run21_script.md`
