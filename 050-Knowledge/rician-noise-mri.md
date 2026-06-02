---
title: "Rician Noise in MRI"
type: knowledge
updated: 2026-04-27
tags: [math, mri-physics, noise, medical-imaging]
---

# Rician Noise in MRI

## Why Not Gaussian?

MRI scanners acquire complex-valued signals (real + imaginary channels). Each channel has independent Gaussian noise. But clinical images are magnitude images:

    magnitude = sqrt((signal + noise_re)^2 + noise_im^2)

This magnitude operation creates Rician-distributed noise.

## Rician PDF

    p(x | v, sigma) = (x / sigma^2) * exp(-(x^2 + v^2) / (2*sigma^2)) * I_0(x*v / sigma^2)

where:
- v = true signal amplitude
- sigma = Gaussian noise std in each channel
- I_0 = modified Bessel function of the first kind

## Key Properties

- **High SNR (v >> sigma):** Rician approximates Gaussian N(v, sigma^2) — additive noise
- **Low SNR (v ~ sigma):** Positive bias (noise floor) — signal is overestimated
- **Zero signal (v = 0):** Reduces to Rayleigh distribution — background is never truly zero

## Synthetic Degradation

Our degradation engine correctly simulates Rician noise:

    re = signal + N(0, sigma) * sigma_map
    im = N(0, sigma) * sigma_map
    degraded = sqrt(re^2 + im^2)

With optional spatially-varying sigma_map (0.5*sigma to 1.5*sigma) to simulate distance-dependent SNR from the RF coil.

## SURE Applicability

SURE assumes Gaussian noise. For magnitude MRI, SURE is valid when:
- SNR is high enough that Rician approximates Gaussian
- Working with squared-magnitude images
- For fetal HASTE at clinical field strengths, this holds in the brain region

## Used In
- [[fetenh-net]] — synthetic degradation engine (foundational_degradation.py)
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Gudbjartsson & Patz. "The Rician Distribution of Noisy MRI Data", MRM 1995.
