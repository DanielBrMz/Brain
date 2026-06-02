---
title: "Theorem Lab — GM-SGM Research (Purdue)"
type: project
status: active
created: 2026-04-25
updated: 2026-04-25
tags: [project, research, purdue, optimization, robust-ml, geometric-median, sgm]
---

# Theorem Lab — GM-SGM: Robust Optimization under Gradient Corruption

> Collaboration with José María Soto Valenzuela at Purdue University / Tec de Monterrey.
> Repo: https://github.com/Gorchon/theorem-lab

---

## What is it

A research paper + codebase on **Geometric Median Switching Gradient Method (GM-SGM)** — a robust extension of the Switching Gradient Method (SGM) that replaces mean gradient aggregation with geometric median aggregation to resist adversarial/Byzantine gradient corruption in distributed and constrained optimization.

## Core Idea

**SGM** solves constrained optimization by switching between ∇f (objective) and ∇g (constraint) based on feasibility. But it's fragile under gradient corruption because it uses the mean.

**GM-SGM** replaces mean with geometric median (breakdown point 1/2 — tolerates up to 50% corruption):
- Geometric median aggregation of per-sample objective + constraint gradients
- Median-based feasibility test to protect switching decisions
- Soft switching (smooth interpolation near constraint boundary)

## Paper Status

**Title:** "Geometric Median Switching Gradient Method (GM-SGM): Robust Optimization under Gradient Corruption"
**Authors:** José María Soto Valenzuela (lead), Daniel Barreras Meraz
**Affiliation:** Purdue University, Tecnológico de Monterrey
**Status:** Draft — sections 1-6 written, conclusion is "(So far)"

### Sections Complete
1. Introduction — motivation, contributions
2. Background — SGM formulation, geometric median definition
3. Proposed Method — GM-SGM algorithm (Algorithm 1)
4. Convex Quadratic Validation — controlled 2D experiments
5. Non-convex mNPC Experiments — Fashion-MNIST with per-class constraints
6. Block Coordinate Selection + Memory — BGMD-inspired scalability (Algorithm 2)

### What's Missing
- Convergence theory / formal analysis
- Larger-scale experiments (CIFAR-10, ImageNet subset)
- Comparison with other robust aggregation methods (trimmed mean, Krum, centered clipping)
- Discussion / related work section
- Final conclusion

## Repo Structure

```
theorem-lab/
├── FashionMnistExperiments/     # Core paper experiments
│   ├── fashion_mnpc_gm_sgm_experiment.py      # Main SGM vs GM-SGM comparison
│   ├── fashion_mnpc_gm_sgm_blockmem.py        # Block + memory variant
│   ├── fashion_mnpc_constraints.py             # Constraint framework
│   ├── experimentAgg.py                        # Aggregation experiments
│   └── results/                                # Saved .pt logs + plots per epoch count
├── GM-SGM_vs_SGM/               # Convex quadratic trajectory experiments
│   └── gm_vs_sgm.py
├── GM_Robustness/               # Isolated geometric median robustness tests
│   └── gm_vs_mean.py
├── gross_corruption_model/      # Gross corruption baseline experiments
├── Drafts/                      # WIP code, exploratory experiments
│   ├── draft.txt                # Full training script with all 3 modes
│   └── gm_sgm_blockmem_experiments/
├── LatexBackUp/
│   └── main.txt                 # Full LaTeX paper source
└── README.md
```

## Key Algorithms

### Algorithm 1: GM-SGM
1. Sample mini-batch, compute per-sample gradients
2. Aggregate via geometric median: ∇̂f, ∇̂g
3. Robust feasibility: ĝ = median({g_i(w)})
4. Soft switching: p = min{1, [1 + β(ĝ - ε)]₊}
5. Update: w ← w - η(p∇̂g + (1-p)∇̂f)

### Algorithm 2: GM-SGM + Block + Memory
Same as Algorithm 1 but:
- Compute importance scores s_j = Σ G[i,j]²
- Select top-k coordinates (block selection)
- Accumulate residual in memory vector
- Augment gradients with memory before GM aggregation
- Complexity: O(bd) → O(bk)

## Experiments

### Fashion-MNIST (mNPC framework)
- 3-layer MLP, 10 classes
- Target class: Sneaker (class 7)
- Constraints: κ_i = 0.3 for all non-target classes
- Corruption: 40% workers produce fully corrupted gradients
- 11 workers, Weiszfeld geometric median (10 iterations)
- Epochs tested: 30, 80, 100, 120, 150, 200

### Convex Quadratic
- f(w) = (w₀-1)² + (w₁-2)², g(w) = w₀ + w₁ - 2
- 3D trajectory visualization
- Clean SGM vs corrupted SGM vs GM-SGM

## Key Results
- SGM under 40% corruption: persistent constraint violations, chaotic trajectories
- GM-SGM under same corruption: stable convergence, all constraints satisfied
- Block GM-SGM (β=0.3): ~70% speedup with preserved robustness

## Related Work

### Core References
1. **Hashemi et al. (2023)** — "Optimization via First-Order Switching Methods: Skew-Symmetric Dynamics and Optimistic Discretization." arXiv:2301.08683. *The SGM paper this builds on.*
2. **Acharya et al. (2022)** — "Robust Training in High Dimensions via Block Coordinate Geometric Median Descent." AISTATS. *BGMD — block selection + memory mechanism.*

### Related (for literature review expansion)
- **Cohen et al. (2016)** — "Geometric Median in Nearly Linear Time." STOC. *Efficient GM computation.*
- **Blanchard et al. (2017)** — "Machine Learning with Adversaries: Byzantine Tolerant Gradient Descent." NeurIPS. *Krum aggregation.*
- **Yin et al. (2018)** — "Byzantine-Robust Distributed Learning." ICML. *Trimmed mean, coordinate-wise median.*
- **Karimireddy et al. (2021)** — "Learning from History for Byzantine Robust Optimization." ICML. *Centered clipping.*
- **Teng & Lin (2024)** — "Multi-class Neyman-Pearson Classification." *mNPC framework used in experiments.*
- **Chen et al. (2017)** — "Distributed Statistical Machine Learning in Adversarial Settings." STOC. *Breakdown point analysis.*

## Collaborator

**José María Soto Valenzuela (Chema)** — also works at Sidepocket (WebAuthn PRs). Lead author on this paper, Purdue CS.

## Next Steps
- [ ] Add convergence theory section
- [ ] Run CIFAR-10 experiments
- [ ] Add comparison with Krum, trimmed mean, centered clipping
- [ ] Write discussion / related work
- [ ] Finalize conclusion
- [ ] Clean up repo for camera-ready submission
