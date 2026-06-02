---
title: "Victoria Hydrocephalus Model — Detailed Next Steps Plan"
type: plan
created: 2026-05-16
updated: 2026-05-16
tags: [bch, hydrocephalus, segmentation, victoria, plan]
---

# Victoria Hydrocephalus Model — Next Steps Plan

Expert council consensus plan. Model is at 0.935 Mean Dice (inter-rater ceiling).
All augmentation experiments statistically indistinguishable (p=0.646).
The model is good. The remaining work is validation, publication, and clinical utility.

**Code:** `/neuro/labs/grantlab/research/MRI_processing/victoria.hopcohen/Code/unit_model_hydrocephalus/`
**Data:** `/neuro/labs/grantlab/research/MRI_processing/victoria.hopcohen/Hydrocephalus/`
**Checkpoints:** `outputs_diagnostic/fold_0..4/best_model.pth` (the 0.935 model)
**Python env:** `/neuro/users/victoria.hopcohen/.local/share/mamba/envs/hydrocephalus`
**Server:** hanyang (10.26.67.148), also busan (10.88.88.2) if hanyang is busy

---

## PHASE 1: IMMEDIATE (1-2 days)

### 1.1 Test-Time Augmentation (TTA)

**WHY:** TTA is the single highest-ROI improvement available. Averaging predictions over geometric transforms reduces boundary noise without any retraining. Expected improvement: +0.005-0.015 Dice, bringing the model to ~0.94-0.95.

**WHAT — exact implementation:**

```python
# TTA with 8 flip orientations (3 axes = 2^3 = 8 combinations)
import torch
import numpy as np
from monai.inferers import sliding_window_inference

def tta_predict(model, image, roi_size=(128,128,128), overlap=0.5):
    """
    Test-time augmentation with 8 flip orientations.
    image: (1, 1, D, H, W) tensor
    Returns: (1, 3, D, H, W) averaged softmax probabilities
    """
    axes_combos = [
        [],        # original
        [2],       # flip D
        [3],       # flip H
        [4],       # flip W
        [2,3],     # flip D+H
        [2,4],     # flip D+W
        [3,4],     # flip H+W
        [2,3,4],   # flip all
    ]

    accumulated = torch.zeros_like(
        sliding_window_inference(image, roi_size, 4, model, overlap=overlap, mode="gaussian")
    )

    for axes in axes_combos:
        # Flip input
        x = image
        for ax in axes:
            x = torch.flip(x, dims=[ax])

        # Predict
        pred = sliding_window_inference(x, roi_size, 4, model, overlap=overlap, mode="gaussian")
        pred = torch.softmax(pred, dim=1)

        # Unflip prediction
        for ax in reversed(axes):
            pred = torch.flip(pred, dims=[ax])

        accumulated += pred

    # Average and argmax
    averaged = accumulated / len(axes_combos)
    return averaged
```

**Key decisions:**
- Use softmax probabilities, NOT logits, for averaging. Logit averaging gives disproportionate weight to high-confidence predictions. (Dr. ML and Dr. Stats agree; Dr. Engineer notes logit averaging is sometimes used for calibration but softmax is standard for segmentation TTA.)
- 8 orientations (flips only). Do NOT add 90-degree rotations — fetal brain orientation is already variable, and 24+ orientations would 3x inference time for marginal gain.
- Use `mode="gaussian"` in sliding window (already used) — this weights center voxels higher in overlapping patches.
- Overlap 0.5 is fine. Do not increase to 0.75 — the 4x inference cost from TTA is already substantial.

**HOW to measure success:**
- Run TTA inference on all 17 manual subjects using the existing 5-fold setup (each subject predicted by its held-out fold model)
- Compare: Dice with TTA vs Dice without TTA, per subject
- Report: paired Wilcoxon signed-rank test (n=17, non-parametric appropriate for small n)
- Expected: p < 0.05 for improvement, +0.005-0.015 mean Dice

**RISK if skipped:** Leaving +0.01 Dice on the table for free. Every competing method will use TTA. Reviewers will ask why you didn't.

---

### 1.2 Connected Component Post-Processing

**WHY:** The model occasionally produces small disconnected blobs (especially for ventricles in mild cases). Removing these improves HD95 more than Dice, but both benefit. HD95 is more clinically relevant than Dice for surgical planning.

**WHAT — exact implementation:**

```python
import numpy as np
from scipy import ndimage

def postprocess_prediction(pred_argmax, min_brain_cc_voxels=500, min_vent_cc_voxels=50):
    """
    Post-process a 3D segmentation prediction.
    pred_argmax: (D, H, W) integer array, 0=bg, 1=brain, 2=ventricle

    Steps:
    1. Brain: keep largest connected component only
    2. Ventricle: keep largest CC, then enforce ventricle-inside-brain constraint
    3. Fill small holes in brain mask
    """
    result = np.zeros_like(pred_argmax)

    # Step 1: Brain — largest connected component
    brain_mask = (pred_argmax == 1) | (pred_argmax == 2)  # brain includes ventricle region
    if brain_mask.sum() > 0:
        labeled, n_cc = ndimage.label(brain_mask)
        if n_cc > 0:
            cc_sizes = ndimage.sum(brain_mask, labeled, range(1, n_cc + 1))
            largest_cc = np.argmax(cc_sizes) + 1
            brain_mask = (labeled == largest_cc)

    # Step 2: Fill holes in brain (small background pockets inside brain)
    brain_filled = ndimage.binary_fill_holes(brain_mask)

    # Step 3: Ventricle — largest CC, must be inside brain
    vent_mask = (pred_argmax == 2)
    vent_mask = vent_mask & brain_filled  # enforce containment
    if vent_mask.sum() > 0:
        labeled_v, n_cc_v = ndimage.label(vent_mask)
        if n_cc_v > 0:
            cc_sizes_v = ndimage.sum(vent_mask, labeled_v, range(1, n_cc_v + 1))
            largest_cc_v = np.argmax(cc_sizes_v) + 1
            vent_mask = (labeled_v == largest_cc_v)

    # Assemble
    result[brain_filled] = 1
    result[vent_mask] = 2

    return result
```

**Key decisions:**
- Process brain FIRST, then ventricles. Brain provides the containment constraint for ventricles. (All experts agree.)
- Keep largest CC only for brain. For ventricles, also keep largest CC only — in hydrocephalus, the ventricles are a single connected structure (Dr. Clinical confirms: even in asymmetric ventriculomegaly, the ventricular system is connected at the foramina).
- Fill holes in brain mask. Small internal background pockets are always segmentation errors, never real anatomy. (Dr. Clinical: "There is no background inside the fetal brain.")
- Do NOT use min_vent_cc_voxels as a hard filter — just keep the largest. In severe hydrocephalus the ventricles are huge; in mild cases they might be small but real.
- `min_brain_cc_voxels=500` is a safety check — if brain CC is tiny, something is very wrong.

**HOW to measure success:**
- Compare HD95 before and after post-processing (expect largest improvement here)
- Compare Dice before and after (expect small improvement, 0.001-0.005)
- Report number of subjects where post-processing changed the prediction
- Count: how many disconnected CCs were removed per subject (document this)

**RISK if skipped:** HD95 outliers in the paper. A single disconnected blob 30mm away from the brain inflates HD95 catastrophically. This is a known failure mode that reviewers will check.

**DEBATE:** Dr. Data argues for keeping the top-2 ventricle CCs (bilateral ventricles could be disconnected at the midline in some slices). Dr. Clinical disagrees — at this resolution (0.5-0.8mm isotropic after NeSVoR), the third ventricle connects them. Dr. ML suggests: keep largest CC, but log cases where a second CC > 20% of the largest exists, and manually review those. **Resolution: keep largest only, but log multi-CC cases for review.**

---

### 1.3 Publication-Quality Figures and Metrics Table

**WHY:** These are needed regardless of any other work. Generate them now while the analysis is fresh.

**WHAT — exact deliverables:**

**Figure 1: Representative segmentation results (3x4 grid)**
- 3 subjects: one "easy" (high Dice), one "median", one "hard" (lowest Dice)
- 4 columns: original image, ground truth overlay, prediction overlay, error map
- Axial, coronal, sagittal views (pick the slice with largest ventricle cross-section)
- Use: red=brain boundary, blue=ventricle boundary, green=overlap
- Resolution: 300 DPI, saved as both PDF and PNG

**Figure 2: Box plots of per-fold Dice scores**
- Side-by-side boxes for brain and ventricle Dice
- Individual data points overlaid (n=17 is small enough to show all points)
- Include horizontal line at inter-rater agreement level (0.88-0.93 shaded band)
- This figure makes the "at ceiling" argument visually

**Figure 3: Bland-Altman plot (ventricle volume)**
- X-axis: mean of manual and predicted ventricle volume (mL)
- Y-axis: difference (predicted - manual)
- Include: mean bias line, +/- 1.96 SD limits of agreement
- This is THE clinical validation figure

**Figure 4: Scatter plot — predicted vs manual ventricle volume**
- With identity line (y=x)
- Report: Pearson r, ICC(2,1), regression equation
- Color-code by gestational age if available

**Table 1: Per-fold and overall metrics**
```
| Fold | N | Brain Dice | Vent Dice | Mean Dice | Brain HD95 | Vent HD95 |
|------|---|-----------|-----------|-----------|-----------|-----------|
| 0    | . | ...       | ...       | ...       | ...       | ...       |
| ...  |   |           |           |           |           |           |
| Overall | 17 | mean +/- std | ... | ... | ... | ... |
```

**Table 2: Comparison with inter-rater agreement**
- Include published inter-rater Dice values for fetal ventricle segmentation
- Sources: Payette et al. 2021, Fidon et al. 2021, FeTA challenge papers
- Show that 0.935 is at or above human inter-rater performance

**HOW to implement:**
```python
# Use matplotlib with publication settings
import matplotlib
matplotlib.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})
```

Save all figures to: `outputs_diagnostic/figures/` (persistent, on NFS)

**RISK if skipped:** You will regenerate these multiple times later under time pressure. Do them once, properly, now.

---

## PHASE 2: SHORT-TERM (1-2 weeks)

### 2.1 nnU-Net Baseline

**WHY:** nnU-Net is the de facto standard baseline in medical image segmentation. Any MICCAI/MedIA reviewer will ask "did you compare to nnU-Net?" If your 3D UNet beats or matches nnU-Net, it validates your architecture choice. If nnU-Net wins, you adopt it.

**WHAT — exact steps:**

**Step 1: Data format conversion (1 hour)**
```bash
# nnU-Net expects a specific folder structure
# Task ID: pick 601 (arbitrary, 5xx are common examples)
NNUNET_RAW=/path/to/nnUNet_raw/Dataset601_FetalHydro

mkdir -p $NNUNET_RAW/imagesTr
mkdir -p $NNUNET_RAW/labelsTr
mkdir -p $NNUNET_RAW/imagesTs  # optional, can use cross-val instead
```

Convert data:
```python
# For each subject in data_list.csv:
# 1. Copy recon image to imagesTr/HYDRO_NNN_0000.nii.gz
#    (the _0000 suffix = single modality channel 0)
# 2. Merge brain + ventricle labels into single multi-class label:
#    0=background, 1=brain, 2=ventricle
#    Save to labelsTr/HYDRO_NNN.nii.gz

# Create dataset.json:
{
    "channel_names": {"0": "T2w_NeSVoR"},
    "labels": {"background": 0, "brain": 1, "ventricle": 2},
    "numTraining": 49,  # all subjects (17 manual + pseudo)
    "file_ending": ".nii.gz"
}
```

**Step 2: Install nnU-Net v2 (30 min)**
```bash
# In Victoria's conda env or a new one:
pip install nnunetv2
# Set environment variables:
export nnUNet_raw="/path/to/nnUNet_raw"
export nnUNet_preprocessed="/path/to/nnUNet_preprocessed"
export nnUNet_results="/path/to/nnUNet_results"
```

**Step 3: Plan and preprocess (10 min)**
```bash
nnUNetv2_plan_and_preprocess -d 601 --verify_dataset_integrity
# This auto-configures: patch size, batch size, augmentation, architecture
```

**Step 4: Train 5-fold (8-12 hours on A5000)**
```bash
# Train all 5 folds (can parallelize across GPUs)
for fold in 0 1 2 3 4; do
    nnUNetv2_train 601 3d_fullres $fold
done
```

**Step 5: Compare results**
```bash
nnUNetv2_find_best_configuration 601
# Extract per-fold Dice scores from the JSON outputs
# Compare to your 0.935 using same statistical test (Nadeau-Bengio)
```

**HOW to measure success:**
- If nnU-Net Dice is within 0.01 of your model: report both, note equivalence. Your model wins on simplicity (no nnU-Net dependency for deployment).
- If nnU-Net Dice is > 0.01 better: adopt nnU-Net. It auto-configures everything and is the community standard.
- If nnU-Net Dice is > 0.01 worse: strong evidence your architecture choices were correct. Highlight this in the paper.

**DEBATE:** Dr. Engineer argues nnU-Net is overkill — the model is already at ceiling. Dr. Stats counters that without a calibrated baseline, reviewers cannot assess whether 0.935 is good for THIS task with THIS data. Dr. ML notes nnU-Net will also auto-configure augmentation correctly (unlike the miscalibrated elastic deformation). **Resolution: run it. 1 day of work, massive credibility for the paper.**

**RISK if skipped:** Paper rejected at top venues. "No comparison to nnU-Net" is a standard reviewer complaint in 2025-2026.

---

### 2.2 Clinical Validation Metrics

**WHY:** Dice and HD95 are not clinically meaningful on their own. Clinicians care about ventricle volume, ventricular-brain ratio (VBR), and how these correlate with manual measurements. A Bland-Altman plot showing agreement between predicted and manual VBR is worth more than +0.01 Dice for clinical adoption.

**WHAT — exact metrics to compute:**

**2.2.1 Ventricle Volume (mL)**
```python
def compute_volume_ml(mask, voxel_spacing_mm):
    """Volume in mL from a binary mask."""
    voxel_vol_mm3 = np.prod(voxel_spacing_mm)
    return mask.sum() * voxel_vol_mm3 / 1000.0  # mm^3 -> mL
```

Compute for each subject:
- Manual ventricle volume
- Predicted ventricle volume
- Manual brain volume
- Predicted brain volume

**2.2.2 Ventricular-Brain Ratio (VBR)**
```python
vbr = ventricle_volume / brain_volume  # typically 0.05-0.40 for hydrocephalus
```

This is THE clinical metric. It tracks hydrocephalus severity and treatment response.

**2.2.3 Bland-Altman Analysis**
```python
from scipy import stats

def bland_altman(manual, predicted):
    mean = (manual + predicted) / 2
    diff = predicted - manual
    mean_diff = np.mean(diff)  # bias
    std_diff = np.std(diff, ddof=1)
    loa_upper = mean_diff + 1.96 * std_diff
    loa_lower = mean_diff - 1.96 * std_diff

    # Check for proportional bias
    slope, intercept, r, p, se = stats.linregress(mean, diff)
    proportional_bias = p < 0.05

    return {
        'bias': mean_diff,
        'std': std_diff,
        'loa_upper': loa_upper,
        'loa_lower': loa_lower,
        'proportional_bias': proportional_bias,
        'proportional_p': p,
    }
```

**2.2.4 Intraclass Correlation Coefficient**
```python
# ICC(2,1) — two-way random, single measures, absolute agreement
# Use pingouin library:
import pingouin as pg
icc = pg.intraclass_corr(
    data=df, targets='subject', raters='method', ratings='volume'
)
# Report ICC(2,1) with 95% CI
# Target: ICC > 0.90 (excellent agreement)
```

**2.2.5 Per-GA Analysis**
- If gestational age metadata is available: scatter plot of Dice vs GA
- Hypothesis: model may perform worse at early GA (smaller ventricles, less contrast)
- If GA is not in the current data: note as a limitation, request from Victoria

**HOW to measure success:**
- VBR bias < 0.02 (2% absolute VBR difference)
- ICC > 0.90 for ventricle volume
- Limits of agreement within clinically acceptable range (Dr. Clinical: +/- 2 mL for ventricle volume, +/- 0.05 for VBR)
- No proportional bias (p > 0.05 in Bland-Altman regression)

**RISK if skipped:** The paper becomes a pure ML paper with no clinical relevance. Cannot publish in NeuroImage, AJNR, or Radiology without clinical validation metrics. Limits publication to ML-only venues (MICCAI workshop at best).

---

### 2.3 Error Analysis

**WHY:** Understanding WHERE and WHY the model fails is more valuable than the aggregate Dice score. It reveals whether failures are random (noise) or systematic (bias), and guides what data to collect next.

**WHAT — exact analysis:**

**2.3.1 Worst-subject deep dive**
- Rank all 17 manual subjects by Dice (per-class)
- For the bottom 3:
  - Visualize predictions slice-by-slice (all 3 planes)
  - Identify error patterns: over-segmentation vs under-segmentation
  - Check: is this a difficult anatomy (asymmetric ventricles, choroid plexus confusion, thin cortex)?
  - Check: is this a data quality issue (NeSVoR reconstruction artifact, motion corruption)?

**2.3.2 Spatial error heatmap**
```python
# For each subject, compute the error map (FP + FN)
# Register all error maps to a common space (e.g., the median-sized subject)
# Average to create a population error heatmap
# This reveals: "errors concentrate at the choroid plexus" or "errors at the cortical surface"
```

Dr. Clinical expects errors to concentrate at:
1. Choroid plexus / ventricle boundary (hardest boundary even for radiologists)
2. Temporal horn tips (thin, variable, easy to miss)
3. Third ventricle (small, midline, often excluded from manual labels)
4. Cortical surface near skull (partial volume effects)

**2.3.3 Failure mode classification**
For each error voxel, classify as:
- **Boundary imprecision:** error within 2 voxels of the true boundary → expected, not fixable beyond inter-rater level
- **Topological error:** disconnected components, holes → fixable by post-processing
- **Systematic bias:** consistent over/under-segmentation of a structure → fixable by more training data of that anatomy
- **Data quality error:** error correlates with reconstruction artifact → not fixable by the model, need upstream QC

**2.3.4 Per-subject report card**
Generate a 1-page PDF per subject:
- 3-plane views with overlay
- Per-class Dice and HD95
- Volume comparison (manual vs predicted)
- Error map overlay
- Flag any data quality concerns

Save to: `outputs_diagnostic/subject_reports/`

**HOW to measure success:**
- Identify top 3 failure modes with relative frequency
- Determine if errors are random or systematic
- If systematic: propose targeted fix (more data of that type, architectural change, or post-processing rule)

**RISK if skipped:** You cannot write the Discussion section of the paper. You cannot answer reviewer questions about failure modes. You cannot prioritize what to annotate next.

---

### 2.4 Pseudo-Label Quality Review

**WHY:** 32 of 49 training subjects have pseudo-labels (17 pseudo hydro + 15 pseudo severe vent). If pseudo-labels have systematic errors, the model has learned those errors. This must be quantified before publication.

**WHAT — exact protocol:**

**2.4.1 Select 8 subjects for radiologist review**
Selection criteria (stratified):
- 2 pseudo-hydro subjects with highest model confidence (easy cases — are pseudo-labels correct?)
- 2 pseudo-hydro subjects with lowest model confidence (hard cases — are pseudo-labels wrong?)
- 2 pseudo-severe-vent subjects with highest VBR (most pathological)
- 2 pseudo-severe-vent subjects with lowest VBR (borderline — most likely to have label errors)

**2.4.2 What the radiologist should check**
For each of the 8 subjects, have a radiologist (or Victoria under radiologist guidance) review:
- [ ] Ventricle boundary: is the choroid plexus included or excluded? (Must be EXCLUDED — it is not CSF)
- [ ] Brain boundary: does it include the cortical plate? Does it stop at the skull?
- [ ] Third ventricle: is it labeled? (Check consistency with manual labels)
- [ ] Aqueduct: is it labeled as ventricle? (Usually too small to see)
- [ ] Extra-axial CSF: is any subarachnoid CSF incorrectly labeled as ventricle?
- [ ] Overall quality score: 1 (unusable), 2 (minor errors), 3 (good), 4 (excellent)

**2.4.3 Quantitative pseudo-label assessment**
For the 17 pseudo-hydro subjects: use the trained model (from manual data only, the original 0.919 model) to predict, then compare model prediction to pseudo-label:
```python
# If model prediction and pseudo-label agree: high confidence the pseudo-label is correct
# If they disagree: the pseudo-label may be wrong, or the model may be wrong
# This gives a "pseudo-label confidence score" without needing manual review of all 17
agreement_dice = dice(model_prediction, pseudo_label)
# Subjects with agreement_dice < 0.85 → prioritize for manual review
```

**HOW to measure success:**
- All 8 reviewed subjects score >= 2 (minor errors or better)
- If any score 1: remove from training, retrain, report impact
- Agreement Dice between original model and pseudo-labels > 0.90 for at least 14/17 subjects
- Document choroid plexus inclusion/exclusion protocol explicitly

**DEBATE:** Dr. Stats argues pseudo-labels should be excluded from the primary analysis entirely — report manual-only results as the main finding, pseudo-label expansion as a secondary analysis. Dr. Data argues the 0.935 model (with pseudo-labels) IS the main result since it's better. Dr. ML suggests: report both. Main table: 0.919 (17 manual), secondary: 0.935 (49 subjects with pseudo-labels). **Resolution: report both. The 17-manual result is the scientifically rigorous primary finding. The 49-subject result demonstrates scalability.**

**RISK if skipped:** Reviewer asks "how do you know your pseudo-labels are correct?" and you have no answer. Paper rejected.

---

### 2.5 Ensemble Prediction

**WHY:** You already have 5 trained models (one per fold). Ensembling all 5 for inference on new subjects is free and always improves performance. This is your deployment model.

**WHAT:**
```python
def ensemble_predict(models, image, roi_size=(128,128,128)):
    """Average predictions from all 5 fold models."""
    accumulated = None
    for model in models:
        model.eval()
        with torch.no_grad():
            pred = tta_predict(model, image, roi_size)  # TTA within each model
            if accumulated is None:
                accumulated = pred
            else:
                accumulated += pred
    averaged = accumulated / len(models)
    return averaged.argmax(dim=1)
```

Combine with TTA: 5 models x 8 flips = 40 forward passes per subject. At 128^3 patches with sliding window, this takes ~2-5 minutes per subject on an A5000. Acceptable for clinical use.

**HOW to measure:**
- Cannot evaluate on the 17 manual subjects (each was in one fold's training set)
- Use for inference on NEW subjects only
- Report ensemble predictions alongside single-best-fold predictions on any new test data

**RISK if skipped:** Leaving performance on the table for deployment. Every serious segmentation pipeline uses ensembles.

---

## PHASE 3: MEDIUM-TERM (1-2 months)

### 3.1 More Manual Annotations

**WHY:** The only reliable path past 0.935 Dice is more manual training data. The model is data-limited, not architecture-limited. All experts agree on this.

**WHAT — annotation plan:**

**Target: 40-50 total manual subjects** (23-33 new annotations)

Priority order for new annotations:
1. **Severe hydrocephalus** (VBR > 0.30) — 5-8 subjects. The model sees these least; they have the most unusual anatomy.
2. **Early GA** (< 24 weeks) — 5-8 subjects. Smaller brains, less contrast, harder to segment.
3. **Late GA** (> 34 weeks) — 3-5 subjects. Larger, more folding, different proportions.
4. **Asymmetric ventriculomegaly** — 3-5 subjects. One large, one normal ventricle. Tests model's ability to handle bilateral asymmetry.
5. **Borderline cases** (VBR 0.05-0.10) — 3-5 subjects. Currently in the "severe ventriculomegaly" pseudo-label set, but boundary between normal and pathological.

**Annotation protocol (must be documented and consistent):**
1. Tool: ITK-SNAP or 3D Slicer (whichever Victoria uses — must be consistent)
2. Brain label: includes all intracranial tissue (cortical plate, white matter, deep gray, brainstem, cerebellum). Excludes: skull, extra-axial CSF, eyes.
3. Ventricle label: includes lateral ventricles (body, atrium, temporal horns, frontal horns, occipital horns), third ventricle, fourth ventricle. Excludes: choroid plexus, aqueduct (too small), subarachnoid CSF.
4. Choroid plexus protocol: must be explicitly defined. Options:
   - (a) Exclude from ventricle label (label as brain tissue). Preferred — cleaner boundary.
   - (b) Include in ventricle label. Simpler but inflates ventricle volume.
   - Whichever is chosen, apply CONSISTENTLY to all subjects.
5. Double annotation: 5 subjects should be annotated by 2 raters to establish intra-study inter-rater agreement.

**HOW to measure success:**
- Retrain 5-fold CV with 40-50 subjects
- Target: 0.945-0.960 Dice (extrapolating from 0.919 at n=17 to 0.935 at n=34)
- More importantly: narrower confidence intervals (95% CI width < 0.02 vs current 0.042)
- Inter-rater agreement (from 5 double-annotated subjects) establishes the true ceiling

**RISK if skipped:** The model stays at 0.935 forever. Cannot claim generalization beyond the 17 training anatomies. Cannot publish in a top journal without demonstrating the approach scales.

---

### 3.2 External Validation

**WHY:** A model trained and tested on one scanner/institution cannot claim generalizability. External validation is required for clinical translation and expected by reviewers at top venues.

**WHAT — options ranked by feasibility:**

1. **FeTA Challenge dataset** (publicly available)
   - Contains fetal brain MRI with annotations from multiple sites
   - Not hydrocephalus-specific, but includes some ventriculomegaly cases
   - Can test brain segmentation component
   - Advantage: immediate access, published benchmark numbers to compare against

2. **Collaboration with another institution**
   - Contact: UCSF (Oishi lab), KCL (Rutherford group), UZH (Jakab lab)
   - These groups have fetal MRI segmentation datasets
   - Even 5-10 external subjects would demonstrate generalizability

3. **Different scanner at BCH**
   - If BCH has both 1.5T and 3T fetal MRI, use the other field strength as external validation
   - Same institution but different acquisition parameters

**Protocol for external validation:**
- Apply the trained model WITHOUT any fine-tuning
- Report Dice, HD95, volume metrics on external data
- Compare to inter-rater agreement at the external site (if available)
- If performance drops > 0.05 Dice: investigate domain shift, consider fine-tuning

**HOW to measure success:**
- External Dice > 0.90 (within 0.04 of internal performance)
- No catastrophic failures (no subject with Dice < 0.70)
- Volume correlation ICC > 0.85

**RISK if skipped:** Paper limited to single-center retrospective study. Cannot claim clinical utility. Limits journal tier to specialty journals vs high-impact venues.

---

### 3.3 Manuscript Preparation

**WHY:** The model is ready for publication. The question is WHERE to publish and WHAT story to tell.

**WHAT — target journals (ranked by impact and fit):**

| Journal | IF | Fit | Timeline |
|---------|-----|-----|----------|
| NeuroImage | ~7 | Good — fetal neuroimaging + methods | 6-8 weeks review |
| Human Brain Mapping | ~5 | Good — brain mapping focus | 4-6 weeks review |
| Medical Image Analysis | ~10 | Excellent — methods journal | 8-12 weeks review |
| AJNR | ~4 | Good — clinical neuroradiology | 4-6 weeks review |
| Frontiers in Neuroscience | ~4 | Good — open access, faster | 4-8 weeks review |

**Dr. Stats recommends: Medical Image Analysis** if nnU-Net comparison is included and external validation is done. **NeuroImage or Human Brain Mapping** if clinical validation metrics are strong but no external data. **Frontiers** as a safe first-publication option for a student.

**Story structure:**
1. **Introduction:** Fetal hydrocephalus monitoring requires accurate ventricle volumetry. Manual segmentation is time-consuming and variable. Automated methods exist for normal fetal brains (FeTA challenge) but not for pathological hydrocephalus specifically.

2. **Methods:** 3D U-Net with DiceFocal loss, trained on NeSVoR reconstructions. Semi-supervised expansion with pseudo-labels. 5-fold cross-validation. TTA + ensemble + post-processing.

3. **Results:**
   - Primary: 0.935 Dice on 17 manually annotated subjects (5-fold CV)
   - Secondary: statistical equivalence with augmentation variants (p=0.646)
   - Clinical: Bland-Altman VBR, volume ICC, per-GA performance
   - Comparison: vs nnU-Net baseline
   - Error analysis: failure modes and spatial distribution

4. **Discussion:**
   - Performance at inter-rater agreement level
   - Pseudo-label approach enables scaling without expert annotation
   - Limitations: single-center, NeSVoR-dependent, n=49
   - Future: longitudinal tracking, treatment response monitoring

**Figure plan:**
- Fig 1: Method overview (architecture diagram + training pipeline)
- Fig 2: Representative results (good/median/poor subjects)
- Fig 3: Quantitative results (box plots + comparison)
- Fig 4: Clinical validation (Bland-Altman + volume scatter)
- Fig 5: Error analysis (spatial heatmap + failure modes)
- Supplementary: all per-subject results, augmentation experiment comparison

**RISK if skipped:** The work is never published. Victoria's contribution is lost. The model is never used clinically.

---

## SUMMARY: PRIORITY MATRIX

| Action | Effort | Impact | Priority |
|--------|--------|--------|----------|
| 1.1 TTA | 2 hours | +0.01 Dice for free | DO FIRST |
| 1.2 Post-processing | 1 hour | HD95 improvement, robustness | DO FIRST |
| 1.3 Figures/tables | 4 hours | Publication requirement | DO FIRST |
| 2.1 nnU-Net baseline | 1 day | Publication requirement | HIGH |
| 2.2 Clinical metrics | 1 day | Clinical relevance | HIGH |
| 2.3 Error analysis | 1 day | Understanding + Discussion section | HIGH |
| 2.4 Pseudo-label review | 2 days | Scientific rigor | HIGH |
| 2.5 Ensemble | 2 hours | Deployment quality | MEDIUM |
| 3.1 More annotations | 2-4 weeks | Only path to higher Dice | MEDIUM |
| 3.2 External validation | 2-4 weeks | Generalizability | MEDIUM |
| 3.3 Manuscript | 2-4 weeks | Career output | HIGH |

## CONSENSUS STATEMENTS (all 5 experts agree)

1. **Stop tuning augmentation.** All experiments are equivalent. The model is data-limited.
2. **Ship the 0.935 model** with TTA + post-processing as the working clinical tool.
3. **nnU-Net baseline is non-negotiable** for publication at any venue above workshop level.
4. **Clinical validation metrics (Bland-Altman, VBR, ICC) are non-negotiable** for any clinical venue.
5. **More manual annotations are the only path to higher Dice.** Architecture changes will not break through the ceiling.
6. **Report the 17-manual result as primary, 49-subject result as secondary.** The pseudo-label expansion is a contribution, not the main finding.
7. **Document the choroid plexus protocol.** This is the single largest source of inter-rater disagreement in ventricle segmentation.

## DISSENT LOG

- **Dr. Engineer** argues TTA is unnecessary overhead for a model at ceiling. Other 4 experts disagree — TTA is standard practice and the overhead is minimal at inference time.
- **Dr. Data** argues 128 mild/moderate ventriculomegaly subjects should be included (currently excluded). **Dr. Clinical** strongly disagrees — mixing mild VM (essentially normal ventricles) with hydrocephalus dilutes the training signal and changes the task from "hydrocephalus segmentation" to "general ventricle segmentation." **Resolution: keep excluded from hydrocephalus model. Could be a separate model or a severity-stratified analysis.**
- **Dr. Stats** argues the paper should not report the 0.935 number at all in the abstract — only the 0.919 from manual-only training, since selection bias from choosing the best of 4 runs inflates apparent performance. **Dr. ML** disagrees — 0.935 with pseudo-labels is a legitimate result if properly described. **Resolution: report 0.935 as the main result but clearly state it uses pseudo-labels, and report 0.919 as the manual-only baseline.**
