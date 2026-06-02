---
title: "MedLens - HackPrinceton Spring 2026"
type: project
created: 2026-04-17
updated: 2026-04-17
tags: [project, hackathon, healthcare, medical-imaging, AR]
---

# MedLens - HackPrinceton Spring 2026

> AI-powered medical scan explorer with 3D/AR visualization and agentic patient communication.
> April 17-19, 2026. Princeton University.

## Team

- Daniel Barreras (ML/Backend): Segmentation pipeline, GPU inference, agentic orchestration, 3D mesh generation
- Alfredo (Frontend): NiiVue.js viewer, Three.js 3D rendering, WebXR AR, combined UI
- Jake (NLP/Integration): K2 medical reasoning, patient-friendly report generation, ElevenLabs voice, interactive Q&A

## Track

Primary: Best Healthcare Hack (Apple Watch Series 11)
Also competing: Best Overall (PS5), Gemini API (MLH), ElevenLabs (MLH)

## Problem

Patients receive radiology reports they cannot understand. Scans are 2D slices that mean nothing to a non-specialist. There is no tool that lets a patient explore their own scan interactively and get plain-language explanations of what each structure means.

## Solution

Upload any MRI scan. AI segments every structure, reasons through the findings like a radiologist, generates a patient-friendly explanation, and lets you explore your scan in 3D/AR. Tap any structure to hear what it means. Ask follow-up questions and the agent responds pointing to the relevant anatomy.

## Architecture

Input: MRI scan (NIfTI or DICOM)

Step 1 - Segmentation (Daniel, GPUs)
MRI scan goes to GPU cluster via SSH tunnel. Pre-trained segmentation model (TotalSegmentator for full body or FreeSurfer for brain) generates a labeled mask. Each structure gets an ID and anatomical label. Output: segmentation mask + structure labels JSON.

Step 2 - Medical Reasoning (Jake, K2)
Segmentation results + scan metadata feed into K2-Think-v2 from MBZUAI. The model analyzes each segmented structure, flags anything notable, compares to normative expectations. Output: structured medical analysis per structure (JSON). Fallback: Gemini API with medical prompting.

Step 3 - Patient Communication (Jake)
Medical analysis feeds into a patient communication agent. Agent translates medical jargon into plain language with safety disclaimers. Each finding maps to a structure_id so the frontend can highlight it. ElevenLabs generates voice narration. Output: patient-friendly report (text + audio) with structure_id references.

Step 4 - 3D Mesh Generation (Daniel)
Segmentation mask converts to 3D meshes via marching cubes. Each structure becomes a separate mesh with its own color and label. Export as GLB for Three.js. Output: GLB file with labeled meshes.

Step 5 - Interactive Viewer (Alfredo)
NiiVue.js displays the original MRI scan with segmentation overlay (2D slice view). Three.js renders the 3D meshes. Click/tap on any structure to trigger the explanation for that structure_id. Voice plays via ElevenLabs audio. Highlighted structure pulses or changes color when selected.

Step 6 - AR Layer (Alfredo, stretch goal)
WebXR on top of Three.js scene. Patient can view the 3D model in AR through phone browser.

Step 7 - Interactive Q&A Agent (Jake + Daniel)
K2 or Gemini with function calling. Patient asks questions, agent responds with text + highlights structures in 3D. Agent tools: analyze_structure, highlight_in_3d, compare_to_normal, explain_simple, speak.

## Tech Stack

- Backend: Python, FastAPI, SSH tunnel to GPUs
- Segmentation: TotalSegmentator or FreeSurfer (pre-trained)
- Medical NLP: K2-Think-v2 (primary), Gemini API (fallback)
- Voice: ElevenLabs API
- Frontend: HTML/JS, NiiVue.js, Three.js, WebXR
- 3D conversion: scikit-image marching cubes, trimesh for GLB export
- References: [[https://github.com/niivue/niivue]], [[https://niivue.com/docs/]], [[https://github.com/mpsych/boostlet]]

## Timeline

Friday 8PM - Saturday 8AM: Core pipeline (segmentation, NLP, basic viewer)
Saturday 8AM - Saturday 8PM: Integration, 3D interaction, agent Q&A
Saturday 8PM - Sunday 8AM: Polish, AR stretch goal, demo prep

## Risks

- K2 too heavy: fallback to Gemini API
- SSH tunnel unstable: pre-compute segmentation for 3-5 demo scans, cache GLB files
- WebXR fails: 3D viewer without AR still wins
- Medical accuracy concerns: emphasize patient communication tool, not diagnostic. Safety disclaimers.

## Sample Data

Anonymized brain MRI from public datasets (OpenNeuro, IXI). No BCH patient data at hackathon.

## Related

- [[fetenh-net|FetEnhNet - Fetal MRI Enhancement]]
- [[../060-Life/job-search|Job Search Pipeline]]
