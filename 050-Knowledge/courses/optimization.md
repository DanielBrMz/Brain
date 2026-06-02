---
title: "Course: Optimization"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, mathematics, optimization]
prerequisites: [linear-algebra, real-analysis]
---

# Optimization

> *"The great watershed in optimization is not between linearity and nonlinearity, but between convexity and nonconvexity."* — R. Tyrrell Rockafellar

Back to [[../math-syllabus|Mathematics Syllabus]] | Related: [[linear-algebra]], [[real-analysis]], [[probability-statistics]]

---

## Motivation

Optimization is the science of making the best decision subject to constraints. It lies at the heart of machine learning (training neural networks), operations research (scheduling, logistics), finance (portfolio optimization), signal processing (compressed sensing), and engineering design. The modern theory cleanly separates tractable problems (convex optimization, linear programming) from intractable ones (general nonconvex, combinatorial), and provides powerful algorithms with convergence guarantees for the tractable cases. Understanding this theory is essential for anyone who builds or uses computational models.

## Prerequisites

- [[linear-algebra]] — eigenvalues, positive definiteness, SVD, matrix calculus
- [[real-analysis]] — continuity, compactness, differentiation, inverse/implicit function theorems
- Basic multivariable calculus (gradients, Hessians, Taylor expansions)
- Some [[probability-statistics]] for stochastic optimization methods

## Recommended References

- **Boyd & Vandenberghe**, *Convex Optimization* — the modern classic (freely available online)
- **Nocedal & Wright**, *Numerical Optimization* — comprehensive for algorithms
- **Bertsekas**, *Nonlinear Programming* — rigorous, covers duality deeply
- **Rockafellar**, *Convex Analysis* — foundational theory
- **Beck**, *First-Order Methods in Optimization* — modern treatment of proximal/splitting methods
- **Bertsimas & Tsitsiklis**, *Introduction to Linear Optimization* — excellent for LP and integer programming

---

## Part I: Foundations of Convex Optimization (Weeks 1--4)

### Week 1: Convex Sets

**Topics:**
- Convex sets: C is convex iff θx + (1-θ)y ∈ C for all x, y ∈ C and θ ∈ [0,1]
- Examples: hyperplanes, halfspaces, polyhedra, balls, ellipsoids, cones
- Operations preserving convexity: intersection, affine image/preimage, perspective, linear-fractional maps
- Convex hull: conv(S) = smallest convex set containing S
- Cones: convex cones, conic hull, proper cones, generalized inequalities
- Separating and supporting hyperplane theorems

**Key Results:**
- **Separating Hyperplane Theorem:** If C and D are nonempty disjoint convex sets, there exists a ≠ 0 and b such that a^T x ≤ b for x ∈ C and a^T x ≥ b for x ∈ D.
  - *Proof sketch (when C, D are closed and one is compact):* The continuous function ||x - y|| on the compact set C × {y ∈ D} achieves its minimum (or use the more general argument via projection onto closed convex sets in Hilbert space). The hyperplane perpendicular to x* - y* at the midpoint separates.
  - *Importance:* This is the geometric foundation of duality theory.
- **Supporting Hyperplane Theorem:** At every boundary point of a convex set, there exists a supporting hyperplane.

### Week 2: Convex Functions

**Topics:**
- Definition: f is convex iff dom(f) is convex and f(θx + (1-θ)y) ≤ θf(x) + (1-θ)f(y)
- Strictly convex, strongly convex (f(x) - (m/2)||x||^2 is convex for some m > 0)
- Examples: affine, norms, max, log-sum-exp, quadratic forms x^T Px (P ≽ 0)
- First-order condition: f convex iff f(y) ≥ f(x) + ∇f(x)^T(y - x) (function lies above all tangent hyperplanes)
- Second-order condition: f convex iff ∇^2 f(x) ≽ 0 (Hessian is PSD)
- Operations preserving convexity: non-negative weighted sums, composition rules, pointwise supremum, perspective, conjugate
- Epigraph: f is convex iff epi(f) = {(x,t) : f(x) ≤ t} is a convex set
- Sublevel sets of convex functions are convex (converse is false: quasiconvexity)

**Key Insight:** Convexity of f means every local minimum is a global minimum. This single property is what makes convex optimization tractable. For strongly convex f, the global minimum is unique.

### Week 3: Convex Optimization Problems

**Topics:**
- Standard form: minimize f_0(x) subject to f_i(x) ≤ 0, h_j(x) = 0
- Convex optimization: f_0, f_i convex; h_j affine
- Feasible set, optimal value, optimal set
- Equivalent transformations: change of variables, eliminating equality constraints, introducing slack/epigraph variables
- Important problem classes:
  - Linear Programming (LP): min c^T x s.t. Ax ≤ b
  - Quadratic Programming (QP): min (1/2)x^T Px + q^T x s.t. Ax ≤ b
  - Second-Order Cone Programming (SOCP)
  - Semidefinite Programming (SDP): min tr(CX) s.t. tr(A_i X) = b_i, X ≽ 0
- Hierarchy: LP ⊂ QP ⊂ SOCP ⊂ SDP ⊂ Convex Programs

### Week 4: Duality

**Topics:**
- Lagrangian: L(x, λ, ν) = f_0(x) + Σ λ_i f_i(x) + Σ ν_j h_j(x)
- Lagrange dual function: g(λ, ν) = inf_x L(x, λ, ν) — always concave, even if original problem is not convex
- Dual problem: maximize g(λ, ν) subject to λ ≥ 0
- Weak duality: d* ≤ p* (always holds)
- Strong duality: d* = p* (holds for convex problems under constraint qualification, e.g., Slater's condition)
- Slater's condition: if there exists a strictly feasible point (f_i(x) < 0 for all i), strong duality holds
- Complementary slackness: at optimality, λ_i f_i(x*) = 0

**Key Results:**
- **KKT Conditions:** If strong duality holds and f_0, f_i are differentiable, then x* is optimal iff there exist λ*, ν* such that:
  1. Stationarity: ∇f_0(x*) + Σ λ_i* ∇f_i(x*) + Σ ν_j* ∇h_j(x*) = 0
  2. Primal feasibility: f_i(x*) ≤ 0, h_j(x*) = 0
  3. Dual feasibility: λ_i* ≥ 0
  4. Complementary slackness: λ_i* f_i(x*) = 0
  - *For convex problems with strong duality, KKT conditions are necessary and sufficient.*
  - *Intuition:* At the optimum, the gradient of the objective must be expressible as a non-negative combination of the constraint gradients (you cannot improve without violating a constraint).

---

## Part II: Algorithms for Smooth Optimization (Weeks 5--8)

### Week 5: Unconstrained Optimization — First-Order Methods

**Topics:**
- Gradient descent: x_{k+1} = x_k - α_k ∇f(x_k)
- Convergence analysis:
  - For L-smooth convex f: f(x_k) - f* ≤ O(1/k) with step size α = 1/L
  - For L-smooth, m-strongly convex f: ||x_k - x*|| ≤ O((1 - m/L)^k) — linear convergence
  - Condition number κ = L/m governs convergence rate
- Line search methods: exact line search, backtracking (Armijo), Wolfe conditions
- Momentum methods:
  - Heavy ball method (Polyak): x_{k+1} = x_k - α∇f(x_k) + β(x_k - x_{k-1})
  - Nesterov's accelerated gradient: achieves O(1/k^2) for convex, O((1 - √(m/L))^k) for strongly convex — optimal among first-order methods
- Conjugate gradient method

**Key Result:**
- **Nesterov's Optimal Rate:** For L-smooth convex functions, no first-order method can achieve convergence faster than O(1/k^2) (lower bound via "resisting oracle" argument). Nesterov's method achieves this bound.
  - *Intuition:* First-order methods only access gradient information. The condition number κ = L/m creates an "information bottleneck" — the method cannot distinguish certain hard instances until enough iterations have passed.

### Week 6: Unconstrained Optimization — Second-Order Methods

**Topics:**
- Newton's method: x_{k+1} = x_k - [∇^2 f(x_k)]^{-1} ∇f(x_k)
  - Local quadratic convergence (near optimum, errors square each iteration)
  - Affine invariance: performance independent of coordinate system
  - Newton decrement: λ(x) = (∇f(x)^T [∇^2 f(x)]^{-1} ∇f(x))^{1/2}
- Damped Newton (with backtracking): global convergence + local quadratic convergence
- Quasi-Newton methods: approximate Hessian to avoid O(n^3) per step
  - BFGS: rank-2 update to Hessian approximation; superlinear convergence
  - L-BFGS: limited-memory variant; O(n) storage; the workhorse for large-scale smooth optimization
- Gauss-Newton and Levenberg-Marquardt for nonlinear least squares
- Trust region methods

### Week 7: Stochastic Optimization

**Topics:**
- Stochastic gradient descent (SGD): x_{k+1} = x_k - α_k g_k, where E[g_k] = ∇f(x_k)
  - Convergence: O(1/√k) for convex, O(1/k) for strongly convex (with appropriate step size decay)
  - Variance of stochastic gradient controls constant factors
- Mini-batch SGD: variance reduction via averaging
- Variance reduction methods: SVRG, SAGA — achieve linear convergence for finite sums
- Adaptive methods:
  - AdaGrad: per-coordinate adaptive step sizes
  - RMSProp: exponential moving average of squared gradients
  - Adam: combines momentum and adaptive step sizes; the default for deep learning
  - AdamW: Adam with decoupled weight decay
- Learning rate schedules: step decay, cosine annealing, warmup, cyclical

**Key Insight:** For ML training with n data points, full gradient costs O(n) per step; SGD costs O(1). For convex problems, SGD achieves ε-accuracy in O(1/ε^2) stochastic steps vs O(1/ε) full gradient steps. Since each SGD step is n times cheaper, SGD wins when ε is not too small — which is typical in ML where statistical error dominates optimization error.

### Week 8: Constrained Optimization Algorithms

**Topics:**
- Projected gradient descent: x_{k+1} = Π_C(x_k - α∇f(x_k))
  - Convergence rates same as unconstrained if projection is cheap
- Frank-Wolfe (conditional gradient) method: linear minimization oracle instead of projection
- Barrier (interior point) methods:
  - Log-barrier: approximate indicator function with -(1/t) log(-f_i(x))
  - Central path: as t → ∞, solutions approach the constrained optimum
  - Newton steps on the barrier problem; self-concordance theory
  - Polynomial-time complexity: O(√m log(1/ε)) Newton steps for m constraints
- Augmented Lagrangian method / method of multipliers
- Penalty methods

**Key Result:**
- **Interior Point Methods achieve polynomial complexity for LP, QP, SOCP, SDP.** The number of Newton steps is O(√m log(1/ε)), independent of the problem dimension n (though each Newton step costs O(n^3) in general). This was a breakthrough: the simplex method is exponential in the worst case (though fast in practice).

---

## Part III: Nonsmooth and Structured Optimization (Weeks 9--11)

### Week 9: Linear Programming

**Topics:**
- LP standard form: min c^T x s.t. Ax = b, x ≥ 0
- Geometry: optimal solution at a vertex of the polyhedron (if bounded and feasible)
- Simplex method: move along edges of the polyhedron; finite termination with anti-cycling rules
  - Exponential worst case (Klee-Minty) but excellent practical performance
- Duality in LP: dual of min c^T x s.t. Ax = b, x ≥ 0 is max b^T y s.t. A^T y ≤ c
  - Strong duality always holds for LP (no constraint qualification needed)
  - Complementary slackness: x_i (c - A^T y)_i = 0
- Interior point methods for LP: Karmarkar's algorithm, path-following methods
- Sensitivity analysis; shadow prices (dual variables as prices)
- Network flow problems as LPs

### Week 10: Proximal Methods and Splitting

**Topics:**
- Subgradients: generalization of gradients for nonsmooth convex functions
- Subgradient method: converges but slowly (O(1/√k)); does not use structure
- Proximal operator: prox_{tf}(v) = argmin_x (f(x) + (1/2t)||x - v||^2)
  - Moreau envelope: smoothed version of f
  - Examples: prox of L1 norm is soft-thresholding; prox of indicator is projection
- Proximal gradient descent (ISTA): for min f(x) + g(x) with f smooth, g nonsmooth
  - x_{k+1} = prox_{αg}(x_k - α∇f(x_k))
  - Convergence: O(1/k) for convex
- Accelerated proximal gradient (FISTA): O(1/k^2) — optimal
- ADMM (Alternating Direction Method of Multipliers):
  - Solves min f(x) + g(z) s.t. Ax + Bz = c
  - Splits into x-update, z-update, dual variable update
  - Extremely versatile; handles distributed optimization, consensus problems
  - Convergence: O(1/k) for convex; often faster in practice

**Key Applications:**
- **LASSO** (L1-regularized least squares): min ||Ax - b||^2 + λ||x||_1. Proximal gradient with soft-thresholding. Produces sparse solutions.
- **Basis pursuit** (compressed sensing): min ||x||_1 s.t. Ax = b. Under RIP conditions, recovers the sparsest solution.
- **Total variation denoising:** min ||x - y||^2 + λ TV(x). ADMM naturally splits the smooth and nonsmooth parts.

### Week 11: Semidefinite Programming and Conic Optimization

**Topics:**
- SDP: optimize linear objective over the intersection of the PSD cone with an affine subspace
- SDP duality; strong duality (with Slater's condition for the PSD cone)
- Interior point methods for SDP: O(√n log(1/ε)) iterations, each involving an n×n eigendecomposition or Cholesky
- SDP relaxations:
  - MAX-CUT: Goemans-Williamson 0.878-approximation via SDP relaxation
  - Boolean quadratic programming: relax x ∈ {-1,1}^n to X ≽ 0, diag(X) = 1
- Sum-of-squares (SOS) optimization and connections to polynomial optimization
- Robust optimization and worst-case analysis via SDP

---

## Part IV: Advanced Topics (Weeks 12--15)

### Week 12: Duality Theory (Deep Dive)

**Topics:**
- Convex conjugate (Fenchel conjugate): f*(y) = sup_x (y^T x - f(x))
- Fenchel-Moreau theorem: f** = f for closed convex functions
- Fenchel duality: min f(x) + g(Ax) has dual max -f*(-A^T y) - g*(y)
- Minimax theorems: Sion's theorem, von Neumann's minimax theorem for zero-sum games
- Saddle point characterization of optimality
- Lagrangian duality as a special case of Fenchel duality

**Key Results:**
- **Fenchel-Moreau Theorem:** A proper lower-semicontinuous convex function equals its double conjugate: f** = f.
  - *Intuition:* f* encodes f via supporting hyperplanes. Taking the conjugate again reconstructs f as the pointwise supremum of affine functions. This fails only if f is not closed (l.s.c.) — then f** is the l.s.c. convex closure of f.
- **Von Neumann Minimax Theorem:** If X, Y are compact convex and L(x,y) is convex-concave and continuous, then min_x max_y L = max_y min_x L.

### Week 13: Combinatorial Optimization

**Topics:**
- Integer programming (IP) and mixed-integer programming (MIP)
- NP-hardness of general IP; the P vs NP question
- Branch and bound; cutting planes; branch and cut
- LP relaxation: solve the LP relaxation and round; integrality gap
- Totally unimodular matrices: LP relaxation is automatically integral (network flow, bipartite matching)
- Approximation algorithms: greedy, local search, randomized rounding
- Submodular optimization: greedy achieves (1 - 1/e) approximation for maximizing monotone submodular functions under cardinality constraints
- Matroid optimization; greedy on matroids

**Key Result:**
- **Greedy Algorithm for Submodular Maximization:** For monotone submodular f with f(∅) = 0, greedy selection achieves f(S) ≥ (1 - 1/e) f(S*), and this bound is tight unless P = NP.
  - *Importance:* Submodularity ("diminishing returns") appears in sensor placement, feature selection, influence maximization in social networks.

### Week 14: Nonconvex Optimization

**Topics:**
- Landscape of nonconvex optimization: local minima, saddle points, plateaus
- When nonconvexity is tractable:
  - Problems with no spurious local minima (some matrix factorization, phase retrieval under overparameterization)
  - Geodesically convex problems on manifolds
- Gradient descent for nonconvex smooth functions: converges to stationary point in O(1/ε^2) iterations
- Escaping saddle points: perturbed GD, cubic regularization
- Manifold optimization: optimization on Stiefel manifold, Grassmannian
- Global optimization: simulated annealing, genetic algorithms (heuristic; no polynomial guarantees)
- Neural network training: loss landscape, implicit regularization, lottery ticket hypothesis

**Key Insight:** For training neural networks, the loss function is highly nonconvex, yet SGD works remarkably well in practice. Theoretical understanding is incomplete, but partial explanations include: (1) overparameterization creates many global minima, (2) most saddle points are "strict" (have negative curvature directions), (3) SGD noise helps escape bad regions, (4) the implicit bias of SGD favors low-complexity solutions.

### Week 15: Optimization in Machine Learning

**Topics:**
- Empirical risk minimization: min (1/n) Σ ℓ(f_θ(x_i), y_i)
- Regularization: L2 (ridge), L1 (LASSO), elastic net, dropout (implicit)
- Optimization vs generalization: training loss vs test loss; early stopping as regularization
- Distributed optimization: data parallelism, model parallelism, communication-efficient methods (local SGD, gradient compression)
- Federated learning: optimization under communication and privacy constraints
- Hyperparameter optimization: grid search, random search, Bayesian optimization (Gaussian processes + acquisition functions)
- Neural architecture search (NAS): combinatorial + continuous relaxation (DARTS)
- Second-order methods for ML: K-FAC, natural gradient, Shampoo

**Connections:**
- Loss functions are typically sums → SGD and variance reduction (Week 7)
- L1 regularization → proximal methods, LASSO (Week 10)
- SVM dual → QP (Week 3)
- Kernel methods → SDP relaxations and representer theorem
- Reinforcement learning → stochastic optimization with non-stationary objectives

---

## Applications

### Machine Learning
- **Training deep networks:** SGD + Adam on nonconvex loss landscapes; batch normalization, learning rate warmup
- **Convex ML models:** SVMs (QP dual), logistic regression (smooth convex), LASSO (proximal)
- **Generative models:** GANs as minimax problems; diffusion models as score matching optimization
- **Optimal transport:** Wasserstein distance computation via LP/entropic regularization (Sinkhorn)

### Operations Research
- **Supply chain optimization:** LP and MIP for routing, scheduling, inventory
- **Revenue management:** dynamic pricing via LP/stochastic optimization
- **Network design:** minimum cost flow, shortest path (LP on totally unimodular systems)

### Signal Processing
- **Compressed sensing:** L1 minimization recovers sparse signals from underdetermined systems (see [[linear-algebra]] for RIP and SVD connections)
- **Beamforming:** SOCP and SDP formulations for antenna array design
- **Image reconstruction:** total variation minimization via ADMM/proximal methods

### Finance
- **Portfolio optimization:** Markowitz mean-variance = QP; with transaction costs = SOCP
- **Risk measures:** CVaR optimization is an LP
- **Option pricing:** American options via optimal stopping = dynamic programming

---

## Summary of Key Theorems and Results

| Result | Statement (abbreviated) | Significance |
|--------|------------------------|--------------|
| KKT Conditions | Necessary + sufficient for convex with strong duality | Characterize optimal points |
| Strong Duality | p* = d* under Slater's condition | Enables dual methods and certificates |
| Nesterov's Lower Bound | Ω(1/k^2) for first-order methods on smooth convex | Establishes optimality of acceleration |
| Interior Point Complexity | O(√m log(1/ε)) Newton steps | Polynomial-time for conic programs |
| Fenchel-Moreau | f** = f for closed convex f | Foundation of conjugate duality |
| Minimax Theorem | min max = max min for convex-concave | Game theory, GAN training, robustness |
| Submodular Greedy | (1-1/e)-approximation | Near-optimal for diminishing returns |

---

*Last updated: 2026-03-22*
