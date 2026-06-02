---
title: "BME-X Paper vs Code Compliance Audit"
type: reference
updated: 2026-05-10
tags: [fetenh, bme-x, audit]
---

# BME-X Paper vs Code — Rigorous Claim-by-Claim Audit

**Paper:** "A foundation model for enhancing magnetic resonance images and downstream segmentation, registration and diagnostic tasks"
**Journal:** Nature Biomedical Engineering, Vol 9, April 2025, pp 521-538
**DOI:** https://doi.org/10.1038/s41551-024-01283-7
**Code:** https://github.com/DBC-Lab/Brain_MRI_Enhancement

**Note on code structure:** The repo contains THREE separate codebases:
1. `Training_files/` — Caffe prototxt (the actual training definition)
2. `BME_X/` — PyTorch inference port (what users download and run)
3. Root-level (`trainer.py`, `networks/net.py`) — An unrelated ViT+registration model

This audit compares the paper's Methods section (pages 534-535) against both Caffe and PyTorch code.

---

## 1. ARCHITECTURE

### Claim 1.1: "We selected the DU-Net architecture as our backbone classification model"
**Paper (p534):** "we selected the DU-Net architecture as our backbone classification model. The DU-Net architecture consists of an encoder and a decoder, as well as skip connections."

**Caffe (`Training_files/train.prototxt`):**
- Seg network (layers `Labelconv1a` through `Labelconv6_3`, lines 33-2728): encoder-decoder with skip connections via `Concat` layers (e.g. line 973 `Labelconcat8` concatenates encoder features with deconv output). Confirmed DU-Net-like.

**PyTorch (`BME_X/models/DUNet3D_seg_recon_softmax.py`):**
- Class `DenseUNet3d`, lines 9-739. Same structure: encoder with pooling, decoder with ConvTranspose3d, skip connections via `torch.cat`.

**Verdict: MATCH** — Both implementations follow the DU-Net encoder-decoder with skip connections pattern.

---

### Claim 1.2: "the encoder goes through three groups: dense block + Conv + batch normalization (BN) + rectified linear unit (ReLu), followed by a dense block to connect the encoder and decoder"
**Paper (p534):** Three encoder groups, each containing a dense block followed by Conv+BN+ReLU.

**Caffe:**
- Three `Pooling` layers at lines 473, 859, 934 → three resolution levels → three encoder groups.
- Each group has Conv→BN→Scale→ReLU followed by dense connections (Conv→Dropout→Concat→BN→Scale→ReLU, repeated 3 times).
- Example first dense connection (lines 97-210): `LabelConvolution1`(32ch) → `LabelConvolution2`(8ch) → `LabelDropout1` → `LabelConcat1`(32+8=40ch) → `LabelBatchNorm2` → `LabelScale2` → `LabelReLU2`

**PyTorch (lines 16-175):**
- Same pattern: `conv1`(64ch) → `conv2`(64ch) → `conv3`(16ch) → `dropout3` → `torch.cat` → `bn3`(80ch) → `relu3`
- Three `maxpool` layers for downsampling, three `deconv` for upsampling.

**Verdict: MATCH** on structure. **MISMATCH** on channel counts:
- Caffe initial conv: **32** channels (line 45: `num_output: 32`)
- PyTorch initial conv: **64** channels (line 16: `nn.Conv3d(1, 64, ...)`)
- Caffe dense growth: **8** channels (line 173: `num_output: 8`)
- PyTorch dense growth: **16** channels (line 24: `nn.Conv3d(64, 16, ...)`)

---

### Claim 1.3: "the decoder consists of three Deconv + BN + ReLu + dense block"
**Paper (p534):** Three decoder blocks with transposed convolution.

**Caffe:**
- Three `Deconvolution` layers: `Labeldeconv4` (line 947, k=4, s=2, out=64), `Labeldeconv5` (line 1292), `Labeldeconv6` (line 1954).
- Each followed by Concat (skip connection) → Conv+BN+ReLU → dense block.

**PyTorch:**
- Three `nn.ConvTranspose3d`: `deconv11` (line 72, 128→128, k=4, s=2), `deconv15` (line 92, 352→128), `deconv23` (line 131, 352→64).

**Verdict: MATCH** on structure. Channel dimensions differ between Caffe and PyTorch (same ratio as encoder).

---

### Claim 1.4: "At the end of the network, a Conv automatically generates class probabilities for each voxel"
**Paper (p534):** A Conv layer generates class probabilities.

**Caffe (lines 2619-2679):**
```
Labelconv6_3-Convolution1: Conv(num_output=4)
→ Labelconv6_3-BatchNorm1: BatchNorm
→ Labelconv6_3-Scale1: Scale(bias_term=true)
→ Labelconv6_3-ReLU1: ReLU (in-place)
→ SoftmaxWithLoss (applies softmax internally)
```

**PyTorch (lines 172-174, 541-546):**
```python
self.conv32 = nn.Conv3d(112, 4, kernel_size=3, padding=1)
self.bn32 = nn.BatchNorm3d(4)
self.relu32 = nn.ReLU()
# In forward():
output = self.relu32(conv6_3_BatchNorm1)  # line 543
output_soft = self.softmax(output)         # line 546
```

**Verdict: PARTIAL MISMATCH**
- Paper says "a Conv" generates probabilities. Actual chain is Conv → BN → Scale → ReLU → (then softmax applied by loss or explicitly).
- Paper omits BN, Scale, and ReLU on the classification output.
- ReLU before softmax is scientifically unusual: it clips negative logits to 0, which means the softmax can never assign very low probabilities to any class (since e⁰ = 1 is the minimum input to softmax). This biases the classifier toward uniform predictions for uncertain voxels.

---

### Claim 1.5: "To ensure the compatibility of the concatenated data, we apply a Conv + BN + ReLu block to pre-process both the tissue classification and intensity image data"
**Paper (p534):** Conv+BN+ReLU applied to both streams before concatenation.

**Caffe (lines 2730-2878):**
```
Tissue stream: Labelconv6_4-Convolution1(4→32, k=3) → BatchNorm → Scale → ReLU
Image stream:  conv1a(1→32, k=3) → BatchNorm → Scale → ReLU
→ Concat_recon_pro (32+32=64ch, axis=1)
```
Input to tissue stream: `Labelconv6_3-BatchNorm1` — the **ReLU'd logits** (4 channels, NOT softmax probabilities). The `SoftmaxWithLoss` layer applies softmax internally for the loss but does NOT modify the blob.

**PyTorch (lines 176-183, 545-554):**
```python
# Connection
self.conv1_con = nn.Conv3d(4, 32, kernel_size=3, padding=1)   # tissue
self.conv2_con = nn.Conv3d(1, 32, kernel_size=3, padding=1)   # image
# In forward():
output_soft = self.softmax(output)              # line 546 ← SOFTMAX APPLIED
output_con = self.conv1_con(output_soft)        # line 547 ← feeds probabilities
volMR_con = self.conv2_con(x)                   # line 551 ← feeds original image
concat1_recon = torch.cat([output_bn_con, volMR_bn_con], dim=1)  # line 554
```

**Verdict: MATCH on structure, MISMATCH on data flow**
- Paper says "classification output" is concatenated — ambiguous whether this means logits or probabilities.
- Caffe feeds **ReLU'd logits** (unbounded positive values, 4ch) to connection block.
- PyTorch feeds **softmax probabilities** (values in [0,1], sum to 1, 4ch) to connection block.
- These carry fundamentally different information. Logits preserve confidence magnitude; softmax squashes it.

---

### Claim 1.6: "At the end of the network, a Conv layer is used to generate the high-quality image output"
**Paper (p534):** A Conv layer generates the enhanced image.

**Caffe (lines 5400-5464):**
```
conv6_3-Convolution1: Conv(num_output=1, k=3)
→ conv6_3-BatchNorm1: BatchNorm
→ conv6_3-Scale1: Scale(bias_term=true)
→ conv6_3-ReLU1: ReLU (in-place on conv6_3-BatchNorm1)
→ Reconstructionloss: EuclideanLoss (reads conv6_3-BatchNorm1, which is now ReLU'd)
```

**PyTorch (lines 342-344, 736-739):**
```python
self.conv32_recon = nn.Conv3d(112, 1, kernel_size=3, padding=1)
self.bn32_recon = nn.BatchNorm3d(1)
self.relu32_recon = nn.ReLU()
# In forward():
output_recon = self.relu32_recon(conv6_3_BatchNorm1_recon)  # line 738
return output, output_recon                                  # line 739
```

**Verdict: MISMATCH**
- Paper says "a Conv layer." Code has Conv → BN → Scale → ReLU — four operations.
- The ReLU is present in BOTH Caffe and PyTorch (not a porting bug).
- BN on a 1-channel regression output is scientifically unusual — it normalizes the prediction by batch statistics, preventing the network from learning absolute intensity values.
- ReLU clips negative predictions. Since BN centers to zero-mean, this clips approximately half the distribution early in training.

---

## 2. LOSS FUNCTIONS

### Claim 2.1: "We use a cross-entropy loss L₁ to evaluate errors between the predicted tissue class probability and the expected class"
**Paper (p534, Eq. 2):** L₁ = −(1/N) Σᵢ Σⱼ xⱼ(i) ln x̂ⱼ(i)

**Caffe (lines 2698-2712):**
```
layer {
  name: "loss"
  type: "SoftmaxWithLoss"
  bottom: "Labelconv6_3-BatchNorm1"
  bottom: "dataSeg"
  top: "loss"
  loss_weight: 1
  loss_param { ignore_label: -1 }
  softmax_param { axis: 1 }
  include: { phase: TRAIN }
}
```

**PyTorch (`trainer.py`, lines 94, 187-188):**
```python
loss_func = nn.CrossEntropyLoss(reduction='none')
# ...
loss_matrix = loss_func(logits, in_label.squeeze().long())
loss = torch.mean(torch.mul(loss_matrix, in_weight))
```
Note: `trainer.py` is the ViT model, NOT BME-X training. The PyTorch BME-X inference code has no training loop.

**Verdict: MATCH** — CE loss with weight 1 is present in Caffe. Note: Caffe receives ReLU'd logits → internal softmax → CE, which is mathematically equivalent to standard CE on raw logits (ReLU just clips negative logits to 0 before softmax).

---

### Claim 2.2: "We use a MSE loss L₂ to calculate errors between predicted high-quality images and the corresponding ground truth"
**Paper (p534, Eq. 3):** L₂ = (1/N) Σᵢ (y(i) − ŷ(i))²

**Caffe (lines 5470-5478):**
```
layer {
  name: "Reconstructionloss"
  type: "EuclideanLoss"
  bottom: "conv6_3-BatchNorm1"
  bottom: "dataT1GroundTruth"
  top: "Reconstructionloss"
  loss_weight: 0.0000001
  include: { phase: TRAIN }
}
```

**Verdict: PARTIAL MISMATCH**
- Caffe `EuclideanLoss` computes **(1/2N)** Σ(y−ŷ)², NOT (1/N) as the paper states.
- The factor of 1/2 is standard in Caffe (simplifies the gradient to (y−ŷ)/N instead of 2(y−ŷ)/N).
- Gradients are half of what the paper's formula implies.
- The loss is present and active with weight 10⁻⁷ — confirming joint training.

---

### Claim 2.3: "L = L₁ + λL₂, where λ was set as 10⁻⁷"
**Paper (p534):** Total loss combines CE and MSE.

**Caffe:**
- `loss` (SoftmaxWithLoss): `loss_weight: 1` (line 2704)
- `Reconstructionloss` (EuclideanLoss): `loss_weight: 0.0000001` (line 5476)
- Caffe sums all weighted losses automatically.

**Verdict: MATCH** — Both losses are present with correct weights.

---

## 3. TRAINING CONFIGURATION

### Claim 3.1: "The kernels were initialized with Xavier"
**Paper (p534):** Xavier initialization.

**Caffe (throughout train.prototxt):**
```
weight_filler {
  type: "xavier"
}
```
Present on every convolution layer.

**PyTorch (`BME_X/models/networks.py`, lines 12-16):**
```python
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
```

**Verdict: MATCH for Caffe, MISMATCH for PyTorch** — PyTorch uses Normal(0, 0.02), not Xavier. If the released PyTorch model was retrained, it used different initialization than the paper describes.

---

### Claim 3.2: "We used the stochastic gradient descent strategy for the network optimization"
**Paper (p534):** SGD optimizer.

**Caffe (`solver.prototxt`):**
```
# solver mode: CPU or GPU
# optimizer type: SGD by default.
# type:"Adam"        ← commented out
solver_mode: GPU
```
No explicit `type:` line → defaults to SGD.

**Verdict: MATCH**

---

### Claim 3.3: "The learning rate was set as 0.005 and multiplied by 0.1 after each epoch"
**Paper (p534):** LR=0.005, decay ×0.1 per epoch.

**Caffe (`solver.prototxt`):**
```
base_lr: 0.005
lr_policy: "step"
gamma: 0.1
stepsize: 222
```

**Verdict: MATCH** — base_lr and gamma match exactly. "Each epoch" = each stepsize (222 iterations = 2000 patches / (batch_size 3 × iter_size 3)).

---

### Claim 3.4: "the models were trained for five epochs"
**Paper (p534):** Five epochs of training.

**Caffe (`solver.prototxt`):**
```
stepsize: 222
max_iter: 5000000
```

If "epoch" = 222 iterations (one pass through 2000 patches at effective batch 9):
- 5 epochs = 1,110 iterations
- But `max_iter = 5,000,000` — training continues for 22,522× longer

After 5 step decays (1110 iters), LR = 0.005 × 0.1⁵ = 5×10⁻⁸. The remaining ~5M iterations train at negligible learning rate.

**Verdict: AMBIGUOUS**
- If "epoch" means one LR step: 5 "epochs" of meaningful learning, then ~5M iters of negligible fine-tuning. The paper's claim is technically defensible but misleading.
- If "epoch" means one full data pass: max_iter should be ~1110, not 5,000,000. The training runs 4,500× longer than stated.
- The paper does not mention max_iter or the distinction between meaningful and negligible-LR training.

---

### Claim 3.5: "We randomly extracted 2,000 patches (size: 40 × 40 × 40 for images with a resolution of 0.8 × 0.8 × 0.8 mm³)"
**Paper (p535):** Patch size 40³, resolution 0.8mm.

**Caffe (`solver.prototxt`, comment on line 24):**
```
#In this case, training_data.hdf5 includes 2000 training patches
```
2000 patches: MATCH.

**PyTorch (`BME_X/models/test_model.py`, line 39):**
```python
patchsize = 32
```

**PyTorch (`output.log`, line 45):**
```
patchSize: 32
```

**Testing subject resolution:**
```
Shape: (300, 300, 300)
Voxel size: (0.8, 0.8, 0.8)
```
Resolution 0.8mm: MATCH.

**Verdict: MISMATCH on patch size**
- Paper: 40×40×40 (32mm coverage at 0.8mm)
- Code: 32×32×32 (25.6mm coverage at 0.8mm)
- Cannot verify Caffe training patch size (embedded in HDF5 data, not in prototxt)
- The PyTorch inference code definitively uses 32³

---

### Claim 3.6: "allocating 95% to the training set and 5% to the validation set"
**Paper (p535):** 95/5 train/val split.

**Caffe (`solver.prototxt`):**
```
test_iter: 100
test_interval: 100
```
Test phase exists with 100 iterations every 100 training iterations.

**PyTorch (`trainer.py`, lines 308-341):**
```python
'''
if (epoch + 1) % args.val_every == 0:
    epoch_time = time.time()
    val_avg_acc = val_epoch(...)
    ...
'''
```
Entire validation block is **commented out**.

**Verdict: CANNOT VERIFY** — Caffe has test phase configured but we can't see the actual data split. PyTorch validation is disabled. No early stopping mechanism visible in either implementation.

---

## 4. PREPROCESSING AND DATA

### Claim 4.1: "All pre-processed results by iBEAT V2.0, including intensity inhomogeneity correction, skull stripping and cerebellum removal, passed the quality control"
**Paper (p535):** iBEAT preprocessing applied to generate ground truth.

**`output.log` (inference pipeline, lines 67-81):**
```
Processing file: .../sub-170499_ses-V02_run-1_T2w.nii.gz
Reorient to RAI direction
Bias correction (N4)
Downsample to 1.6*1.6*1.6
Histogram matching
Skull stripping
Upsample to original space
Save brainmask
```

**Verdict: UNDISCLOSED PREPROCESSING**
- The paper describes iBEAT preprocessing for generating **ground truth training data**.
- The output.log reveals that **the same preprocessing (N4, histogram matching, skull stripping) is also applied to input images at inference time**.
- The paper does NOT disclose N4 bias correction or histogram matching as inference preprocessing steps.
- **Histogram matching** to an age-specific template (`Template/template.img`) standardizes intensities across scanners BEFORE the model sees the data. This substantially explains the "harmonization" result that the paper attributes to the model architecture.

---

### Claim 4.2: "tissue classification maps for both training and testing data are automatically predicted by the proposed classification model, rather than by iBEAT V2.0"
**Paper (p534):** The model's own classifier generates tissue maps, not iBEAT.

**Caffe (`train.prototxt`):**
- Training input: `dataSeg` — ground truth tissue labels (from iBEAT) used as CE loss target.
- The classifier learns to reproduce iBEAT labels, then at inference the classifier's own predictions are used.

**PyTorch (`DUNet3D_seg_recon_softmax.py`, lines 545-554):**
- At inference, `output_soft = self.softmax(output)` → feeds into connection block.
- No iBEAT is called at inference time for tissue labels.

**Verdict: MATCH** — Internally consistent. Training uses iBEAT labels as ground truth. Inference uses the model's own predictions. The statement is correct but could be clearer that iBEAT is still the source of supervision during training.

---

## 5. ARCHITECTURAL DISCREPANCIES BETWEEN CAFFE AND PYTORCH

These are not paper claims but critical differences between the two implementations in the same repository.

### 5.1: Channel dimensions

| Layer | Caffe | PyTorch | Ratio |
|-------|-------|---------|-------|
| Initial conv | 1→32 | 1→64 | 2× |
| Dense growth | 8 per layer | 16 per layer | 2× |
| Encoder block 2 | 32→64 | 64→128 | 2× |
| Bottleneck | 64→128 | 128→256 | 2× |
| Total params (seg) | ~2.5M | ~16.4M | **6.6×** |
| Total params (full model) | ~5.5M | ~33M | **6×** |

### 5.2: Connection block input

| | Caffe | PyTorch |
|---|-------|---------|
| Seg output processing | Conv→BN→Scale→ReLU (in-place) | Conv→BN→ReLU→**softmax** |
| What enters connection | 4ch ReLU'd logits (values ≥ 0, unbounded) | 4ch probabilities (values in [0,1], sum=1) |
| Information preserved | Confidence magnitude (high logit = high confidence) | Only relative ratios (magnitude lost) |

### 5.3: Weight initialization

| | Caffe | PyTorch |
|---|-------|---------|
| Conv weights | Xavier: var = 2/(fan_in + fan_out) | Normal(0, 0.02): fixed std regardless of layer size |
| BN weights | Not specified (Caffe default) | Normal(1.0, 0.02) |

---

## 6. SUMMARY

### What the paper gets right:
- Overall architecture (two DU-Nets, connection block, joint training)
- Loss function structure (CE + λ×MSE, λ=10⁻⁷)
- Optimizer and learning rate schedule
- Training data source and tissue label generation
- Resolution (0.8mm)

### What the paper gets wrong or omits:
1. **Patch size**: claims 40³, code uses 32³
2. **MSE formula**: off by factor of 2 from Caffe implementation
3. **"Conv layer" for output**: actual chain is Conv→BN→Scale→ReLU
4. **"Five epochs"**: training runs for 5M iterations (22,500 "epochs")
5. **Inference preprocessing**: N4 bias correction, histogram matching, and skull stripping are applied at inference but not disclosed as model input requirements
6. **Histogram matching explains harmonization**: the paper's key claim about cross-scanner harmonization is substantially attributable to preprocessing, not the model architecture

### What the released PyTorch code gets wrong vs Caffe training:
1. **6.6× more parameters** (different channel counts)
2. **Softmax vs logits** in the connection block
3. **Normal vs Xavier** weight initialization

These discrepancies mean anyone using the released PyTorch code is running a different model than what generated the paper's results.

---

## 7. DOCKER IMAGE AND DOCUMENTATION AUDIT

**Docker image:** `yuesun814/bme-x:v1.0.5`
**Documentation:** https://brain-mri-enhancement.readthedocs.io/en/latest/

### 7.1: Documentation confirms undisclosed preprocessing

The ReadTheDocs documentation lists the pipeline steps as:
1. RAI orientation correction
2. Intensity inhomogeneity correction
3. Skull stripping (via LifespanStrip framework)
4. Image enhancement for brain region
5. Quality Index (QI) calculation

This confirms that N4 bias correction and skull stripping happen BEFORE the model, as discovered in `output.log`. However, the documentation **still does not mention histogram matching** — yet the `Caffe_Templates/README.md` file explicitly states:

> "These template files are used for ***histogram matching*** before testing an image."

And the repo contains **16 age-specific templates** for histogram matching:
```
Template-Fetal-T2w.nii.gz
Template-Month{0,3,6,9,12,18,24}-T1w.nii.gz  (7 files)
Template-Month{0,3,6,9,12,18,24}-T2w.nii.gz  (7 files + fetal)
```

**This means histogram matching IS part of the pipeline but is hidden from the user-facing documentation.** It's disclosed only in the Caffe_Templates README inside the source repo, not in the official docs or the paper.

### 7.2: Documentation does not mention age requirements

The documentation shows no `--age` argument. Yet `output.log` (line 85) shows:
```
Skipping BME-X! Age information is required!
```

The Docker pipeline reads age from `participants.tsv` in the BIDS dataset. If age is missing, enhancement is SKIPPED entirely — the output is only the preprocessed (N4 + skull-stripped) image, not the enhanced one. The documentation does not warn users about this requirement.

### 7.3: The Docker pipeline adds a Quality Index (QI)

The documentation mentions a "Quality Index (QI)" value between 0 and 1. This is NOT mentioned in the paper. It appears to be a post-hoc metric added to the output JSON sidecars.

### 7.4: Model checkpoint availability

Two Dropbox links provide pre-trained models:
- `Model/` → one link (likely Caffe models)
- `BME_X/checkpoints/` → another link (likely PyTorch weights)

Neither link is archived or versioned. If Dropbox links break, the models are lost.

### 7.5: Template files confirm age-specific models

The template filenames confirm **8 age groups for T1w** (0, 3, 6, 9, 12, 18, 24+ months) and **9 for T2w** (fetal + 0, 3, 6, 9, 12, 18, 24+ months). This matches the paper's claim of training "enhancement models at different developmental stages."

Notably, T2w has a **fetal template** but T1w does not — consistent with the paper's use of T2w for fetal imaging (fetal MRI is typically T2-weighted due to fluid-filled structures).

---

## 8. COMPLETE DISCREPANCY MATRIX

| # | Category | Paper Claim | Caffe Code | PyTorch Code | Docker/Docs | Severity |
|---|----------|------------|------------|-------------|-------------|----------|
| 1 | Patch size | 40³ | In HDF5 (unverifiable) | GitHub: 32³, **Container: 40³** | Not mentioned | **RESOLVED: Container matches paper. GitHub repo is outdated.** |
| 2 | MSE formula | (1/N)Σ(y-ŷ)² | (1/2N)Σ(y-ŷ)² | N/A (no training) | N/A | MEDIUM |
| 3 | Recon output | "a Conv layer" | Conv+BN+Scale+ReLU | Conv+BN+ReLU | N/A | MEDIUM |
| 4 | Epochs | 5 | max_iter=5M (22,500 epochs) | N/A | N/A | HIGH |
| 5 | Channel count | Not specified | 32 init, 8 growth | 64 init, 16 growth | N/A | HIGH |
| 6 | Connection input | "classification output" | ReLU'd logits | softmax probs | N/A | HIGH |
| 7 | Weight init | Xavier | Xavier | Normal(0,0.02) | N/A | MEDIUM |
| 8 | Preprocessing | iBEAT for GT only | N/A | N/A | N4+skull strip at inference | HIGH |
| 9 | Histogram matching | Not mentioned | Templates in repo | Templates in repo | Hidden in README only | VERY HIGH |
| 10 | Age requirement | Not mentioned as hard req | N/A | N/A | Silently skips if missing | HIGH |
| 11 | Harmonization | "emergent from architecture" | N/A | N/A | Histogram matching does it | VERY HIGH |

---

## 9. DOCKER CONTAINER CODE — THE DEFINITIVE IMPLEMENTATION

The Docker container (`yuesun814/bme-x:v1.0.5`, 6.27GB) contains the ACTUAL production code. Key files extracted and analyzed:

### 9.1: The Real Pipeline (`/BME-X.py` — main entry point)

**Step 1: Intensity rescaling** — percentile clipping [0.001, 99.999] then `IntensityWindowing` to [0, 1000]
**Step 2: N4 bias correction** — `N4BiasFieldCorrectionImageFilter` with [50, 50, 30, 20] iterations
**Step 3: Downsample to 1.6mm** — for skull stripping only
**Step 4: Histogram match** to `/Template/template.hdr` — 1024 levels, 7 match points
**Step 5: Skull stripping** — `sliding_window_inference` with DUNet3D (seg-only, 32ch init, ROI 64³, overlap 0.85)
  - Input normalized by `/10000.0`
  - Tissue channels merged: brain = GM + WM, non-brain = 1 - brain
  - Binary opening (kernel 3), largest connected component, hole filling
**Step 6: BME-X enhancement** — calls `BMEX()` from `BME_X_enhanced.py`

### 9.2: The Real Enhancement Pipeline (`/BME_X/BME_X_enhanced.py`)

**CRITICAL FINDINGS from container code:**

**Patch size is 40×40×40** (line: `d1 = 40, d2 = 40, d3 = 40`). Paper is CORRECT. GitHub `test_model.py` (patchsize=32) is outdated/wrong.

**Stride is 18** (line: `step1 = 18, step2 = 18, step3 = 18`). NOT stride 5 as in GitHub `test_model.py`.

**Margin is 5** — only the center 30×30×30 of each 40³ patch is used. Edge voxels are discarded to avoid boundary artifacts.

**N4 applied TWICE** — once on the full head image (step 2), then again on the skull-stripped brain before enhancement (line: `corrector.Execute(filenameT1)`). Paper mentions N4 only as iBEAT preprocessing for ground truth.

**Resolution: 0.8mm** for postnatal, **0.75mm for fetal** (line: `new_spacing = (0.75, 0.75, 0.75) if age_number == 'fetal' else (0.8, 0.8, 0.8)`). Paper says 0.8mm only.

**Histogram matching to age-specific template** — uses `/BME_X/Templates/Template-Month{N}-{T1w|T2w}.nii.gz`. 1024 levels, 7 match points.

**REVERSE histogram matching at the end** — the enhanced brain is histogram-matched BACK to the original input distribution before compositing with skull:
```python
matched_matRecon = hist_match(result_nii, filenameT1_forhist)
```
This means the model's internal output is in template space, but the final output is mapped back to the original scanner's intensity characteristics. The "harmonization" only exists internally.

**Skull compositing** — final image = original_skull × (1-brain_mask) + enhanced_brain × brain_mask

**Quality Index** — QI = TCT_original / TCT_enhanced (ratio, not difference). Higher = worse original quality. Written to `{stem}-QI.txt`.

### 9.3: Age-to-Model Mapping (from container code)

```python
age >= 21 months  → Month24 model
15-20 months      → Month18 model
10-14 months      → Month12 model
7-9 months        → Month9 model
5-6 months        → Month6 model
2-4 months        → Month3 model
0-1 months        → Month0 model
< 0 (negative GA) → Fetal model
```

### 9.4: Three DUNet3D Variants in Container

| File | Init ch | Growth | Recon? | Purpose | Model file |
|------|---------|--------|--------|---------|------------|
| `/DUNet3D.py` | 32 | 8 | No (seg only) | Skull stripping | `T1T2w-model.pt` (33MB) |
| `/BME_X/models/DUNet3D_seg_recon_softmax.py` | 64 | 16 | Yes (seg+recon) | Enhancement | `BMEX-Month*-T*-model.pt` (132MB each) |
| `/BME_X/models/DenseUNet3d.py` | 64 | 16 | No (mostly commented out) | Unused/debug | — |

The skull-stripping DUNet3D (32ch/8 growth) **matches the Caffe prototxt exactly**. The enhancement DUNet3D (64ch/16 growth) is the **larger PyTorch-specific architecture** with ~6× more parameters.

### 9.5: 17 Pre-trained Models in Container

- 1 skull-stripping model: `T1T2w-model.pt` (33MB)
- 16 enhancement models: `BMEX-{Fetal,Month0-24}-{T1,T2}-model.pt` (132MB each)
- Total: ~2.1GB of model weights

### 9.6: Updated Discrepancy Matrix (with container evidence)

| # | Paper | GitHub repo | Docker container | Verdict |
|---|-------|-------------|-----------------|---------|
| Patch size | 40³ | 32³ | **40³** | Paper=Container. GitHub wrong. |
| Stride | Not stated | 5 | **18** | Container is definitive |
| Margin | Not stated | None | **5 (use center 30³)** | Container adds edge trimming |
| Resolution | 0.8mm | 0.8mm | **0.8mm postnatal, 0.75mm fetal** | Fetal difference undisclosed |
| N4 correction | On GT only | On input | **Twice: full head + skull-stripped** | Double N4 undisclosed |
| Histogram match | Not mentioned | Templates in repo | **Both directions: input→template, output→original** | Round-trip matching undisclosed |
| Channel counts | Not specified | 64/16 (seg+recon) | **32/8 (skull strip), 64/16 (enhancement)** | Two different architectures |
| Connection input | "classification output" | softmax probs | softmax probs (same as GitHub) | Caffe used logits |
