---
title: "Mathematical Foundations — Medical Image Segmentation & Enhancement"
type: knowledge
updated: 2026-04-27
tags: [math, deep-learning, medical-imaging, fetenh, hydrocephalus, reference]
---

# Mathematical Foundations — Medical Image Segmentation & Enhancement

Syllabus of all mathematical concepts underpinning FetEnhNet (image enhancement) and Victoria's Hydrocephalus Model (segmentation). Organized from foundations up.

---

## 1. Linear Algebra & Signal Processing

### 1.1 Convolution

The core operation in CNNs. For a 2D image I and kernel K of size m x n:

    (I * K)(x,y) = sum_i sum_j I(x-i, y-j) * K(i,j)

In practice, implemented as cross-correlation. A 3D convolution (used in the hydro 3D UNet) extends this to volumetric data with a kernel K(i,j,k).

### 1.2 Fourier Transform (FFT)

Used in: Frequency Loss, motion ghosting degradation, Gibbs ringing.

The 2D Discrete Fourier Transform:

    F(u,v) = sum_x sum_y f(x,y) * exp(-j2pi(ux/M + vy/N))

Key properties:
- **Magnitude spectrum** |F(u,v)| encodes spatial frequency content
- **High frequencies** = edges, texture, fine detail
- **Low frequencies** = smooth intensity variations
- Blurring attenuates high frequencies; the Frequency Loss penalizes this directly

### 1.3 Affine Transformations

Used in: NeSVoR inverse alignment, label projection, image reorientation.

A 4x4 affine matrix maps between coordinate spaces:

    [x']   [a11 a12 a13 tx] [x]
    [y'] = [a21 a22 a23 ty] [y]
    [z']   [a31 a32 a33 tz] [z]
    [1 ]   [  0   0   0  1] [1]

Encodes rotation, scaling, shearing, and translation. Inverse transform:

    vol_voxels = inv(vol_affine) @ slice_affine @ slice_voxels

This is the formula used to project tissue labels from reconstructed NeSVoR volumes back onto raw HASTE slices.

---

## 2. Probability & Statistics

### 2.1 Gaussian (Normal) Distribution

    p(x) = (1 / sqrt(2pi*sigma^2)) * exp(-(x-mu)^2 / (2*sigma^2))

Used in: Gaussian noise degradation, Gaussian blur (PSF), SSIM kernel, Adam optimizer (moment estimates).

### 2.2 Rician Distribution

The correct noise model for magnitude MRI images:

    p(x | v, sigma) = (x / sigma^2) * exp(-(x^2 + v^2) / (2*sigma^2)) * I_0(x*v / sigma^2)

where v is the true signal, sigma is the Gaussian noise std, and I_0 is the modified Bessel function of the first kind.

Why Rician not Gaussian? MRI scanners acquire complex-valued data (real + imaginary channels, each with Gaussian noise). The magnitude image sqrt(Re^2 + Im^2) follows a Rician distribution:

    magnitude = sqrt((signal + noise_re)^2 + noise_im^2)

At high SNR, Rician approximates Gaussian. At low SNR, Rician has a positive bias (the "noise floor"). Our synthetic degradation engine models this correctly.

### 2.3 Bayes' Theorem (conceptual)

    P(class | pixels) = P(pixels | class) * P(class) / P(pixels)

Underpins why class imbalance matters: rare classes (ventricles, cortical plate) have low P(class), so the model defaults to predicting majority classes unless corrected via weighted losses or oversampling.

### 2.4 K-Fold Cross-Validation

With small datasets (N=17), a single train/test split is unreliable. K-fold CV:

1. Split N subjects into K folds (K=5 here)
2. For each fold k: train on K-1 folds, evaluate on fold k
3. Every subject appears in exactly one test fold
4. Report mean +/- std across all N subjects

This gives unbiased performance estimates and reveals per-subject variance, critical with N=17.

---

## 3. Loss Functions

### 3.1 L1 Loss (Mean Absolute Error)

    L_L1 = (1/N) * sum |pred_i - target_i|

Robust to outliers (compared to L2/MSE). Used as the primary pixel-wise reconstruction loss in FetEnhNet.

### 3.2 L2 Loss (Mean Squared Error)

    L_L2 = (1/N) * sum (pred_i - target_i)^2

Penalizes large errors quadratically. Foundation for PSNR and SURE loss. Not used directly due to tendency to produce blurry results.

### 3.3 Dice Loss

The Dice coefficient measures overlap between two sets A and B:

    Dice(A, B) = 2|A intersect B| / (|A| + |B|)

For soft (differentiable) predictions:

    Dice(c) = (2 * sum(pred_c * target_c) + smooth) / (sum(pred_c) + sum(target_c) + smooth)

    L_dice = 1 - (1/C) * sum_c Dice(c)

Properties:
- Range [0, 1] where 1 = perfect overlap
- Handles class imbalance naturally (each class contributes equally via macro-averaging)
- The smooth term (typically 1.0) prevents division by zero and gradient explosion when a class is absent
- Used in both FetEnhNet (SoftDiceLoss) and Hydro model (via MONAI DiceFocalLoss)

### 3.4 Cross-Entropy Loss

For C classes with ground truth one-hot y and predicted probabilities p:

    L_CE = -sum_c y_c * log(p_c)

With class weights w_c to handle imbalance:

    L_wCE = -sum_c w_c * y_c * log(p_c)

Label smoothing replaces hard targets y_c in {0,1} with softened targets:

    y_smooth = y * (1 - epsilon) + epsilon / C

This prevents overconfident predictions and helps with noisy labels (e.g., atlas-projected tissue labels that may have boundary errors).

### 3.5 Focal Loss

    FL(p_t) = -(1 - p_t)^gamma * log(p_t)

where p_t is the predicted probability for the true class.

The (1-p_t)^gamma modulation:
- **Easy examples** (p_t -> 1): weight -> 0, contribution suppressed
- **Hard examples** (p_t -> 0): weight -> 1, full contribution
- gamma=0: standard CE. gamma=2 (our setting): aggressively down-weights easy background

Combined with Dice in MONAI's DiceFocalLoss (lambda_dice=0.5, lambda_focal=0.5, gamma=2.0) for the hydro model.

### 3.6 SSIM Loss (Structural Similarity)

    SSIM(x, y) = ((2*mu_x*mu_y + C1)(2*sigma_xy + C2)) / ((mu_x^2 + mu_y^2 + C1)(sigma_x^2 + sigma_y^2 + C2))

Computed over 11x11 Gaussian-weighted windows. Three components:
- **Luminance**: (2*mu_x*mu_y + C1) / (mu_x^2 + mu_y^2 + C1)
- **Contrast**: (2*sigma_x*sigma_y + C2) / (sigma_x^2 + sigma_y^2 + C2)
- **Structure**: (sigma_xy + C2/2) / (sigma_x*sigma_y + C2/2)

Stability constants: C1 = (0.01)^2, C2 = (0.03)^2 (for [0,1] range).

L_SSIM = 1 - SSIM (so minimizing loss = maximizing similarity).

SSIM captures perceptual similarity better than L1/L2 because it considers local structure, not just pixel values.

### 3.7 Frequency Loss

    L_freq = L1(|FFT(pred)|, |FFT(target)|)

Applied to 2D rFFT magnitudes with orthonormal normalization. Directly penalizes blurring by comparing frequency spectra. Complements L1+SSIM which are dominated by low-frequency pixel values.

Reference: Zhao et al. "Loss Functions for Image Restoration with Neural Networks", IEEE TCI 2017.

### 3.8 SURE Loss (Stein's Unbiased Risk Estimator)

The key self-supervised loss — enables training without clean ground truth.

**Stein's Lemma** (1981): For x ~ N(mu, sigma^2 I) and a differentiable function f:

    E[||f(x) - mu||^2] = E[||f(x) - x||^2] - n*sigma^2 + 2*sigma^2 * div(f)(x)

This means we can estimate the MSE to the TRUE clean signal using ONLY the noisy observation, without ever seeing the clean signal.

**Spatially-variant MC-SURE** (Pfaff et al., 2023): For non-uniform noise sigma(x,y):

    SURE(f) = ||f(y) - y||^2 - sum_d sigma_d^2 + 2 * div_y(sigma^2 . f(y))

Divergence estimated via Monte Carlo:

    div(sigma^2 . f(y)) approx b^T * (sigma^2 . (f(y + eps*b) - f(y)) / eps)

where b ~ N(0, I). This requires TWO forward passes per batch.

Critical sensitivity: overestimated sigma -> divergence dominates -> negative loss -> training collapse. Underestimated sigma -> model learns identity.

Reference: Pfaff et al., Scientific Reports 13:22629 (2023).

---

## 4. Evaluation Metrics

### 4.1 PSNR (Peak Signal-to-Noise Ratio)

    PSNR = 10 * log10(MAX^2 / MSE)

where MAX is the maximum pixel value (1.0 for normalized images). Higher = better. Our FetEnhNet reports delta-PSNR (improvement over degraded input).

### 4.2 Dice Coefficient

Same as Dice Loss section (3.3) but used as a metric (not loss). Reported per-class and macro-averaged. The hydro model reports Brain Dice and Ventricle Dice separately because ventricle segmentation is harder (smaller, variable shape).

### 4.3 Hausdorff Distance (HD95)

    HD(A, B) = max(max_a min_b d(a,b), max_b min_a d(a,b))

The 95th percentile variant (HD95) is robust to outlier voxels:

    HD95(A, B) = P95(all pairwise min-distances from A to B union B to A)

Measures the worst-case boundary error in millimeters. Important for clinical use because a high Dice with poor HD95 means the overall volume is correct but the boundary has large local errors.

---

## 5. Network Architecture

### 5.1 U-Net

Encoder-decoder with skip connections (Ronneberger et al., 2015):

- **Encoder**: repeated [Conv -> BN -> ReLU -> MaxPool] blocks, doubling channels at each level (32 -> 64 -> 128 -> 256 for hydro; + 512 for 2D)
- **Bottleneck**: deepest representation
- **Decoder**: [Upsample -> Concat(skip) -> Conv -> BN -> ReLU] blocks
- **Skip connections**: concatenate encoder features to decoder at each level, preserving spatial detail lost during downsampling

The 3D variant uses 3D convolutions and 3D max pooling, operating on volumetric patches (128^3).

### 5.2 Residual Units (ResBlocks)

    y = F(x) + x

where F is a stack of [Conv -> BN -> ReLU -> Conv -> BN]. The identity shortcut:
- Enables gradient flow through very deep networks (solves vanishing gradients)
- Lets layers learn residual corrections rather than full transformations
- `num_res_units=2` in MONAI UNet adds 2 residual blocks per encoder/decoder level

### 5.3 FiLM Conditioning (Feature-wise Linear Modulation)

    FiLM(x, tissue) = gamma(tissue) * x + beta(tissue)

where gamma and beta are learned per-pixel scale and shift parameters derived from the tissue probability map via a 1x1 convolution. Applied in each decoder block.

This is how the enhancement network applies different processing strategies per tissue type (e.g., aggressive denoising in CSF, gentle sharpening in cortical plate).

Reference: Perez et al. "FiLM: Visual Reasoning with a General Conditioning Layer", AAAI 2018.

### 5.4 Batch Normalization

    BN(x) = gamma * (x - mu_batch) / sqrt(sigma_batch^2 + eps) + beta

Normalizes activations per mini-batch to zero mean, unit variance. Learned gamma/beta allow the network to undo the normalization if needed. Stabilizes training, enables higher learning rates, provides mild regularization.

### 5.5 Dropout

During training, randomly zero out activations with probability p:

    x_dropped = x * mask / (1 - p)    where mask ~ Bernoulli(1-p)

Regularization that prevents co-adaptation of neurons. The 1/(1-p) scaling ensures expected values match at test time (when dropout is disabled). Hydro model uses p=0.1 (3D) and p=0.2 (2D).

---

## 6. Optimization

### 6.1 Adam Optimizer

Adaptive moment estimation (Kingma & Ba, 2015):

    m_t = beta1 * m_{t-1} + (1-beta1) * g_t          (first moment / mean)
    v_t = beta2 * v_{t-1} + (1-beta2) * g_t^2         (second moment / variance)
    m_hat = m_t / (1 - beta1^t)                        (bias correction)
    v_hat = v_t / (1 - beta2^t)
    theta_t = theta_{t-1} - lr * m_hat / (sqrt(v_hat) + eps)

Per-parameter learning rates adapted by gradient history. Default beta1=0.9, beta2=0.999. Weight decay (L2 regularization) adds lambda*theta to the gradient: `weight_decay=1e-5`.

### 6.2 Cosine Annealing Learning Rate

    lr(t) = eta_min + 0.5 * (eta_max - eta_min) * (1 + cos(pi * t / T_max))

Smoothly decays LR from initial value to eta_min following a cosine curve over T_max epochs. Avoids the sharp drops of step schedules. Both models use this with eta_min=1e-6.

### 6.3 Early Stopping

Monitor validation metric; stop training if no improvement after `patience` epochs. Prevents overfitting by selecting the model at the point of best generalization. The hydro model uses patience=50 (3D) and patience=20 (2D).

---

## 7. Image Degradation Physics

### 7.1 Point Spread Function (PSF) / Gaussian Blur

Convolution of image with a Gaussian kernel:

    G(x,y) = (1 / (2*pi*sigma^2)) * exp(-(x^2 + y^2) / (2*sigma^2))

    I_blurred = I * G

Anisotropic variant uses different sigma_x, sigma_y, rotated by angle theta. Models directional PSF broadening from gradient imperfections.

### 7.2 B1 Bias Field

Smooth multiplicative intensity inhomogeneity from RF coil non-uniformity:

    I_biased(x,y) = I(x,y) * B(x,y)

where B is a smooth polynomial field:

    B(x,y) = 1 + sum_{p=1}^{order} sum_{q=0}^{p} c_{pq} * x^(p-q) * y^q

Correcting bias requires multiplicative (not additive) correction — this is why the additive residual in the current FetEnhNet architecture fails on bias field (-0.84 dB).

### 7.3 Motion Ghosting

Periodic motion during MRI acquisition creates ghost copies in k-space:

    K_ghosted(kx, ky) = K(kx, ky) + alpha * K(kx, ky) * exp(-j*2pi*shift*ky)

The ghost appears as a shifted copy along the phase-encode direction (ky), attenuated by intensity alpha.

### 7.4 Gibbs Ringing

k-space truncation causes oscillatory artifacts near sharp edges:

    I_gibbs = IFFT(K * rect_window)

The rectangular window in k-space creates sinc-function ringing in image space (Gibbs phenomenon). Simulated by zeroing high-frequency k-space components and inverting.

---

## 8. Image Registration

### 8.1 Coordinate Systems in Fetal MRI

Five coordinate spaces in the FetEnhNet pipeline:
1. **Scanner (RAS)** — physical mm, Right-Anterior-Superior
2. **Raw stack voxel** — integer indices in the acquired HASTE stack
3. **NeSVoR reconstructed voxel** — indices in the 3D isotropic reconstruction
4. **Atlas space** — standard template coordinates for segmentation
5. **Slice space** — per-slice 2D grid within each raw stack

### 8.2 Dice Overlap for Registration Quality

Used to evaluate how well projected labels align with the brain:

    Dice(projected_mask, target_mask) >= 0.80 for "good" registration

The 8-flip search tests all combinations of axis flips to find the correct orientation, then refines with binary shape registration.

---

## 9. Sliding Window Inference

For 3D volumes too large to fit in GPU memory:

1. Extract overlapping patches of size P (128^3)
2. Run model on each patch independently
3. Aggregate predictions with Gaussian weighting (center weighted more than edges)
4. Overlap ratio 0.5 ensures smooth blending at patch boundaries

This avoids boundary artifacts that would occur with non-overlapping patches.

---

## 10. One-Hot Encoding

Convert integer class labels to binary channel representation:

    label = [0, 1, 2, 1]  ->  [[1,0,0], [0,1,0], [0,0,1], [0,1,0]]

Required for Dice computation and loss functions that operate on per-class probability maps. For C classes, creates a C-channel tensor where channel c has 1 where the label equals c.

---

## Reading List

| Topic | Reference |
|-------|-----------|
| U-Net | Ronneberger et al. "U-Net: Convolutional Networks for Biomedical Image Segmentation", MICCAI 2015 |
| FiLM | Perez et al. "FiLM: Visual Reasoning with a General Conditioning Layer", AAAI 2018 |
| Adam | Kingma & Ba. "Adam: A Method for Stochastic Optimization", ICLR 2015 |
| Batch Norm | Ioffe & Szegedy. "Batch Normalization: Accelerating Deep Network Training", ICML 2015 |
| ResNet | He et al. "Deep Residual Learning for Image Recognition", CVPR 2016 |
| Dice Loss | Milletari et al. "V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation", 3DV 2016 |
| Focal Loss | Lin et al. "Focal Loss for Dense Object Detection", ICCV 2017 |
| SSIM | Wang et al. "Image Quality Assessment: From Error Visibility to Structural Similarity", IEEE TIP 2004 |
| Frequency Loss | Zhao et al. "Loss Functions for Image Restoration with Neural Networks", IEEE TCI 2017 |
| SURE | Stein. "Estimation of the Mean of a Multivariate Normal Distribution", Annals of Statistics, 1981 |
| MC-SURE for MRI | Pfaff et al. "Self-supervised MRI denoising using Stein's unbiased risk estimator", Sci. Reports 2023 |
| Rician noise | Gudbjartsson & Patz. "The Rician Distribution of Noisy MRI Data", MRM 1995 |
| NeSVoR | Xu et al. "NeSVoR: Implicit Neural Representation for Slice-to-Volume Reconstruction", IEEE TMI 2023 |
| BME-X | Cai et al. (architecture inspiration for tissue-conditioned enhancement) |
| Hausdorff Distance | Huttenlocher et al. "Comparing Images Using the Hausdorff Distance", IEEE TPAMI 1993 |
| Cosine Annealing | Loshchilov & Hutter. "SGDR: Stochastic Gradient Descent with Warm Restarts", ICLR 2017 |
