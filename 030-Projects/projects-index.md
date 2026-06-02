---
title: "Projects — Index"
type: moc
created: 2026-03-19
updated: 2026-03-22
tags: [projects, index, moc]
---

# Projects — Index

## Active

### Sidepocket Inc (Tech Lead)

| Project | Stack | Status | Note |
|---------|-------|--------|------|
| [[sidepocket-infrastructure\|Sidepocket Infrastructure]] | AWS, Docker, ECS, 8 microservices | Active | Full engineering context — start here |
| [[sidepocket-engineering\|Sidepocket Engineering Notes]] | NAV, Redis, S3 Parquet, debugging | Active | Formulas, recipes, S3 schema |
| [[sidepocket-team\|Sidepocket Team]] | People | Active | Team roster, Slack IDs, roles |
| [[sidepocket-webapp\|Sidepocket Webapp]] | Next.js 15, Bun, tRPC | Active | PWA frontend (local dev) |
| [[sidepocket-backend\|Sidepocket Backend (sp-app)]] | Flask, GraphQL, PostgreSQL | Active | Local clone of app-backend |
| [[sidepocket-codebase\|Sidepocket Codebase]] | All 9 services detailed | Active | Service-by-service code documentation |

### BCH / HMS Research (Grant Lab, FNNDSC)

| Project | Stack | Status | Note |
|---------|-------|--------|------|
| [[fetenh-net\|FetEnhNet]] | PyTorch, ResU-Net + FiLM | Active | Fetal MRI enhancement — run11 is current best (+4.48 dB) |
| [[fetenh-net-codebase\|FetEnhNet Codebase]] | Model architecture + training code | Active | Detailed code documentation |
| [[neuronscope\|NeuronScope]] | FastAPI, PyTorch, WebSocket | Active | Activation sparsity visualization — v2 complete |
| [[sparse-slm\|ActivSparse-SLM]] | SLTrain, ReLU, MoE, Wanda | Complete | Puentes collab — 125M sparse LLM, 50% pruning +0.3% PPL |

### BCH / HMS Shared Tools

| Project | Stack | Status | Note |
|---------|-------|--------|------|
| [[bch-seg-pipeline\|Segmentation Pipeline]] | Python, Apptainer, FSL, FreeSurfer | Active | 8-step fetal brain MRI processing pipeline |
| [[bch-surface-pipeline\|Surface Pipeline]] | Python, FreeSurfer | Active | Cortical surface extraction from manual segmentations |

### Other

| Project | Stack | Status | Note |
|---------|-------|--------|------|
| [[sidepocket-endorser-cms\|sp-endorser-cms]] | Next.js 15, Payload CMS 3.9, PostgreSQL, S3 | Active | Endorser content management system |
| [[sp-backend-api-testing\|sp-backend-api-testing]] | Cypress 13.13.2, JavaScript | Active | E2E API testing suite |
| [[hackharvard2025\|HackHarvard 2025]] | Flask, React, Mapbox, Gemini AI | Completed | "Boston Daddy" — AI smart city platform |
| [[support-project\|Support Toolkit]] | Python 3.12, Micromamba | Active | Personal daily-use scripts and tools |

## Completed / Archive Candidates

| Project | Stack | Status | Note |
|---------|-------|--------|------|
| [[nextblog\|nextblog]] | Next.js 16, Prisma | Completed | Blog platform — archive when confirmed |

---

## Project Locations

```
~/Documents/Projects/Personal/
├── webapp/                    # Sidepocket frontend
├── sp-app/                    # Sidepocket backend
├── nextblog/                  # Blog platform
├── sp-backend-api-testing/    # Newman API test harness
└── ../Support/               # Personal toolkit (audio, media, scraping, etc.)

~/Documents/Projects/
└── HackHarvard2025/           # Hackathon project (not under Personal/)

# BCH/HMS (via SSH — NFS shared across sejong/busan/hanyang/gangnam)
/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/
├── projects/fetenh_net/       # FetEnhNet — main research project
├── projects/activ_sparse_slm/ # ActivSparse-SLM (completed)
├── data/                      # MRI datasets (CHD_TD, ASD, VM, Normative, Placenta, etc.)
├── experiments/               # Degradation study, training data, manifests
├── scripts/                   # auto_project_after_recon.sh, disk_audit.sh
├── papers/                    # Literature reviews + PDFs
└── logs/                      # Reconstruction logs per server

# Shared tools
/neuro/labs/grantlab/research/MRI_processing/tools/
├── seg_pipeline/              # Segmentation pipeline (8 steps)
├── surface_procesing_pipeline/ # Surface extraction (6 steps)
├── BOUNTI_segmentation_*.sif  # Deep learning segmentation container
└── utils/                     # Shared utilities
```

---

## Reference

- [[github-repos|GitHub Repos (DanielBrMz)]] — all 44 repos indexed
- [[local-project-file-structures|Local Project File Structures]] — complete file-level documentation of all local projects (audited 2026-03-22)

## Templates

- [[_template-project|Project Template]] — use when creating a new project note
