---
title: "Support -- Personal Toolkit"
type: project
created: 2026-03-22
updated: 2026-03-22
tags: [project, personal, tools, automation, neuroimaging]
---

# Support -- Personal Toolkit

> Multi-domain utility project: audio transcription, media processing, web scraping, CI/CD analysis, neuroimaging research support, and shell utilities.

## Overview

| Attribute | Value |
|-----------|-------|
| Path | `~/Documents/Projects/Support` |
| Environment | Conda (via `environment.yml`) |
| Python | 3.12 |
| GPU | CUDA 12.8 (RTX 4060) |

## Setup

```bash
conda env create -f environment.yml
conda activate support
```

## Directory Structure

```
Support/
+-- environment.yml           # Conda env (Python 3.12, CUDA 12.8, ~40 deps)
+-- analysis/                 # Data analysis & CI/CD diagnostics
|   +-- cypress/              # GitHub Actions Cypress failure analysis
|   +-- boston/                # Boston energy usage geospatial mapping
|   +-- misc/                 # Survey analysis, standby art
+-- Andrea/                   # Neuroimaging research (fetal MRI)
|   +-- Scripts/
|       +-- FeTA_challenge/   # Fetal brain biometry (BIP, VSD, HC)
|       +-- dHCP_SP/          # Diffusion MRI processing pipeline
|       +-- phantoms/         # Phantom registration
|       +-- segmentation/     # Ventricle segmentation
+-- audio/                    # Audio format conversion (ffmpeg)
+-- transcription/            # Whisper-based audio transcription
+-- scraping/                 # Web scraping
|   +-- forms/                # Google Forms automation (Selenium)
|   +-- blog/                 # Blogspot blog scraper
+-- shell/                    # Utility scripts
|   +-- fetch_models.sh       # MRI Singularity container transfer
|   +-- populate_db.sh        # Database initialization
|   +-- commit_files.sh       # Git commit with custom dates
+-- media/                    # Audio/video storage (raw/, processed)
+-- docs/                     # Documentation and context files
+-- .claude/                  # Claude Code project config
```

## Key Components

### analysis/cypress/cypress_analyzer.py
Analyzes failed GitHub Actions Cypress E2E test runs for Sidepocket. Connects to GitHub API, extracts failed endpoint URLs from logs, groups by path, generates JSON/CSV failure reports with failure rate percentages.

### analysis/boston/boston_data.py
Interactive Folium maps of Boston building energy/water consumption. Multiple visualization layers (circles, heatmap, clustered markers), ZIP code geocoding, cost analysis.

### transcription/transcribe_audio.py
GPU-accelerated Whisper transcription (faster-whisper with CUDA, fallback to openai-whisper). Supports large-v3 model, auto language detection, SRT subtitle export, punctuation restoration via HuggingFace transformer. Primary workflow: YouTube -> yt-dlp -> convert -> transcribe.

### audio/audio_converter.py
FFmpeg-based audio format conversion (mp3, ogg, wav, flac). Batch directory processing with configurable bitrate.

### Andrea/ -- Neuroimaging Research
Collaboration with Andrea on fetal MRI analysis:
- **FeTA challenge:** Fetal brain biometry measurements (BIP, OFD, VSD, HC) from segmentation masks using nibabel + FSL
- **dHCP_SP:** Diffusion tensor imaging pipeline (DTI fitting, dMRI-to-T2w registration, tissue decomposition, constrained spherical deconvolution) using FSL + MRtrix3 + Apptainer containers
- **Phantoms:** Phantom registration and alignment to templates

### scraping/forms/forms-scrapping.py
Google Forms multi-page question extractor using Selenium + Firefox with anti-detection. Handles text inputs, multiple choice, file uploads.

### scraping/blog/scrape_blog_local.py
Blogspot blog scraper with Spanish date parsing, archive page discovery, session-based requests.

### shell/fetch_models.sh
Transfers MRI Singularity containers from remote server via rsync. Manages: fetal CP/CSF segmentation, brain mask extraction, QA models, NeSVoR reconstruction, parcellation. Requires 40GB+ disk space.

## Key Dependencies

| Category | Packages |
|----------|----------|
| ML/Audio | openai-whisper, faster-whisper, torch (CUDA 12.8), torchaudio |
| Neuroimaging | nibabel, FSL (AUR), FreeSurfer (AUR), MRtrix3, Apptainer |
| Scraping | selenium, beautifulsoup4, requests, yt-dlp |
| Data | pandas, numpy, scipy, matplotlib, scikit-learn, scikit-image |
| Geospatial | folium |
| Google APIs | google-api-python-client, google-auth-oauthlib |
| Documents | python-docx |

## Typical Workflows

1. **Transcription pipeline:** YouTube URL -> yt-dlp -> audio_converter -> transcribe_audio (Whisper + punctuation)
2. **CI/CD monitoring:** GitHub Actions runs -> cypress_analyzer -> failure reports (JSON/CSV)
3. **Neuroimaging:** Fetal MRI -> biometry extraction / DTI fitting / parcellation (Singularity containers)
4. **Web scraping:** Google Form/Blog URL -> Selenium/BS4 -> structured output

## Related

- [[projects-index|Projects Index]]
- [[../010-System/packages-aur|AUR Packages]] -- freesurfer-bin, fsl installed
- [[../040-Roles/research-engineer-bch|BCH Role]] -- Andrea collaboration context
- [[../060-Life/daniel-profile|Profile]]
