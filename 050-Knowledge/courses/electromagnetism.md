---
title: "Course: Electromagnetism"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, physics, electromagnetism]
prerequisites: [multivariable calculus, vector calculus, ODEs, classical-mechanics]
---

# Electromagnetism

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[classical-mechanics]], [[quantum-mechanics]], [[mri-physics]], [[biomedical-engineering]]*

## Motivation

Electromagnetism is one of the four fundamental forces and the first to be understood as a field theory. Maxwell's equations — four lines that unify electricity, magnetism, and optics — are arguably the most consequential equations in physics. They predicted electromagnetic waves, demanded special relativity, and provided the template for all subsequent gauge field theories (QED, QCD, electroweak). For applied work, electromagnetism underpins MRI physics, circuit design, antenna engineering, photonics, and plasma physics. Understanding EM deeply is essential for [[mri-physics]] and [[biomedical-engineering]].

## Prerequisites

- **Vector calculus:** Gradient, divergence, curl, Laplacian. Divergence theorem, Stokes' theorem. Curvilinear coordinates (spherical, cylindrical).
- **ODEs and PDEs:** Separation of variables, boundary value problems.
- **Classical mechanics:** Lagrangian formulation helpful but not strictly required.

---

## I. Electrostatics

### 1.1 Coulomb's Law and the Electric Field

- Coulomb's law: $\vec{F} = \frac{1}{4\pi\epsilon_0} \frac{q_1 q_2}{r^2} \hat{r}$.
- Electric field: $\vec{E}(\vec{r}) = \frac{1}{4\pi\epsilon_0} \int \frac{\rho(\vec{r}')(\vec{r} - \vec{r}')}{|\vec{r} - \vec{r}'|^3} d^3r'$.
- Superposition principle.
- Field lines: conventions and interpretation.

### 1.2 Gauss's Law

- Integral form: $\oint \vec{E} \cdot d\vec{A} = Q_{\text{enc}}/\epsilon_0$.
- Differential form: $\nabla \cdot \vec{E} = \rho/\epsilon_0$.
- Symmetry arguments: spherical, cylindrical, planar.
- Applications: uniformly charged sphere, infinite line, infinite plane, concentric shells.

### 1.3 Electric Potential

- $\vec{E} = -\nabla V$.
- $V(\vec{r}) = \frac{1}{4\pi\epsilon_0} \int \frac{\rho(\vec{r}')}{|\vec{r} - \vec{r}'|} d^3r'$.
- Equipotential surfaces. Relation to field lines.
- Potential energy of charge configurations.

### 1.4 Poisson's and Laplace's Equations

- Poisson: $\nabla^2 V = -\rho/\epsilon_0$.
- Laplace: $\nabla^2 V = 0$ (charge-free regions).
- Uniqueness theorems (first and second).
- **Boundary value problems:**
  - Separation of variables in Cartesian, spherical, cylindrical coordinates.
  - Legendre polynomials and spherical harmonics.
  - Bessel functions for cylindrical problems.

### 1.5 Method of Images

- Grounded conducting plane: image charge.
- Conducting sphere: image charge location and magnitude.
- Induced surface charge.

### 1.6 Multipole Expansion

- Monopole, dipole, quadrupole terms.
- Electric dipole: $\vec{p} = \sum q_i \vec{r}_i$.
- Dipole field: $V \sim \frac{\vec{p} \cdot \hat{r}}{4\pi\epsilon_0 r^2}$.
- Torque and energy of dipole in external field.

### 1.7 Electrostatics in Matter

- Polarization $\vec{P}$, bound charges ($\rho_b = -\nabla \cdot \vec{P}$, $\sigma_b = \vec{P} \cdot \hat{n}$).
- Displacement field: $\vec{D} = \epsilon_0 \vec{E} + \vec{P}$.
- Linear dielectrics: $\vec{P} = \epsilon_0 \chi_e \vec{E}$, $\vec{D} = \epsilon \vec{E}$.
- Boundary conditions at dielectric interfaces.

---

## II. Magnetostatics

### 2.1 Magnetic Force and the Lorentz Force Law

- $\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})$.
- Magnetic force does no work.
- Cyclotron motion, velocity selector, Hall effect.

### 2.2 Biot-Savart Law

- $\vec{B}(\vec{r}) = \frac{\mu_0}{4\pi} \int \frac{\vec{J}(\vec{r}') \times (\vec{r} - \vec{r}')}{|\vec{r} - \vec{r}'|^3} d^3r'$.
- Applications: straight wire, circular loop, solenoid.

### 2.3 Ampere's Law

- Integral form: $\oint \vec{B} \cdot d\vec{l} = \mu_0 I_{\text{enc}}$.
- Differential form: $\nabla \times \vec{B} = \mu_0 \vec{J}$.
- Symmetry applications: infinite wire, solenoid, toroid.

### 2.4 Magnetic Vector Potential

- $\vec{B} = \nabla \times \vec{A}$.
- Gauge freedom: $\vec{A} \to \vec{A} + \nabla \Lambda$.
- Coulomb gauge: $\nabla \cdot \vec{A} = 0$.
- Multipole expansion of $\vec{A}$: magnetic dipole moment $\vec{m} = \frac{1}{2}\int \vec{r}' \times \vec{J}\, d^3r'$.

### 2.5 Magnetostatics in Matter

- Magnetization $\vec{M}$, bound currents ($\vec{J}_b = \nabla \times \vec{M}$, $\vec{K}_b = \vec{M} \times \hat{n}$).
- Auxiliary field: $\vec{H} = \vec{B}/\mu_0 - \vec{M}$.
- Linear media: $\vec{M} = \chi_m \vec{H}$, $\vec{B} = \mu \vec{H}$.
- Diamagnetism, paramagnetism, ferromagnetism (qualitative).

---

## III. Electrodynamics

### 3.1 Electromotive Force and Faraday's Law

- Motional EMF: $\mathcal{E} = \oint (\vec{v} \times \vec{B}) \cdot d\vec{l}$.
- Faraday's law: $\nabla \times \vec{E} = -\partial \vec{B}/\partial t$.
- Lenz's law as a consequence.
- Inductance (self and mutual). Energy stored in magnetic field.

### 3.2 Maxwell's Displacement Current

- The inconsistency: $\nabla \cdot (\nabla \times \vec{B}) = \mu_0 \nabla \cdot \vec{J} \neq 0$ for time-varying fields.
- Displacement current: $\vec{J}_d = \epsilon_0 \partial \vec{E}/\partial t$.
- Ampere-Maxwell law: $\nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \epsilon_0 \partial \vec{E}/\partial t$.

### 3.3 Maxwell's Equations — Complete

**Differential form:**

| Equation | Name |
|----------|------|
| $\nabla \cdot \vec{E} = \rho/\epsilon_0$ | Gauss (electric) |
| $\nabla \cdot \vec{B} = 0$ | Gauss (magnetic) |
| $\nabla \times \vec{E} = -\partial \vec{B}/\partial t$ | Faraday |
| $\nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \epsilon_0 \partial \vec{E}/\partial t$ | Ampere-Maxwell |

**Integral form:**

| Equation | Name |
|----------|------|
| $\oint \vec{E} \cdot d\vec{A} = Q_{\text{enc}}/\epsilon_0$ | Gauss (electric) |
| $\oint \vec{B} \cdot d\vec{A} = 0$ | Gauss (magnetic) |
| $\oint \vec{E} \cdot d\vec{l} = -d\Phi_B/dt$ | Faraday |
| $\oint \vec{B} \cdot d\vec{l} = \mu_0 I_{\text{enc}} + \mu_0 \epsilon_0 d\Phi_E/dt$ | Ampere-Maxwell |

- Continuity equation: $\nabla \cdot \vec{J} + \partial \rho/\partial t = 0$ (consequence, not independent).
- Boundary conditions derived from Maxwell's equations.

---

## IV. Electromagnetic Waves

### 4.1 Wave Equation in Vacuum

- Derivation from Maxwell's equations: $\nabla^2 \vec{E} = \mu_0 \epsilon_0 \frac{\partial^2 \vec{E}}{\partial t^2}$.
- Speed of light: $c = 1/\sqrt{\mu_0 \epsilon_0}$. Maxwell's great unification of optics and electromagnetism.

### 4.2 Plane Waves

- Monochromatic plane wave: $\vec{E} = E_0 \hat{n} \, e^{i(\vec{k}\cdot\vec{r} - \omega t)}$.
- Transversality: $\vec{k} \cdot \vec{E} = 0$, $\vec{k} \cdot \vec{B} = 0$.
- Relationship: $\vec{B} = \frac{1}{c}\hat{k} \times \vec{E}$.

### 4.3 Energy and Momentum

- Poynting vector: $\vec{S} = \frac{1}{\mu_0}\vec{E} \times \vec{B}$.
- Energy density: $u = \frac{1}{2}(\epsilon_0 E^2 + B^2/\mu_0)$.
- Intensity: time-averaged Poynting vector.
- Momentum density: $\vec{g} = \vec{S}/c^2$. Radiation pressure.

### 4.4 Polarization

- Linear, circular, elliptical polarization.
- Jones vectors and Stokes parameters.
- Polarizers, wave plates, optical activity.

### 4.5 Reflection and Refraction

- Boundary conditions at interfaces.
- Snell's law from phase matching.
- Fresnel equations: reflection and transmission coefficients.
- Brewster's angle. Total internal reflection. Evanescent waves.

### 4.6 Waves in Matter

- Dispersion relation in dielectrics: $k = n\omega/c$.
- Absorption: complex index of refraction.
- Conductors: skin depth $\delta = \sqrt{2/\mu\sigma\omega}$.
- Plasma frequency: $\omega_p = \sqrt{ne^2/m\epsilon_0}$.

---

## V. Radiation

### 5.1 Retarded Potentials

- Retarded time: $t_r = t - |\vec{r} - \vec{r}'|/c$.
- Retarded potentials: $V(\vec{r}, t) = \frac{1}{4\pi\epsilon_0}\int \frac{\rho(\vec{r}', t_r)}{|\vec{r} - \vec{r}'|} d^3r'$.
- Jefimenko's equations.

### 5.2 Electric Dipole Radiation

- Oscillating electric dipole: $\vec{p}(t) = p_0 \cos(\omega t) \hat{z}$.
- Far-field radiation pattern: $\vec{E} \propto \sin\theta / r$.
- Radiated power: Larmor formula $P = \frac{\mu_0 q^2 a^2}{6\pi c}$.
- Radiation resistance.

### 5.3 Magnetic Dipole and Quadrupole Radiation

- Higher-order multipole contributions.
- Relative magnitudes: $P_{\text{mag}} / P_{\text{elec}} \sim (v/c)^2$.

### 5.4 Antennas (Brief)

- Half-wave dipole, quarter-wave monopole.
- Radiation pattern, directivity, gain.

---

## VI. Waveguides and Cavities

### 6.1 Waveguides

- Rectangular waveguide: TE and TM modes.
- Cutoff frequency: $\omega_{mn} = c\pi\sqrt{(m/a)^2 + (n/b)^2}$.
- Group velocity, phase velocity, dispersion.
- Coaxial cable: TEM mode.

### 6.2 Resonant Cavities

- Standing waves in rectangular and cylindrical cavities.
- Quality factor $Q$.
- Applications: microwave ovens, particle accelerators, MRI RF coils (see [[mri-physics]]).

---

## VII. Special Relativity from the EM Perspective

### 7.1 Historical Motivation

- The failure of Galilean invariance for Maxwell's equations.
- Michelson-Morley experiment. The aether hypothesis and its demise.
- Einstein's two postulates.

### 7.2 Lorentz Transformations

- Lorentz boost. Time dilation, length contraction, relativity of simultaneity.
- Four-vectors: spacetime position $x^\mu$, four-velocity $u^\mu$, four-momentum $p^\mu$.
- Invariant interval: $ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2$.

### 7.3 Covariant Formulation of Electrodynamics

- Four-potential: $A^\mu = (V/c, \vec{A})$.
- Field strength tensor: $F^{\mu\nu} = \partial^\mu A^\nu - \partial^\nu A^\mu$.
- Maxwell's equations in covariant form: $\partial_\mu F^{\mu\nu} = \mu_0 J^\nu$ and $\partial_{[\alpha} F_{\beta\gamma]} = 0$.
- Transformation of $\vec{E}$ and $\vec{B}$ between frames: a "pure electric" field in one frame has a magnetic component in another.

### 7.4 Relativistic Electrodynamics

- Electromagnetic field invariants: $\vec{E} \cdot \vec{B}$ and $E^2 - c^2 B^2$.
- Stress-energy tensor of the electromagnetic field.
- Radiation from relativistic charges: relativistic Larmor formula, synchrotron radiation.

---

## VIII. Gauge Invariance

### 8.1 Gauge Transformations

- $V \to V - \partial \Lambda/\partial t$, $\vec{A} \to \vec{A} + \nabla \Lambda$.
- Physical fields $\vec{E}$, $\vec{B}$ are gauge invariant.
- Coulomb gauge: $\nabla \cdot \vec{A} = 0$.
- Lorenz gauge: $\partial_\mu A^\mu = 0$ (Lorentz covariant).

### 8.2 Gauge Invariance as a Principle

- Local U(1) gauge symmetry of electrodynamics.
- Connection to quantum electrodynamics: the photon as the gauge boson.
- Generalization: non-abelian gauge theories (Yang-Mills). SU(2) and SU(3).
- Gauge invariance as the organizing principle of the Standard Model.

---

## IX. Electromagnetism in Media (Advanced)

### 9.1 Frequency-Dependent Response

- Drude model for conductors.
- Lorentz oscillator model for dielectrics.
- Kramers-Kronig relations: causality constrains the dielectric function.
- Anomalous dispersion.

### 9.2 Magnetohydrodynamics (Brief)

- Conducting fluids in magnetic fields.
- Frozen-in flux theorem.
- Applications: astrophysics, fusion plasmas.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Maxwell's equations | Complete classical EM in four equations |
| Superposition | Linearity enables decomposition of complex problems |
| Gauge invariance | Fundamental symmetry; template for all gauge theories |
| Electromagnetic waves | Light is an EM wave; optics unified with EM |
| Covariant formulation | EM demands special relativity; $\vec{E}$ and $\vec{B}$ are frame-dependent aspects of $F^{\mu\nu}$ |
| Boundary conditions | Key to solving practical problems (waveguides, cavities, interfaces) |
| Multipole expansion | Systematic approximation for distant fields |
| Retarded potentials | Causality in EM; finite speed of information |

---

## Recommended References

1. **Griffiths** — *Introduction to Electrodynamics* (4th ed.). The best undergraduate text. Clear, well-motivated, excellent problems.
2. **Jackson** — *Classical Electrodynamics* (3rd ed.). The graduate standard. Comprehensive but demanding. Essential reference.
3. **Purcell & Morin** — *Electricity and Magnetism* (3rd ed.). Beautiful treatment emphasizing relativity from the start.
4. **Zangwill** — *Modern Electrodynamics*. Modern graduate text; excellent alternative to Jackson.
5. **Landau & Lifshitz** — *The Classical Theory of Fields* (Vol. 2). Relativistic EM done right.
6. **Schwinger et al.** — *Classical Electrodynamics*. Advanced; Green's function methods.

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
