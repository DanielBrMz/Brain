---
title: "Hausdorff Distance (HD95)"
type: knowledge
updated: 2026-04-27
tags: [math, metric, segmentation, medical-imaging]
---

# Hausdorff Distance (HD95)

## Definition

The Hausdorff distance measures the worst-case boundary disagreement between two sets:

    HD(A, B) = max( max_a min_b d(a,b),  max_b min_a d(a,b) )

This is the maximum of all minimum point-to-point distances. It finds the single worst boundary error.

## 95th Percentile Variant

HD is sensitive to outliers (one bad voxel dominates). HD95 uses the 95th percentile instead:

    HD95(A, B) = P95( {min_b d(a,b) for all a} union {min_a d(a,b) for all b} )

Reported in millimeters (using voxel spacing from the NIfTI affine).

## Interpretation

- HD95 = 2mm: boundaries differ by at most 2mm (at 95th percentile) — excellent
- HD95 = 6mm: moderate boundary errors — acceptable for brain, concerning for ventricles
- HD95 > 20mm: major segmentation failures

## Hydro Model Results

| Model | Brain HD95 | Ventricle HD95 |
|-------|-----------|----------------|
| 3D UNet | 6.18 mm | 4.36 mm |
| 2D Axial | 14.21 mm | 37.69 mm |
| 2D Multiview | 16.74 mm | 57.47 mm |

The 2D models have catastrophic boundary errors, especially for ventricles.

## Why Report HD95 alongside Dice?

A model can have high Dice (correct volume) but poor HD95 (bad boundaries):
- Dice = volumetric overlap, dominated by bulk agreement
- HD95 = boundary precision, catches local failures
- Clinically, boundary accuracy matters for surgical planning and volumetric analysis

## Used In
- [[victoria-hydro-model]] — per-case evaluation metric
- [[math-foundations-medical-imaging-dl]] — full syllabus

## Reference
Huttenlocher et al. "Comparing Images Using the Hausdorff Distance", IEEE TPAMI 1993.
