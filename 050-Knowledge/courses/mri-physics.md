---
title: "Course: MRI Physics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, physics, mri, medical-imaging, neuroimaging]
prerequisites: [quantum-mechanics, electromagnetism, statistical-mechanics, signal-processing]
---

# MRI Physics

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[quantum-mechanics]], [[electromagnetism]], [[statistical-mechanics]], [[neuroscience]], [[biomedical-engineering]]*

## Motivation

Magnetic Resonance Imaging is the primary non-invasive modality for soft tissue imaging with no ionizing radiation. It is the backbone of Daniel's research at BCH — fetal brain MRI, cortical surface analysis, and slice-to-volume reconstruction all demand deep understanding of MRI physics. This course covers the complete chain from nuclear spin physics to clinical image formation, with special emphasis on fetal MRI challenges and advanced sequences.

## Prerequisites

- **Quantum mechanics:** Spin-1/2 systems, Larmor precession, Pauli matrices (see [[quantum-mechanics]]).
- **Electromagnetism:** Maxwell's equations, electromagnetic induction, RF fields (see [[electromagnetism]]).
- **Statistical mechanics:** Boltzmann distribution, thermal equilibrium polarization (see [[statistical-mechanics]]).
- **Signal processing:** Fourier transforms, sampling theory, convolution (see [[biomedical-engineering]]).

---

## I. Nuclear Magnetic Resonance — Foundations

### 1.1 Nuclear Spin and Magnetic Moment

- Nuclei with odd numbers of protons or neutrons possess intrinsic spin angular momentum $\vec{I}$.
- Magnetic moment: $\vec{\mu} = \gamma \hbar \vec{I}$, where $\gamma$ is the gyromagnetic ratio.
- Key nuclei:
  - $^1$H (proton): $\gamma/(2\pi) = 42.577$ MHz/T. Most abundant, highest sensitivity. The basis of clinical MRI.
  - $^{13}$C: $\gamma/(2\pi) = 10.705$ MHz/T. Low natural abundance (1.1%).
  - $^{23}$Na: $\gamma/(2\pi) = 11.262$ MHz/T. Spin-3/2.
  - $^{31}$P: $\gamma/(2\pi) = 17.235$ MHz/T. Important for spectroscopy.
- Spin-1/2 nuclei ($^1$H, $^{13}$C, $^{31}$P): two energy levels in a magnetic field. Spin > 1/2 ($^{23}$Na): quadrupolar effects.

### 1.2 Zeeman Effect and Energy Splitting

- In external field $B_0$ (conventionally along $\hat{z}$):
  - Hamiltonian: $\hat{H} = -\gamma \hbar \hat{I}_z B_0$.
  - Energy levels: $E_m = -\gamma \hbar m B_0$, $m = -I, -I+1, \ldots, I$.
  - For spin-1/2: two levels separated by $\Delta E = \gamma \hbar B_0$.

### 1.3 Larmor Precession

- Classical picture: magnetic moment in $B_0$ precesses about the field axis.
- **Larmor frequency:** $\omega_0 = \gamma B_0$ (angular), $f_0 = \gamma B_0 / (2\pi)$ (linear).
- At 1.5T: $f_0 = 63.87$ MHz. At 3T: $f_0 = 127.74$ MHz.
- Quantum mechanical derivation: expectation value of $\hat{\mu}$ precesses at $\omega_0$.

### 1.4 Thermal Equilibrium Magnetization

- Boltzmann population ratio: $N_\uparrow / N_\downarrow = e^{\gamma\hbar B_0 / k_B T}$.
- High-temperature approximation ($\gamma\hbar B_0 \ll k_BT$): $\Delta N / N \approx \gamma\hbar B_0 / (2k_BT)$.
- At 3T, 37C: $\Delta N / N \approx 10^{-5}$. MRI detects this tiny surplus.
- Net equilibrium magnetization: $M_0 = \frac{N\gamma^2\hbar^2 I(I+1)B_0}{3k_BT}$ (Curie law).
- **Consequence:** Signal increases with $B_0$ (motivation for higher field strengths) and proton density.

### 1.5 The Rotating Frame

- Laboratory frame: $M$ precesses at $\omega_0$ — inconvenient.
- Rotating frame at $\omega_0$: $M$ appears stationary at equilibrium.
- Effective field: $\vec{B}_{\text{eff}} = (B_0 - \omega/\gamma)\hat{z} + B_1\hat{x}'$.
- On resonance ($\omega = \omega_0$): $B_{\text{eff}} = B_1$ (transverse only). Magnetization nutates about $B_1$.

---

## II. Excitation and RF Pulses

### 2.1 RF Excitation

- Apply oscillating magnetic field $B_1(t) = B_1 \cos(\omega_{\text{RF}} t)$ perpendicular to $B_0$.
- On resonance: magnetization tips away from $\hat{z}$ at rate $\omega_1 = \gamma B_1$.
- **Flip angle:** $\alpha = \gamma B_1 \tau_p$ where $\tau_p$ is pulse duration.
- 90-degree pulse: tips $M$ fully into transverse plane. Maximum signal.
- 180-degree pulse: inverts $M$ (used for refocusing and inversion recovery).

### 2.2 Selective Excitation

- Slice selection: apply $B_1$ during a gradient $G_z$. Only spins at resonance frequency $\omega_0 + \gamma G_z z$ are excited.
- Slice thickness: $\Delta z = \Delta\omega / (\gamma G_z) = 2\pi \Delta f / (\gamma G_z)$.
- Pulse shape determines slice profile:
  - Rectangular pulse → sinc slice profile (poor).
  - Sinc pulse → rectangular slice profile (ideal but truncated).
  - SLR (Shinnar-Le Roux) design: optimized pulse design for arbitrary flip angles.
- Bandwidth-time product.

### 2.3 Adiabatic Pulses

- Frequency or amplitude swept slowly enough that $M$ follows $B_{\text{eff}}$.
- Adiabatic condition: $|d\alpha/dt| \ll \gamma B_{\text{eff}}$.
- Advantage: uniform flip angle despite $B_1$ inhomogeneity.
- Hyperbolic secant pulse. Adiabatic inversion.

---

## III. Relaxation

### 3.1 Bloch Equations

- Phenomenological equations of motion for magnetization $\vec{M}$:
$$\frac{dM_x}{dt} = \gamma(\vec{M} \times \vec{B})_x - \frac{M_x}{T_2}$$
$$\frac{dM_y}{dt} = \gamma(\vec{M} \times \vec{B})_y - \frac{M_y}{T_2}$$
$$\frac{dM_z}{dt} = \gamma(\vec{M} \times \vec{B})_z - \frac{M_z - M_0}{T_1}$$
- Solutions in rotating frame after 90-degree pulse:
  - Transverse: $M_{xy}(t) = M_0 e^{-t/T_2} e^{-i\Delta\omega t}$ (free induction decay, FID).
  - Longitudinal: $M_z(t) = M_0(1 - e^{-t/T_1})$ (recovery).

### 3.2 T1 Relaxation (Spin-Lattice / Longitudinal)

- Recovery of $M_z$ toward equilibrium $M_0$.
- Physical mechanism: energy exchange between spin system and molecular environment ("lattice") at the Larmor frequency.
- **BPP theory (Bloembergen, Purcell, Pound):** $T_1$ depends on spectral density of molecular motions at $\omega_0$.
  - $T_1$ shortest when correlation time $\tau_c \approx 1/\omega_0$.
  - Small molecules (fast tumbling, short $\tau_c$): long $T_1$.
  - Large molecules (slow tumbling): long $T_1$.
  - Medium molecules (tissue water): $T_1$ minimum.
- Typical values at 3T: CSF ~4000 ms, gray matter ~1300 ms, white matter ~830 ms, fat ~370 ms.
- $T_1$ increases with field strength (spectral density argument).

### 3.3 T2 Relaxation (Spin-Spin / Transverse)

- Decay of $M_{xy}$ due to loss of phase coherence among spins.
- Physical mechanism: local field fluctuations from neighboring spins cause individual precession rates to vary.
- $T_2 \leq T_1$ always ($T_2 = T_1$ only for extreme motional narrowing).
- Typical values at 3T: CSF ~2000 ms, gray matter ~80 ms, white matter ~70 ms, fat ~60 ms.
- $T_2$ relatively independent of field strength.

### 3.4 T2* Relaxation

- $1/T_2^* = 1/T_2 + 1/T_2'$ where $T_2'$ is from static field inhomogeneities.
- $T_2' \propto$ susceptibility differences, shimming quality.
- Gradient echo sequences sensitive to $T_2^*$; spin echo sequences refocus $T_2'$ component.
- **BOLD contrast** in fMRI exploits $T_2^*$ sensitivity to deoxyhemoglobin (see Section XII).

### 3.5 Tissue Contrast Origin

- Differences in $T_1$, $T_2$, and proton density ($\rho$) among tissues create contrast.
- Pulse sequence parameters (TR, TE, TI) weight the image toward different contrasts.

---

## IV. Signal Detection and the FID

### 4.1 Free Induction Decay

- After excitation, precessing transverse magnetization induces EMF in receiver coil (Faraday's law).
- Signal: $s(t) \propto M_0 e^{-t/T_2^*} e^{-i\omega_0 t}$.
- Demodulation to baseband (quadrature detection): in-phase and quadrature channels → complex signal.

### 4.2 Signal-to-Noise Ratio (SNR)

- SNR $\propto B_0^{7/4}$ (theoretical; simplified).
- SNR $\propto$ voxel volume, $\sqrt{\text{number of averages}}$, $1/\sqrt{\text{bandwidth}}$.
- Tradeoffs: resolution vs. SNR vs. scan time.

---

## V. Spatial Encoding and k-Space

### 5.1 Magnetic Field Gradients

- Linear gradient: $B_z(\vec{r}) = B_0 + \vec{G} \cdot \vec{r}$.
- Gradient coils: $G_x$, $G_y$, $G_z$ — produce linear variations in $B_z$.
- Gradient strength: clinical systems 40-80 mT/m. Slew rate: 150-200 T/m/s.

### 5.2 Slice Selection

- Gradient during RF pulse selects a slice (Section II.2).
- Slice-select gradient + refocusing lobe.

### 5.3 Frequency Encoding (Readout)

- During signal acquisition, apply gradient $G_x$: spins at different $x$ positions precess at different frequencies.
- $\omega(x) = \gamma(B_0 + G_x \cdot x)$.
- Fourier transform of the signal yields the spin density projection along $x$.

### 5.4 Phase Encoding

- Before readout, apply gradient $G_y$ for time $t_y$: phase $\phi(y) = \gamma G_y y t_y$.
- Repeat acquisition with different $G_y$ amplitudes. Each repetition encodes one line of k-space.
- Total scan time = $N_y \times TR$ (for conventional Cartesian).

### 5.5 k-Space Formalism

- Define $\vec{k}(t) = \frac{\gamma}{2\pi}\int_0^t \vec{G}(t')\, dt'$.
- Signal: $s(\vec{k}) = \int \rho(\vec{r})\, e^{-i2\pi\vec{k}\cdot\vec{r}}\, d\vec{r}$.
- **The MRI signal is the Fourier transform of the spin density (weighted by relaxation).**
- Image reconstruction: inverse Fourier transform of k-space data.
- k-space properties:
  - Center of k-space: contrast (low spatial frequencies).
  - Periphery: edges and fine detail (high spatial frequencies).
  - Symmetric in theory (Hermitian symmetry for real images).

### 5.6 Sampling and Reconstruction

- **Nyquist criterion:** Sampling rate must be $\geq 2 f_{\max}$ to avoid aliasing.
- Field of view: $\text{FOV} = 1/\Delta k$.
- Resolution: $\Delta x = 1 / (2 k_{\max}) = \text{FOV} / N$.
- **Partial Fourier:** Exploit conjugate symmetry to acquire slightly over half of k-space. Reduces scan time. Phase correction needed.
- **Parallel imaging:**
  - **SENSE (Sensitivity Encoding):** Undersample k-space, use coil sensitivity maps to unfold aliased images. Image domain.
  - **GRAPPA (Generalized Autocalibrating Partially Parallel Acquisitions):** Estimate missing k-space lines from acquired data using learned kernels. k-space domain.
  - Acceleration factor $R$: SNR penalty $\sim \sqrt{R} \cdot g$ where $g$ is the geometry factor.
- **Compressed sensing:** Exploit sparsity in some transform domain. Random undersampling of k-space. Iterative reconstruction with $L_1$ regularization.

### 5.7 Non-Cartesian Sampling

- Radial: lines through k-space center. Robust to motion. Oversamples center.
- Spiral: efficient coverage. Sensitive to off-resonance.
- EPI (echo planar imaging): zig-zag traversal in single shot.
- Propeller / BLADE: rotating strips through k-space center. Motion-robust.

---

## VI. Pulse Sequences

### 6.1 Spin Echo (SE)

- 90° — TE/2 — 180° — TE/2 — echo.
- 180° refocuses static field inhomogeneities ($T_2'$): echo signal decays as $T_2$ (not $T_2^*$).
- Contrast control: TR controls $T_1$ weighting, TE controls $T_2$ weighting.
  - Short TR, short TE → $T_1$-weighted.
  - Long TR, long TE → $T_2$-weighted.
  - Long TR, short TE → proton density weighted.

### 6.2 Gradient Echo (GRE)

- $\alpha$ — readout with gradient reversal — echo.
- No 180° refocusing: signal decays as $T_2^*$.
- Ernst angle: $\alpha_E = \arccos(e^{-TR/T_1})$ maximizes steady-state signal.
- Fast: short TR possible. Used for BOLD fMRI, angiography, susceptibility-weighted imaging.
- Spoiled GRE (SPGR/FLASH): spoil residual transverse magnetization.
- Balanced SSFP (TrueFISP/FIESTA): maintain steady state of both $M_z$ and $M_{xy}$. High SNR efficiency. $T_2/T_1$ contrast. Banding artifacts from off-resonance.

### 6.3 Inversion Recovery (IR)

- 180° (inversion) — TI — 90° (readout) — ...
- $M_z(TI) = M_0(1 - 2e^{-TI/T_1})$.
- **STIR (Short TI Inversion Recovery):** TI chosen to null fat signal (~160 ms at 1.5T).
- **FLAIR (Fluid-Attenuated Inversion Recovery):** TI chosen to null CSF (~2200 ms at 3T). Reveals periventricular lesions.
- Excellent $T_1$ contrast but long scan times (need long TR for full recovery).

### 6.4 Turbo/Fast Spin Echo (TSE/FSE)

- Multiple 180° refocusing pulses after initial 90°: echo train.
- Echo train length (ETL): number of echoes per TR.
- Each echo has different TE → different $T_2$ weighting → blurring if ETL is long.
- Effective TE: the echo that fills the center of k-space.
- Speed advantage: scan time reduced by factor of ETL.
- **HASTE (Half-Fourier Acquisition Single-shot Turbo Spin Echo):**
  - Single-shot: entire image from one excitation.
  - Half-Fourier: acquire slightly over half of k-space lines.
  - Very fast (< 1 second per slice). Heavy $T_2$ weighting.
  - **Critical for fetal MRI:** Motion-frozen snapshots. Thick slices (3-4 mm). Acquired in multiple orthogonal planes.
  - Limitations: low SNR (single shot), SAR from many 180° pulses, blurring from long echo train.

### 6.5 Echo Planar Imaging (EPI)

- Single-shot: entire k-space from one excitation using oscillating readout gradient.
- Very fast (50-100 ms per image).
- Gradient echo EPI (GE-EPI): BOLD fMRI. Spin echo EPI (SE-EPI): diffusion imaging.
- Limitations: distortion from $B_0$ inhomogeneity, Nyquist ghosting, limited resolution, chemical shift artifacts.
- Segmented EPI: multi-shot reduces distortion at cost of speed.

### 6.6 Diffusion-Weighted Imaging (DWI)

- Stejskal-Tanner sequence: two strong gradient pulses flanking a 180° pulse.
- Signal attenuation: $S = S_0 e^{-bD}$ where $b = \gamma^2 G^2 \delta^2(\Delta - \delta/3)$.
- $b$-value: gradient strength and timing. Typical clinical: $b = 1000$ s/mm$^2$.
- Apparent diffusion coefficient (ADC): measured diffusion coefficient (reflects tissue microstructure).
- Clinical applications: acute stroke (restricted diffusion in ischemia), tumor characterization.

### 6.7 Diffusion Tensor Imaging (DTI)

- Apply diffusion gradients in $\geq 6$ non-collinear directions.
- Diffusion tensor $\mathbf{D}$: $3 \times 3$ symmetric positive-definite matrix.
- Eigenvalues $\lambda_1 \geq \lambda_2 \geq \lambda_3$: diffusivities along principal axes.
- Eigenvectors: fiber orientation.
- Derived metrics:
  - Fractional anisotropy (FA): $FA = \sqrt{\frac{3}{2}} \frac{\sqrt{(\lambda_1 - \bar{\lambda})^2 + (\lambda_2 - \bar{\lambda})^2 + (\lambda_3 - \bar{\lambda})^2}}{\sqrt{\lambda_1^2 + \lambda_2^2 + \lambda_3^2}}$.
  - Mean diffusivity (MD): $\bar{\lambda} = (\lambda_1 + \lambda_2 + \lambda_3)/3$.
  - Axial diffusivity (AD): $\lambda_1$.
  - Radial diffusivity (RD): $(\lambda_2 + \lambda_3)/2$.
- **Tractography:** Trace white matter pathways by following eigenvector $\hat{e}_1$.
  - Deterministic: streamline integration.
  - Probabilistic: sample from orientation distribution at each step.
- Limitations of DTI: crossing fibers (single tensor cannot resolve). Solutions: HARDI, Q-ball, CSD, multi-shell methods.
- **Relevance to fetal/neonatal imaging:** White matter development, myelination tracking.

---

## VII. Image Contrast

### 7.1 T1-Weighted Imaging

- Short TR (400-600 ms), short TE (10-20 ms).
- Fat bright, fluid dark, gray matter darker than white matter.
- Post-gadolinium: enhancing lesions bright.
- Use: anatomy, post-contrast lesion detection.

### 7.2 T2-Weighted Imaging

- Long TR (>2000 ms), long TE (80-120 ms).
- Fluid bright, fat intermediate.
- Use: pathology detection (edema, inflammation).

### 7.3 Proton Density (PD) Weighted

- Long TR, short TE.
- Contrast from differences in proton concentration.

### 7.4 FLAIR

- T2-weighted with CSF nulled. See Section VI.3.
- Ideal for periventricular and cortical lesions.

### 7.5 Contrast Agents

- Gadolinium chelates: paramagnetic, shorten $T_1$ (appear bright on $T_1$w).
- Relaxivity: $1/T_1 = 1/T_{1,0} + r_1 [Gd]$.
- Iron oxide particles: superparamagnetic, shorten $T_2$/$T_2^*$.
- Safety: nephrogenic systemic fibrosis (NSF) risk in renal failure. Linear vs. macrocyclic agents.
- **Fetal MRI: gadolinium generally avoided** (crosses placenta, unknown fetal effects).

---

## VIII. Artifacts

### 8.1 Motion Artifacts

- Ghosting along phase-encode direction (periodic motion during acquisition).
- Respiratory and cardiac motion. Navigator echoes, triggering, breath-holding.
- **Fetal motion:** Unpredictable, cannot be gated. Requires fast single-shot sequences (HASTE, EPI) and retrospective motion correction.

### 8.2 Chemical Shift Artifact

- Fat and water protons resonate at slightly different frequencies ($\Delta f \approx 3.5$ ppm $\approx 450$ Hz at 3T).
- Type 1: spatial misregistration along readout direction.
- Type 2 (in/out of phase): signal cancellation at fat-water interfaces in GRE.
- Fat suppression: STIR, spectral (CHESS), Dixon method.

### 8.3 Susceptibility Artifacts

- Local field distortions at tissue-air or tissue-bone interfaces.
- Signal loss and geometric distortion (especially in EPI).
- Worse at higher field strength.
- Shimming: active and passive.

### 8.4 Aliasing (Wrap-Around)

- FOV too small: anatomy outside FOV wraps to opposite side.
- Phase-encode aliasing more problematic (frequency aliasing filtered).
- Prevention: increase FOV, oversampling, saturation bands.

### 8.5 Gibbs Ringing (Truncation Artifact)

- Oscillations near sharp signal transitions.
- Due to finite sampling in k-space (truncation of Fourier series).
- Worse with fewer phase-encode steps.
- Can mimic syrinx in spinal cord.
- Mitigation: increase matrix size, apply apodization filter (at cost of resolution).

### 8.6 Zipper Artifact, Herringbone, Spike

- RF leakage → zipper line.
- Gradient malfunction or data corruption → herringbone/spike noise in k-space.

---

## IX. Fetal MRI — Specific Considerations

### 9.1 Why Fetal MRI?

- Complements ultrasound: superior soft tissue contrast, less operator-dependent, not limited by maternal habitus/oligohydramnios/fetal position.
- Indications: CNS anomalies (ventriculomegaly, cortical malformations, posterior fossa abnormalities), body anomalies, placental assessment.
- Typically performed after 18 weeks gestational age.

### 9.2 Acquisition Strategy

- **HASTE/ssFSE:** Workhorse sequence. Single-shot, motion-frozen. T2-weighted.
  - Typical parameters: TR ~1000-1500 ms, TE ~80-100 ms, slice thickness 3-4 mm, in-plane resolution 1-1.5 mm.
  - Acquired in 3 orthogonal planes relative to fetal brain (not maternal body).
- **Multi-planar acquisition:** Axial, coronal, sagittal relative to fetal brain anatomy. Operator re-prescribes planes as fetus moves.
- **T1-weighted:** GRE or IR sequences. Less commonly used; for hemorrhage, calcification, fat.
- **DWI:** Single-shot EPI. Restricted diffusion in acute pathology.
- **No gadolinium** in standard fetal protocols.

### 9.3 Motion Challenges

- Fetal motion is stochastic: translational and rotational, unpredictable timing.
- Inter-slice motion: different slices acquired at different times → inconsistent geometry.
- **Slice-to-volume reconstruction (SVR):**
  - Acquire multiple stacks of 2D slices in different orientations.
  - Retrospectively estimate fetal motion (6 DOF rigid-body transform per slice).
  - Reconstruct a high-resolution 3D isotropic volume.
  - Iterative: motion estimation ↔ reconstruction.
  - Key algorithms/tools:
    - **NeSVoR (Neural Slice-to-Volume Reconstruction):** Deep learning-based SVR using implicit neural representations. Learned outlier rejection. State-of-the-art for fetal brain reconstruction.
    - **SVRTK:** Classical iterative SVR (Kuklisova-Murgasova et al.).
    - **IRTK:** Image registration toolkit.
  - Output: isotropic 3D volume (typically 0.5-0.8 mm) suitable for segmentation and surface analysis.

### 9.4 Fetal Brain Development Imaging

- **Gestational age milestones:**
  - ~16 weeks: smooth brain, early Sylvian fissure.
  - ~20 weeks: parieto-occipital fissure, calcarine sulcus.
  - ~24 weeks: central sulcus, superior temporal sulcus.
  - ~28 weeks: pre/postcentral gyri, cingulate sulcus.
  - ~32 weeks: secondary sulci developing.
  - ~36 weeks: tertiary sulci, near-adult pattern.
- Cortical folding analysis: gyrification index, sulcal depth, curvature (see [[neuroscience]]).
- Volumetric analysis: total brain volume, cortical plate, subplate, white matter, ventricles.
- Automated segmentation: atlas-based, deep learning (U-Net, nnU-Net).

### 9.5 Placental MRI

- T2*-weighted for oxygenation mapping.
- DWI for perfusion/diffusion.
- BOLD for oxygen dynamics.
- Challenging: maternal breathing motion, field inhomogeneity.

---

## X. Hardware

### 10.1 Main Magnet

- Superconducting solenoid: niobium-titanium alloy in liquid helium (4.2 K).
- Clinical field strengths: 1.5T, 3T (research: 7T, 9.4T, 11.7T).
- Homogeneity specification: <1 ppm over 40 cm DSV after shimming.
- Quench: sudden loss of superconductivity. Rapid helium boiloff. Emergency.
- Fringe field: the 5 Gauss (0.5 mT) line defines the controlled access area.

### 10.2 Gradient Coils

- Produce linear spatial variations in $B_z$.
- Specifications: maximum amplitude (mT/m), slew rate (T/m/s).
- Performance limits: peripheral nerve stimulation, acoustic noise.
- Eddy currents: time-varying gradients induce currents in conducting structures → field distortions. Pre-emphasis compensation.
- Actively shielded gradients reduce eddy currents.

### 10.3 RF Coils

- **Transmit coils:** Body coil (birdcage design), local transmit coils. Produce $B_1$ field.
- **Receive coils:** Phased arrays. Multiple small surface coils for high SNR.
  - Each coil element has a sensitivity profile $C_j(\vec{r})$.
  - Signal combination: sum of squares, adaptive combine.
  - Coil sensitivity maps used in parallel imaging (SENSE, GRAPPA).
- RF shielding to prevent external interference.

### 10.4 Shimming

- **Passive:** Ferromagnetic shim plates.
- **Active:** Shim coils (linear and higher-order spherical harmonics).
- Improves $B_0$ homogeneity → reduces $T_2'$, chemical shift, EPI distortion.

---

## XI. Safety

### 11.1 Static Magnetic Field

- Projectile hazard (ferromagnetic objects).
- Bioeffects: generally benign at clinical fields. Vertigo and nausea at 7T+.
- Implant safety: MR Safe, MR Conditional, MR Unsafe classification.

### 11.2 Specific Absorption Rate (SAR)

- RF power deposition in tissue: $\text{SAR} = \frac{\sigma |E|^2}{2\rho}$ (W/kg).
- Limits (IEC): whole body 2 W/kg (normal mode), 4 W/kg (first controlled), head 3.2 W/kg.
- SAR $\propto B_0^2$, $\propto$ flip angle$^2$, $\propto$ duty cycle.
- **Fetal MRI SAR concern:** Fetal tissue heating. Conservative SAR limits applied. Favor low-SAR sequences.
- SAR reduction: lower flip angles, VERSE pulses, parallel transmit.

### 11.3 Gradient Safety

- Peripheral nerve stimulation (PNS): tingling from time-varying gradients.
- Acoustic noise: up to 130 dB. Ear protection mandatory.

### 11.4 Contraindications

- Cardiac pacemakers (some MR-Conditional now), cochlear implants, metallic foreign bodies (especially orbital), certain aneurysm clips.
- Pregnancy: no known harmful effects from MRI, but gadolinium avoided.

---

## XII. Advanced Techniques

### 12.1 Functional MRI (fMRI)

- **BOLD (Blood Oxygen Level Dependent) contrast:**
  - Deoxyhemoglobin is paramagnetic → shortens $T_2^*$.
  - Neural activity → increased blood flow (neurovascular coupling) → decreased deoxyhemoglobin → increased $T_2^*$ signal.
  - Indirect measure of neural activity.
- Acquisition: GE-EPI, TR ~1-2 s (or multiband: ~0.5 s).
- Analysis: GLM (general linear model), ICA, seed-based connectivity.
- Resting-state fMRI: functional connectivity networks without task.
- **Fetal fMRI:** Emerging field. Extreme challenges (motion, small brain, physiological noise).

### 12.2 MR Spectroscopy (MRS)

- Measure metabolite concentrations by chemical shift spectrum.
- Key metabolites: NAA (neuronal marker), choline, creatine, myo-inositol, lactate, lipids.
- Single-voxel (PRESS, STEAM) and multi-voxel (CSI) techniques.
- Water suppression required.
- Quantification: LCModel, jMRUI.

### 12.3 Perfusion Imaging

- **Dynamic susceptibility contrast (DSC):** Bolus of gadolinium tracked through brain. CBV, CBF, MTT maps.
- **Dynamic contrast-enhanced (DCE):** Permeability mapping ($K^{\text{trans}}$).
- **Arterial spin labeling (ASL):** Endogenous contrast — magnetically label inflowing blood. No gadolinium needed. Lower SNR. Good for pediatrics/fetal (no contrast agent).

### 12.4 MR Angiography

- Time-of-flight (TOF): bright blood from inflow effect.
- Phase contrast: velocity encoding.
- Contrast-enhanced MRA: gadolinium bolus.
- 4D flow: time-resolved 3D velocity fields.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Larmor precession | Fundamental frequency relationship: $\omega_0 = \gamma B_0$ |
| Bloch equations | Govern magnetization dynamics including relaxation |
| k-space | Signal is Fourier transform of image; central insight of MRI |
| T1, T2, T2* | Tissue-specific relaxation → contrast |
| HASTE | Single-shot T2w: essential for fetal MRI |
| Slice-to-volume reconstruction | Overcomes fetal motion for 3D volumetric analysis |
| Parallel imaging | Accelerated acquisition (SENSE, GRAPPA) |
| Diffusion imaging | Microstructural probe (DWI/DTI/tractography) |
| SAR | Safety limit on RF power; especially important for fetal imaging |

---

## Recommended References

1. **Haacke et al.** — *Magnetic Resonance Imaging: Physical Principles and Sequence Design* (2nd ed.). Comprehensive physics and engineering.
2. **Bernstein, King, Zhou** — *Handbook of MRI Pulse Sequences*. Definitive engineering reference.
3. **Nishimura** — *Principles of Magnetic Resonance Imaging*. Concise, signal-processing perspective.
4. **Levitt** — *Spin Dynamics* (2nd ed.). NMR quantum mechanics. Rigorous.
5. **Liang & Lauterbur** — *Principles of Magnetic Resonance Imaging: A Signal Processing Perspective*. Fourier/k-space emphasis.
6. **Prayer (ed.)** — *Fetal MRI*. Clinical/technical reference for fetal imaging.
7. **Xu et al.** — NeSVoR: Implicit Neural Representation for Slice-to-Volume Reconstruction in MRI. (2023).
8. **Kuklisova-Murgasova et al.** — Reconstruction of Fetal Brain MRI with Intensity Matching and Complete Outlier Removal. Medical Image Analysis (2012).

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
