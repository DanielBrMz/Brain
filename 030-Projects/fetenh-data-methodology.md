---
title: "FetEnhNet -- Qualitative-First Data Preparation Methodology"
type: methodology
status: active
created: 2026-04-14
updated: 2026-04-14
tags: [fetenh-net, methodology, data-preparation, quality-control]
related: [[fetenh-data-knowledge-graph]], [[fetenh-net]]
---

# FetEnhNet -- Qualitative-First Data Preparation

> Human-supervised, visual-first approach to building the tissue conditioning dataset. Quantitative metrics document and confirm what the researcher has visually approved.

---

## Core principle

**The researcher decides. Automation assists.**

Every subject in the final training dataset has been:
1. Selected by the researcher from the QA spreadsheet
2. Visually inspected at the raw data level
3. Visually confirmed at the alignment/overlay level
4. Quantitatively documented (Dice, coverage metrics)

No subject enters the dataset based on a metric alone.

## Why qualitative first

Quantitative methods (Dice, MI, PSNR) can report high scores on wrong results:
- Dice 0.90 with left-right flipped anatomy (sagittal symmetry)
- MI convergence to local minimum (brain in wrong position but partial overlap)
- High overlap but wrong tissue assigned to wrong region

A 2-second visual check catches all of these. A metric cannot.

Conversely, a metric of 0.82 on a visually correct alignment is fine for conditioning. The metric reflects resolution loss (0.5mm atlas projected to 3mm raw slices), not misalignment.

The human is better at global assessment (is this right?). The computer is better at local measurement (by how much?). Use each for what it does best.

## Workflow

```
QA spreadsheet + CanonicalData
       |
       v
[A] Human selects subjects, assigns cohorts
       |
       v
[B] Human verifies raw data quality
       |
       v
[C] Automation proposes alignment
       |
       v
[D] Human confirms or corrects alignment visually
       |
       v
[E] Automation computes Dice (documents the decision)
       |
       v
[F] Manifest generated (only human-approved entries)
```

Each step is documented: who approved, when, what the Dice was.

## What this means for tooling

Tools should present information for human decision, not make decisions:
- Show the overlay, don't just report the Dice
- Show the raw data quality, don't just filter by a threshold
- Show cohort distributions, don't just count subjects
- Log human approvals with timestamps, don't auto-approve

## What this means for the paper

We can state: "Each subject's tissue label projection was visually verified by the researcher against the raw HASTE anatomy. Subjects with anatomically incorrect overlays were either corrected via interactive alignment or excluded."

This is stronger than: "We applied automated registration and filtered by Dice >= 0.85."

## Related

- [[fetenh-data-knowledge-graph]] -- Complete data map
- [[fetenh-label-projection-pipeline]] -- Technical registration pipeline
- [[medical-image-registration]] -- Why automated methods fail on some subjects
