# BCH Meeting Minutes -- 2026-04-14

**Date:** 2026-04-14
**Project:** FetEnhNet -- Tissue Label Projection Pipeline
**Attendees:** Daniel Barreras Meraz + Grant Lab team

---

## Presented

**1. Tissue Label Projection Pipeline**

The main focus of this week was solving the tissue label projection problem: how to accurately project manual tissue segmentations from the 31-week atlas space onto raw HASTE stack slices in scanner coordinates. This is necessary for correct FiLM conditioning in the enhancement network's second stage.

Five coordinate systems are involved in this chain (atlas, pipeline recon, NeSVoR atlas-aligned, NeSVoR scanner-space, and raw scanner space). A key finding was that the pipeline reconstruction output is not in scanner coordinates, confirmed via checkerboard comparison. This explained why all previous projection attempts using the pipeline's own transform failed.

14 registration approaches were tested, ranging from SimpleITK mutual information with various initializations, to binary brain shape registration, SynthMorph (deep learning, FreeSurfer 8.1), ANTs multi-start with 7 initial rotations, and pipeline-chain approaches. The winning method uses binary brain shape registration combined with a per-subject search over all 8 axis-flip combinations, selecting the flip that gives the highest Dice score against the brain mask. This addresses the rotational ambiguity caused by the brain's sagittal symmetry.

Starting from 212 subjects with manual segmentations across protocols (160 CHD, 28 Heterotaxy, 18 Normative, 6 Placenta), 83 passed a quality filter, 33 were verified with complete data on the NFS, and 25 succeeded at automated registration with Dice at or above 0.80. Of those, 19 achieved Dice above 0.90. The method is fully automated for these subjects.

**2. Loss Function Formalization**

The supervised loss and MC-SURE loss were presented with full mathematical definitions and plain-language explanations of each variable and term. MC stands for Monte Carlo, referring to the random sampling approximation of the divergence term. The divergence measures how sensitive the network is to input noise. The Monte Carlo trick estimates this with one random perturbation and one extra forward pass, making it computationally cheap.

For the noise level sigma required by SURE, we use per-slice estimation from the background region outside the brain mask. This is an approximation but is within a factor of 1.5 of the true noise, compared to the 3x overestimate from the hardcoded fallback in Run20.

**3. FiLM Conditioning**

FiLM (Feature-wise Linear Modulation) was explained from scratch. At each decoder layer, internal features are scaled and shifted based on the tissue type at each pixel. A 1x1 convolution maps the 4-class tissue probability vector into per-channel scale and shift values. This allows the network to learn tissue-specific enhancement strategies: preserving edges at cortical plate regions, smoothing aggressively in CSF.

**4. Comparable Difference Metric (Pending)**

The current signed-difference visualization is not comparable across subjects because intensity normalization differs per stack. The proposed replacement is a sigma-normalized difference that divides the pixel-level change by the background noise level, making the metric comparable across subjects. Implementation is planned for Run22 evaluation.

---

## Feedback Received

### 1. Present the complete pipeline end-to-end
- The group wants to see the full picture in the next presentation: from data preparation, through the tissue label projection, to the training process, and finally the model working on real images
- **Action:** Prepare a comprehensive walkthrough showing the complete data-to-output pipeline for the next meeting

---

## Action Items

| # | Item | Owner |
|---|------|-------|
| 1 | Prepare end-to-end pipeline presentation (data prep to model output) | Daniel |
| 2 | Scale tissue projection to 50+ subjects (160 CHD in CanonicalData) | Daniel |
| 3 | Implement sigma-normalized difference metric | Daniel |
| 4 | Split 317 LOW stacks into 250 train + 67 val for proper SURE validation | Daniel |
| 5 | Launch Run22 with aligned labels, regularization, and fixed checkpoint selection | Daniel |
