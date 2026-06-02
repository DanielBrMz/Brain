---
title: "Research Engineer — BCH/HMS FNNDSC (Grant Lab)"
type: role
status: active
created: 2026-03-20
updated: 2026-03-20
tags: [role, bch, hms, fnndsc, research, mri, fetal, deep-learning, grant-lab]
---

# Research Engineer — BCH/HMS FNNDSC (Grant Lab)

## Overview

- **Institution:** Boston Children's Hospital (BCH) + Harvard Medical School (HMS)
- **Lab:** FNNDSC — Fetal-Neonatal Neuroimaging & Developmental Science Center
- **Group:** Grant Lab
- **Title:** Fetal MRI Research Engineer
- **Supervisor:** Kiho Im
- **Username:** `daniel.barrerasmeraz`

## Focus

Deep learning methods for fetal brain MRI — specifically enhancing raw HASTE stack images (2D slices, NOT reconstructed volumes). Rician noise, physics-based degradations per-slice.

## Main Project

**[[../030-Projects/fetenh-net|FetEnhNet]]** — Tissue-Conditioned Deep Learning Enhancement of Fetal MRI Raw Stacks

- Stage 1: TissueClassifier (3-level U-Net → 4-class soft tissue maps)
- Stage 2: EnhancementNet (4-level ResU-Net + FiLM conditioning)
- Current best: run11 — mean +4.48 dB PSNR, +0.161 SSIM improvement
- Symposium abstract submitted March 18, 2026 (FNNDSC Spring 2026)
- 3-minute talk + 5 slides due April 3, 2026

## Other Projects

- **NeuroNScope** — see memory file for details
- **Sparse SLM (Puentes collaboration)** — ActivSparse-SLM proposal

## Infrastructure

| Server | GPUs | Role |
|--------|------|------|
| sejong (10.26.66.103) | 3× RTX A5000 (72GB) | Primary workstation |
| busan (10.26.66.171) | 3× RTX A5000 (72GB) | Compute, VPN peer |
| hanyang (10.26.67.148) | 2× RTX A5000 (48GB) | K8s node, recon jobs |
| gangnam (10.72.8.45) | 2× RTX A5000 (48GB) | K8s master, CHD recon |

All servers share NFS: `/neuro/users/` and `/neuro/labs/`

## Working Directory

```
/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/
├── projects/
│   └── fetenh_net/          # Main project
├── data/                    # Datasets
├── scripts/                 # Utility scripts
├── experiments/             # Experiment configs and results
└── CLAUDE.md               # Project-specific Claude instructions
```

## Environments

| Name | Purpose | Python | Key Packages |
|------|---------|--------|-------------|
| bmex_fetal | FetEnhNet training | 3.10 | PyTorch 1.13.1 |
| analysis | Figures/data analysis | — | pandas, matplotlib, nibabel |
| fetalsynthseg | Synth segmentation | — | PyTorch 2.1.2 |
| iguane | TensorFlow models | — | TF 2.15 |

**Pipeline env (shared):**
```bash
eval "$(micromamba shell hook --shell bash)"
micromamba activate /neuro/labs/grantlab/research/MRI_processing/environment
```

## Key Contacts

| Person | Role |
|--------|------|
| Kiho Im | Supervisor |
| Hyeokjin Kwon | Collaborator (tissue labels discussion) |
| Victoria Hop-Cohen | MRI processing team |
| Quentin | MRI processing team |

## Related Notes

- [[../030-Projects/fetenh-net|FetEnhNet Project]]
- [[../020-Infrastructure/servers-index|Server Inventory]]
- [[../020-Infrastructure/wireguard|WireGuard VPN (BCH)]]
- [[../060-Life/daniel-profile|Daniel Profile]]
- [[../060-Life/career-timeline|Career Timeline]]
- [[../030-Projects/BCH-Meeting-Minutes|Meeting Minutes]]
