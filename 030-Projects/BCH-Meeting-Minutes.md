---
tags:
  - bch
  - meeting-minutes
  - fnndsc
---

# BCH / FNNDSC Meeting Minutes

> Weekly research meetings with Kiho Im's group at Boston Children's Hospital / Harvard Medical School.
> Daniel took over meeting minutes responsibility from Victoria Hop Cohen starting January 29, 2026.

## Team
- **PI:** Kiho Im
- **Members:** Hyeokjin Kwon, Yair Beltran, Quentin Moliterno, Kyeong Ho Kim, Victoria Hop Cohen, Suzette Saucedo Olvera, Seungyoon Jeong, Andrea Gondova, Daniel Barreras Meraz

---

## Individual Meeting Notes

- [[BCH-Meeting-2026-03-24|March 24 — Run18 presentation + label projection]]
- [[BCH-Meeting-2026-03-31|March 31 — Run20 plan, SURE loss reintroduction]]
- [[BCH-Meeting-2026-04-07|April 7 — Run21 progress presentation]]
- [[BCH-Meeting-2026-04-14|April 14 — Label projection pipeline, 14 registration approaches]]
- [[BCH-Meeting-2026-05-05|May 5 — BME-X baseline, degradation calibration, MONAI port]]

---

## January 6, 2026
*Author: Victoria Hop Cohen*

**Hydrocephalus:**
Progress:
- The ventricles have been accurately masked.
- The ventricular volume has been obtained.

Next steps:
- Compare ventricular volumes to validate the results.
- Using the same premise as the ventricular masking code, mask the whole brain.
- Obtain whole brain volume for all subjects.
- Perform a statistical analysis of the whole brain volume results.
  - Graph whole brain volume vs gestational age (and check for outliers).

**Cortical surface regional metrics:**
- Continue to run the matlab scripts on the chosen subjects.
- After, obtain regional metrics for control, CHD and placenta protocol subjects (as requested on a previous email).
- Explore the possibility of translating the matlab scripts into a third (mini) processing script (to be run after choosing the best template for a given brain), in Python.

**Other:**
- Explore strategies to improve processing efficiency.

---

## January 13, 2026
*Author: Victoria Hop Cohen*

**Hydrocephalus:**
Progress:
- The brain has been masked using Synthstrip
- Manual corrections have been performed in 7/14 subjects
  - Expected completion date: Tuesday

Next steps:
- Obtain the whole brain volume for all subjects.
- Perform a brief statistical analysis on both the ventricular volumes and the whole brain volumes (as a precaution).

**Cortical surface regional metrics:**
- Continue to run the matlab scripts on the chosen subjects.
- After, obtain regional metrics for control, CHD and placenta protocol subjects (as requested on a previous email).
- Explore the possibility of translating the matlab scripts into a third (mini) processing script (to be run after choosing the best template for a given brain), in Python.

**Other:**
- Explore strategies to improve processing efficiency.

---

## January 29, 2026
*Author: Daniel Barreras Meraz*

**Image Degradation Methods:**
Progress:
- Implemented four degradation techniques (Gaussian Noise, Rician Noise, Gaussian Smoothing, Bias Field)
- Conducted initial parameter calibration testing
- Motion artifact method discarded from pipeline

Next steps:
- Investigate alternative tools of Gaussian and Rician noise methods
- Implement brightness/intensity checks on subjects before applying degradations
- Compare synthetic degraded images against actual low-quality BCH subjects (CHD and Placenta protocols)
- Adjust sampling strategy: use more subjects with maximum 2 slices per subject
- Perform all degradation techniques and paste them in a single slide per subject.

**Raw Stack Quality Assessment:**
Progress:
- Identified BCH datasets and selected all subjects (High and Low Quality) from them

Next steps:
- Build reference set of actual low-quality cases to guide parameter calibration.

---

## February 10, 2026
*Author: Daniel Barreras Meraz*

**Raw Stack Quality Assessment:**
Progress:
- Attempted to quantitatively measure image degradation using several techniques:
  - SNR calculation (Dietrich method with Rayleigh correction)
  - Sharpness measurement (normalized Sobel gradient)
  - Bias Field Uniformity (BFU) estimation
  - Coefficient of Variation (CV) analysis
- Analyzed all 43 LOW quality raw stacks and identified 1366 HIGH quality raw stacks from BCH datasets
- Implemented many-to-many synthetic degradation matching pipeline to establish parameter ranges

Key Discussion Points:
- Quantitative metrics alone are insufficient to clearly identify which specific degradations affect image quality
- Bias field measurement is particularly challenging because different bias fields exist in maternal tissue versus actual fetal brain tissue (noted by Yair)
- Need to focus specifically on degradations affecting the brain within the brain stack, not the entire volume

Next Steps:
1. Perform qualitative classification (similar to Seungyoon's approach) focusing specifically on:
   - Noise characteristics affecting the fetal brain
   - Bias field patterns within the brain region
2. Build characterization cohorts of low-quality images based on qualitative visual assessment
3. Create reference sets with specific subjects per degradation category (noise-dominant, bias-dominant, mixed)
4. Inject synthetic degradations into high-quality raw stacks to match each qualitative cohort
5. Compare synthetic degraded images against actual low-quality cohort examples to validate degradation realism

**Image Degradation Methods:**
Progress:
- Used anatomically centered slice selection (middle of brain in axial view)

Next Steps:
- Shift from quantitative parameter optimization to qualitative cohort matching
- Focus degradation assessment on brain region only (exclude maternal tissue)
- Generate visual comparison galleries per qualitative cohort

---

## March 3, 2026
*Author: Daniel Barreras Meraz*

**1. Dataset Status**
The training dataset is complete:
- 319 HIGH-quality fetal MRI stacks selected across 6 acquisition protocols
- 1,276 paired NIfTI stacks generated
- 317 LOW-quality real subjects characterized by dominant degradation cohort
- Extended quality metrics computed for all subjects (SNR, sharpness, motion score, CNR, gestational age)

**2. Model Architecture**
We reviewed the BME-X paper as a reference and identified the key adaptations needed for fetal raw stack images. BME-X was designed for adult skull-stripped 3D volumes and relies on automated tissue segmentation labels, neither of which is available or appropriate for fetal HASTE data.

We look forward to propose an architecture adapted from BME-X for full field-of-view 2D fetal slices. A working implementation has been developed and validated through a full unit test suite to confirm all components behave correctly before any data is introduced.

We would like to meet to walk through the architecture visually and discuss the design together as it will be easier to be in the same page during our next group meeting.

---

## March 6, 2026
*Author: Daniel Barreras Meraz*

**1. Architecture Walkthrough**
I walked through the FetEnhNet architecture visually. The model works in two stages. The first stage is a lightweight U-Net that produces a soft tissue probability map for each raw slice, labeling regions as background, cortical plate, white matter/subplate, or CSF. The second stage is an enhancement network that uses those tissue maps to guide how it processes each pixel. This conditioning mechanism lets the network apply different enhancement strategies depending on what tissue type is present, which is the core idea adapted from BME-X. The key differences from BME-X are that there is no skull-stripping, processing 2D slices rather than 3D volumes, and the tissue maps come from our own fetal segmentation pipeline rather than adult templates.

One point that came up during the discussion was a concern about circularity in the ground truth. The tissue labels used to supervise the classifier are derived from NeSVoR reconstructions, and those reconstructions are themselves built from the same raw stacks being enhanced. The tissue labels are only needed during training as a supervision signal. Once trained, the classifier learns to predict tissue maps directly from raw slices without any reconstruction involved. At inference on real low-quality subjects, no reconstruction is needed at any stage.

**2. Training and What I Found**
I launched the first training experiments and confirmed the pipeline runs end-to-end. When tissue conditioning was added, the results on some degradation types improved, but performance was inconsistent across runs and the tissue classifier could not learn reliably. After looking more closely at the training behavior the problem was identified: only about 30% of training subjects had tissue labels available, all from the CHD protocol which already had reconstructions done as part of the standard processing pipeline. The other protocols had no reconstructions, so there were no labels to project. This meant the conditioning pathway was receiving a meaningful training signal from only 1 in 3 subjects per batch, which was not enough for the model to learn stable tissue-aware enhancements.

**3. Reconstruction Campaign**
To get tissue labels for the remaining subjects across all protocols, the full NeSVoR reconstruction pipeline needed to run on each one first, then project the resulting segmentation back into raw stack space. Reconstruction was not part of the original plan for this project since it is computationally expensive and typically done as a separate preprocessing step, but it turned out to be the only way to generate the tissue labels the model needs.

Parallel reconstruction batches were set up across the three GPUs on the server, one for Ventriculomegaly, one for ASD, and one for Placenta.

After resolving issues, coverage across training subjects went from approximately 30% to 83.5%:
- Ventriculomegaly: 52/52 subjects labeled
- Placenta: 24/24 subjects labeled
- Down Syndrome: 2/2 subjects labeled
- CHD: 85/92 subjects labeled
- ASD: 30/32 subjects labeled
- Normative: 15/47 subjects labeled (session directories are read-only, to be resolved)

**4. Next Steps**
Share results from run 16 and visual comparisons against the baseline and against real low-quality subjects once training finishes. Follow up on the Normative read-only access issue to recover the remaining 32 subjects. If run 16 confirms the tissue conditioning is working as expected, consider re-enabling the self-supervised loss term for run 17 to leverage the 317 real low-quality subjects during training.

---

## March 17, 2026
*Author: Daniel Barreras Meraz*

**1. Preliminary Results (Daniel)**
Preliminary results from training runs 14 through 17 were presented. These runs incorporated the expanded tissue label coverage achieved through the reconstruction campaign, bringing labeled subjects from approximately 30% to 83.5% across all protocols.

**2. Ground Truth for Classification Model (Daniel)**
We initially used iBeat v2.0 as the source of ground truth tissue labels for the classification model. After evaluating the results, we moved to using our own manual segmentations instead, which are more appropriate for fetal anatomy and better aligned with the specific protocols in our dataset.

A key open problem is figuring out the inverse transform from NeSVoR and FSL in order to accurately overlay the tissue maps onto the specific region of the raw stack where the brain is located. There is also an interpolation problem between raw stack slices that needs to be addressed for correct alignment, since the slice spacing and orientation in the original acquisitions do not match the reconstructed volume grid. Getting this registration as close as possible is critical for the conditioning pathway to work correctly, since the tissue labels need to be precisely aligned with the raw slices the model is trying to enhance. Progress has been made on understanding the transform chain and a complete proposal with the working hypothesis is expected for the next meeting.

**3. Literature Review (Yair)**
Yair presented a comprehensive literature review covering image enhancement and denoising techniques across different organ systems, not limited to brain MRI. The review provides a broader perspective on applicable methods and will inform the next phase of the project. Yair will move to developing a classification model based on masking, applying insights from the review.

**4. Next Steps**
- Continue iterating on training with the updated ground truth from manual segmentations
- Investigate the NeSVoR and FSL inverse transform pipeline to improve tissue map overlay accuracy on raw stacks
- Address the inter-slice interpolation problem for correct alignment between reconstructed labels and raw stack geometry
- Prepare a complete proposal with the working hypothesis for the next meeting

---

## March 17, 2026
*Author: Daniel Barreras Meraz*

**1. Preliminary Results**
Preliminary results from training runs 14 through 17 were presented to the group. These runs incorporated the expanded tissue label coverage (83.5%) achieved through the reconstruction campaign described in the previous meeting.

**2. Ground Truth for Classification Model**
Initially used iBeat v2.0 as the source of ground truth tissue labels for the classification model. After evaluating the results, we moved to using our own manual segmentations instead, which are more appropriate for fetal anatomy and better aligned with the specific protocols in our dataset.

Tissue label visualizations were prepared and shared with Hyeokjin for further analysis, including multi-protocol comparisons, reconstruction overlays, and raw vs reconstructed slice comparisons.

**3. Literature Review (Yair Beltran)**
Yair presented a comprehensive literature review covering image enhancement and denoising techniques across different organ systems, not limited to brain MRI. The review provides a broader perspective on applicable methods and will inform the next phase of the project.

**4. Next Steps**
Yair will move to developing a classification model based on masking, applying insights from the literature review. Continue iterating on training with the updated ground truth from manual segmentations. Evaluate whether the switch from iBeat to manual segmentations improves tissue conditioning stability across runs.

---

## March 22, 2026 -- Kiho's Feedback on March 17 Minutes

*Kiho responded to the March 17 meeting minutes with clarification questions. Daniel's replies:*

**On preliminary results (runs 14-17):**
Kiho did not understand the reference to the reconstruction campaign. Daniel clarified: initially only ~30% of training subjects had tissue labels (CHD protocol only). The full NeSVoR reconstruction pipeline was run on Ventriculomegaly, Placenta, ASD, Normative, and Down Syndrome protocols to project segmentations back into raw stack space, bringing coverage from ~30% to 83.5%. Runs 14-17 were the first experiments using this expanded label set.

**On Yair's classification model based on masking:**
Kiho asked whether this means a brain masking model that can run on bad-quality images. Daniel confirmed: the goal is a brain masking model that reliably segments the brain region on raw stack images including low-quality ones, to focus enhancement and quality assessment on the brain rather than the full field of view.

**On next steps:**
Kiho asked whether all three next steps are for defining ground truth segmentation on raw stack images. Daniel confirmed: the inverse transform, interpolation correction, and training iterations are all about accurately aligning tissue labels from the reconstructed volume with original raw slices.

Kiho also asked about trying image enhancement with brain masking. Daniel confirmed this is planned: once Yair's masking model works reliably on low-quality images, it could constrain the enhancement network to operate within the brain region only, improving training stability and output quality. Integration to be discussed once initial results from both pipelines are available.

---

## March 24, 2026
*Author: Daniel Barreras Meraz*

**1. Run18 Results — Brain Mask FiLM Conditioning (Daniel)**

Results from Run18 were presented. This run replaced the 4-class tissue map FiLM conditioning from Run17 with a 2-class brain mask, which is already available in raw stack space and requires no inverse transform projection.

Run18 trained for 100 epochs on sejong (3× RTX A5000), with best validation loss at epoch 82. The improvement over Run17 was substantial across all metrics:

| Metric | Run17 (Tissue, 4-class) | Run18 (Brain Mask, 2-class) |
|--------|------------------------|-------------------------------|
| Best val_sup | 0.0790 | 0.0541 (31.5% lower) |
| Blur PSNR gain | +0.32 dB | +4.04 dB |
| Noise PSNR gain | +3.43 dB | +5.10 dB |
| Overall SSIM gain | +0.081 | +0.126 |

The underperformance of Run17 is attributed to inaccurate tissue label projection onto raw stacks. The brain mask approach sidesteps that problem entirely and sets a strong new baseline. Visual comparisons were shown: 10 synthetic test pairs across 5 degradation types, and a gallery of 24 real low-quality subjects (not cherry-picked).

**2. NeSVoR Inverse Transform Pipeline — In Progress (Daniel)**

Work is ongoing to accurately project tissue segmentation labels from the reconstructed volume back onto individual raw stack slices, which is necessary for correct tissue-level FiLM conditioning in future runs.

`project_labels.py` was written to perform the projection using the per-slice affine matrices from NeSVoR's `--simulated-slices` output. The formula applied is:

```
vol_voxels = inv(vol_affine) @ slice_affine @ slice_voxels
```

Projection was validated visually on FCB080: the projected intensity aligns well with the brain region in simulated slices. Batch processing was launched across all 77 training subjects on 3 GPUs (~5 minutes per subject). As of the meeting, 25+ CHD subjects were complete.

**3. SURE Loss for Self-Supervised Denoising (Discussion)**

The group discussed incorporating a SURE (Stein's Unbiased Risk Estimator) loss term to improve denoising performance without requiring paired clean references. SURE provides a computable estimate of the mean squared error from the noisy observation alone, making it well-suited as a self-supervised signal on the 317 real low-quality subjects that have no clean ground truth.

Previous attempts used SURE in runs 12 and 13. Run12 was abandoned at epoch 20 because λ_sure=0.1 was too aggressive and destabilized training. Run13 used λ_sure=0.01 but combined it with tissue conditioning that was not yet reliable, limiting the gains. The consensus is that SURE should be reintroduced now with a calibrated λ, applied on top of a stable enhancement backbone with correct tissue conditioning rather than alongside an unstable classifier.

The reference implementation discussed is: *"Self-supervised MRI denoising using Stein's unbiased risk estimator"*, Scientific Reports (2023). https://www.nature.com/articles/s41598-023-49023-2

**4. Next Steps**

- Finish the NeSVoR batch projection across all 77 training subjects (remaining ASD, Placenta, Normative protocols)
- Project actual tissue segmentation labels (not just intensity) onto raw slices using the validated affine pipeline
- Train a new run with correctly projected tissue labels as FiLM conditioning — compare against Run18 brain mask baseline to determine if tissue-level conditioning adds value when the projection is accurate
- Once a stable tissue-conditioned model is established, reintroduce SURE loss with a calibrated λ to leverage the 317 real low-quality subjects as an unsupervised denoising signal
- Significantly expand the training dataset with synthetic images covering the full range of degradation parameter values to achieve complete degradation space coverage

---

## April 14, 2026
*Author: Daniel Barreras Meraz*

**1. Tissue Label Projection Pipeline**

The main focus was solving the tissue label projection problem: projecting manual tissue segmentations from atlas space onto raw HASTE slices for correct FiLM conditioning. Five coordinate systems are involved and the pipeline reconstruction was confirmed to not be in scanner coordinates via checkerboard test. 14 registration approaches were tested. The winning method uses binary brain shape registration with per-subject 8-flip search. From 212 subjects with manual segs, 25 passed automated registration at Dice 0.80 or above (19 above 0.90).

**2. Loss Functions and FiLM**

MC-SURE loss and supervised loss were formalized with full variable definitions. FiLM conditioning was explained: per-pixel scale and shift of decoder features based on tissue type via learned 1x1 convolutions. Sigma for SURE is estimated per-slice from the background region.

**3. Comparable Difference Metric**

Proposed sigma-normalized difference to replace the current non-comparable signed-difference visualization. Implementation planned for Run22.

**4. Feedback**

Present the complete pipeline end-to-end in the next meeting: from data preparation through tissue label projection to training and the model working on real images.

**5. Next Steps**

- Scale tissue projection to 50+ subjects using CanonicalData (160 CHD subjects available)
- Split 317 LOW stacks into 250 train + 67 validation for proper SURE evaluation
- Implement sigma-normalized difference metric
- Launch Run22 with aligned tissue labels, weight decay, dropout, early stopping, and fixed checkpoint selection
- Prepare end-to-end pipeline walkthrough for next meeting

---

## May 5, 2026
*Author: Daniel Barreras Meraz*

**1. Dataset expansion and alignment campaign**

The inverse alignment campaign completed processing across all available subjects. The final dataset now includes 538 usable subjects (490 correct + 48 partial alignment) spanning 8 protocols: CHD (220), Ventriculomegaly (124), Normative (82), ASD (51), Heterotaxy (32), SpinaBifida (23), Placenta (5), and HBCD (1). This yields approximately 164,000 non-empty brain slices with projected iBEAT tissue labels in raw HASTE stack space. 21 subjects remain marked as wrong alignment due to degenerate atlas registration (mostly SpinaBifida with Chiari II malformation); these are unfixable without recomputing the initial seg_pipeline registration.

An HDF5 training dataset was built from these subjects: 179,601 training slices (55 GB), 24,356 validation, and 20,547 test slices, stratified by protocol with seed 42. Per-stack QA scores from Sungmin's fetal_brain_QA model were integrated into the FetEnhNet Explorer, categorizing stacks as Good (>=0.6), Fair (0.4-0.6), or Bad (<0.4).

**2. BME-X baseline approach (Daniel)**

Following Hyeokjin's direction from the April 28 meeting, the training strategy was restructured around a proper BME-X replication as the baseline. Key changes:

- Switched from FiLM conditioning to concatenation for the baseline (matching BME-X exactly: tissue map concatenated with input as extra channels to the enhancement DU-Net)
- Changed enhancement loss from L1 to MSE (BME-X uses MSE, $L_2 = \frac{1}{N}\sum(y - \hat{y})^2$)
- Staged training: tissue classifier trained first with DiceCE, frozen, then enhancement trained on top
- FiLM conditioning retained as a separate variant to compare against the concatenation baseline
- Five loss variants (MSE, L1, SSIM, perceptual, frequency) will each be trained independently on the same data, then the best combination selected

**3. Degradation calibration (Daniel + Yair)**

Degradation types were aligned between Daniel's and Yair's implementations. The final set follows Hyeokjin's directive: noise (Rician, sigma 0.005-0.06), blur (Gaussian, sigma 0.3-1.1 mm), bias field, and downsampling (1.0-1.5x for small brain simulation). Motion ghosting, signal dropout, and Gibbs ringing were dropped as not applicable to HASTE.

Yair explored MONAI transforms as drop-in replacements for the degradation engine: RandBiasField (Legendre polynomial basis, exp field), RandGaussianSmooth, RandGaussianNoise, and RandKSpaceSpikeNoise. A severity parameter s=[0,1] was defined to control degradation intensity uniformly across types. Extensive visual galleries were shown comparing degradations at s=0.3, 0.6, and 0.8 across multiple subjects and seeds.

Daniel's bias field implementation was updated from raw polynomial monomials to the MONAI Legendre polynomial algorithm (without importing MONAI as a dependency). The key improvement is using `np.polynomial.legendre.leggrid2d` with exponentiation (`img * exp(field)`) for always-positive, physically realistic B1 patterns.

**4. MONAI-based reimplementation (Yair)**

Yair presented a MONAI-based reimplementation of FetEnhNet using MONAI's DenseBlock, CacheDataset, and transform pipeline. The architecture keeps the DU-Net topology from BME-X with the joint CE + lambda*MSE loss. Notable simplifications: asymmetric 1/2/3 dense-block stacking per stage was replaced with uniform one dense block per stage, and MONAI's standard Compose pipeline (LoadImaged, ScaleIntensityd, RandSpatialCropd, NormalizeIntensityd) replaced custom data loading.

111 subjects were successfully pre-processed through the full pipeline (NeSVoR reconstruction + segmentation + inverse alignment) in approximately 6 hours, using `--n-iter 3000 --n-samples 128` which reduced processing time by about 70% without significant quality loss.

**5. Data augmentation strategy**

Augmentation was implemented following the nnU-Net v2 + fetal MRI literature consensus. All spatial transforms are applied identically to both image and tissue label (nearest-neighbor interpolation for labels) to maintain alignment for concatenation mode: horizontal/vertical flip (p=0.5), rotation +/-15 degrees (p=0.3), scaling 0.8-1.2x (p=0.2), random crop 192x192 then pad to 256 (p=0.5). Intensity augmentation (image only): gamma 0.7-1.5 (p=0.15), brightness 0.8-1.2x (p=0.15).

**6. Next steps**

- Train tissue classifier (Stage 1) and validate Dice > 0.85
- Launch all five loss variant trainings in parallel across busan/hanyang/sejong
- Generate comparison table (PSNR/SSIM/LPIPS/Sharpness/Tissue Dice) across all variants
- Evaluate concatenation (BME-X baseline) vs FiLM conditioning (our improvement) on the same data
- SURE fine-tune on real LOW stacks after selecting best supervised combination
- Daniel to prepare handoff documentation per Hyeokjin's request
