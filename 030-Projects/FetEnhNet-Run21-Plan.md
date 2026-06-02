# FetEnhNet Run21 — Publication Plan

**Created:** 2026-04-05
**Updated:** 2026-04-09
**Status:** 🟡 In Progress — Phase 3 active (evaluation)
**Goal:** Publishable FetEnhNet training with scientifically correct SURE self-supervision

---

## Root Cause Analysis (Run20/Run20b failure)

### What happened
Every time SURE was added it appeared "too aggressive" and was discarded. The real cause was never the hyperparameters — it was a **data pipeline bug**.

### The bug
`UnpairedLowDataset._getitem_impl()` never returned a `noise_map` key:
```python
return {
    'noisy':      _to_tensor(sl),
    'subject_id': r['subject_id'],
    # ← 'noise_map' missing
}
```

The trainer's fallback: `sigma_map = None` → `torch.full_like(y, 0.15)` (hardcoded default).

Real fetal HASTE MRI noise after [0,1] normalization: σ ≈ 0.03–0.07.
Fallback used: σ = 0.15. **Overestimate factor: 3–5×.**

### Why this breaks SURE
The MC-SURE divergence term is scaled by σ²:
```python
div_est = (b * (sigma2 * (fy_pert - fy) / eps)).sum() / numel
```
With σ=0.15 vs true σ≈0.05 → divergence term inflated by **(0.15/0.05)² = 9×**.

Minimizing SURE with overestimated σ pushes the model to **maximize divergence** (become a contracting/over-smoothing map), not toward better enhancement. `val_sup` immediately jumps +0.014 on the first SURE epoch even at near-zero weight, because the gradient *direction* is wrong.

### Smoking gun in the logs
```
Epoch 22 (no SURE): val_sup=0.0737, time=100s   ← stable
Epoch 23 (SURE on): val_sup=0.0880, time=287s   ← instant +0.014 jump
```

### Other contributing factors
- `generate_noise_maps.py` was written for the paired manifest (has `clean_path`), never for the unpaired real stacks (`test_real_backup.csv`)
- `sure_sigma=0.15` class default was never updated from a placeholder value
- No diagnostic logging of actual σ values during training — the bug was invisible

### Additional bugs found during Run21 (2026-04-06)

**Bug 3 — `lambda_sure_target` activates SURE in the supervised run**
`--lambda_sure 0.0` only sets `cfg.lambda_sure` (used by `FetEnhNetLoss`). The trainer warmup scheduler reads `cfg.lambda_sure_target` (default 0.01), which is a separate arg. With default warmup_start=11, SURE started at ep 12 in Run21_sup with weight≈0.000526. Fix: `--low_csv none --lambda_sure_target 0.0` in Run21_sup.

**Bug 4 — `model_fn` used `torch.zeros_like(y)` instead of real `sigma_map`**
SURE's divergence estimator computes the Jacobian of `f(y; sigma_map)`, but the closure passed `torch.zeros` as the noise channel, making it estimate the Jacobian of `f(y; 0)` — a different function. Fix: capture `sigma_map` in closure as `_sigma_ctx`. Symptom: val_sup jumped +0.013 exactly at ep 32 and stayed elevated.

**Bug 5 — `sigma_map` assigned after it was captured in closure (UnboundLocalError)**
In trainer.py, `_sigma_ctx = sigma_map` appeared 13 lines before `sigma_map = unp_batch['noise_map']...`. Python scoping treats it as a local variable → `UnboundLocalError` crash at first SURE epoch. Fix: moved `sigma_map = ...` assignment to before the closure definition.

---

## The Fix (3 code changes)

### Fix 1 — `dataset.py`: Add σ estimation to `UnpairedLowDataset`

In `_getitem_impl`, after loading the slice:
```python
from src.utils.noise_estimator import estimate_background

sigma     = estimate_background(sl)                           # background std
sigma     = float(np.clip(sigma, 0.005, 0.20))               # sanity bounds
noise_map = np.full_like(sl, sigma, dtype=np.float32)

return {
    'noisy':      _to_tensor(sl),
    'noise_map':  _to_tensor(noise_map),   # ← the missing line
    'subject_id': r['subject_id'],
}
```

### Fix 2 — `trainer.py`: Log actual σ for the first SURE batch each epoch

```python
if n_batches == 0 and use_sure and sigma_map is not None:
    self._sure_sigma_log = sigma_map.mean().item()
# Then include in epoch return dict: 'sure_sigma': self._sure_sigma_log
```

### Fix 3 — Validation diagnostic script

`scripts/validate_sure_sigma.py` — runs once before training:
- Loads real LOW slices from `test_real_backup.csv`
- Computes σ via background estimation
- Prints distribution (mean, std, percentiles)
- Flags any slices with σ > 0.15 as outliers
- **Measured result: σ_mean=0.017, range 0.005–0.060** (not 0.03–0.08 as estimated — actual fetal HASTE noise is lower)
- 271/317 records loadable (46 ASD stacks inaccessible); no outliers

### Fix 4 — `model_fn` captures real `sigma_map` (see Bug 4 above)
`_sigma_ctx = sigma_map` captured in closure; `nm = _sigma.detach()` used in forward.
sigma_map assignment moved before closure definition (Fix 5 ordering fix).

### Fix 6 — `model_fn` runs enhancer in eval mode (batchnorm contamination)
During SURE divergence estimation, `model_fn` is called twice: once for `f(y)` and
once for `f(y+εb)`. Running in train mode causes batchnorm to (a) update running stats
from the perturbed input `y+εb` (meaningless) and (b) use different batch statistics for
the two calls, biasing the divergence estimate. Fix: save/restore `enhancer.training`
state inside model_fn, force eval mode for both SURE forward passes. Gradient flow is
unaffected. Applied 2026-04-06 (takes effect on next launch of Run21_sure).

---

## Training Plan

### Checkpoints to use
- **Supervised pre-SURE baseline**: `checkpoints/run20b/epoch_020.pt`
  Last epoch before SURE corrupted Run20b (val_sup=0.0723, clean weights)

### Run21_sup — Supervised-only ablation baseline
| Parameter | Value |
|---|---|
| Resume from | `run20b/epoch_020.pt` |
| Total epochs | 300 (280 more from ep 20) |
| SURE | Disabled (`lambda_sure=0.0`) |
| Batch | 16/GPU |
| GPU | gangnam GPU 0 |
| Log | `logs/run21_sup_gangnam.log` |
| Checkpoint | `checkpoints/run21_sup/` |

Purpose: publication ablation baseline. "Supervised FetEnhNet without SURE."

### Run21_sure — SURE with correct σ
| Parameter | Value |
|---|---|
| Resume from | `run20b/epoch_020.pt` |
| Total epochs | 300 (280 more from ep 20) |
| SURE | Enabled, λ=0.01 |
| SURE warmup | start=30, end=200 (slow ramp) |
| σ source | On-the-fly background estimation |
| Batch | 16/GPU |
| GPU | gangnam GPU 1 |
| Log | `logs/run21_sure_gangnam.log` |
| Checkpoint | `checkpoints/run21_sure/` |

Both runs start from identical weights → clean ablation. Single variable: SURE.

### Dataset sizes (train_v3 — 9.6× larger than train_v2)
| Manifest | Rows | Purpose |
|---|---|---|
| `train_v3.csv` | 12,932 | Synthetic paired training (all degradation types) |
| `val_v3.csv` | 3,233 | Validation pairs |
| `test_real_backup.csv` | 317 | Unpaired real LOW stacks (SURE self-supervision) |

train_v3 vs train_v2: **9.6× more synthetic data** (12,932 vs 1,344 pairs). This uses the full degradation study dataset, covering all 6 degradation types at multiple severity levels.

### Training status (as of 2026-04-09)
| Run | Epoch | val_sup | sure | σ | Time/ep | Status |
|---|---|---|---|---|---|---|
| Run21_sup | 300/300 | 0.0799 final | 0.0 | — | 187s | ✅ Done |
| Run21_sure | 300/300 | ~0.090 final | ~0 (display rounds down) | 0.015–0.022 | 545s | ✅ Done (finished Apr 8) |

Note: Run21_sure epoch counter restarted from 1 on last launch (log overwritten by `tee`). Internal training state resumed from `run20b/epoch_020.pt` (confirmed by val_sup=0.073 at ep 1 — not from scratch). SURE activates at display-ep 32 (warmup_start=30 in 0-indexed internal count).

σ=0.0174 confirmed at first SURE epoch — correct (vs old 0.15 fallback). val_sup jumped +0.0047 at ep 32 activation (borderline — monitoring ep 33+).

### Success criteria during training
- `val_sup` for Run21_sure must remain ≤ Run21_sup throughout
- Logged `sure_sigma` should be ~0.015–0.025 (actual measured range, not 0.03–0.08)
- If `val_sup` climbs > 0.005 above Run21_sup at any point → reduce λ to 0.005

---

## Evaluation Protocol

### Quantitative (synthetic test set)
**Test set**: `test_synthetic.csv` — 174 pairs, 6 degradation types
**Script**: `python scripts/evaluate.py --ckpt <checkpoint>`

Metrics per degradation type:
- PSNR (dB): before degradation, after model, delta
- SSIM: before, after, delta

Expected result (updated after domain-shift analysis 2026-04-06):
- Run21_sup likely wins on synthetic test (trained on synthetic, val on synthetic)
- Run21_sure may be slightly worse on synthetic (domain shift from SURE on real images)
- Both significantly better than degraded input
- **The synthetic test result alone is not the full story — see real evaluation below**

### Quantitative (real LOW stacks — no reference)
**Why this matters**: SURE was trained to minimize risk on real images. The correct
evaluation of SURE benefit is on real images, not the synthetic test set.

**Test set**: `test_real_backup.csv` — 317 real LOW stacks (CHD, ASD, Placenta cohorts)
**Script**: `python scripts/evaluate_real.py --ckpt_sup ... --ckpt_sure ... --gallery`

No-reference metrics (all computed on brain-masked region):
- **Sharpness**: variance of Laplacian — higher = sharper edges
- **Noise**: background std — lower = less noise (same estimator as training)
- **SNR**: mean_brain / std_background
- **CNR**: |mean_brain - mean_bg| / pooled std

Expected result:
- Run21_sure > Run21_sup on SNR and CNR (SURE trained on real noise distribution)
- Run21_sure ≥ Run21_sup on sharpness
- Both > input on all metrics

### Qualitative (visual gallery)
- Run `evaluate_real.py --gallery --n_gallery 6`
- Automatically selects 6 highest-SNR cases balanced across CHD/ASD/Placenta cohorts
- Output: side-by-side PNG: input | Run21_sup | Run21_sure
- Located at: `results/run21_real_eval/gallery/`

### Statistical rigor
- Paired t-test on per-sample PSNR delta (n=174)
- Report mean ± std per degradation type
- Save per-sample CSV for reviewers

---

## Ablation Table (synthetic test, final.pt ep 300)

| Model | Noise PSNR Δ | Blur PSNR Δ | Bias PSNR Δ | Mixed_nb PSNR Δ | Mixed_nbs PSNR Δ | Mean SSIM Δ |
|---|---|---|---|---|---|---|
| Degraded input | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Run21_sup (supervised only) | +2.36 | +5.92 | +2.37 | +4.95 | +1.18 | +0.119 |
| Run21_sure (+ SURE) | +1.78 | +5.03 | +3.16 | +3.32 | +1.37 | +0.123 |

Note: Run21_sup wins on synthetic (expected — supervised model trained/validated on synthetic pairs).
Run21_sure slightly better on bias (+3.16 vs +2.37) and SSIM. The real test is on real images (pending).

---

## Publication Readiness Checklist

- [x] Phase 1: dataset.py fix implemented and validated
- [x] Phase 1: σ diagnostic script run, distribution confirmed (σ_mean=0.017, range 0.005–0.060)
- [x] Phase 1: model_fn closure fixed to use real sigma_map (Bug 4+5)
- [x] Phase 2: Run20 DDP killed, Run20b clean checkpoint saved
- [x] Phase 2: Run21_sup launched and running (ep 152, clean supervised baseline)
- [x] Phase 2: Run21_sure launched and running (ep 32, SURE just activated, σ=0.0174 ✅)
- [x] Phase 2: val_sup of Run21_sure ≤ Run21_sup throughout training — **FAILED**: SURE run overfits more, val_sup higher by ep 300
- [x] Phase 3: evaluate.py run on both models (synthetic, 174 pairs) — completed 2026-04-09
- [ ] Phase 3: evaluate_real.py run on both models (real LOW, 317 stacks, no-reference) — **RUNNING on busan GPU 1** (launched 2026-04-09)
- [ ] Phase 3: Visual gallery generated (evaluate_real.py --gallery) — generating with real eval above
- [ ] Phase 3: Statistical tests computed (paired t-test on synthetic; mean±std on real)
- [x] Ablation table filled in (synthetic, 2026-04-09)
- [ ] Learning curve figures saved (sup, val_sup, sure vs epoch)
- [ ] Methods section: document σ estimation approach

---

## Files Changed
- `src/training/dataset.py` — Fix 1 (UnpairedLowDataset noise_map on-the-fly estimation)
- `src/training/trainer.py` — Fix 2 (σ diagnostic logging), Fix 4 (model_fn uses real sigma_map), Fix 5 (sigma_map assigned before closure), Fix 6 (eval mode in model_fn for batchnorm)
- `scripts/validate_sure_sigma.py` — Fix 3 (new diagnostic script)
- `scripts/evaluate_real.py` — NEW: no-reference evaluation on real LOW stacks with visual gallery
- `scripts/launch_run21_sup_gangnam.sh` — launch script with `--low_csv none --lambda_sure_target 0.0`
- `scripts/launch_run21_sure_gangnam.sh` — launch script with `--lambda_sure_warmup_start 30`

## Evaluation Commands (run after ep 300)
```bash
PROJ=/neuro/labs/grantlab/research/MRI_processing/daniel.barrerasmeraz/projects/fetenh_net
PYTHON=/neuro/users/daniel.barrerasmeraz/.local/share/mamba/envs/bmex_fetal/bin/python3
cd $PROJ

# Synthetic evaluation (both models)
$PYTHON scripts/evaluate.py --ckpt checkpoints/run21_sup/best.pt  --out_csv results/run21_sup_synthetic.csv
$PYTHON scripts/evaluate.py --ckpt checkpoints/run21_sure/best.pt --out_csv results/run21_sure_synthetic.csv

# Real image evaluation (side-by-side comparison + gallery)
$PYTHON scripts/evaluate_real.py \
    --ckpt_sup  checkpoints/run21_sup/best.pt \
    --ckpt_sure checkpoints/run21_sure/best.pt \
    --out_dir   results/run21_real_eval \
    --gallery
```

---

## Overfitting Finding (2026-04-07)

Both runs show classic overfitting to synthetic training pairs:
- val_sup peaks early (ep 12–17) then climbs throughout training
- Train loss keeps falling while val rises → model memorizing training pairs, not generalizing
- **Run21_sure best.pt was saved at ep 17 — before SURE activated at ep 32 — zero SURE benefit in that checkpoint**

Correct checkpoint strategy for SURE runs: select by no-reference real-image metric (SNR/CNR on real stacks), not val_sup.

For Run22: address overfitting before launching (mask alignment fix + regularization).

## Meeting Feedback (2026-04-07)

1. Replace difference map colorbar with cross-subject comparable metric
2. Add alignment figures (cross-software generalizable alignment method)
3. Add formal loss function slide (L_sup and L_SURE, math + plain language)
4. Fix mask alignment before next training attempt
5. Explain overfitting in next presentation — confirm whether gap is domain shift or overfit

## Notes
- Run20b `epoch_020.pt` is the cleanest supervised checkpoint we have
- Run20b `epoch_300.pt` will show SURE *hurts* vs epoch_020 — useful negative result for paper
- SURE is theoretically only valid for additive Gaussian noise; blur/bias pairs have `noise_map=0` so SURE is skipped for them — this is correct behavior, document in methods
