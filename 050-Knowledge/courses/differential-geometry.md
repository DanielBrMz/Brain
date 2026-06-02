---
title: "Course: Differential Geometry"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, mathematics, differential-geometry]
prerequisites: [multivariable-calculus, linear-algebra, real-analysis, topology-basics]
---

# Differential Geometry

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
> *Related: [[topology]], [[complex-analysis]], [[functional-analysis]]*

---

## 1. Motivation

Differential geometry studies the geometry of smooth shapes — curves, surfaces, and their higher-dimensional generalizations called manifolds. It is the mathematical language of general relativity, gauge theory, and modern theoretical physics. But its reach extends to robotics (configuration spaces), computer vision (shape analysis), statistics (information geometry), and machine learning (optimization on manifolds).

The central theme is: **curvature governs geometry**. A flat sheet of paper and a sphere are both 2-dimensional surfaces, but their intrinsic geometries differ because one is curved. Differential geometry makes this precise and studies the consequences.

## 2. Prerequisites

- **Multivariable calculus:** Partial derivatives, inverse/implicit function theorems, differential forms on R^n.
- **Linear algebra:** Dual spaces, tensor products, bilinear forms.
- **Real analysis:** Completeness, compactness, smooth functions.
- **Topology basics:** Topological spaces, continuity, compactness, connectedness. See [[topology]].

---

## 3. Detailed Topic Outline

### Part I: Smooth Manifolds

#### 3.1 Topological and Smooth Manifolds

- **Definition.** An n-dimensional topological manifold is a second-countable Hausdorff space locally homeomorphic to R^n.
- **Smooth structure:** An atlas of charts (U_α, φ_α) with smooth transition maps φ_β ∘ φ_α^{-1}.
- **Intuition:** A manifold is a space that "locally looks like R^n" but may have nontrivial global topology. The smooth structure lets us do calculus.
- Examples: R^n, S^n, tori T^n, projective spaces RP^n and CP^n, Lie groups, Grassmannians.
- Smooth maps between manifolds; diffeomorphisms.
- Partitions of unity — the key technical tool for going from local to global.

#### 3.2 Tangent and Cotangent Bundles

- **Tangent space** T_pM at a point p: equivalence classes of curves, or derivations on germs of smooth functions.
- **Tangent bundle** TM = ∪_p T_pM — a 2n-dimensional manifold. Sections of TM are vector fields.
- **Cotangent space** T_p*M: dual of T_pM. Elements are linear functionals on tangent vectors.
- **Cotangent bundle** T*M. Sections are 1-forms (covector fields).
- Differential of a map: df_p: T_pM → T_{f(p)}N — the linearization of f at p.
- **Intuition:** The tangent bundle "attaches a copy of R^n" to each point, encoding all possible velocities. The cotangent bundle encodes all possible measurements of velocity.

#### 3.3 Vector Fields and Flows

- Vector fields as sections of TM, or as first-order differential operators.
- Integral curves and flows: the flow φ_t of X satisfies dφ_t(p)/dt = X(φ_t(p)).
- Existence and uniqueness of flows (ODE theory on manifolds).
- **Lie bracket** [X, Y]: measures the failure of flows to commute. [X, Y] = XY - YX as differential operators.
- Complete vector fields; compactly supported vector fields are complete.

### Part II: Tensors and Differential Forms

#### 3.4 Tensor Fields

- Tensors of type (r, s) at a point: multilinear maps (T_p*M)^r × (T_pM)^s → R.
- Tensor fields: smooth assignments of tensors to each point.
- Tensor operations: contraction, tensor product, symmetrization, antisymmetrization.
- The metric tensor (preview): a symmetric (0,2)-tensor field — see Riemannian geometry below.

#### 3.5 Differential Forms and the Exterior Derivative

- **k-forms:** Antisymmetric (0, k)-tensor fields. The space Ω^k(M).
- Wedge product: α ∧ β, making Ω*(M) a graded algebra.
- **Exterior derivative** d: Ω^k(M) → Ω^{k+1}(M).
  - d^2 = 0 (fundamental property).
  - For 0-forms (functions): df is the usual differential.
  - Leibniz rule: d(α ∧ β) = dα ∧ β + (-1)^k α ∧ dβ.
- **Closed forms** (dω = 0) vs. **exact forms** (ω = dη). Exact implies closed; the converse depends on topology.
- **de Rham cohomology** H^k_{dR}(M) = (closed k-forms)/(exact k-forms).
  - Measures topological obstructions to finding antiderivatives.
  - H^0 counts connected components; H^1 detects "holes" around which you can't define a potential.
  - Connection to [[topology|singular cohomology]] via de Rham's theorem.

#### 3.6 Integration on Manifolds and Stokes' Theorem

- Orientation of manifolds: consistent choice of "positive" volume forms.
- Integration of n-forms on oriented n-manifolds.
- Manifolds with boundary; induced orientation on ∂M.
- **Stokes' Theorem.** For an oriented n-manifold M with boundary ∂M and an (n-1)-form ω:
  ∫_M dω = ∫_{∂M} ω.
- **Intuition:** This single theorem unifies the fundamental theorem of calculus, Green's theorem, the divergence theorem, and the classical Stokes' theorem. The exterior derivative d generalizes all the vector calculus operators (grad, curl, div).
- Applications: de Rham's theorem (proof sketch), Gauss-Bonnet as a special case.

### Part III: Riemannian Geometry

#### 3.7 Riemannian Metrics

- **Riemannian metric** g: a smoothly varying inner product on each tangent space. Makes M a metric space.
- Examples: the round metric on S^n, the hyperbolic metric on H^n, product metrics, warped products.
- Length of curves, distance, volume form dV_g.
- Isometries and local isometries.
- **Musical isomorphisms:** g converts vectors to covectors (♭: TM → T*M) and back (♯: T*M → TM).

#### 3.8 Connections and Covariant Differentiation

- **The problem:** There is no canonical way to differentiate vector fields on a manifold (no global coordinates). A connection provides a rule for "parallel transport."
- **Affine connection** ∇: ∇_X Y is the covariant derivative of Y along X.
- **Levi-Civita connection:** The unique connection that is (1) compatible with the metric (∇g = 0) and (2) torsion-free (∇_X Y - ∇_Y X = [X, Y]).
- **Christoffel symbols** Γ^k_{ij} in local coordinates.
- Parallel transport along curves; holonomy.

#### 3.9 Geodesics

- **Geodesics:** Curves γ satisfying ∇_{γ'} γ' = 0 — "straightest possible paths."
- Geodesic equation in coordinates: γ̈^k + Γ^k_{ij} γ̇^i γ̇^j = 0.
- **Exponential map** exp_p: T_pM → M sending v to γ_v(1).
- Normal coordinates; Gauss's lemma.
- Geodesics as locally length-minimizing curves.
- Completeness: Hopf-Rinow theorem — geodesic completeness ⟺ metric completeness (for connected manifolds).

#### 3.10 Curvature

- **Riemann curvature tensor** R(X, Y)Z = ∇_X ∇_Y Z - ∇_Y ∇_X Z - ∇_{[X,Y]} Z.
  - Measures the failure of parallel transport to be path-independent.
  - Measures the failure of covariant derivatives to commute.
- **Symmetries:** R(X,Y)Z = -R(Y,X)Z; ⟨R(X,Y)Z, W⟩ = ⟨R(Z,W)X, Y⟩; first Bianchi identity.
- **Sectional curvature** K(σ): curvature of the 2-plane σ ⊂ T_pM. Determines R completely.
  - K > 0: sphere-like (geodesics converge). K = 0: flat (Euclidean). K < 0: saddle-like (geodesics diverge).
- **Ricci curvature** Ric(X, Y) = trace of Z ↦ R(Z, X)Y. An (0,2)-tensor. Measures average sectional curvature.
- **Scalar curvature** S = trace of Ricci. A single function on M.
- **Gauss-Bonnet theorem** (surfaces): ∫_M K dA = 2π χ(M).
  - *Intuition:* Total curvature is a topological invariant. A sphere of any shape always has total curvature 4π.
- Generalization: Chern-Gauss-Bonnet in higher dimensions.

### Part IV: Advanced Topics

#### 3.11 Lie Groups and Lie Algebras

- **Lie group:** A smooth manifold that is also a group (with smooth multiplication and inversion).
- Examples: GL(n), O(n), SO(n), U(n), SU(n), SL(n), Sp(n), Heisenberg group.
- **Lie algebra** g = T_eG: the tangent space at the identity, with the Lie bracket [X, Y].
- Exponential map exp: g → G.
- Left-invariant vector fields and Maurer-Cartan form.
- Adjoint representation Ad: G → GL(g).
- Compact Lie groups: bi-invariant metrics, Peter-Weyl theorem (preview).

#### 3.12 Fiber Bundles and Connections (Overview)

- **Vector bundles:** A family of vector spaces varying smoothly over a manifold.
- **Principal bundles:** Fiber is a Lie group G. Frame bundle as an example.
- **Ehresmann connections** on principal bundles; connection 1-forms.
- **Curvature 2-form** Ω = dω + ω ∧ ω — the curvature of a connection.
- **Gauge transformations:** Changes of trivialization. The gauge group.
- **Chern-Weil theory:** Characteristic classes (Chern classes, Pontryagin classes) from curvature. Topological invariants computed from geometry.

#### 3.13 Semi-Riemannian Geometry and General Relativity

- Lorentzian manifolds: signature (n-1, 1). Timelike, spacelike, null vectors.
- The Einstein field equations: G_{μν} + Λg_{μν} = 8πT_{μν}, where G = Ric - (S/2)g.
- Geodesics as free-fall trajectories; geodesic deviation and tidal forces.
- Schwarzschild solution, Kerr solution (structure, not derivation).
- Penrose singularity theorems (statement): curvature conditions force geodesic incompleteness.

---

## 4. Key Theorems — Summary

| Theorem | Statement (abbreviated) | Significance |
|---------|------------------------|--------------|
| Stokes' Theorem | ∫_M dω = ∫_{∂M} ω | Unifies all integral theorems of vector calculus |
| de Rham's Theorem | H*_{dR}(M) ≅ H*_{sing}(M; R) | Differential forms compute topology |
| Gauss-Bonnet | ∫ K dA = 2πχ(M) | Total curvature is topological |
| Hopf-Rinow | Geodesic complete ⟺ metric complete | Foundational for global geometry |
| Nash Embedding | Every Riemannian manifold embeds isometrically in R^N | Intrinsic and extrinsic geometry are equivalent |
| Cartan-Hadamard | Complete, simply connected, K ≤ 0 ⟹ diffeomorphic to R^n | Negative curvature forces simple topology |
| Bonnet-Myers | Ric ≥ (n-1)κ > 0 ⟹ diameter ≤ π/√κ | Positive Ricci forces compactness |

---

## 5. Applications

- **General relativity:** Spacetime is a 4-dimensional Lorentzian manifold; gravity is curvature. See Section 3.13.
- **Gauge theory / particle physics:** Yang-Mills theory uses connections on principal bundles. The Standard Model is built on SU(3)×SU(2)×U(1) gauge theory.
- **Computer vision and graphics:** Shape analysis, surface reconstruction, mesh processing, optimal transport on manifolds.
- **Robotics:** Configuration spaces of robotic arms are manifolds; geodesics give optimal motions.
- **Machine learning:** Optimization on manifolds (Stiefel, Grassmann), information geometry (Fisher metric — see [[information-theory]]), natural gradient descent.
- **Topology:** Geometric methods prove topological results (Hodge theory, Bochner technique, Ricci flow → Poincare conjecture).

---

## 6. Recommended References

1. **Lee, J.M.** *Introduction to Smooth Manifolds* (GTM 218). — The standard first course. Comprehensive and clear.
2. **Lee, J.M.** *Riemannian Manifolds: An Introduction to Curvature* (GTM 176). — Natural continuation of the above.
3. **do Carmo, M.** *Riemannian Geometry.* — Elegant, geometrically motivated, classic.
4. **Tu, L.** *An Introduction to Manifolds.* — Gentler introduction; good for self-study.
5. **Spivak, M.** *A Comprehensive Introduction to Differential Geometry* (5 vols). — Encyclopedic. Use as reference.
6. **Nakahara, M.** *Geometry, Topology and Physics.* — For physicists; covers fiber bundles and gauge theory.
7. **Jost, J.** *Riemannian Geometry and Geometric Analysis.* — Advanced; includes geometric analysis topics.

---

## 7. Exercises and Milestones

- [ ] Construct smooth atlases for S^2, T^2, and RP^2.
- [ ] Prove that TM is a 2n-dimensional manifold.
- [ ] Compute the Lie bracket of two vector fields on R^3.
- [ ] Verify that d^2 = 0 for the exterior derivative.
- [ ] Derive the geodesic equations on the sphere S^2 with the round metric.
- [ ] Compute the Christoffel symbols for the hyperbolic plane in the upper half-plane model.
- [ ] Compute the Riemann curvature tensor of S^2 and verify constant sectional curvature.
- [ ] Verify the Gauss-Bonnet theorem for the torus (K = 0, χ = 0).
- [ ] Show that SO(3) is a 3-dimensional Lie group and identify its Lie algebra with (R^3, ×).
- [ ] Derive the Schwarzschild metric from Einstein's equations (assuming spherical symmetry and vacuum).

---

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
