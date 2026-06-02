---
title: "Survey: Number Theory"
type: course
subtype: survey
status: active
created: 2026-03-22
tags: [knowledge, course, mathematics, number-theory, survey]
prerequisites: [abstract-algebra, real-analysis, complex-analysis-basics]
---

# Number Theory (Survey)

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
> *Related: [[complex-analysis]], [[topology]], [[information-theory]]*

> [!info] Detailed Sub-Courses
> This is the **overview survey**. For in-depth treatment, see:
> - [[elementary-number-theory|Elementary Number Theory]] — Divisibility, primes, congruences, quadratic reciprocity
> - [[analytic-number-theory|Analytic Number Theory]] — Riemann zeta, PNT, L-functions, sieve methods
> - [[algebraic-number-theory|Algebraic Number Theory]] — Number fields, class groups, $p$-adic numbers
> - [[cryptographic-number-theory|Cryptographic Number Theory]] — RSA, ECC, lattice-based, post-quantum

---

## 1. Motivation

Number theory, the "queen of mathematics" (Gauss), is the study of the integers and their generalizations. Its questions are often easy to state — Is every even number greater than 2 the sum of two primes? How are the primes distributed? — but their answers draw on the deepest ideas in all of mathematics: complex analysis, algebraic geometry, representation theory, and topology.

Beyond its intrinsic beauty, number theory is the foundation of modern cryptography. RSA, Diffie-Hellman, and elliptic curve cryptography all rely on the computational difficulty of number-theoretic problems. The interplay between the pure and applied sides is one of the great stories of 20th-century mathematics.

## 2. Prerequisites

- **Abstract algebra:** Groups, rings, fields, polynomial rings, quotient structures.
- **Real analysis:** Sequences, series, asymptotic notation.
- **Complex analysis basics:** Analytic functions, contour integrals, residues (for analytic number theory). See [[complex-analysis]].

---

## 3. Detailed Topic Outline

### Part I: Elementary Number Theory

#### 3.1 Divisibility and the Euclidean Algorithm

- Divisibility, greatest common divisor, least common multiple.
- **Division algorithm:** a = bq + r with 0 ≤ r < b.
- **Euclidean algorithm:** Computes gcd(a, b) in O(log min(a,b)) steps.
- **Bezout's identity:** gcd(a, b) = ax + by for some integers x, y. Extended Euclidean algorithm computes x, y.
- **Intuition:** The integers are a Euclidean domain — the Euclidean algorithm is the engine that drives elementary number theory.

#### 3.2 Primes and the Fundamental Theorem of Arithmetic

- **Prime numbers:** p > 1 with no divisors other than 1 and p.
- **Fundamental Theorem of Arithmetic (FTA).** Every integer n > 1 factors uniquely (up to order) as a product of primes.
- **Intuition:** Primes are the "atoms" of multiplication. FTA says this atomic decomposition is unique — not obvious, and fails in some rings (e.g., Z[√-5]).
- Euclid's proof that there are infinitely many primes.
- Sieve of Eratosthenes.

#### 3.3 Congruences and Modular Arithmetic

- **Congruence:** a ≡ b (mod m) means m | (a - b).
- Z/mZ as a ring. Units (Z/mZ)* and Euler's totient φ(m).
- **Fermat's Little Theorem:** a^{p-1} ≡ 1 (mod p) for gcd(a, p) = 1.
- **Euler's theorem:** a^{φ(m)} ≡ 1 (mod m) for gcd(a, m) = 1.
- **Chinese Remainder Theorem (CRT):** If gcd(m_i, m_j) = 1, the system x ≡ a_i (mod m_i) has a unique solution mod m_1 · · · m_k.
  - *Intuition:* Z/mnZ ≅ Z/mZ × Z/nZ when gcd(m,n) = 1. The integers "decompose" along coprime moduli.
- **Wilson's theorem:** (p-1)! ≡ -1 (mod p).
- Hensel's lemma: lifting solutions from mod p to mod p^k.

#### 3.4 Quadratic Residues and Quadratic Reciprocity

- **Quadratic residue:** a is a QR mod p if x^2 ≡ a (mod p) is solvable.
- **Legendre symbol** (a/p) ∈ {-1, 0, 1}.
- **Euler's criterion:** (a/p) ≡ a^{(p-1)/2} (mod p).
- **Law of Quadratic Reciprocity (Gauss).** For odd primes p ≠ q:
  (p/q)(q/p) = (-1)^{(p-1)(q-1)/4}.
- Supplements: (-1/p) = (-1)^{(p-1)/2} and (2/p) = (-1)^{(p^2-1)/8}.
- **Intuition:** Whether p is a square mod q is reciprocally related to whether q is a square mod p. This is surprising and deep — Gauss gave 8 proofs. Higher reciprocity laws (cubic, quartic, Artin) drove the development of algebraic number theory and class field theory.
- **Jacobi symbol** and its computational utility.

#### 3.5 Arithmetic Functions

- **Multiplicative functions:** f(mn) = f(m)f(n) when gcd(m,n) = 1.
- Key examples:
  - φ(n): Euler's totient.
  - τ(n): number of divisors.
  - σ(n): sum of divisors.
  - μ(n): Mobius function (μ(1) = 1, μ(p_1...p_k) = (-1)^k, μ(n) = 0 if p^2 | n).
- **Mobius inversion:** If g(n) = Σ_{d|n} f(d), then f(n) = Σ_{d|n} μ(n/d) g(d).
- **Dirichlet series** and Euler products: Σ f(n)/n^s = Π_p (Σ f(p^k)/p^{ks}).
- Convolution: (f * g)(n) = Σ_{d|n} f(d) g(n/d). Multiplicative functions form a group under convolution.

#### 3.6 Continued Fractions

- Simple continued fractions: a = a_0 + 1/(a_1 + 1/(a_2 + ...)).
- Convergents p_n/q_n: best rational approximations.
- Finite CF ⟺ rational. Eventually periodic CF ⟺ quadratic irrational.
- Application: solving Pell's equation x^2 - Dy^2 = 1.
- **Intuition:** Continued fractions reveal the "multiplicative structure" of a real number. The golden ratio has the simplest CF: [1; 1, 1, 1, ...].

### Part II: Analytic Number Theory

#### 3.7 Distribution of Primes

- **Prime counting function** π(x) = #{primes ≤ x}.
- Chebyshev's bounds: c_1 x/log x ≤ π(x) ≤ c_2 x/log x.
- **Prime Number Theorem (PNT).** π(x) ~ x/log x as x → ∞.
  - Equivalently: the n-th prime p_n ~ n log n.
  - *Intuition:* The "probability" that a random integer near x is prime is approximately 1/log x.
- **Proof outline** (Hadamard, de la Vallee Poussin, 1896): Uses the Riemann zeta function and the fact that ζ(s) has no zeros on the line Re(s) = 1. See [[complex-analysis]].
- Stronger forms: π(x) = Li(x) + O(x exp(-c√(log x))), where Li(x) = ∫_2^x dt/log t.
- Primes in arithmetic progressions: **Dirichlet's theorem** — if gcd(a, m) = 1, there are infinitely many primes p ≡ a (mod m). Proved using L-functions.

#### 3.8 The Riemann Zeta Function

- **Definition:** ζ(s) = Σ_{n=1}^∞ 1/n^s for Re(s) > 1.
- **Euler product:** ζ(s) = Π_p (1 - p^{-s})^{-1}. Encodes the fundamental theorem of arithmetic analytically.
- **Analytic continuation** to all of C \ {1}, with a simple pole at s = 1.
- **Functional equation:** ξ(s) = ξ(1-s) where ξ(s) = π^{-s/2} Γ(s/2) ζ(s).
- **Trivial zeros** at s = -2, -4, -6, ...
- **Riemann Hypothesis (RH).** All non-trivial zeros of ζ(s) lie on the critical line Re(s) = 1/2.
  - *Significance:* RH implies the best possible error term in the PNT: π(x) = Li(x) + O(√x log x).
  - Verified numerically for the first 10^{13}+ zeros. Unproven since 1859.
- Special values: ζ(2) = π^2/6 (Basel problem), ζ(2n) ∈ π^{2n} Q. Values at odd integers remain mysterious (Apery: ζ(3) is irrational).

#### 3.9 Dirichlet L-Functions and Characters

- **Dirichlet character** χ: (Z/mZ)* → C*, extended to Z.
- **L-function:** L(s, χ) = Σ χ(n)/n^s. Euler product: Π_p (1 - χ(p)p^{-s})^{-1}.
- L(1, χ) ≠ 0 for χ ≠ χ_0 — the key input for Dirichlet's theorem on primes in progressions.
- **Generalized Riemann Hypothesis:** All nontrivial zeros of L(s, χ) lie on Re(s) = 1/2.

### Part III: Algebraic Number Theory

#### 3.10 Number Fields and Rings of Integers

- **Number field** K = Q(α): a finite extension of Q.
- **Ring of integers** O_K: the integral closure of Z in K. Example: Z[i] for K = Q(i), Z[ω] for K = Q(ω) with ω = e^{2πi/3}.
- O_K is a Dedekind domain: every nonzero ideal factors uniquely into prime ideals.
- **Intuition:** Unique factorization of elements may fail (e.g., in Z[√-5]: 6 = 2·3 = (1+√-5)(1-√-5)), but unique factorization of ideals always holds. This was Dedekind's brilliant rescue of FTA in general number rings.
- Norm of an ideal; ramification, splitting, inertia of primes.

#### 3.11 Class Groups and Units

- **Class group** Cl(K) = (fractional ideals) / (principal ideals). Measures the failure of unique factorization of elements.
- **Class number** h_K = |Cl(K)|. h_K = 1 iff O_K is a PID (unique factorization of elements holds).
- **Finiteness of the class number** (Minkowski's theorem, geometry of numbers).
  - *Intuition:* Minkowski's lattice point theorem — a convex body in R^n large enough relative to the volume of a lattice must contain a lattice point. Applied to ideal classes in the Minkowski embedding.
- **Dirichlet's unit theorem:** O_K* ≅ Z^{r_1+r_2-1} × (roots of unity), where r_1, r_2 are the numbers of real and complex embeddings.
- Regulator and its role in the class number formula.

#### 3.12 Quadratic Fields and Binary Quadratic Forms

- Q(√d): ring of integers, discriminant, class number.
- **Which primes are representable as x^2 + ny^2?** — answered by class field theory.
- Genus theory of Gauss.
- Imaginary quadratic fields: finite class numbers, connection to complex multiplication.
- Real quadratic fields: infinite unit groups (fundamental unit via continued fractions).

### Part IV: Elliptic Curves and Cryptography

#### 3.13 Elliptic Curves

- An elliptic curve over a field K: E: y^2 = x^3 + ax + b (char ≠ 2, 3, discriminant ≠ 0).
- **Group law:** The set E(K) ∪ {O} forms an abelian group using the chord-tangent construction.
- **Mordell's theorem (Mordell-Weil).** E(Q) is a finitely generated abelian group: E(Q) ≅ Z^r ⊕ E(Q)_{tors}.
  - The rank r is mysterious and conjecturally related to L-functions (BSD conjecture).
- **Hasse's theorem:** |#E(F_p) - (p+1)| ≤ 2√p. The number of points over a finite field is close to p+1.
- Torsion: Mazur's theorem classifies possible torsion groups of E(Q).
- j-invariant; isomorphism classes.
- Modularity theorem (Wiles et al.): Every elliptic curve over Q is modular. This proved Fermat's Last Theorem.

#### 3.14 Elliptic Curve Cryptography (ECC)

- **Discrete logarithm problem on E(F_p):** Given P and Q = nP, find n. No known subexponential algorithm (unlike Z/pZ).
- **ECDH (Elliptic Curve Diffie-Hellman):** Key exchange using the DLP on E.
- **ECDSA (Elliptic Curve Digital Signature Algorithm):** Digital signatures.
- Advantages over RSA: comparable security at much smaller key sizes (256-bit ECC ~ 3072-bit RSA).
- Curve selection: NIST curves (P-256, P-384), Curve25519, Ed25519.
- **Pairing-based cryptography:** Weil and Tate pairings; applications to identity-based encryption, BLS signatures.

#### 3.15 Other Cryptographic Applications

- **RSA:** Based on difficulty of factoring n = pq. Relies on Euler's theorem.
- **Primality testing:** Miller-Rabin (probabilistic), AKS (deterministic polynomial time).
- **Factoring algorithms:** Trial division, Pollard's rho, quadratic sieve, number field sieve.
- **Lattice-based cryptography (post-quantum):** Shortest vector problem, LWE. Connections to geometry of numbers.

---

## 4. Key Theorems — Summary

| Theorem | Statement (abbreviated) | Significance |
|---------|------------------------|--------------|
| Fundamental Theorem of Arithmetic | Unique prime factorization in Z | The structural bedrock |
| Quadratic Reciprocity | (p/q)(q/p) = (-1)^{(p-1)(q-1)/4} | Governs solvability of quadratic congruences |
| Dirichlet's Theorem | Infinitely many primes in a + mZ (gcd(a,m)=1) | Primes are equidistributed in residue classes |
| Prime Number Theorem | π(x) ~ x/log x | Quantitative distribution of primes |
| Unique Factorization of Ideals | Every ideal in O_K factors uniquely into primes | Rescues unique factorization in number rings |
| Finiteness of Class Number | Cl(K) is finite | Failure of unique factorization is bounded |
| Dirichlet Unit Theorem | O_K* ≅ Z^{r_1+r_2-1} × μ | Structure of units in number rings |
| Mordell-Weil | E(Q) is finitely generated | Rational points on elliptic curves are tractable |
| Hasse Bound | |#E(F_p) - p - 1| ≤ 2√p | Point counts cluster around p+1 |
| Modularity (Wiles) | Every E/Q is modular | Proved Fermat's Last Theorem |

---

## 5. Major Open Problems

- **Riemann Hypothesis:** Non-trivial zeros of ζ(s) have Re(s) = 1/2.
- **Goldbach's Conjecture:** Every even n > 2 is the sum of two primes.
- **Twin Prime Conjecture:** Infinitely many primes p with p+2 also prime. (Zhang 2013: bounded gaps; Maynard-Tao: gaps ≤ 246.)
- **Birch and Swinnerton-Dyer (BSD) Conjecture:** rank(E(Q)) = ord_{s=1} L(E, s).
- **abc Conjecture:** For coprime a + b = c, the radical rad(abc) is usually "large" relative to c.

---

## 6. Recommended References

1. **Hardy, G.H. & Wright, E.M.** *An Introduction to the Theory of Numbers.* — The classic. Encyclopedic.
2. **Ireland, K. & Rosen, M.** *A Classical Introduction to Modern Number Theory* (GTM 84). — Bridges elementary and algebraic.
3. **Neukirch, J.** *Algebraic Number Theory.* — The standard graduate text for algebraic methods.
4. **Silverman, J.H.** *The Arithmetic of Elliptic Curves* (GTM 106). — The standard for elliptic curves.
5. **Iwaniec, H. & Kowalski, E.** *Analytic Number Theory.* — Comprehensive and modern.
6. **Koblitz, N.** *A Course in Number Theory and Cryptography.* — For the applied side.
7. **Davenport, H.** *Multiplicative Number Theory.* — Focused on primes and L-functions.

---

## 7. Exercises and Milestones

- [ ] Prove the infinitude of primes (at least two different proofs).
- [ ] Implement the extended Euclidean algorithm and use it to find modular inverses.
- [ ] Prove Fermat's Little Theorem using group theory.
- [ ] Verify quadratic reciprocity for (3/7) and (7/3).
- [ ] Compute the continued fraction expansion of √7 and solve x^2 - 7y^2 = 1.
- [ ] Show that Z[√-5] is not a UFD by finding two distinct factorizations of 6.
- [ ] Prove that the class number of Q(√-5) is 2.
- [ ] Implement the group law on an elliptic curve over a finite field.
- [ ] Verify Hasse's bound for y^2 = x^3 + x over F_p for several primes p.
- [ ] Implement ECDH key exchange using Curve25519 (or a toy curve).

---

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
