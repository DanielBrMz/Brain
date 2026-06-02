---
title: "SSIM — Structural Similarity Index"
type: knowledge
updated: 2026-04-27
tags: [math, metric, loss-function, image-quality]
---

# SSIM — Structural Similarity Index

## Definition

    SSIM(x, y) = l(x,y) * c(x,y) * s(x,y)

Three components computed over local 11x11 Gaussian windows:

- **Luminance:** l = (2*mu_x*mu_y + C1) / (mu_x^2 + mu_y^2 + C1)
- **Contrast:** c = (2*sigma_x*sigma_y + C2) / (sigma_x^2 + sigma_y^2 + C2)
- **Structure:** s = (sigma_xy + C2/2) / (sigma_x*sigma_y + C2/2)

Simplified:

    SSIM = ((2*mu_x*mu_y + C1)(2*sigma_xy + C2)) / ((mu_x^2 + mu_y^2 + C1)(sigma_x^2 + sigma_y^2 + C2))

Stability constants: C1 = (k1*L)^2, C2 = (k2*L)^2 where L = dynamic range, k1=0.01, k2=0.03.

## Why SSIM over MSE/PSNR?

MSE/PSNR treat all pixel errors equally. SSIM captures:
- Mean luminance (brightness match)
- Variance (contrast match)
- Covariance (structural pattern match)

A blurred image can have good MSE but poor SSIM because the structure (edges, textures) is destroyed.

## As a Loss Function

    L_SSIM = 1 - SSIM(pred, target)

Minimizing L_SSIM maximizes structural similarity. Combined with L1:

    L_sup = 0.7 * L1 + 0.3 * L_SSIM

## Used In
- [[fetenh-net]] — SSIMLoss component of supervised loss (lambda_ssim=0.3)
- [[fetenh-foundational-model]] — delta-SSIM reported per degradation type
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Wang et al. "Image Quality Assessment: From Error Visibility to Structural Similarity", IEEE TIP 2004.
