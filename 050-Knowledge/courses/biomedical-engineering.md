---
title: "Course: Biomedical Engineering"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, engineering, biomedical, medical-imaging, signal-processing]
prerequisites: [calculus, linear-algebra, physics, signal-processing]
---

# Biomedical Engineering

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[mri-physics]], [[electromagnetism]], [[neuroscience]], [[quantum-mechanics]], [[biochemistry]]*

## Motivation

Biomedical engineering applies engineering principles to medicine and biology. This course emphasizes medical imaging modalities, image reconstruction algorithms, and signal processing — the technical foundations of Daniel's work in fetal brain MRI reconstruction and analysis. Understanding how images are formed, reconstructed, and processed across modalities (MRI, CT, ultrasound, PET) provides the engineering perspective complementary to the physics covered in [[mri-physics]] and the neuroscience in [[neuroscience]].

## Prerequisites

- **Calculus and linear algebra:** Multivariable calculus, matrix operations, eigenvalue problems.
- **Physics:** Classical mechanics, electromagnetism, wave phenomena.
- **Signal processing:** Fourier transforms, linear systems, filtering (covered in this course if needed).
- **Programming:** Python/MATLAB for implementing reconstruction algorithms.

---

## I. Signal Processing Fundamentals

### 1.1 Continuous-Time Signals and Systems

- Signal classification: continuous/discrete, deterministic/stochastic, periodic/aperiodic, energy/power.
- Linear time-invariant (LTI) systems: superposition, shift-invariance.
- Impulse response $h(t)$ and convolution: $y(t) = (x * h)(t) = \int x(\tau) h(t - \tau)\, d\tau$.
- System properties: causality, stability (BIBO: $\int |h(t)| dt < \infty$).

### 1.2 Fourier Analysis

- **Continuous Fourier Transform (CFT):**
  - Forward: $X(f) = \int_{-\infty}^{\infty} x(t)\, e^{-i2\pi ft}\, dt$.
  - Inverse: $x(t) = \int_{-\infty}^{\infty} X(f)\, e^{i2\pi ft}\, df$.
  - Properties: linearity, time shift → phase shift, convolution ↔ multiplication, Parseval's theorem.
- **Discrete-Time Fourier Transform (DTFT):** For sampled signals.
- **Discrete Fourier Transform (DFT):** Finite-length sequences. Computed via FFT (Cooley-Tukey: $O(N \log N)$).
- **2D and 3D Fourier transforms:** Essential for image processing.
  - $F(k_x, k_y) = \iint f(x, y)\, e^{-i2\pi(k_x x + k_y y)}\, dx\, dy$.
  - Central slice theorem (Fourier slice theorem): connects projection data to 2D FT.

### 1.3 Sampling Theory

- **Nyquist-Shannon sampling theorem:** A bandlimited signal with bandwidth $B$ is perfectly reconstructed from samples taken at rate $f_s \geq 2B$.
- Aliasing: undersampling causes high frequencies to masquerade as low frequencies.
- Anti-aliasing filter: low-pass before sampling.
- Reconstruction: ideal sinc interpolation (impractical); practical: windowed sinc, linear, spline.
- **Application to MRI:** k-space sampling is Fourier sampling. FOV = $1/\Delta k$, resolution = $1/(2k_{\max})$. Nyquist violation → aliasing artifact (see [[mri-physics]]).

### 1.4 Filtering

- **Low-pass filter:** Passes frequencies below cutoff. Smoothing. Noise reduction.
- **High-pass filter:** Passes frequencies above cutoff. Edge enhancement.
- **Band-pass filter:** Passes frequency band. Signal isolation.
- **FIR and IIR filters:** Finite vs. infinite impulse response. FIR always stable, linear phase possible.
- **Wiener filter:** Optimal linear filter for noise reduction (minimizes MSE). Requires signal and noise power spectra.
- **Matched filter:** Maximizes SNR for known signal in noise.
- **Spatial filtering in images:**
  - Convolution kernels: Gaussian blur, Sobel edge detection, Laplacian.
  - Frequency domain: multiply by transfer function.
  - Non-linear: median filter (edge-preserving noise reduction), bilateral filter.

### 1.5 Windowing and Spectral Analysis

- Spectral leakage from finite observation.
- Window functions: rectangular, Hamming, Hanning, Blackman, Kaiser.
- Tradeoff: main lobe width vs. sidelobe level.
- Short-time Fourier transform (STFT): time-frequency analysis.
- Wavelets (brief): multi-resolution analysis. Good time-frequency localization.

---

## II. Medical Imaging Modalities

### 2.1 Magnetic Resonance Imaging (MRI)

- Full treatment in [[mri-physics]]. Summary of engineering aspects:
  - Signal generation: nuclear spin precession → Faraday induction.
  - Spatial encoding: gradient fields → k-space. Fourier reconstruction.
  - Pulse sequence design: timing of RF and gradients determines contrast and speed.
  - Hardware: superconducting magnet, gradient coils, RF coils (phased arrays).
  - Reconstruction: 2D/3D FFT for Cartesian; gridding + FFT for non-Cartesian; iterative for undersampled data.
- **Engineering challenges:** SNR optimization, gradient performance, parallel imaging, compressed sensing, real-time MRI.

### 2.2 X-Ray and Computed Tomography (CT)

**X-ray physics:**
- X-ray generation: bremsstrahlung and characteristic radiation from electron bombardment of anode (tungsten).
- Tube voltage (kVp): determines maximum photon energy and beam penetration.
- Tube current (mA): determines photon flux (dose).
- Attenuation: $I = I_0 e^{-\mu x}$ (Beer-Lambert law).
- Linear attenuation coefficient $\mu$: depends on material and photon energy.
- Interactions: photoelectric effect (dominant at low energy, high Z → bone contrast), Compton scattering (dominant at diagnostic energies in soft tissue).
- Hounsfield units: $HU = 1000 \times \frac{\mu - \mu_{\text{water}}}{\mu_{\text{water}}}$. Water = 0, air = -1000, bone = +1000.

**CT acquisition:**
- Fan beam / cone beam geometry.
- Helical (spiral) scanning: continuous rotation + table translation. Pitch.
- Multi-detector CT (MDCT): multiple detector rows for faster volumetric coverage.
- Projection data: line integrals of $\mu$ along ray paths.

**CT reconstruction:**
- **Radon transform:** $p(\theta, s) = \int_L \mu(x, y)\, dl$ (line integral along path $L$).
- **Central slice theorem:** The 1D FT of a projection at angle $\theta$ is a line through the 2D FT of the object at the same angle.
- **Filtered back projection (FBP):**
  1. Take 1D FT of each projection.
  2. Apply ramp filter $|f|$ (compensates for non-uniform sampling density in Fourier space).
  3. Inverse FT to get filtered projection.
  4. Back-project: smear filtered projections back across image.
  - Ramp filter amplifies noise → apply window (Hamming, Shepp-Logan).
- **Iterative reconstruction:**
  - Forward model: $\vec{p} = A\vec{\mu}$ where $A$ is the system matrix (geometry, physics).
  - Algebraic reconstruction technique (ART): row-by-row update.
  - SIRT, SART: simultaneous/ordered updates.
  - Statistical (model-based): maximize likelihood: $\hat{\mu} = \arg\max_\mu P(\vec{p} | \mu)$.
  - Penalized likelihood: add regularization (total variation, quadratic).
  - Advantages: handles noise, incomplete data, complex geometry. Disadvantage: computational cost.
- **Dose reduction:** Iterative reconstruction enables lower dose. Deep learning denoising.

### 2.3 Ultrasound (US)

**Physics:**
- Sound waves in tissue: longitudinal pressure waves. Speed: ~1540 m/s in soft tissue.
- Acoustic impedance: $Z = \rho c$. Reflection at interfaces: $R = \left(\frac{Z_2 - Z_1}{Z_2 + Z_1}\right)^2$.
- Frequency: 2-18 MHz (diagnostic). Higher frequency → better resolution but less penetration.
- Attenuation: ~0.5 dB/cm/MHz in soft tissue.

**Image formation:**
- Pulse-echo: transmit short pulse, receive echoes from interfaces.
- A-mode: amplitude vs. depth. B-mode: brightness-modulated 2D image.
- Beamforming: phased array transducer, electronic focusing and steering.
- Delay-and-sum beamforming. Adaptive beamforming.
- Frame rate: limited by speed of sound and imaging depth.

**Modes:**
- B-mode: standard 2D anatomical imaging.
- M-mode: motion display along a single line (cardiac).
- Doppler: blood flow velocity from frequency shift. $\Delta f = \frac{2f_0 v \cos\theta}{c}$.
  - Continuous wave, pulsed wave, color Doppler, power Doppler.
- 3D/4D ultrasound: volume acquisition.
- Elastography: tissue stiffness mapping (shear wave speed).
- Contrast-enhanced: microbubble agents.

**Advantages:** Real-time, portable, no ionizing radiation, inexpensive.
**Limitations:** Operator-dependent, limited by bone/air interfaces, limited soft tissue contrast compared to MRI.

### 2.4 Positron Emission Tomography (PET)

**Physics:**
- Radiotracer: positron-emitting isotope ($^{18}$F, $^{11}$C, $^{15}$O, $^{68}$Ga) attached to biologically active molecule.
- **$^{18}$F-FDG (fluorodeoxyglucose):** Glucose analog. Trapped in metabolically active cells. Standard oncology tracer.
- Positron emission → annihilation with electron → two 511 keV photons emitted at ~180 degrees.
- Coincidence detection: two opposing detectors register events within timing window (~ns).
- Line of response (LOR): the line connecting the two detectors.

**Image formation:**
- Sinogram: collection of LORs organized by angle and offset.
- Reconstruction: FBP or iterative (OSEM — ordered subsets expectation maximization, most common clinical method).
- Corrections: attenuation (CT-based), scatter, randoms, dead time, normalization, decay.
- Resolution: ~4-6 mm (clinical), ~1-2 mm (preclinical).

**PET/CT and PET/MRI:**
- PET/CT: anatomical localization + attenuation correction from CT.
- PET/MRI: simultaneous acquisition. Better soft tissue contrast. No additional radiation for attenuation correction (MR-based methods: Dixon, atlas-based).

### 2.5 Single Photon Emission Computed Tomography (SPECT)

- Gamma-emitting radiotracers ($^{99m}$Tc, $^{201}$Tl, $^{123}$I).
- Gamma camera: collimator (parallel hole, pinhole, fan beam) + scintillation crystal (NaI) + PMTs.
- Collimator provides directional information (unlike PET coincidence).
- Rotation around patient → projection data → reconstruction (FBP or iterative).
- Lower sensitivity and resolution than PET. More widely available.
- Applications: myocardial perfusion, bone scan, brain perfusion (HMPAO).

---

## III. Image Reconstruction Algorithms

### 3.1 Analytical Methods

- **Filtered back projection (FBP):** Standard for CT. See Section II.2.
- **Direct Fourier reconstruction:** Sample Fourier space → inverse FFT. Requires interpolation (gridding) for non-uniform samples.
- **Gridding reconstruction for MRI:**
  - Non-Cartesian k-space trajectories (radial, spiral) don't fall on a regular grid.
  - Gridding: convolve samples with a convolution kernel (Kaiser-Bessel) onto Cartesian grid → FFT → deapodization.
  - Density compensation: weight each sample by inverse of local sampling density.

### 3.2 Iterative Methods

- **General framework:** $\hat{x} = \arg\min_x \|Ax - b\|^2 + \lambda R(x)$
  - $A$: system matrix (forward model).
  - $b$: measured data.
  - $R(x)$: regularization term.
  - $\lambda$: regularization parameter.
- **Conjugate gradient (CG):** Efficient for quadratic objectives. SENSE reconstruction uses CG.
- **ADMM (Alternating Direction Method of Multipliers):** Splits problem into subproblems. Good for non-smooth regularizers ($L_1$).
- **FISTA (Fast Iterative Shrinkage-Thresholding):** Accelerated proximal gradient. Compressed sensing MRI.
- **OSEM (Ordered Subsets EM):** Standard PET reconstruction. EM algorithm with subset acceleration.
- **Total variation (TV) regularization:** $R(x) = \|\nabla x\|_1$. Preserves edges while denoising. Common in compressed sensing MRI and low-dose CT.
- **Dictionary learning / sparse coding:** Learn adaptive basis from data. Patch-based.

### 3.3 Deep Learning Reconstruction

- **Unrolled networks:** Map iterative algorithm steps to neural network layers. Learn regularizer/step sizes.
  - Examples: ADMM-Net, Variational Network, MoDL.
- **U-Net and variants:** Encoder-decoder for image-to-image denoising/artifact removal.
- **Physics-informed networks:** Incorporate forward model as a known layer. Data consistency.
- **Generative models:** GANs, diffusion models for image synthesis and reconstruction.
- **Self-supervised:** Learn from undersampled data without fully sampled references (SSDU).
- **Applications:**
  - Accelerated MRI: learn to reconstruct from fewer k-space samples.
  - Low-dose CT denoising.
  - PET: low-count reconstruction.
  - **Fetal MRI:** NeSVoR uses implicit neural representations for slice-to-volume reconstruction (see [[mri-physics]]).

---

## IV. Image Processing and Analysis

### 4.1 Image Enhancement

- Histogram equalization: redistribute intensity values for improved contrast.
- Adaptive histogram equalization (CLAHE): local contrast enhancement.
- Noise reduction: Gaussian smoothing, non-local means, BM3D.
- Sharpening: unsharp masking, Laplacian enhancement.

### 4.2 Image Segmentation

- **Thresholding:** Global (Otsu), adaptive/local.
- **Region-based:** Region growing, watershed.
- **Edge-based:** Canny edge detector, active contours (snakes).
- **Level sets:** Implicit surface evolution. Handles topology changes.
- **Atlas-based segmentation:**
  - Register atlas (with labels) to target image.
  - Propagate labels via deformation field.
  - Multi-atlas: register multiple atlases, fuse labels (majority voting, STAPLE).
- **Deep learning segmentation:**
  - **U-Net:** Encoder-decoder with skip connections. Standard for medical image segmentation.
  - **nnU-Net:** Self-configuring U-Net framework. State-of-the-art across many medical segmentation tasks.
  - **V-Net:** 3D volumetric segmentation.
  - **Attention mechanisms:** Focus on relevant regions.
  - **Transformer-based:** ViT, Swin-UNETR for large receptive fields.
  - Training strategies: data augmentation, transfer learning, semi-supervised, self-supervised.
- **Fetal brain segmentation:** Particularly challenging due to: small structures, developing anatomy (different from adult), motion artifacts, varying gestational age. Age-specific atlases and specialized deep learning models required.

### 4.3 Image Registration

- **Goal:** Find spatial transformation $T$ mapping one image to another.
- **Transformation models:**
  - Rigid: 6 DOF (3 rotation, 3 translation). Used for intra-subject brain registration.
  - Affine: 12 DOF (adds scaling and shear).
  - Deformable (non-rigid): dense displacement field or parametric (B-spline, thin-plate spline).
  - Diffeomorphic: invertible, smooth. Preserves topology. LDDMM, SyN (ANTs).
- **Similarity metrics:**
  - Sum of squared differences (SSD): same modality.
  - Normalized cross-correlation (NCC): intensity scaling invariance.
  - Mutual information (MI): multi-modality (MRI-CT, T1-T2).
- **Optimization:** Gradient descent, L-BFGS, multi-resolution (coarse to fine).
- **Tools:** ANTs (SyN), FSL (FLIRT/FNIRT), FreeSurfer, Elastix, VoxelMorph (deep learning).
- **Application to fetal MRI:** Slice-to-volume reconstruction requires per-slice rigid registration with robust outlier handling (see [[mri-physics]]).

### 4.4 Morphological Analysis

- Cortical surface extraction, thickness measurement, curvature computation (see [[neuroscience]]).
- Volume measurement: intracranial volume, structure volumes.
- Shape analysis: spherical harmonic descriptors, point distribution models.
- Longitudinal analysis: measure change over time (important for fetal development across gestational ages).

---

## V. Biosensors and Bioinstrumentation

### 5.1 Biosensors

- Biological recognition element (enzyme, antibody, nucleic acid) + transducer (electrochemical, optical, piezoelectric, thermal).
- Glucose biosensor: glucose oxidase + amperometric electrode. Continuous glucose monitors.
- Immunoassays: ELISA (enzyme-linked immunosorbent assay). Lateral flow (pregnancy tests, COVID rapid tests).
- DNA biosensors: hybridization detection.
- Lab-on-a-chip / microfluidics: miniaturized analysis systems.

### 5.2 Electrophysiological Instrumentation

- ECG (electrocardiography): cardiac electrical activity. 12-lead system.
- EEG (electroencephalography): brain electrical activity. 10-20 electrode system. Frequency bands (delta, theta, alpha, beta, gamma).
- EMG (electromyography): muscle electrical activity.
- Instrumentation amplifier: high CMRR, high input impedance. AD620, INA128.
- Noise sources: thermal (Johnson), 1/f (flicker), 60 Hz power line. Shielding, filtering, averaging.

### 5.3 Physiological Monitoring

- Pulse oximetry: SpO$_2$ from absorption ratio at 660 nm (red) and 940 nm (IR). Beer-Lambert law.
- Blood pressure: invasive (arterial line) and non-invasive (oscillometric cuff).
- Respiratory monitoring: impedance pneumography, capnography (CO$_2$).

---

## VI. Biomechanics

### 6.1 Tissue Mechanics

- Stress-strain relationships. Elastic modulus.
- Viscoelasticity: creep, stress relaxation. Standard linear solid model.
- Biological tissues are nonlinear, anisotropic, viscoelastic, inhomogeneous.
- Bone: cortical (compact) vs. cancellous (trabecular). Wolff's law: bone remodels along stress lines.
- Soft tissue: collagen and elastin networks. Hyperelastic models (Mooney-Rivlin, Ogden).
- MR elastography: measure tissue stiffness non-invasively (liver fibrosis staging).

### 6.2 Cardiovascular Mechanics

- Hemodynamics: Poiseuille flow, Windkessel model, pulse wave velocity.
- Heart as a pump: pressure-volume loops, Frank-Starling mechanism.
- Computational fluid dynamics (CFD) from 4D flow MRI data.

### 6.3 Musculoskeletal Biomechanics

- Gait analysis: kinematics (joint angles), kinetics (forces, moments), EMG.
- Joint mechanics: hip, knee (ligaments, meniscus).
- Finite element analysis (FEA) of implants and bones.

---

## VII. Tissue Engineering and Prosthetics

### 7.1 Tissue Engineering

- Scaffold + cells + growth factors → engineered tissue.
- Scaffold materials: natural (collagen, fibrin, decellularized ECM) and synthetic (PLA, PGA, PLGA, PCL).
- Bioreactors: mechanical/chemical stimulation.
- Current state: skin grafts (clinical), cartilage, blood vessels. Organs (kidney, liver, heart) remain research-stage.

### 7.2 Prosthetics and Implants

- Passive prosthetics: mechanical limbs.
- Powered prosthetics: myoelectric control (EMG-driven).
- Neural interfaces: brain-computer interfaces (BCIs). Utah array, ECoG, BCI for locked-in patients.
- Cochlear implants: electrode array in cochlea, sound processor.
- Deep brain stimulation (DBS): electrodes in STN/GPi for Parkinson's, essential tremor.
- Biocompatibility: material-tissue interaction. Foreign body response. ISO 10993.

---

## VIII. Medical Device Regulation

### 8.1 Regulatory Framework (US)

- FDA classifications: Class I (lowest risk, most exempt), Class II (510(k) — substantial equivalence), Class III (PMA — pre-market approval, highest risk).
- 510(k) pathway: demonstrate device is substantially equivalent to a predicate device.
- PMA pathway: clinical trials demonstrating safety and efficacy. Required for Class III.
- De Novo pathway: novel low-to-moderate risk devices without a predicate.
- Quality system regulation (QSR) / 21 CFR 820: design controls, process validation, CAPA.

### 8.2 Software as a Medical Device (SaMD)

- FDA framework for software that performs medical functions (diagnosis, treatment decisions).
- Classification based on significance of information provided and healthcare situation.
- Applies to AI/ML-based imaging tools, CAD systems, reconstruction algorithms.
- Predetermined change control plan: framework for updates to ML algorithms post-clearance.
- **Relevance:** Any clinical tool for fetal brain analysis (segmentation, anomaly detection) would be SaMD.

### 8.3 International

- CE marking (EU MDR): European market access.
- ISO 13485: quality management for medical devices.
- IEC 62304: software lifecycle for medical device software.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Fourier transform | Foundation of all imaging reconstruction (MRI, CT, US) |
| Sampling theorem | Determines resolution, FOV, aliasing across modalities |
| Filtered back projection | Standard CT reconstruction; conceptual basis |
| Iterative reconstruction | Modern approach: better noise handling, enables dose/scan reduction |
| k-space | MRI-specific Fourier encoding framework |
| Image registration | Aligning images across time, subjects, modalities |
| Deep learning segmentation | U-Net family: current state-of-the-art for medical image analysis |
| Slice-to-volume reconstruction | Key technique for fetal MRI research |
| Compressed sensing | Reconstruct from undersampled data using sparsity |
| Regulatory (SaMD) | Any clinical imaging tool requires FDA clearance |

---

## Recommended References

1. **Prince & Links** — *Medical Imaging: Signals and Systems* (2nd ed.). Comprehensive treatment of all modalities from a signals perspective.
2. **Bushberg et al.** — *The Essential Physics of Medical Imaging* (4th ed.). Clinical physics focus. Covers all modalities.
3. **Oppenheim & Willsky** — *Signals and Systems* (2nd ed.). Classic signal processing text.
4. **Gonzalez & Woods** — *Digital Image Processing* (4th ed.). Comprehensive image processing.
5. **Kak & Slaney** — *Principles of Computerized Tomographic Imaging*. Free online. CT reconstruction math.
6. **Bernstein, King, Zhou** — *Handbook of MRI Pulse Sequences*. Engineering reference for MRI.
7. **Lustig, Donoho, Pauly** — "Sparse MRI: The Application of Compressed Sensing for Rapid MR Imaging" (Magnetic Resonance in Medicine, 2007).
8. **Ronneberger, Fischer, Brox** — "U-Net: Convolutional Networks for Biomedical Image Segmentation" (MICCAI, 2015).
9. **Isensee et al.** — "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation" (Nature Methods, 2021).
10. **Avants et al.** — "A Reproducible Evaluation of ANTs Similarity Metric Performance in Brain Image Registration" (NeuroImage, 2011).

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
