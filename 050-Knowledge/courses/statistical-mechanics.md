---
title: "Course: Statistical Mechanics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, physics, statistical-mechanics, thermodynamics]
prerequisites: [classical-mechanics, quantum-mechanics, probability, multivariable-calculus]
---

# Statistical Mechanics

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[classical-mechanics]], [[quantum-mechanics]], [[biochemistry]], [[mri-physics]]*

## Motivation

Statistical mechanics bridges the microscopic world of atoms and quantum states to the macroscopic world of temperature, pressure, and entropy. It explains why thermodynamics works and provides the tools to compute thermodynamic quantities from first principles. Phase transitions, critical phenomena, and fluctuations are all within its domain. For MRI, the Boltzmann distribution determines the net magnetization of nuclear spins (the tiny energy splitting at room temperature explains why MRI signals are inherently weak). For biochemistry, enzyme kinetics and protein folding are fundamentally statistical mechanical problems.

## Prerequisites

- **Classical mechanics:** Hamiltonian formulation, phase space, Liouville's theorem.
- **Quantum mechanics:** Energy eigenvalues, degeneracy, identical particles, spin statistics.
- **Probability:** Combinatorics, probability distributions, central limit theorem.
- **Multivariable calculus:** Partial derivatives, Legendre transforms, Stirling's approximation.

---

## I. Foundations

### 1.1 Microstates and Macrostates

- **Microstate:** Complete specification of all microscopic degrees of freedom ($6N$ phase space coordinates classically, or a quantum state vector).
- **Macrostate:** Specification by macroscopic variables ($E$, $V$, $N$, $T$, $P$, etc.). Many microstates correspond to one macrostate.
- Multiplicity $\Omega(E, V, N)$: the number of microstates consistent with a macrostate.
- Phase space volume (classical): $\Omega \propto \int d^{3N}q\, d^{3N}p$ over the energy shell.

### 1.2 The Fundamental Postulate (Equal a Priori Probabilities)

- For an isolated system in equilibrium, all accessible microstates are equally probable.
- This is an axiom — not derivable from mechanics. Its justification is empirical success and ergodic theory (partial).

### 1.3 Entropy

- **Boltzmann entropy:** $S = k_B \ln \Omega$.
- **Gibbs entropy:** $S = -k_B \sum_i p_i \ln p_i$ (or $S = -k_B \text{Tr}(\hat{\rho} \ln \hat{\rho})$ quantum mechanically).
- Second law: entropy of an isolated system never decreases.
- Connection to information theory: Shannon entropy.

### 1.4 Temperature, Pressure, Chemical Potential

- $1/T = (\partial S/\partial E)_{V,N}$ — temperature as the "price" of energy in units of entropy.
- $P/T = (\partial S/\partial V)_{E,N}$.
- $\mu/T = -(\partial S/\partial N)_{E,V}$.
- Equilibrium conditions: thermal ($T_1 = T_2$), mechanical ($P_1 = P_2$), diffusive ($\mu_1 = \mu_2$).

---

## II. Ensembles

### 2.1 Microcanonical Ensemble (Fixed $E$, $V$, $N$)

- Isolated system. All microstates at energy $E$ equally probable.
- Entropy: $S(E, V, N) = k_B \ln \Omega(E, V, N)$.
- Example: two-state system (paramagnet). Counting with binomial coefficients.
- Example: Einstein solid. Multiplicity and Stirling's approximation.
- Negative temperature (population inversion): when $\Omega$ decreases with $E$.

### 2.2 Canonical Ensemble (Fixed $T$, $V$, $N$)

- System in thermal contact with a heat bath at temperature $T$.
- **Boltzmann distribution:** $P_i = \frac{e^{-E_i / k_B T}}{Z}$.
- **Partition function:** $Z(T, V, N) = \sum_i e^{-E_i / k_B T}$ (discrete) or $Z = \int e^{-H/k_BT} \frac{d^{3N}q\, d^{3N}p}{N! h^{3N}}$ (classical).
- Thermodynamics from $Z$:
  - Free energy: $F = -k_B T \ln Z$.
  - Energy: $\langle E \rangle = -\partial \ln Z / \partial \beta$ where $\beta = 1/k_BT$.
  - Entropy: $S = -\partial F / \partial T$.
  - Pressure: $P = -\partial F / \partial V$.
- **Energy fluctuations:** $\langle(\Delta E)^2\rangle = k_B T^2 C_V$. Relative fluctuations $\sim 1/\sqrt{N}$ → thermodynamic limit.
- Equivalence to microcanonical in the thermodynamic limit.

### 2.3 Grand Canonical Ensemble (Fixed $T$, $V$, $\mu$)

- System can exchange energy and particles with a reservoir.
- **Grand partition function:** $\mathcal{Z} = \sum_{N=0}^{\infty} e^{\beta\mu N} Z(T, V, N) = \sum_{N, i} e^{-\beta(E_i - \mu N)}$.
- **Grand potential:** $\Phi = -k_B T \ln \mathcal{Z} = F - \mu N = -PV$.
- Average particle number: $\langle N \rangle = k_B T \, \partial \ln \mathcal{Z} / \partial \mu$.
- Particle number fluctuations: $\langle(\Delta N)^2\rangle = k_B T \, \partial \langle N \rangle / \partial \mu$.

---

## III. Thermodynamic Potentials and Relations

### 3.1 Legendre Transforms

- Internal energy $U(S, V, N)$ → Helmholtz $F(T, V, N)$ → Gibbs $G(T, P, N)$, Enthalpy $H(S, P, N)$.
- Grand potential $\Phi(T, V, \mu)$.
- Natural variables for each potential.

### 3.2 Maxwell Relations

- From equality of mixed partial derivatives:
  - $(\partial T/\partial V)_S = -(\partial P/\partial S)_V$, etc.
- Systematic derivation from thermodynamic potentials.

### 3.3 Response Functions

- Heat capacities: $C_V = T(\partial S/\partial T)_V$, $C_P = T(\partial S/\partial T)_P$.
- Compressibility: $\kappa_T = -(1/V)(\partial V/\partial P)_T$.
- Thermal expansion: $\alpha = (1/V)(\partial V/\partial T)_P$.
- Relations between response functions: $C_P - C_V = TV\alpha^2/\kappa_T$.

---

## IV. Ideal Systems

### 4.1 Classical Ideal Gas

- Partition function: $Z = V^N / (N! \lambda_{\text{th}}^{3N})$ where $\lambda_{\text{th}} = h/\sqrt{2\pi m k_B T}$.
- Equation of state: $PV = Nk_BT$.
- Entropy: Sackur-Tetrode equation. Resolution of Gibbs paradox via $N!$.
- Equipartition theorem: $\langle E \rangle = \frac{f}{2}k_BT$ per degree of freedom (when energy is quadratic).

### 4.2 Diatomic and Polyatomic Gases

- Rotational and vibrational contributions.
- Freezing out of degrees of freedom at low temperature.
- Specific heat of diatomic gas: plateau structure $C_V = 3/2, 5/2, 7/2$ (in units of $Nk_B$).

### 4.3 Paramagnets

- Two-state system in magnetic field: $E = \pm \mu B$.
- Partition function, magnetization, susceptibility.
- Curie's law: $\chi \propto 1/T$.
- **Connection to MRI:** Nuclear spin-1/2 in external field $B_0$. Population difference $\Delta N/N \approx \gamma\hbar B_0 / (2k_BT)$. At 3T and 300K, $\Delta N/N \sim 10^{-5}$: the signal is incredibly weak, which is why MRI needs sensitive coils and signal averaging. See [[mri-physics]].

---

## V. Quantum Statistical Mechanics

### 5.1 Identical Particles and Occupation Numbers

- Single-particle states with energies $\epsilon_i$. Occupation number $n_i$.
- Grand partition function factorizes over single-particle states.

### 5.2 Fermi-Dirac Distribution (Fermions)

- $\langle n_i \rangle = \frac{1}{e^{\beta(\epsilon_i - \mu)} + 1}$.
- Fermi energy $E_F$, Fermi surface. $T = 0$: sharp step function.
- Low-temperature expansion: Sommerfeld expansion. Electronic specific heat $C_V \propto T$.
- Applications: electrons in metals, white dwarfs, neutron stars.

### 5.3 Bose-Einstein Distribution (Bosons)

- $\langle n_i \rangle = \frac{1}{e^{\beta(\epsilon_i - \mu)} - 1}$.
- $\mu \leq 0$ for massive bosons.
- Planck distribution for photons ($\mu = 0$): $\langle n \rangle = 1/(e^{\beta\hbar\omega} - 1)$.
- Blackbody radiation: Stefan-Boltzmann law, Wien's law.
- Phonons and Debye model: $C_V \propto T^3$ at low $T$.

### 5.4 Bose-Einstein Condensation

- Below critical temperature $T_c$, macroscopic occupation of ground state.
- $T_c \propto n^{2/3} / m$.
- Experimental realization in ultracold atomic gases (1995).
- Superfluidity connection.

---

## VI. Phase Transitions and Critical Phenomena

### 6.1 Classification

- **First-order transitions:** Discontinuity in first derivative of free energy (latent heat, density jump). Examples: melting, boiling.
- **Second-order (continuous) transitions:** Discontinuity in second derivative (specific heat, susceptibility diverge). No latent heat. Examples: ferromagnetic transition, superfluid transition.
- Order parameter: magnetization for ferromagnet, density difference for liquid-gas.

### 6.2 The Ising Model

- Hamiltonian: $H = -J\sum_{\langle ij \rangle} s_i s_j - h\sum_i s_i$, $s_i = \pm 1$.
- 1D Ising: exact solution (transfer matrix). No phase transition at $T > 0$.
- 2D Ising: Onsager's exact solution (1944). Phase transition at $T_c = 2J / (k_B \ln(1 + \sqrt{2}))$.
- 3D Ising: no exact solution; studied by numerical simulation and renormalization group.

### 6.3 Mean Field Theory

- Replace neighbor interactions with average (mean) field.
- Self-consistency equation: $m = \tanh(\beta J z m + \beta h)$.
- Predicts $T_c = Jz/k_B$ (overestimates due to neglect of fluctuations).
- Critical exponents in mean field: $\beta = 1/2$, $\gamma = 1$, $\delta = 3$, $\alpha = 0$ (discontinuous).

### 6.4 Landau Theory

- Free energy expanded in powers of order parameter: $F = F_0 + a(T)m^2 + bm^4 + \ldots$
- $a(T) = a_0(T - T_c)$: sign change drives transition.
- Predicts mean-field critical exponents.
- First-order transitions when cubic terms are present.
- Limitations: fails near $T_c$ in low dimensions (Ginzburg criterion).

### 6.5 Critical Phenomena

- **Universality:** Critical exponents depend only on dimensionality and symmetry of order parameter, not microscopic details.
- **Scaling relations:** $\alpha + 2\beta + \gamma = 2$, etc.
- **Renormalization group (conceptual):** Coarse-graining and flow in parameter space. Fixed points correspond to critical points. Wilson's breakthrough.
- **Correlation length:** $\xi \propto |T - T_c|^{-\nu}$. Diverges at $T_c$.

---

## VII. Fluctuations and Linear Response

### 7.1 Fluctuation-Dissipation Theorem

- Energy fluctuations ↔ heat capacity.
- Density fluctuations ↔ compressibility.
- Magnetization fluctuations ↔ susceptibility.
- General form: response function proportional to equilibrium correlation function.

### 7.2 Correlation Functions

- Pair correlation function: $g(r) = \langle \rho(\vec{r})\rho(0)\rangle / \langle\rho\rangle^2$.
- Ornstein-Zernike form near critical point.
- Static structure factor $S(k)$: measured by scattering experiments.

---

## VIII. Kinetic Theory and Non-Equilibrium

### 8.1 Boltzmann Equation

- Distribution function $f(\vec{r}, \vec{v}, t)$.
- Boltzmann equation: $\frac{\partial f}{\partial t} + \vec{v} \cdot \nabla f + \frac{\vec{F}}{m} \cdot \nabla_v f = \left(\frac{\partial f}{\partial t}\right)_{\text{coll}}$.
- Collision integral. Molecular chaos (Stosszahlansatz).
- H-theorem: $H = \int f \ln f\, d^3v$ decreases monotonically → approach to equilibrium.
- Maxwell-Boltzmann distribution as the equilibrium solution.

### 8.2 Transport Phenomena

- Diffusion: Fick's law, diffusion coefficient from random walks.
- Viscosity: momentum transport.
- Thermal conductivity: energy transport.
- Mean free path and transport coefficients from kinetic theory.

### 8.3 Non-Equilibrium Statistical Mechanics (Introduction)

- Linear response theory: Kubo formula.
- Onsager reciprocal relations.
- Master equation. Detailed balance.
- Langevin equation and Brownian motion.
- Fokker-Planck equation.
- Fluctuation theorems (Jarzynski equality, Crooks relation) — modern developments.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Boltzmann distribution | Foundation of thermal physics; connects to MRI signal |
| Partition function | Generates all thermodynamics |
| Ensembles | Different boundary conditions → different $Z$ |
| Fermi-Dirac / Bose-Einstein | Quantum statistics; explains metals, superfluids, lasers |
| Phase transitions | Emergence of qualitative change from quantitative variation |
| Universality | Critical behavior independent of microscopic details |
| Fluctuation-dissipation | Response and fluctuations are two sides of one coin |
| Boltzmann equation | Bridge from micro to macro; kinetic theory |
| Entropy | Information-theoretic and thermodynamic roles |

---

## Recommended References

1. **Pathria & Beale** — *Statistical Mechanics* (4th ed.). Comprehensive graduate text.
2. **Reif** — *Fundamentals of Statistical and Thermal Physics*. Classic; clear on fundamentals.
3. **Schroeder** — *Introduction to Thermal Physics*. Excellent undergraduate text.
4. **Kardar** — *Statistical Physics of Particles* and *Statistical Physics of Fields*. Modern two-volume treatment. Field theory approach in Vol. 2.
5. **Landau & Lifshitz** — *Statistical Physics Part 1* (Vol. 5). Elegant and concise.
6. **Sethna** — *Statistical Mechanics: Entropy, Order Parameters, and Complexity*. Modern; connections to information theory, biology, computation.
7. **Chandler** — *Introduction to Modern Statistical Mechanics*. Short, clear, chemical physics perspective.

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
