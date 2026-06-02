---
title: "SURE Loss — Stein's Unbiased Risk Estimator"
type: knowledge
updated: 2026-04-27
tags: [math, loss-function, self-supervised, denoising]
---

# SURE Loss — Stein's Unbiased Risk Estimator

## The Problem

We want to train a denoising network f on real noisy images, but we have no clean ground truth. Can we estimate how close f(y_noisy) is to the unknown clean image x?

## Stein's Lemma (1981)

For y = x + noise where noise ~ N(0, sigma^2 I):

    E[||f(y) - x||^2] = E[||f(y) - y||^2] - n*sigma^2 + 2*sigma^2 * div(f)(y)

The left side (what we want to minimize) equals the right side (computable from y alone). We never need x.

## Divergence Estimation (Monte Carlo)

The divergence div(f)(y) = sum_i df_i/dy_i is intractable for neural networks. MC estimate:

    div(f)(y) approx (1/eps) * b^T * (f(y + eps*b) - f(y))

where b ~ N(0, I). Requires two forward passes.

## Spatially-Variant MC-SURE (Pfaff et al. 2023)

Real MRI noise varies spatially (closer to coil = less noise). Extended formula:

    SURE(f) = ||f(y) - y||^2 - sum_d sigma_d^2 + 2 * div_y(sigma^2 . f(y))

where sigma_d is the per-pixel noise standard deviation.

## Critical Sensitivity

- **sigma too high** -> divergence dominates -> loss goes negative -> training collapse
- **sigma too low** -> model learns identity (no denoising)
- For synthetic pairs: use the known degradation sigma
- For real data: estimate from background statistics

## Status in FetEnhNet

- Runs 12-13: SURE attempted but lambda_sure=0.1 too aggressive, destabilized training
- Run 13: lambda_sure=0.01 but combined with unreliable tissue conditioning
- Next: reintroduce with calibrated lambda on top of stable foundational model (Run 02)

## Used In
- [[fetenh-net]] — planned self-supervised component for real LOW stacks
- [[math-foundations-medical-imaging-dl]] — full syllabus

## References
- Stein. "Estimation of the Mean of a Multivariate Normal Distribution", Annals of Statistics, 1981.
- Pfaff et al. "Self-supervised MRI denoising using Stein's unbiased risk estimator", Sci. Reports 2023.
