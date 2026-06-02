---
title: "Course: Quantum Mechanics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, physics, quantum-mechanics]
prerequisites: [linear algebra, ODEs/PDEs, classical-mechanics, probability]
---

# Quantum Mechanics

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[classical-mechanics]], [[electromagnetism]], [[statistical-mechanics]], [[mri-physics]], [[neuroscience]]*

## Motivation

Quantum mechanics is the framework underlying all of modern physics and chemistry. It governs atomic structure, chemical bonding, solid-state physics, nuclear physics, and particle physics. For Daniel's work, the spin physics of quantum mechanics is the direct foundation of nuclear magnetic resonance and MRI (see [[mri-physics]]). Quantum computing, quantum information, and quantum sensing all require deep fluency in this formalism. Understanding measurement, entanglement, and decoherence is increasingly relevant to engineering applications.

## Prerequisites

- **Linear algebra:** Vector spaces, inner products, eigenvalue problems, Hermitian and unitary matrices, tensor products.
- **ODEs and PDEs:** Separation of variables, Sturm-Liouville theory, special functions.
- **Classical mechanics:** Hamiltonian formulation, Poisson brackets (see [[classical-mechanics]]).
- **Probability and statistics:** Probability distributions, expectation values, variance.

---

## I. Historical Foundations and Wave-Particle Duality

### 1.1 The Crises of Classical Physics

- Blackbody radiation: ultraviolet catastrophe, Planck's quantization $E = nh\nu$.
- Photoelectric effect: Einstein's photon hypothesis $E = h\nu$, work function.
- Compton scattering: photon momentum $p = h/\lambda$.
- Atomic spectra: discrete emission lines, Balmer series.
- Bohr model: quantized orbits, $E_n = -13.6/n^2$ eV. Successes and failures.

### 1.2 Wave-Particle Duality

- de Broglie hypothesis: $\lambda = h/p$.
- Davisson-Germer experiment: electron diffraction.
- Double-slit experiment: interference of single particles. The central mystery.
- Complementarity (Bohr): wave and particle aspects are complementary, never simultaneously observed.

### 1.3 Wave Packets and Uncertainty

- Wave packet as superposition: $\psi(x,t) = \int \phi(k) e^{i(kx - \omega t)} dk$.
- Group velocity vs. phase velocity.
- Heisenberg uncertainty principle: $\Delta x \Delta p \geq \hbar/2$.
- Energy-time uncertainty: $\Delta E \Delta t \geq \hbar/2$ (careful interpretation).

---

## II. The Schrodinger Equation

### 2.1 Time-Dependent Schrodinger Equation

- Postulate: $i\hbar \frac{\partial}{\partial t}|\psi\rangle = \hat{H}|\psi\rangle$.
- Position representation: $i\hbar \frac{\partial \psi}{\partial t} = -\frac{\hbar^2}{2m}\nabla^2\psi + V\psi$.
- Probability interpretation: $|\psi(x,t)|^2$ as probability density. Normalization.
- Probability current: $\vec{j} = \frac{\hbar}{2mi}(\psi^*\nabla\psi - \psi\nabla\psi^*)$.
- Continuity equation: $\partial\rho/\partial t + \nabla \cdot \vec{j} = 0$.

### 2.2 Time-Independent Schrodinger Equation

- Separation of variables: $\psi(x,t) = \phi(x)e^{-iEt/\hbar}$.
- Eigenvalue equation: $\hat{H}\phi = E\phi$.
- Stationary states. Time evolution of general states as superposition.

### 2.3 One-Dimensional Problems

- **Infinite square well:** Quantized energies $E_n = n^2\pi^2\hbar^2/(2mL^2)$. Orthonormal eigenfunctions.
- **Finite square well:** Transcendental equations for bound states. Penetration into classically forbidden regions.
- **Harmonic oscillator:** Analytic solution (Hermite polynomials) and algebraic solution (ladder operators $\hat{a}, \hat{a}^\dagger$). $E_n = (n + 1/2)\hbar\omega$. Zero-point energy. Coherent states.
- **Free particle:** Continuous spectrum, plane waves, wave packets.
- **Delta function potential:** Bound state and scattering.
- **Barrier penetration / tunneling:** Transmission coefficient. Applications: alpha decay, scanning tunneling microscope, tunnel diodes.

---

## III. Mathematical Formalism

### 3.1 Hilbert Space

- State vectors $|\psi\rangle$ in a complex Hilbert space.
- Inner product: $\langle\phi|\psi\rangle$. Norm and normalization.
- Completeness: $\sum_n |n\rangle\langle n| = \hat{I}$ (discrete), $\int |x\rangle\langle x| dx = \hat{I}$ (continuous).
- Square-integrability. Rigged Hilbert space (for continuous spectra).

### 3.2 Dirac Notation

- Kets $|\ \rangle$, bras $\langle\ |$, brackets $\langle\ |\ \rangle$.
- Representations: position $\langle x|\psi\rangle = \psi(x)$, momentum $\langle p|\psi\rangle = \tilde{\psi}(p)$.
- Change of basis. Resolution of identity.

### 3.3 Operators

- Linear operators. Hermitian (self-adjoint) operators: $\hat{A}^\dagger = \hat{A}$.
- Observables as Hermitian operators. Real eigenvalues, orthogonal eigenstates.
- Position operator $\hat{x}$, momentum operator $\hat{p} = -i\hbar\partial/\partial x$.
- Projection operators: $\hat{P}_n = |n\rangle\langle n|$.
- Unitary operators: $\hat{U}^\dagger\hat{U} = \hat{I}$. Time evolution operator $\hat{U}(t) = e^{-i\hat{H}t/\hbar}$.

### 3.4 Commutators and Uncertainty

- Commutator: $[\hat{A}, \hat{B}] = \hat{A}\hat{B} - \hat{B}\hat{A}$.
- Canonical commutation relation: $[\hat{x}, \hat{p}] = i\hbar$.
- Generalized uncertainty principle: $\Delta A \Delta B \geq \frac{1}{2}|\langle[\hat{A}, \hat{B}]\rangle|$.
- Compatible observables: $[\hat{A}, \hat{B}] = 0$ implies simultaneous eigenstates (complete set of commuting observables, CSCO).

### 3.5 Postulates of Quantum Mechanics

1. States are vectors in Hilbert space.
2. Observables are Hermitian operators.
3. Measurement yields an eigenvalue; state collapses to corresponding eigenstate.
4. Probability of outcome $a_n$: $P(a_n) = |\langle a_n|\psi\rangle|^2$.
5. Time evolution: Schrodinger equation.
6. Identical particles: symmetrization (bosons) or antisymmetrization (fermions).

---

## IV. Angular Momentum

### 4.1 Orbital Angular Momentum

- $\hat{L} = \hat{r} \times \hat{p}$.
- Commutation relations: $[\hat{L}_i, \hat{L}_j] = i\hbar\epsilon_{ijk}\hat{L}_k$.
- $[\hat{L}^2, \hat{L}_z] = 0$: simultaneous eigenstates $|l, m\rangle$.
- Eigenvalues: $L^2 = l(l+1)\hbar^2$, $L_z = m\hbar$, $m = -l, \ldots, l$.
- Spherical harmonics $Y_l^m(\theta, \phi)$.

### 4.2 Spin

- Intrinsic angular momentum with no classical analog.
- Spin-1/2: Pauli matrices $\sigma_x, \sigma_y, \sigma_z$. Spinor representation.
- Stern-Gerlach experiment: quantization of spin projections.
- **Spin in magnetic fields:** $\hat{H} = -\vec{\mu} \cdot \vec{B} = -\gamma \hat{\vec{S}} \cdot \vec{B}$. Larmor precession at $\omega_L = \gamma B$. This is the foundation of NMR/MRI — see [[mri-physics]].
- Spin-1 systems. General spin-$s$ representations.

### 4.3 Addition of Angular Momentum

- Tensor product space: $|j_1, m_1\rangle \otimes |j_2, m_2\rangle$.
- Total angular momentum: $\hat{J} = \hat{J}_1 + \hat{J}_2$.
- Clebsch-Gordan coefficients: $|j, m\rangle = \sum_{m_1, m_2} \langle j_1 m_1; j_2 m_2 | j m \rangle |j_1 m_1\rangle|j_2 m_2\rangle$.
- Triangle rule: $|j_1 - j_2| \leq j \leq j_1 + j_2$.
- Addition of two spin-1/2: singlet and triplet states.

---

## V. Three-Dimensional Problems

### 5.1 Central Potentials

- Separation in spherical coordinates: $\psi(r,\theta,\phi) = R(r) Y_l^m(\theta,\phi)$.
- Radial equation with effective potential.

### 5.2 The Hydrogen Atom

- Coulomb potential: $V(r) = -e^2/(4\pi\epsilon_0 r)$.
- Energy levels: $E_n = -13.6\text{ eV}/n^2$. Degeneracy: $n^2$ (or $2n^2$ with spin).
- Radial wave functions: associated Laguerre polynomials.
- Quantum numbers: $n, l, m_l, m_s$. Selection rules.
- Fine structure: relativistic correction, spin-orbit coupling. $H_{\text{so}} = \frac{1}{2m^2c^2}\frac{1}{r}\frac{dV}{dr}\hat{L}\cdot\hat{S}$.
- Hyperfine structure: nuclear spin interaction. 21 cm line.
- Lamb shift (brief): QED correction.

### 5.3 The 3D Harmonic Oscillator

- Cartesian separation: $E = (n_x + n_y + n_z + 3/2)\hbar\omega$.
- Spherical separation: degeneracy structure.

---

## VI. Approximation Methods

### 6.1 Time-Independent Perturbation Theory

- **Non-degenerate case:**
  - First-order energy: $E_n^{(1)} = \langle n^{(0)}|H'|n^{(0)}\rangle$.
  - First-order state: $|n^{(1)}\rangle = \sum_{m \neq n} \frac{\langle m^{(0)}|H'|n^{(0)}\rangle}{E_n^{(0)} - E_m^{(0)}} |m^{(0)}\rangle$.
  - Second-order energy.
- **Degenerate case:** Diagonalize $H'$ within the degenerate subspace.
- Applications: Stark effect (hydrogen in electric field), Zeeman effect (hydrogen in magnetic field — directly relevant to [[mri-physics]]).

### 6.2 Variational Principle

- $E_{\text{ground}} \leq \langle\psi_{\text{trial}}|H|\psi_{\text{trial}}\rangle / \langle\psi_{\text{trial}}|\psi_{\text{trial}}\rangle$ for any trial state.
- Optimization over parameters.
- Application: helium ground state energy.

### 6.3 WKB Approximation

- Semiclassical limit: $\psi \sim A(x) e^{i\phi(x)/\hbar}$.
- Connection formulas at turning points.
- Bohr-Sommerfeld quantization: $\oint p\, dx = (n + 1/2) h$.
- Tunneling rate through a barrier.

### 6.4 Time-Dependent Perturbation Theory

- Transition probability: $P_{i \to f}(t) = \frac{1}{\hbar^2}|\int_0^t \langle f|H'(t')|i\rangle e^{i\omega_{fi}t'} dt'|^2$.
- Fermi's golden rule: $\Gamma_{i \to f} = \frac{2\pi}{\hbar}|\langle f|H'|i\rangle|^2 \rho(E_f)$.
- Selection rules for electric dipole transitions.
- Absorption and stimulated emission. Einstein A and B coefficients.

---

## VII. Scattering Theory

### 7.1 Partial Wave Analysis

- Scattering amplitude $f(\theta)$, differential cross section $d\sigma/d\Omega = |f(\theta)|^2$.
- Partial wave expansion: $f(\theta) = \sum_l (2l+1) f_l P_l(\cos\theta)$.
- Phase shifts $\delta_l$. Optical theorem.

### 7.2 Born Approximation

- First Born approximation: $f(\vec{q}) \propto \int V(\vec{r}) e^{i\vec{q}\cdot\vec{r}} d^3r$.
- Fourier transform of the potential.
- Application: Coulomb scattering recovers Rutherford formula.

---

## VIII. Identical Particles

### 8.1 Symmetrization Postulate

- Identical particles are truly indistinguishable.
- Bosons: symmetric wave function. Fermions: antisymmetric wave function.
- Spin-statistics theorem (stated without proof; requires QFT).

### 8.2 Pauli Exclusion Principle

- No two fermions can occupy the same quantum state.
- Consequences: periodic table, electron configurations, white dwarfs, neutron stars.

### 8.3 Exchange Interaction

- Exchange energy (not a force but a quantum effect).
- Singlet vs. triplet states of two electrons.
- Helium atom: parahelium and orthohelium.

---

## IX. Entanglement and the Measurement Problem

### 9.1 Entanglement

- Entangled states: $|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle|1\rangle - |1\rangle|0\rangle)$ (Bell state).
- Non-separability. Reduced density matrix of a subsystem.
- EPR argument and Bell's theorem. Bell inequalities. Experimental violation (Aspect, Clauser).
- No-cloning theorem. Quantum teleportation.

### 9.2 Density Matrices

- Pure states: $\hat{\rho} = |\psi\rangle\langle\psi|$.
- Mixed states: $\hat{\rho} = \sum_i p_i |\psi_i\rangle\langle\psi_i|$, $\text{Tr}(\hat{\rho}^2) < 1$.
- Expectation values: $\langle\hat{A}\rangle = \text{Tr}(\hat{\rho}\hat{A})$.
- Von Neumann entropy: $S = -\text{Tr}(\hat{\rho} \ln \hat{\rho})$.
- Decoherence: interaction with environment drives pure states to mixed states. Pointer basis.

### 9.3 The Measurement Problem

- Wave function collapse: what constitutes a "measurement"?
- Interpretations (survey, not advocacy):
  - **Copenhagen:** Measurement is primitive; collapse is real.
  - **Many-worlds (Everett):** No collapse; universal wave function branches.
  - **Decoherent histories:** Consistent sets of histories.
  - **Pilot wave (de Broglie-Bohm):** Deterministic; hidden variables (non-local).
  - **QBism:** Probabilities are subjective (Bayesian).
- Decoherence as a partial resolution: explains the appearance of collapse without solving the problem of outcomes.

---

## X. Applications

### Chemistry

- Molecular orbital theory from quantum mechanics.
- Chemical bonding: LCAO, hybridization.
- Spectroscopy: rotational, vibrational, electronic transitions.
- Computational chemistry: Hartree-Fock, DFT (density functional theory).

### Quantum Computing

- Qubit: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$.
- Quantum gates: Hadamard, CNOT, phase gates. Universality.
- Quantum algorithms: Deutsch-Jozsa, Grover's search, Shor's factoring.
- Quantum error correction (brief).
- Decoherence as the fundamental obstacle.

### MRI / NMR Physics

- Spin-1/2 in magnetic field → Larmor precession (Section IV.2).
- Ensemble of spins → net magnetization (see [[mri-physics]] and [[statistical-mechanics]]).
- RF pulses as spin rotations: $\hat{U} = e^{-i\hat{H}t/\hbar}$ with $\hat{H} = -\gamma\hbar\hat{I}\cdot\vec{B}$.
- Relaxation: $T_1$, $T_2$ from spin-environment interactions (open quantum systems / density matrix formalism).
- Chemical shift from electron shielding (perturbation theory applied to nuclear spin Hamiltonian).

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Wave function | Complete description of a quantum state |
| Superposition | States can be added; interference results |
| Measurement / collapse | Observation changes the state (or appears to) |
| Uncertainty principle | Fundamental limit, not experimental limitation |
| Commutators | Encode compatibility of observables |
| Spin | Intrinsic quantum number; no classical analog; basis of MRI |
| Entanglement | Non-classical correlations; resource for quantum info |
| Perturbation theory | Workhorse for approximate solutions |
| Identical particles | Bosons vs. fermions; Pauli exclusion |
| Density matrix | Mixed states, decoherence, open systems |

---

## Recommended References

1. **Griffiths & Schroeter** — *Introduction to Quantum Mechanics* (3rd ed.). Clear, accessible undergraduate text.
2. **Sakurai & Napolitano** — *Modern Quantum Mechanics* (3rd ed.). The standard graduate text. Spin-first approach.
3. **Shankar** — *Principles of Quantum Mechanics* (2nd ed.). Thorough mathematical treatment.
4. **Cohen-Tannoudji, Diu, Laloe** — *Quantum Mechanics* (2 vols.). Encyclopedic. Excellent complements and applications.
5. **Weinberg** — *Lectures on Quantum Mechanics* (2nd ed.). Modern, axiomatic approach.
6. **Nielsen & Chuang** — *Quantum Computation and Quantum Information*. For the quantum computing track.
7. **Levitt** — *Spin Dynamics* (2nd ed.). NMR-focused quantum mechanics; directly relevant to [[mri-physics]].

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
