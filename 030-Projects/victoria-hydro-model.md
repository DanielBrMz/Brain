---
title: "Victoria's Hydrocephalus Segmentation Model"
type: project
updated: 2026-04-27
tags: [bch, hydrocephalus, segmentation, victoria]
---

# Victoria's Hydrocephalus Segmentation Model

3-class fetal brain MRI segmentation (background / whole brain / ventricles) for hydrocephalus subjects using MONAI UNet.

## People
- **Victoria Hop Cohen** — project lead, data processing, training runs, ventricle masking
- **Daniel Barreras Meraz** — k-fold CV scripts, visualization, comparison tooling, data list
- **Kiho Im** — PI, approved ventriculomegaly expansion (Apr 27)

## Paths
- **Code:** `/neuro/labs/grantlab/research/MRI_processing/victoria.hopcohen/Code/unit_model_hydrocephalus/`
- **Data:** `/neuro/labs/grantlab/research/MRI_processing/victoria.hopcohen/Hydrocephalus/`
- **Python env:** `/neuro/users/victoria.hopcohen/.local/share/mamba/envs/hydrocephalus`
- **Training server:** hanyang (10.26.67.148)

## Data
- 17 hydrocephalus subjects with NeSVoR reconstructions + manual brain & ventricle segmentations
- Data manifest: `data_list.csv` (mrn, image, brain, ventricles columns)
- Input: `recon_to31_nuc.nii` (reconstructed image)
- Labels: `brain_segmentation_final.nii` + `ventricle_segmentation_final.nii`

## Training Runs

| Run | Script | Approach | Result |
|-----|--------|----------|--------|
| 1 | `train.py` | 3D UNet 128^3, seed split | Test Dice 0.893 |
| 2 | `train.py` | 3D UNet, different split | Similar |
| 3 | `train.py` | 3D UNet, third split | Similar |
| 4 | `train_2d_multiview.py` | 2D multiview, 80/10/10 | BROKEN (val Dice -> 0 at ep 16) |
| 5 | `train_2d_multiview.py` | 2D multiview, diff seed | Mean Dice 0.862 |
| **6** | **`train_kfold.py`** | **3D UNet 5-fold CV** | **Mean Dice 0.919 (BEST)** |
| 7 | `train_2d_kfold.py` | 2D axial 5-fold CV | Mean Dice 0.408 |
| 8 | `train_2d_multiview_kfold.py` | 2D multiview 5-fold CV | Mean Dice 0.361 |

## Best Model: 3D UNet 5-Fold CV (Run 6)

Architecture: MONAI 3D UNet (32->64->128->256), batch norm, dropout 0.1
- Loss: DiceFocalLoss (lambda_dice=0.5, lambda_focal=0.5, gamma=2.0)
- Patch size: 128x128x128, sliding window inference (overlap 0.5)
- 200 epochs max per fold, val every 5, patience 50

| Metric | Mean | Std |
|--------|------|-----|
| Brain Dice | 0.915 | 0.016 |
| Ventricle Dice | 0.923 | 0.068 |
| Mean Dice | 0.919 | 0.037 |
| Brain HD95 | 6.175 mm | 1.341 |
| Ventricle HD95 | 4.358 mm | 6.465 |

Checkpoints: `outputs_kfold/fold_0..4/best_model.pth`

## Why 2D Models Failed

2D axial (Dice 0.408) and 2D multiview (0.361) both collapse on ventricle segmentation (Dice 0.215 and 0.140 respectively). The 2D->3D reconstruction from independent slice predictions loses spatial coherence. With only 17 subjects, the 3D approach captures volumetric context that 2D slices cannot.

## Scripts

| Script | Purpose | Author |
|--------|---------|--------|
| `train.py` | 3D UNet single split training | Victoria |
| `train_kfold.py` | 3D UNet 5-fold CV | Victoria |
| `train_2d_singleview.py` | 2D axial single split | Victoria |
| `train_2d_kfold.py` | 2D axial 5-fold CV | Daniel |
| `train_2d_multiview_kfold.py` | 2D multiview 5-fold CV | Daniel |
| `predict.py` | 3D inference on new subjects | Victoria (Daniel fixed affine) |
| `predict_kfold.py` | 3D inference using k-fold best model | Victoria (Daniel fixed affine) |
| `visualize_kfold.py` | K-fold result visualizations (3D) | Daniel |
| `visualize_kfold_2d.py` | K-fold result visualizations (2D) | Victoria |
| `compare_models.py` | Multi-run comparison plots (3 PNGs) | Daniel |
| `plot_training.py` | Single-run training curves | Victoria |

## Next Steps (Apr 27)
1. **Expand dataset** — Kiho approved adding ventriculomegaly subjects
2. **Victoria testing** on ventriculomegaly (2117830, 4333810) — predictions generated Apr 27
3. **Retrain 3D model** with expanded dataset once new subjects are processed
4. **Consider** Spina Bifida subjects (63 in NFS, 0 segs currently)

## Access Notes
- Daniel doesn't have sudo; use `toor` intermediary to switch to `victoria.hopcohen` if needed
- Victoria's env is separate from Daniel's `fetal_pipeline` env
- Shared NFS means code changes on any server are immediately visible on all
