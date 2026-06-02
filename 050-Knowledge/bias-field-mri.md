---
title: "B1 Bias Field in MRI"
type: knowledge
updated: 2026-05-14
tags: [mri-physics, degradation, fetal-imaging]
---

# B1 Bias Field in MRI

## What It Is

A smooth, spatially-varying multiplicative intensity inhomogeneity caused by non-uniform RF (B1) transmit/receive field:

    I_observed(x,y) = I_true(x,y) * B(x,y) + noise

The bias field B is smooth (low-frequency), typically modeled as a polynomial:

    B(x,y) = 1 + sum_{p=1}^{order} sum_{q=0}^{p} c_{pq} * x^(p-q) * y^q

## Physics

- RF coils have non-uniform transmit/receive profiles
- Different parts of the image receive different flip angles
- Affects ALL tissue in the FOV (not just brain — it's a coil property)
- Air has no magnetization → no bias effect on background
- Effect is smooth and low-frequency — varies over centimeters, not pixels

## Why It's Hard to Correct with U-Nets

- Bias is **multiplicative**, not additive
- A residual-learning U-Net predicts: output = input + residual
- This is inherently **additive** → cannot learn multiplicative correction
- FetEnhNet foundational model: -0.84 dB on bias field (makes it WORSE)
- Correct approach: multiplicative correction branch: `output = input * correction_field(input)`

## Synthetic Generation

### Yair's Legendre Polynomial Method (BCH reference, used in production)
```python
bias_2d = 1.0
for order in 1..3:
    for axis in [y, x]:
        bias_2d += strength * grid[axis]^order
bias_2d = gaussian_filter(bias_2d, sigma=H // order)
bias_2d /= max(bias_2d)
result = image * bias_2d  # with tissue mask
```

Strength calibration (matches MONAI RandBiasField coeff ranges):
- strength=0.3 → brain mult ~0.6-1.0 (mild, like MONAI coeff=(0.21, 0.35))
- strength=0.6 → brain mult ~0.4-1.0 (moderate, like coeff=(0.45, 0.75))
- strength=1.0 → brain mult ~0.1-1.0 (heavy, like coeff=(1.08, 1.80))

### Implementation (src/degradation.py)
- Apply to ALL tissue (not just brain) — physically correct B1 behavior
- Tissue mask: threshold at 3% of p95 intensity + heavy smoothing (sigma=5+)
- Random orientation per sample (flip + rotate the field)
- `gaussian_filter(multiplier, sigma=2)` for natural coil-like transitions
- Catalog presets: bias_low (0.3), bias_med (0.6), bias_high (1.0)

## Correction (N4)
- **N4 bias field correction** (ANTs) — iterative B-spline fitting
- BME-X applies N4 TWICE (undisclosed): full head + skull-stripped brain
- Should NOT be applied before training degradation (removes what we synthesize)

## Used In
- [[fetenh-net]] — training degradation + known enhancement weakness
- [[BME-X-Paper-vs-Code-Audit]] — double N4 correction finding
- [[math-foundations-medical-imaging-dl]] — degradation physics section

## Note
Yair: different bias fields exist in maternal tissue vs fetal brain. But the synthetic field should span the full FOV because real B1 does. Assessment should focus on the brain region.
