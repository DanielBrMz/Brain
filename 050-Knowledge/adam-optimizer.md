---
title: "Adam Optimizer & Cosine Annealing"
type: knowledge
updated: 2026-04-27
tags: [math, optimization, deep-learning]
---

# Adam Optimizer & Cosine Annealing

## Adam (Adaptive Moment Estimation)

Combines momentum (first moment) with RMSProp (second moment):

    g_t = gradient at step t
    m_t = beta1 * m_{t-1} + (1-beta1) * g_t          # exponential moving average of gradient
    v_t = beta2 * v_{t-1} + (1-beta2) * g_t^2         # exponential moving average of squared gradient
    m_hat = m_t / (1 - beta1^t)                        # bias correction (important early)
    v_hat = v_t / (1 - beta2^t)
    theta = theta - lr * m_hat / (sqrt(v_hat) + eps)   # update

Defaults: beta1=0.9, beta2=0.999, eps=1e-8.

**Per-parameter learning rates:** Each parameter gets its own effective LR scaled by 1/sqrt(v_hat). Parameters with large gradients get smaller effective LR (stabilized). Parameters with small gradients get larger effective LR (accelerated).

## Weight Decay (L2 Regularization)

    theta = theta - lr * (m_hat / (sqrt(v_hat) + eps) + lambda * theta)

Adds lambda*theta to the gradient, penalizing large weights. Prevents overfitting. Both models use lambda=1e-5.

## Cosine Annealing Schedule

    lr(t) = eta_min + 0.5 * (eta_max - eta_min) * (1 + cos(pi * t / T_max))

- Starts at eta_max (1e-4 in both models)
- Smoothly decays following a cosine curve
- Reaches eta_min (1e-6) at T_max
- No sharp drops like step schedules
- Allows the model to explore broadly early, then fine-tune with small LR

## Used In
- [[victoria-hydro-model]] — Adam + CosineAnnealingLR (both 3D and 2D)
- [[fetenh-net]] — same optimizer setup
- [[math-foundations-medical-imaging-dl]] — full syllabus

## References
- Kingma & Ba. "Adam: A Method for Stochastic Optimization", ICLR 2015.
- Loshchilov & Hutter. "SGDR: Stochastic Gradient Descent with Warm Restarts", ICLR 2017.
