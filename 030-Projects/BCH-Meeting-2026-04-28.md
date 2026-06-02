# BCH Meeting Minutes -- 2026-04-28

**Date:** 2026-04-28
**Project:** FetEnhNet -- Progress Update & New Training Strategy
**Attendees:** Daniel Barreras Meraz + Grant Lab team

---

## Presented

12-page Beamer presentation covering the full pipeline end-to-end:

1. **Problem statement** -- fetal HASTE MRI quality limitations
2. **Data preparation** -- inverse alignment pipeline (Yair's solution), tissue label projection, 363/383 subjects with labels (92.4% coverage, 179K slices)
3. **Method** -- FetEnhNet architecture with FiLM tissue conditioning, training with supervised + SURE losses
4. **Results** -- synthetic evaluation table (Run 01: +4.29 dB overall across 9 enhancement-targeted degradation types), real LOW stack examples with sigma-normalized difference maps
5. **2.5D and perceptual variants** -- Run 05 (2.5D + SURE, best val_sup 0.0785) and Run 07 (2.5D + perceptual, +3.35 dB)

---

## Feedback Received

### 1. Establish baselines before combining losses
- Do not combine loss functions yet. First replicate the BME-X approach exactly as a baseline, then train with each loss type individually. The goal is to understand the effect each loss has on the model before mixing them.
- **Action:** Create a systematic baseline training campaign: one run per loss type, matched conditions.

### 2. Match BME-X degradation types
- Use the same degradation types as BME-X to ensure a fair comparison and reproducibility.
- **Action:** Review BME-X paper/code for exact degradation parameters and replicate them in the training pipeline.

### 3. Improve degradation realism
- Degradation parameter ranges should be informed by experience from data processing, not arbitrary ranges. Use knowledge gained from working with real LOW stacks throughout the pipeline to set realistic values.
- **Action:** Update degradation parameters based on observations from data processing experience.

### 4. Brain augmentation / padding
- Add brain augmentation or padding so that input sizes are standardized and easier to work with across different experiments.
- **Action:** Implement brain-region cropping with consistent padding to a fixed canvas size.

### 5. Tissue classifier step visualization
- Include the tissue classifier prediction as a visualization step in all result figures, so the audience can see what conditioning the model receives at inference time.
- **Action:** Add tissue classifier output panel to all evaluation and comparison figures.

---

## Follow-up from Hyeokjin (email, Apr 28)

Hyeokjin clarified degradation scope for fetal HASTE raw stacks:

1. **Drop BME-X motion/k-space degradations** -- BME-X motion simulation (phase-encode ghosting, k-space corruption) is designed for reconstructed postnatal T1w volumes. These do not apply to fetal HASTE raw stacks where the artifact model is fundamentally different (inter-slice motion, not intra-slice k-space corruption).

2. **Degradation types to use:**
   - **Noise** (Gaussian/Rician) -- already included
   - **Smoothing/blur** -- already included
   - **Bias field** (intensity inhomogeneity) -- discuss with Victoria & Suzette. Look at real LOW data exhibiting this problem and simulate it. This is a priority addition.
   - **Down-sampling** (optional) -- simulate "small brain" cases where the brain region contains few voxels. Down-sample 2D image (e.g. 1x1 -> 1.5x1.5). Just an idea to consider.

---

## Action Items

| # | Item | Owner |
|---|------|-------|
| 1 | Train individual loss baselines (supervised L1, SURE, perceptual, frequency) under identical conditions | Daniel |
| 2 | Implement degradation engine with: noise, smoothing, bias field, (optional) down-sampling -- NO motion/k-space | Daniel |
| 3 | Discuss bias field cases with Victoria & Suzette, review real LOW data with intensity inhomogeneity | Daniel |
| 4 | Update degradation parameters based on data processing experience | Daniel |
| 5 | Implement brain crop + padding to fixed canvas size | Daniel |
| 6 | Add tissue classifier prediction panel to all evaluation figures | Daniel |
| 7 | Consider down-sampling augmentation to simulate small brain cases | Daniel |

---

## Email Thread

### Daniel -> Team (Apr 28, 16:51)
Meeting minutes sent (see Presented and Feedback sections above).

### Hyeokjin -> Team (Apr 28)
Clarified degradation scope:
- Drop BME-X motion/k-space degradations -- don't fit fetal HASTE case
- Keep: noise, smoothing
- Add: bias field (discuss with Victoria & Suzette, look at real LOW data)
- Consider: down-sampling to simulate "small brain" (e.g. 1x1 -> 1.5x1.5)

### Daniel -> Team (reply)
Acknowledged. Will drop motion/k-space, focus on noise + smoothing + bias field. Will reach out to Victoria & Suzette about bias field. Will explore down-sampling idea.
