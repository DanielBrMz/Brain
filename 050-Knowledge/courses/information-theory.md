---
title: "Course: Information Theory"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, mathematics, information-theory]
prerequisites: [probability-theory, linear-algebra, real-analysis-basics]
---

# Information Theory

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
> *Related: [[number-theory]], [[functional-analysis]], [[complex-analysis]]*

---

## 1. Motivation

Information theory, founded by Claude Shannon in 1948, provides a mathematical framework for quantifying information, communication, and uncertainty. Its central concepts — entropy, mutual information, and channel capacity — answer fundamental questions: How much can data be compressed? How fast can data be transmitted reliably over a noisy channel?

What began as a theory of communication has become foundational across science and engineering. In machine learning, the cross-entropy loss function, KL divergence for variational inference, and the minimum description length principle all descend directly from Shannon's ideas. In physics, entropy connects to thermodynamics and black hole physics. In statistics, information-theoretic quantities measure the "value" of data.

## 2. Prerequisites

- **Probability theory:** Random variables, distributions, expectation, conditional probability, convergence.
- **Linear algebra:** Matrix operations, eigenvalues (for Gaussian channels, rate-distortion).
- **Real analysis basics:** Limits, series, logarithms, basic measure theory (for continuous case).

---

## 3. Detailed Topic Outline

### Part I: Entropy and Information Measures

#### 3.1 Entropy

- **Shannon entropy** of a discrete random variable X with PMF p:
  H(X) = -Σ_x p(x) log p(x)  (convention: 0 log 0 = 0).
- Units: bits (log base 2), nats (natural log).
- **Intuition:** H(X) measures the average "surprise" or "uncertainty" in X. A fair coin has H = 1 bit; a biased coin has H < 1 bit. Entropy is maximized by the uniform distribution.
- Properties:
  - H(X) ≥ 0, with equality iff X is deterministic.
  - H(X) ≤ log |X| (X = alphabet), with equality iff X is uniform.
  - Concavity: H is a concave function of the distribution p.
- Binary entropy: H_b(p) = -p log p - (1-p) log(1-p).
- **Joint entropy** H(X, Y) and **conditional entropy** H(Y|X) = H(X,Y) - H(X).
  - H(Y|X) ≤ H(Y): conditioning reduces entropy (on average).
  - Chain rule: H(X_1, ..., X_n) = Σ H(X_i | X_1, ..., X_{i-1}).

#### 3.2 Mutual Information

- **Definition:** I(X; Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X,Y).
- **Intuition:** I(X;Y) is the reduction in uncertainty about X gained by observing Y. It measures the "information shared" between X and Y.
- I(X;Y) ≥ 0, with equality iff X and Y are independent.
- I(X;Y) = I(Y;X) (symmetry, unlike conditional entropy).
- **Conditional mutual information:** I(X; Y | Z) = H(X|Z) - H(X|Y,Z).
- **Chain rule for MI:** I(X_1, ..., X_n; Y) = Σ I(X_i; Y | X_1, ..., X_{i-1}).
- **Data processing inequality:** If X → Y → Z is a Markov chain, then I(X;Z) ≤ I(X;Y). Processing cannot create information.

#### 3.3 Kullback-Leibler Divergence

- **Definition:** D_{KL}(p ‖ q) = Σ_x p(x) log(p(x)/q(x)).
- **Intuition:** D_{KL} measures the "information cost" of using distribution q when the true distribution is p. It is not a distance (not symmetric, no triangle inequality), but it is always non-negative.
- **Gibbs' inequality:** D_{KL}(p ‖ q) ≥ 0, with equality iff p = q. Proved via Jensen's inequality.
- Relationship to entropy: H(X) = log|X| - D_{KL}(p ‖ uniform). Entropy measures "distance from uniformity."
- I(X;Y) = D_{KL}(p(x,y) ‖ p(x)p(y)). Mutual information is KL divergence from independence.
- **Pinsker's inequality:** ‖p - q‖_{TV} ≤ √(D_{KL}(p‖q)/2). Bounds total variation distance.

#### 3.4 Other Divergences and Information Measures

- **Cross-entropy:** H(p, q) = -Σ p(x) log q(x) = H(p) + D_{KL}(p ‖ q).
- **f-divergences:** D_f(p ‖ q) = Σ q(x) f(p(x)/q(x)) for convex f with f(1) = 0. KL, reverse KL, chi-squared, Hellinger, TV are all special cases.
- **Renyi entropy:** H_α(X) = (1/(1-α)) log Σ p(x)^α. Reduces to Shannon entropy as α → 1.
- **Fisher information:** I(θ) = E[(d/dθ log p(X;θ))^2]. Connection to Cramer-Rao bound, information geometry (see [[differential-geometry]]).

#### 3.5 Differential Entropy (Continuous Case)

- **Differential entropy:** h(X) = -∫ f(x) log f(x) dx for continuous RV with density f.
- Can be negative (unlike discrete entropy). Not invariant under change of variables.
- **Maximum entropy distributions:**
  - Support [a,b], no other constraint: uniform.
  - Fixed mean and variance: Gaussian. h(X) ≤ (1/2) log(2πeσ^2), with equality for Gaussian.
- **Intuition:** The Gaussian is the "most uncertain" distribution for a given variance — maximum entropy. This is why Gaussian channels and Gaussian noise are fundamental.

### Part II: Source Coding (Compression)

#### 3.6 Shannon's Source Coding Theorem

- **Lossless source coding:** Represent X^n faithfully using binary strings.
- **Entropy rate** of a stochastic process: H_∞ = lim H(X_n | X_1, ..., X_{n-1}).
- **Shannon's Source Coding Theorem (Noiseless Coding Theorem).**
  - The minimum average code length per symbol for an i.i.d. source is H(X) (in appropriate units).
  - Achievability: codes with average length ≤ H(X) + 1 exist (e.g., Huffman codes).
  - Converse: no code can achieve average length < H(X).
- **Intuition:** Entropy is the fundamental limit of compression. You cannot do better than H bits per symbol, and you can get arbitrarily close.
- **Asymptotic Equipartition Property (AEP):** For i.i.d. X_1, ..., X_n: -(1/n) log p(X_1, ..., X_n) → H(X) in probability. The "typical set" has ~2^{nH} elements.

#### 3.7 Practical Codes

- **Prefix-free codes:** No codeword is a prefix of another. Kraft's inequality: Σ 2^{-l_i} ≤ 1.
- **Huffman coding:** Optimal prefix-free code for known distributions.
- **Arithmetic coding:** Approaches entropy rate for long sequences.
- **Lempel-Ziv (LZ77/LZ78):** Universal compression — achieves entropy rate without knowing the source distribution. Basis of gzip, PNG, etc.

### Part III: Channel Coding (Reliable Communication)

#### 3.8 Channel Models

- **Discrete memoryless channel (DMC):** Defined by transition probabilities p(y|x).
- **Binary symmetric channel (BSC):** Flips each bit with probability p. Capacity = 1 - H_b(p).
- **Binary erasure channel (BEC):** Each bit is erased with probability ε. Capacity = 1 - ε.
- **Additive white Gaussian noise (AWGN):** Y = X + Z, Z ~ N(0, N). Capacity = (1/2) log(1 + P/N) (Shannon-Hartley).

#### 3.9 Channel Capacity and Shannon's Channel Coding Theorem

- **Channel capacity:** C = max_{p(x)} I(X; Y).
  - *Intuition:* C is the maximum rate at which information can be transmitted reliably over the channel.
- **Shannon's Channel Coding Theorem (Noisy Coding Theorem).**
  - *Achievability:* For any rate R < C, there exist codes with block length n and rate R such that the error probability → 0 as n → ∞.
  - *Converse:* For R > C, the error probability is bounded away from 0 for any code.
- **Intuition:** This is one of the most remarkable theorems in mathematics. It says that reliable communication is possible at any rate below capacity — not by making errors less likely for each symbol, but by encoding messages in cleverly structured blocks that spread information across many channel uses.
- Proof idea (achievability): Random coding — choose codewords at random, then show by the AEP that the probability of error is small (joint typicality decoding).
- Proof idea (converse): Fano's inequality.

#### 3.10 Practical Channel Codes

- Hamming codes, Reed-Solomon codes (algebraic).
- Convolutional codes and Viterbi decoding.
- **Turbo codes** (1993): Near-capacity performance via iterative decoding.
- **LDPC codes** (Gallager, rediscovered 1990s): Sparse random parity-check matrices. Near-capacity.
- **Polar codes** (Arikan, 2009): First provably capacity-achieving codes with efficient encoding/decoding. Based on channel polarization.

### Part IV: Rate-Distortion Theory

#### 3.11 Lossy Source Coding

- **Distortion measure** d(x, x̂): quantifies the cost of representing x by x̂.
- **Rate-distortion function:** R(D) = min_{p(x̂|x): E[d(X,X̂)]≤D} I(X; X̂).
  - R(D) is the minimum rate (bits per symbol) needed to represent X with average distortion ≤ D.
- **Shannon's rate-distortion theorem:** R(D) is achievable; rates below R(D) are not.
- Example: Gaussian source with squared error: R(D) = (1/2) log(σ^2/D) for D ≤ σ^2.
- **Intuition:** Rate-distortion theory is the "lossy" counterpart of source coding. It tells you the optimal tradeoff between compression and fidelity.

### Part V: Kolmogorov Complexity

#### 3.12 Algorithmic Information Theory

- **Kolmogorov complexity** K(x): the length of the shortest program (on a universal Turing machine) that outputs x.
- K(x) is **uncomputable** (halting problem), but well-defined up to an additive constant.
- A string is **random** (in the Kolmogorov sense) if K(x) ≥ |x| - O(1) — it cannot be compressed.
- **Connection to Shannon entropy:** For a random variable X, E[K(X)] ≈ H(X) (up to constants). Shannon entropy is the "average-case" version of Kolmogorov complexity.
- **Incompressibility method:** A powerful proof technique — most strings are incompressible, so there exists an incompressible string, and it must have nice properties.
- Connections to Godel's incompleteness, Chaitin's Omega.

### Part VI: Connections to Machine Learning

#### 3.13 Cross-Entropy Loss

- In classification, the cross-entropy loss is L = -Σ y_i log ŷ_i = H(p, q) where p = true labels, q = model predictions.
- Minimizing cross-entropy ⟺ minimizing D_{KL}(p ‖ q) (since H(p) is fixed).
- **Intuition:** Training a classifier with cross-entropy loss is equivalent to finding the distribution q closest to the data distribution p in KL divergence.

#### 3.14 Variational Inference and the ELBO

- Goal: approximate intractable posterior p(z|x) with tractable q(z).
- **Evidence Lower Bound (ELBO):** log p(x) ≥ E_q[log p(x,z)] - E_q[log q(z)] = ELBO.
  - Equivalently: log p(x) = ELBO + D_{KL}(q(z) ‖ p(z|x)).
- Maximizing ELBO ⟺ minimizing D_{KL}(q ‖ p(·|x)).
- **Variational Autoencoders (VAEs):** Encoder = q(z|x), decoder = p(x|z). Loss = reconstruction + KL regularization.
- **Intuition:** The ELBO decomposes the problem of learning a generative model into reconstruction accuracy and distributional fit, both measured information-theoretically.

#### 3.15 Minimum Description Length (MDL)

- **MDL principle:** The best model for data is the one that minimizes the total code length: L(model) + L(data | model).
- Two-part coding: encode the model, then encode the data using the model.
- Connection to Bayesian model selection via the coding interpretation of priors.
- **Intuition:** Occam's razor, formalized. Simpler models have shorter descriptions; complex data needs longer descriptions. The MDL principle trades off model complexity and fit.
- Normalized Maximum Likelihood (NML) and stochastic complexity.

#### 3.16 Information Bottleneck

- Given joint (X, Y), find a compressed representation T of X that maximally preserves information about Y.
- Minimize I(X; T) - β I(T; Y) for Lagrange multiplier β.
- Connection to deep learning: the information bottleneck hypothesis (Tishby) suggests deep networks learn by compressing X while retaining information about Y.
- Debate: the compression phase is observed in some settings but not universally.

#### 3.17 Other Connections

- **Maximum entropy classifiers:** Logistic regression as maximum entropy model.
- **Mutual information estimation:** MINE (Mutual Information Neural Estimation), InfoNCE.
- **Bits-back coding:** ANS + latent variable models.
- **Information-theoretic generalization bounds:** PAC-Bayes via KL, mutual information bounds on generalization gap.

---

## 4. Key Theorems — Summary

| Theorem | Statement (abbreviated) | Significance |
|---------|------------------------|--------------|
| Gibbs' Inequality | D_{KL}(p‖q) ≥ 0 | KL divergence is non-negative; foundation of most inequalities |
| Source Coding Theorem | Minimum avg code length = H(X) | Entropy is the compression limit |
| Channel Coding Theorem | Rates < C are achievable; rates > C are not | Reliable communication at any rate below capacity |
| AEP | -(1/n)log p(x^n) → H | Typical set has ~2^{nH} elements |
| Data Processing Inequality | X→Y→Z ⟹ I(X;Z) ≤ I(X;Y) | Processing cannot create information |
| Rate-Distortion | R(D) = min I(X;X̂) s.t. E[d]≤D | Optimal lossy compression rate |
| Shannon-Hartley | C = (1/2)log(1+SNR) | Capacity of Gaussian channel |

---

## 5. Applications

- **Communications:** Design of modems, WiFi (802.11), 5G, satellite links — all approach Shannon limits using LDPC/turbo/polar codes.
- **Data compression:** ZIP, JPEG, H.264/H.265, MP3 — all rooted in entropy coding and rate-distortion theory.
- **Machine learning:** Cross-entropy loss, VAEs, GANs (Jensen-Shannon divergence), mutual information regularization. See Sections 3.13-3.17.
- **Statistics:** Sufficient statistics (minimal sufficient ⟺ minimal I(X;T) preserving I(T;θ)), Fisher information, experiment design.
- **Physics:** Thermodynamic entropy (Boltzmann), Landauer's principle (erasing a bit costs kT ln 2 energy), black hole entropy (Bekenstein-Hawking), holographic principle.
- **Biology:** Neural coding, DNA information content, evolution as information accumulation.
- **Cryptography:** One-time pad (perfect secrecy requires key entropy ≥ message entropy). Connections to [[number-theory]].

---

## 6. Recommended References

1. **Cover, T. & Thomas, J.** *Elements of Information Theory* (2nd ed.). — The standard textbook. Clear, comprehensive, excellent problems.
2. **MacKay, D.** *Information Theory, Inference, and Learning Algorithms.* — Free online. Beautifully integrates IT with ML and Bayesian inference.
3. **Shannon, C.E.** *A Mathematical Theory of Communication* (1948). — The founding paper. Remarkably readable.
4. **Csiszar, I. & Korner, J.** *Information Theory: Coding Theorems for Discrete Memoryless Systems.* — Rigorous and deep.
5. **Li, M. & Vitanyi, P.** *An Introduction to Kolmogorov Complexity and Its Applications.* — The standard for algorithmic information theory.
6. **Polyanskiy, Y. & Wu, Y.** *Information Theory: From Coding to Learning.* — Modern, integrates learning theory.

---

## 7. Exercises and Milestones

- [ ] Prove H(X) ≤ log|X| with equality iff X is uniform (using Gibbs' inequality).
- [ ] Compute H(X), H(Y), H(X,Y), H(X|Y), I(X;Y) for a joint distribution of your choice.
- [ ] Prove the data processing inequality.
- [ ] Construct a Huffman code for a source with probabilities (1/2, 1/4, 1/8, 1/16, 1/16) and verify its average length ≈ H.
- [ ] Compute the capacity of the BSC(p) and plot C vs. p.
- [ ] Derive the rate-distortion function for a Gaussian source with squared-error distortion.
- [ ] Show that minimizing cross-entropy loss is equivalent to minimizing KL divergence.
- [ ] Derive the ELBO and show log p(x) = ELBO + D_{KL}(q‖p(z|x)).
- [ ] Implement arithmetic coding for a simple source.
- [ ] Estimate mutual information between two variables using a k-NN estimator.

---

> *Back to [[../math-syllabus|Mathematics Syllabus]]*
