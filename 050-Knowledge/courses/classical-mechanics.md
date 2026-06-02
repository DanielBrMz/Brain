---
title: "Course: Classical Mechanics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, physics, mechanics]
prerequisites: [multivariable calculus, linear algebra, ODEs]
---

# Classical Mechanics

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[quantum-mechanics]], [[statistical-mechanics]], [[biomedical-engineering]]*

## Motivation

Classical mechanics is the foundation of all physical science and engineering. Every subsequent physics course — electromagnetism, quantum mechanics, statistical mechanics — builds on its mathematical framework. The Lagrangian and Hamiltonian formulations are not merely elegant restatements of Newton's laws; they are the scaffolding on which quantum field theory, general relativity, and modern control theory are erected. For applied work in robotics, molecular dynamics, and biomechanics, fluency in classical mechanics is non-negotiable.

## Prerequisites

- **Multivariable calculus:** Partial derivatives, multiple integrals, vector calculus (div, grad, curl), Stokes' and divergence theorems.
- **Linear algebra:** Eigenvalue problems, matrix diagonalization, quadratic forms.
- **Ordinary differential equations:** Second-order linear ODEs, phase portraits, basic existence/uniqueness.

---

## I. Newtonian Mechanics

### 1.1 Newton's Laws

- **First law (inertia):** Definition of inertial reference frames. The subtle content: inertial frames exist and can be identified.
- **Second law:** $\vec{F} = m\vec{a}$ as a definition of force and a dynamical equation simultaneously. Distinction between the law as tautology vs. predictive tool (when force laws are specified independently).
- **Third law:** Action-reaction pairs. Strong form (forces along the line of centers) vs. weak form. Failure in electrodynamics (radiation reaction, field momentum).

### 1.2 Forces in Nature

- **Gravity:** Near-earth ($mg$) and universal ($Gmm'/r^2$). Gravitational field as a concept.
- **Contact forces:** Normal force, friction (static and kinetic, coefficient of friction, microscopic origin). Tension in strings and ropes.
- **Spring force:** Hooke's law, $F = -kx$. Linear restoring forces as the universal approximation near equilibrium.
- **Drag forces:** Linear ($-b\vec{v}$) and quadratic ($-c|\vec{v}|\vec{v}$) drag. Terminal velocity. Reynolds number as the criterion.

### 1.3 Work, Energy, Kinetic Energy Theorem

- Work done by a force: $W = \int \vec{F} \cdot d\vec{r}$.
- Work-energy theorem: $W_{\text{net}} = \Delta K$.
- Conservative forces: $\vec{F} = -\nabla U$. Existence criterion: $\nabla \times \vec{F} = 0$ (simply connected domain).
- Potential energy. Energy conservation: $E = K + U = \text{const}$ for conservative systems.
- Energy diagrams: turning points, equilibria (stable, unstable, neutral).

### 1.4 Momentum and Collisions

- Linear momentum: $\vec{p} = m\vec{v}$.
- Impulse-momentum theorem.
- Conservation of momentum in isolated systems.
- Center of mass: definition, motion of the CM, reduction to CM frame.
- Elastic vs. inelastic collisions. Coefficient of restitution.
- Two-body collisions in 1D and 2D. Lab frame vs. CM frame analysis.

### 1.5 Angular Momentum and Torque

- Torque: $\vec{\tau} = \vec{r} \times \vec{F}$.
- Angular momentum: $\vec{L} = \vec{r} \times \vec{p}$.
- $\vec{\tau} = d\vec{L}/dt$.
- Conservation of angular momentum when net torque vanishes.

---

## II. Lagrangian Mechanics

### 2.1 Generalized Coordinates

- Degrees of freedom and constraints. Holonomic vs. non-holonomic constraints.
- Generalized coordinates $q_i$ — any set of independent parameters that fully specify the configuration.
- Configuration space: the manifold of all possible configurations.
- Generalized velocities $\dot{q}_i$.

### 2.2 The Principle of Least Action

- Action functional: $S[q] = \int_{t_1}^{t_2} L(q, \dot{q}, t)\, dt$.
- Hamilton's principle: the physical path is a stationary point of the action (not necessarily a minimum — the name is traditional).
- Derivation of the Euler-Lagrange equations from the variational principle:
$$\frac{d}{dt}\frac{\partial L}{\partial \dot{q}_i} - \frac{\partial L}{\partial q_i} = 0$$
- The Lagrangian: $L = T - U$ for mechanical systems.

### 2.3 Applications of the Euler-Lagrange Equations

- Simple pendulum, double pendulum, spherical pendulum.
- Bead on a rotating wire.
- Atwood machine.
- Particle on a surface of revolution.
- Systems with time-dependent constraints.

### 2.4 Constraints and Lagrange Multipliers

- Holonomic constraints: $f(q_1, \ldots, q_n, t) = 0$.
- Method of Lagrange multipliers: modified Euler-Lagrange equations with constraint forces as multipliers.
- Physical interpretation: the multiplier gives the constraint force.
- Non-holonomic constraints (velocity-dependent, non-integrable): limitations of the Lagrangian method.

### 2.5 Symmetries and Conservation Laws — Noether's Theorem

- **Noether's theorem (statement):** Every continuous symmetry of the Lagrangian corresponds to a conserved quantity.
- Time translation invariance → energy conservation.
- Spatial translation invariance → momentum conservation.
- Rotational invariance → angular momentum conservation.
- Cyclic (ignorable) coordinates: if $\partial L/\partial q_i = 0$, then $p_i = \partial L/\partial \dot{q}_i$ is conserved.
- Deep importance: Noether's theorem unifies all conservation laws under a single principle. It extends to field theory and is the backbone of modern particle physics.

### 2.6 Small Oscillations and Normal Modes

- Equilibrium: $\partial U/\partial q_i = 0$.
- Linearization about equilibrium: mass matrix $M_{ij}$ and stiffness matrix $K_{ij}$.
- Eigenvalue problem: $\det(K - \omega^2 M) = 0$.
- Normal modes: eigenvectors of $M^{-1}K$. Superposition.
- Coupled oscillators: two masses on springs, loaded string (discrete → continuous limit, preview of wave equation).

---

## III. Hamiltonian Mechanics

### 3.1 The Hamiltonian

- Legendre transformation from $L(q, \dot{q}, t)$ to $H(q, p, t)$ where $p_i = \partial L/\partial \dot{q}_i$.
- $H = \sum_i p_i \dot{q}_i - L$.
- When $H = T + U$ (sufficient conditions: $L = T - U$, $T$ homogeneous quadratic in $\dot{q}$, $U$ independent of $\dot{q}$).
- Hamilton's equations:
$$\dot{q}_i = \frac{\partial H}{\partial p_i}, \qquad \dot{p}_i = -\frac{\partial H}{\partial q_i}$$

### 3.2 Phase Space

- Phase space: $(q_1, \ldots, q_n, p_1, \ldots, p_n)$ — $2n$-dimensional.
- Trajectories in phase space never cross (uniqueness of solutions).
- Liouville's theorem: phase space volume is conserved under Hamiltonian flow. Implications for statistical mechanics.

### 3.3 Poisson Brackets

- Definition: $\{f, g\} = \sum_i \left(\frac{\partial f}{\partial q_i}\frac{\partial g}{\partial p_i} - \frac{\partial f}{\partial p_i}\frac{\partial g}{\partial q_i}\right)$.
- Fundamental brackets: $\{q_i, p_j\} = \delta_{ij}$.
- Equations of motion: $\dot{f} = \{f, H\} + \partial f/\partial t$.
- Connection to quantum mechanics: $\{\ ,\ \} \to \frac{1}{i\hbar}[\ ,\ ]$.

### 3.4 Canonical Transformations

- Generating functions (four types: $F_1(q, Q)$, $F_2(q, P)$, $F_3(p, Q)$, $F_4(p, P)$).
- Criterion: preservation of Poisson bracket structure (symplecticity).
- Examples: point transformations, exchange of $q$ and $p$.

### 3.5 Hamilton-Jacobi Theory

- Hamilton-Jacobi equation: $H\!\left(q, \frac{\partial S}{\partial q}, t\right) + \frac{\partial S}{\partial t} = 0$.
- Hamilton's principal function $S(q, \alpha, t)$.
- Separation of variables: when the HJ equation separates, the problem is integrable.
- Connection to wave mechanics (Schrödinger equation as a "wave" version of HJ).
- Action-angle variables for periodic systems.

---

## IV. Rigid Body Dynamics

### 4.1 Kinematics of Rigid Bodies

- Euler's theorem: any displacement of a rigid body with one point fixed is a rotation.
- Rotation matrices and the rotation group SO(3).
- Angular velocity vector $\vec{\omega}$.
- Euler angles $(\phi, \theta, \psi)$: conventions, gimbal lock.

### 4.2 Moment of Inertia Tensor

- Definition: $I_{ij} = \int \rho(\vec{r})(r^2 \delta_{ij} - x_i x_j)\, dV$.
- Principal axes: diagonalization of $I_{ij}$. Principal moments.
- Parallel axis theorem, perpendicular axis theorem.
- Common examples: sphere, cylinder, rod, disk.

### 4.3 Euler's Equations

- Torque-free motion: $I_1 \dot{\omega}_1 - (I_2 - I_3)\omega_2 \omega_3 = 0$ (and cyclic).
- Stability of rotation about principal axes.
- Symmetric top (Lagrangian treatment): precession, nutation.
- The spinning top and gyroscope. Precession of the equinoxes.

---

## V. Central Force Problem

### 5.1 Reduction to One-Body Problem

- Two-body problem: center of mass and relative coordinates.
- Reduced mass: $\mu = m_1 m_2 / (m_1 + m_2)$.

### 5.2 Effective Potential and Orbits

- Conservation of angular momentum → motion in a plane.
- Effective potential: $U_{\text{eff}}(r) = U(r) + L^2/(2\mu r^2)$.
- Orbit equation: $u(\theta) = 1/r(\theta)$, Binet's equation.
- Conic sections for inverse-square law: ellipse, parabola, hyperbola.

### 5.3 The Kepler Problem

- Kepler's three laws derived from Newtonian gravity.
- Eccentricity, semi-major axis, orbital period.
- The Laplace-Runge-Lenz vector: an additional conserved quantity. Hidden SO(4) symmetry.
- Perturbations: precession of orbits (GR correction, oblateness).

### 5.4 Scattering Theory

- Cross section: differential and total.
- Impact parameter and scattering angle.
- Rutherford scattering (Coulomb potential): $d\sigma/d\Omega \propto 1/\sin^4(\theta/2)$.
- Hard sphere scattering.
- Laboratory vs. CM frames for scattering.

---

## VI. Oscillations

### 6.1 Damped Oscillations

- Underdamped, critically damped, overdamped.
- Quality factor $Q$.
- Energy decay.

### 6.2 Driven Oscillations and Resonance

- Steady-state response to harmonic driving.
- Amplitude resonance, phase lag.
- Transient response.
- Mechanical impedance.

### 6.3 Coupled Oscillations

- Normal modes of coupled systems.
- Beats as superposition of normal modes.
- The $N$-body chain: dispersion relation, approach to continuum.

---

## VII. Non-Inertial Reference Frames

- Fictitious forces: centrifugal, Coriolis, Euler.
- Coriolis effect: deflection of projectiles, Foucault pendulum, weather patterns.
- Rotating frame Lagrangian.

---

## VIII. Continuous Systems and Fields (Preview)

- Vibrating string: Lagrangian density, wave equation.
- Transition from discrete to continuous: Lagrangian field theory preview.
- Connection to electromagnetism and quantum field theory.

---

## Applications

### Robotics and Control

- Forward and inverse kinematics via Lagrangian methods.
- Equations of motion for robotic arms (generalized coordinates = joint angles).
- Stability analysis via linearization and normal modes.
- Hamiltonian methods in optimal control (Pontryagin's maximum principle).

### Molecular Dynamics

- Classical trajectories of atoms: Hamiltonian equations integrated numerically (Verlet, leapfrog).
- Symplectic integrators preserve phase space volume — essential for long-time stability.
- Force fields (Lennard-Jones, Coulomb) as potential energy functions.
- Ergodic hypothesis connects time averages to ensemble averages (bridge to [[statistical-mechanics]]).

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Newton's laws | Foundation — but limited to Cartesian coordinates |
| Lagrangian | Coordinate-independent, handles constraints naturally |
| Hamiltonian | Phase space, symplectic structure, bridge to quantum mechanics |
| Noether's theorem | Symmetry ↔ conservation law (the deepest principle) |
| Action principle | Unifying principle across all of physics |
| Phase space | Geometric arena for dynamics; Liouville theorem → stat mech |
| Normal modes | Decomposition of coupled systems; ubiquitous in physics |
| Central force | Kepler problem, scattering — prototypes for all force problems |

---

## Recommended References

1. **Goldstein, Poole, Safko** — *Classical Mechanics* (3rd ed.). The standard graduate text. Thorough on Lagrangian/Hamiltonian methods.
2. **Landau & Lifshitz** — *Mechanics* (Course of Theoretical Physics, Vol. 1). Concise, elegant. Best for building intuition about the action principle.
3. **Taylor** — *Classical Mechanics*. Excellent undergraduate text with clear exposition.
4. **Arnold** — *Mathematical Methods of Classical Mechanics*. Rigorous geometric/topological approach. For the mathematically inclined.
5. **Marion & Thornton** — *Classical Dynamics of Particles and Systems*. Good problem sets.
6. **José & Saletan** — *Classical Dynamics: A Contemporary Approach*. Modern treatment with differential geometry.

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
