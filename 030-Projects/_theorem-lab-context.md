---
title: "Theorem Lab — Quick Context"
type: context
updated: 2026-04-25
tags: [theorem-lab, purdue, context]
---

# Theorem Lab — Quick Context

> One-read context file for Claude. Load this first for any GM-SGM / Purdue work.

## What is it
Paper + code on GM-SGM (Geometric Median Switching Gradient Method) — makes SGM robust to adversarial gradient corruption by replacing mean aggregation with geometric median. Collaboration with Chema (José María Soto) at Purdue.

## Repo
https://github.com/Gorchon/theorem-lab — Python/PyTorch, Fashion-MNIST experiments, convex quadratic demos, LaTeX paper.

## Paper Status (updated 2026-04-28)

**MAJOR REFRAME:** Paper pivoting from "GM applied to SGM" to "Switching Corruption Amplification (SCA) as a new failure mode in constrained optimization."

**New title:** "Switching Corruption Amplification in Constrained Optimization: Why Robust Aggregation Alone Is Not Enough"

**Written (April 28):**
- New abstract (SCA-centered)
- New introduction (`introduction_rewrite.tex`) — rewritten around SCA
- New Section 3: SCA theory (`sca_section.tex`) — Theorem A (Impossibility), Theorem B (Separation)
- Sections 2, 4-6: original (Background, GM-SGM, Convex Validation, mNPC, Block+Memory)
- Section 7: Convergence Analysis (2 theorems + corollary) — `convergence_section.tex`
- Section 8: Baselines results template (`baselines_results_section.tex`)
- Section 9: Related Work (updated with 2025 citations) — `related_work_discussion.tex`
- Section 10: Discussion + Conclusion

**Experiments:**
- Fashion-MNIST 7-method baselines: RUNNING on local RTX 4060 (~55 min total)
- CIFAR-10 code updated with test accuracy (ready to run after Fashion-MNIST)
- Ablation corruption sweep: code written (`ablation_corruption_fraction.py`)
- SCA validation experiment: code written (`switching_accuracy_experiment.py`) — tracks gradient accuracy vs switching decision accuracy to validate Theorem B

**Experiment results (Apr 28, 3:50 AM):**
TRUE SGM switching experiment COMPLETE. Results validate ALL theorems:
- Krum+mean_feas: GradCos=1.000, SwAcc=0.005, 0/9 (Theorem B proven: perfect grads, zero switching)
- GM-SGM full: SwAcc=0.754, Acc=84%, works (joint robustification)
- GM-SGM WITHOUT median test: SwAcc=0.003, 0/9 (median test is essential)
- Krum+median_feas: SwAcc=0.727, 5/9 (any robust agg + median test works)
- Results at FashionMnistExperiments/results_switching/

Penalty-based baselines also done (results_baselines/) but these are secondary.

**LaTeX compiles** to PDF. Paper structure complete.

**Next session TODO:**
1. Fill LaTeX tables with actual experiment numbers
2. Run CIFAR-10 with TRUE switching (need to write cifar10_switching.py)
3. Run ablation corruption fraction sweep
4. Final PDF assembly + proofread
5. Share with Chema

**Full execution plan:** `~/Documents/Projects/theorem-lab/PLAN.md`
**Target venue:** ICML 2026 or NeurIPS 2026

## Key Files
- `LatexBackUp/main.txt` — full paper LaTeX source
- `FashionMnistExperiments/fashion_mnpc_gm_sgm_experiment.py` — main experiment
- `FashionMnistExperiments/fashion_mnpc_gm_sgm_blockmem.py` — block + memory variant
- `GM-SGM_vs_SGM/gm_vs_sgm.py` — convex quadratic comparison
- `Drafts/draft.txt` — clean 3-mode training script

## Core Math
- SGM: switch between ∇f and ∇g based on feasibility g(w) ≤ ε
- GM-SGM: same switching but aggregate gradients via geometric median instead of mean
- Breakdown point 1/2 — tolerates 50% adversarial corruption
- Block selection (BGMD): restrict GM to top-k coordinates, O(bd) → O(bk)
- Memory: accumulate discarded coordinates, reinject next iteration

## What Needs Doing
1. Convergence theory / formal guarantees
2. CIFAR-10 experiments (scale beyond Fashion-MNIST)
3. Baselines: Krum, trimmed mean, centered clipping, coordinate-wise median
4. Discussion + related work section
5. Final conclusion
6. Repo cleanup for submission

## Detailed Notes
- [[theorem-lab-gmsgm]] — full project docs, repo structure, algorithms, literature
