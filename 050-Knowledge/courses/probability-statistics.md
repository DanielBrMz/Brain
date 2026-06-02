---
title: "Survey: Probability and Statistics"
type: course
subtype: survey
status: active
created: 2026-03-22
tags: [knowledge, course, mathematics, probability, statistics, survey]
prerequisites: [real-analysis, linear-algebra]
---

# Probability and Statistics (Survey)

> *"Probability theory is nothing but common sense reduced to calculation."* — Laplace

Back to [[../math-syllabus|Mathematics Syllabus]] | Related: [[real-analysis]], [[linear-algebra]], [[optimization]]

> [!info] Detailed Sub-Courses
> This is the **overview survey**. For in-depth treatment, see:
> - [[probability-theory|Probability Theory]] — Measure-theoretic probability, convergence, martingales, Brownian motion
> - [[mathematical-statistics|Mathematical Statistics]] — MLE, Fisher information, Neyman-Pearson, asymptotics
> - [[stochastic-processes|Stochastic Processes]] — Markov chains, Poisson, Itô calculus, SDEs
> - [[bayesian-statistics|Bayesian Statistics]] — Prior/posterior, MCMC, variational inference
> - [[time-series|Time Series]] — ARIMA, GARCH, state-space, Kalman filter
> - [[causal-inference|Causal Inference]] — do-calculus, potential outcomes, IV, RDD

---

## Motivation

Probability and statistics form the mathematical framework for reasoning under uncertainty. Probability theory, built on measure theory, provides the rigorous foundation for random phenomena. Statistics uses probability to draw inferences from data. Together they underpin machine learning, financial modeling, medical trials, signal processing, and essentially any field that deals with noisy or incomplete information. This course takes the measure-theoretic approach from the start, ensuring a foundation strong enough for advanced topics like martingales, stochastic calculus, and modern statistical learning theory.

## Prerequisites

- [[real-analysis]] — measure theory, Lebesgue integration, L^p spaces, convergence theorems
- [[linear-algebra]] — eigenvalues, positive definite matrices, SVD (for multivariate statistics)
- Basic combinatorics and calculus

## Recommended References

- **Durrett**, *Probability: Theory and Examples* — the standard graduate probability text
- **Williams**, *Probability with Martingales* — elegant, concise
- **Billingsley**, *Probability and Measure* — careful, thorough
- **Casella & Berger**, *Statistical Inference* — the standard for mathematical statistics
- **Schervish**, *Theory of Statistics* — rigorous, Bayesian-friendly
- **Oksendal**, *Stochastic Differential Equations* — for the Ito calculus portion

---

## Part I: Measure-Theoretic Probability (Weeks 1--4)

### Week 1: Probability Spaces and Random Variables

**Topics:**
- Probability space (Ω, F, P): sample space, sigma-algebra of events, probability measure
- Why sigma-algebras? Non-measurable sets exist (Vitali); naive probability on uncountable spaces fails
- Random variables as measurable functions X: Ω → R (or R^n, or general measurable space)
- Distribution (law) of a random variable: μ_X(B) = P(X ∈ B)
- Cumulative distribution function F(x) = P(X ≤ x); properties (right-continuous, non-decreasing, limits 0 and 1)
- Discrete vs continuous vs singular distributions
- Independence of events, random variables, sigma-algebras

**Key Insight:** A random variable is not a "variable" — it is a measurable function on the sample space. The probability space is the domain; the real line is the codomain. This measure-theoretic viewpoint eliminates ambiguity present in elementary treatments.

### Week 2: Expectation and Moments

**Topics:**
- Expectation as Lebesgue integral: E[X] = ∫_Ω X dP
- Properties: linearity, monotonicity, E[|X|] < ∞ iff X is integrable
- Variance: Var(X) = E[(X - EX)^2] = E[X^2] - (EX)^2
- Higher moments; moment generating function M(t) = E[e^{tX}]
- Characteristic function φ(t) = E[e^{itX}] (always exists; uniquely determines distribution)
- Covariance and correlation; covariance matrix for random vectors
- Conditional expectation given an event: E[X | A] = E[X 1_A] / P(A)
- Jensen's inequality: for convex g, E[g(X)] ≥ g(E[X])

**Key Results:**
- **Markov's Inequality:** P(|X| ≥ a) ≤ E[|X|]/a.
- **Chebyshev's Inequality:** P(|X - EX| ≥ a) ≤ Var(X)/a^2.
  - *These are the simplest tail bounds; starting points for concentration inequalities.*

### Week 3: Important Distributions and Transforms

**Topics:**
- Discrete: Bernoulli, Binomial, Poisson, Geometric, Negative Binomial, Hypergeometric
- Continuous: Uniform, Normal (Gaussian), Exponential, Gamma, Beta, Chi-squared, Student's t, F
- The Gaussian distribution: central role, closure under linear combinations, determined by mean and variance among distributions with finite second moment
- Multivariate Gaussian: density, marginals and conditionals are Gaussian, characterized by mean vector and covariance matrix
- Transforms: MGF, characteristic function, probability generating function
- Inversion theorems: recovering distribution from characteristic function

### Week 4: Conditional Expectation (General Theory)

**Topics:**
- Conditional expectation E[X | G] for a sub-sigma-algebra G: defined as the a.s.-unique G-measurable random variable satisfying ∫_A E[X|G] dP = ∫_A X dP for all A ∈ G
- Existence and uniqueness via Radon-Nikodym theorem (from [[real-analysis]])
- Properties: linearity, tower property E[E[X|G]] = E[X], taking out what is known, independence
- Conditional expectation as orthogonal projection in L^2
- Regular conditional distributions

**Key Result:**
- **Tower Property (Law of Iterated Expectation):** If H ⊆ G, then E[E[X|G] | H] = E[X|H].
  - *Proof:* Both sides are H-measurable. For any A ∈ H ⊆ G, ∫_A E[E[X|G]|H] dP = ∫_A E[X|G] dP = ∫_A X dP = ∫_A E[X|H] dP.
  - *Intuition:* Coarsening the information twice is the same as coarsening to the coarser level directly.

---

## Part II: Limit Theorems and Convergence (Weeks 5--7)

### Week 5: Modes of Convergence

**Topics:**
- Almost sure convergence: X_n → X a.s. iff P({ω : X_n(ω) → X(ω)}) = 1
- Convergence in probability: P(|X_n - X| > ε) → 0 for all ε > 0
- Convergence in L^p: E[|X_n - X|^p] → 0
- Convergence in distribution: F_n(x) → F(x) at all continuity points of F
- Relationships: a.s. ⟹ in probability ⟹ in distribution; L^p ⟹ in probability; none of the reverse implications hold in general
- Subsequence characterization: X_n → X in probability iff every subsequence has a further subsequence converging a.s.
- Slutsky's theorem; continuous mapping theorem

### Week 6: Laws of Large Numbers

**Topics:**
- Weak LLN: (X_1 + ... + X_n)/n → μ in probability (requires finite variance, or pairwise independence + finite variance)
- Strong LLN (Kolmogorov): (X_1 + ... + X_n)/n → μ a.s. (requires only finite expectation and i.i.d.)
- Kolmogorov's 0-1 law: tail events have probability 0 or 1
- Borel-Cantelli lemmas (first and second)

**Key Results:**
- **Strong Law of Large Numbers:** If X_1, X_2, ... are i.i.d. with E[|X_1|] < ∞, then (1/n) Σ X_i → E[X_1] a.s.
  - *Proof sketch (truncation method):* Truncate X_i at level n, show the truncated sum converges (using Kolmogorov's maximal inequality and Borel-Cantelli), then show the truncation error is negligible.
- **Borel-Cantelli Lemma I:** If Σ P(A_n) < ∞, then P(A_n i.o.) = 0.
- **Borel-Cantelli Lemma II:** If Σ P(A_n) = ∞ and the A_n are independent, then P(A_n i.o.) = 1.

### Week 7: Central Limit Theorem and Beyond

**Topics:**
- CLT: √n (X̄_n - μ)/σ → N(0,1) in distribution
- Proof via characteristic functions: φ_{√n(X̄-μ)/σ}(t) → e^{-t^2/2}
- Multivariate CLT
- Berry-Esseen theorem: rate of convergence O(1/√n) for the CLT
- Delta method: if √n(X_n - μ) → N(0, σ^2), then √n(g(X_n) - g(μ)) → N(0, σ^2 [g'(μ)]^2)
- Lindeberg-Feller CLT: CLT for independent (not identically distributed) summands under Lindeberg condition

**Key Result:**
- **Central Limit Theorem:** If X_1, X_2, ... are i.i.d. with mean μ and variance σ^2 < ∞, then √n(X̄_n - μ)/σ →_d N(0,1).
  - *Proof sketch (via characteristic functions):* φ_{X_1-μ}(t) = 1 - σ^2 t^2/2 + o(t^2). Then φ_{√n(X̄-μ)/σ}(t) = [φ_{X_1-μ}(t/(σ√n))]^n = [1 - t^2/(2n) + o(1/n)]^n → e^{-t^2/2}. By Levy's continuity theorem, convergence of characteristic functions implies convergence in distribution.

---

## Part III: Martingales (Weeks 8--9)

### Week 8: Discrete-Time Martingales

**Topics:**
- Filtrations {F_n}: increasing sequence of sigma-algebras modeling information flow
- Adapted processes; predictable processes
- Martingale definition: E[X_{n+1} | F_n] = X_n (fair game); supermartingale (≤), submartingale (≥)
- Examples: random walks, Doob martingales, Polya urn, likelihood ratios
- Optional stopping theorem: E[X_T] = E[X_0] under appropriate conditions (bounded stopping time, or bounded martingale, or dominated convergence)
- Martingale transforms

### Week 9: Martingale Convergence

**Topics:**
- Doob's upcrossing inequality
- Martingale convergence theorem: an L^1-bounded martingale converges a.s.
- Doob's maximal inequality: P(max_{k≤n} X_k ≥ λ) ≤ E[X_n^+]/λ (for submartingales)
- L^p convergence of martingales (p > 1): L^p bounded ⟹ L^p convergent
- Uniform integrability and L^1 convergence: X_n → X a.s. and in L^1 iff {X_n} is uniformly integrable
- Backwards martingales and the strong law of large numbers (elegant proof via backward martingale convergence)

**Key Result:**
- **Doob's Martingale Convergence Theorem:** If {X_n} is a submartingale with sup E[X_n^+] < ∞, then X_n → X_∞ a.s. for some integrable X_∞.
  - *Proof sketch:* The number of upcrossings of [a,b] by X_1,...,X_n is bounded in expectation by (E[X_n^+] + |a|)/(b-a). Taking n → ∞, the expected number of upcrossings of [a,b] is finite, so a.s. finite for each rational a < b. A sequence with finitely many upcrossings of every rational interval converges.

---

## Part IV: Statistical Inference (Weeks 10--12)

### Week 10: Point Estimation

**Topics:**
- Statistical model: family {P_θ : θ ∈ Θ} of probability distributions
- Estimators: statistics T(X_1,...,X_n) used to estimate θ
- Bias, variance, mean squared error: MSE = Bias^2 + Variance
- Sufficiency: T is sufficient for θ if the conditional distribution of X given T does not depend on θ
- Fisher-Neyman factorization theorem: T is sufficient iff f(x|θ) = g(T(x), θ) h(x)
- Minimal sufficiency; completeness
- Rao-Blackwell theorem: conditioning on a sufficient statistic improves any estimator
- Maximum likelihood estimation (MLE): θ̂_MLE = argmax_θ L(θ|x)
  - Consistency, asymptotic normality, asymptotic efficiency of MLE under regularity conditions

**Key Results:**
- **Cramer-Rao Lower Bound:** For unbiased estimators, Var(T) ≥ 1/I(θ), where I(θ) = E[(∂/∂θ log f(X|θ))^2] is the Fisher information.
  - *Proof sketch:* Apply Cauchy-Schwarz to Cov(T, ∂/∂θ log f). Since E[T] = θ, differentiating under the integral gives Cov = 1.
- **Rao-Blackwell Theorem:** If T is sufficient and δ is any estimator, then δ* = E[δ|T] has MSE ≤ MSE(δ), with equality iff δ is already a function of T.

### Week 11: Hypothesis Testing

**Topics:**
- Null and alternative hypotheses; test statistics; rejection regions
- Type I error (false positive rate = significance level α), Type II error, power
- Neyman-Pearson lemma: the likelihood ratio test is the most powerful test of size α for simple hypotheses
- Uniformly most powerful tests; monotone likelihood ratio
- Generalized likelihood ratio tests
- p-values: interpretation and common misconceptions
- Multiple testing: Bonferroni correction, Benjamini-Hochberg (FDR control)

**Key Result:**
- **Neyman-Pearson Lemma:** For testing H_0: θ = θ_0 vs H_1: θ = θ_1, the most powerful test of size α rejects when the likelihood ratio L(θ_1)/L(θ_0) > k, where k is chosen so that P_{θ_0}(reject) = α.
  - *Proof sketch:* Let φ* be the NP test and φ any other test of size α. Then ∫(φ* - φ)(f_1 - kf_0) dμ ≥ 0 (because φ* - φ has the same sign as f_1 - kf_0). Since ∫(φ* - φ)f_0 = 0 (both have size α), we get ∫ φ* f_1 ≥ ∫ φ f_1, i.e., power(φ*) ≥ power(φ).

### Week 12: Bayesian Inference and Confidence Intervals

**Topics:**
- Bayesian framework: prior π(θ), likelihood f(x|θ), posterior π(θ|x) ∝ f(x|θ)π(θ)
- Conjugate priors (Beta-Binomial, Normal-Normal, Gamma-Poisson, etc.)
- MAP estimation vs posterior mean; Bayesian credible intervals
- Bayesian vs frequentist: philosophical and practical differences
- Confidence intervals: definition (frequentist coverage guarantee)
- Pivotal quantities; relationship between tests and confidence intervals (duality)
- Bootstrap methods: nonparametric and parametric

**Key Insight:** A 95% confidence interval does not mean "95% probability θ is in this interval." It means: if we repeated the experiment many times, 95% of the constructed intervals would contain the true θ. This is a frequentist guarantee about the procedure, not a probability statement about θ. Bayesian credible intervals do make the latter statement, conditional on the prior.

---

## Part V: Stochastic Processes (Weeks 13--15)

### Week 13: Markov Chains

**Topics:**
- Discrete-time Markov chains: Markov property P(X_{n+1} | X_0,...,X_n) = P(X_{n+1} | X_n)
- Transition matrix; Chapman-Kolmogorov equations
- Classification of states: recurrent vs transient, positive recurrent vs null recurrent
- Irreducibility and aperiodicity
- Stationary distributions: πP = π; existence and uniqueness for irreducible positive recurrent chains
- Ergodic theorem: time averages = space averages (under irreducibility + positive recurrence)
- Convergence to stationarity for irreducible aperiodic chains
- Continuous-time Markov chains: generator matrix, Kolmogorov forward/backward equations
- MCMC: Metropolis-Hastings, Gibbs sampling (connection to Bayesian inference)

### Week 14: Poisson Processes and Brownian Motion

**Topics:**
- Poisson process: definition (independent increments, Poisson-distributed counts), properties
- Superposition, thinning, conditioning
- Renewal processes (brief)
- Brownian motion (Wiener process): definition (continuous paths, independent Gaussian increments)
- Properties: nowhere differentiable a.s., unbounded variation, quadratic variation = t
- Brownian motion as a Gaussian process; covariance function
- Reflection principle; maximum of Brownian motion; hitting times
- Brownian motion as a martingale; also B_t^2 - t is a martingale

**Key Result:**
- **Donsker's Theorem (Functional CLT):** The rescaled random walk S_{⌊nt⌋}/√n converges in distribution (in C[0,1]) to Brownian motion. This is the functional (process-level) generalization of the CLT.

### Week 15: Stochastic Calculus (Introduction)

**Topics:**
- Why classical calculus fails: Brownian motion has infinite variation, so ∫f dB_t cannot be defined pathwise as a Riemann-Stieltjes integral
- Ito integral: construction for simple processes, extension to L^2-adapted processes
- Ito's formula: if f ∈ C^2, then df(B_t) = f'(B_t) dB_t + (1/2)f''(B_t) dt
  - *The extra (1/2)f'' dt term is the fundamental departure from classical calculus; it arises because (dB_t)^2 = dt.*
- Stochastic differential equations (SDEs): dX_t = μ(X_t) dt + σ(X_t) dB_t
- Geometric Brownian motion: dS_t = μS_t dt + σS_t dB_t ⟹ S_t = S_0 exp((μ - σ^2/2)t + σB_t)
- Girsanov's theorem: change of measure to remove drift
- Martingale representation theorem
- Connection to PDEs: Feynman-Kac formula relates SDEs to parabolic PDEs

**Key Result:**
- **Ito's Formula:** For f ∈ C^2 and Ito process X_t:
  df(X_t) = f'(X_t) dX_t + (1/2) f''(X_t) (dX_t)^2
  using the rules (dB_t)^2 = dt, (dB_t)(dt) = 0, (dt)^2 = 0.
  - *This is the chain rule of stochastic calculus. The correction term (1/2)f''dt accounts for the roughness of Brownian paths.*

---

## Applications

### Machine Learning
- **Generalization theory:** PAC learning, VC dimension, Rademacher complexity — all probabilistic
- **Bayesian ML:** Gaussian processes, Bayesian neural networks, variational inference
- **SGD convergence:** martingale arguments and concentration inequalities
- **Generative models:** diffusion models are SDEs; score matching uses Ito calculus
- See [[optimization]] for the optimization aspects

### Finance
- **Black-Scholes model:** geometric Brownian motion + Ito's formula + risk-neutral pricing
- **Portfolio theory:** Markowitz optimization uses covariance matrices (see [[linear-algebra]], [[optimization]])
- **Risk management:** VaR, CVaR, extreme value theory
- **Interest rate models:** Vasicek, CIR, Hull-White — all SDEs

### Medical Imaging / Biostatistics
- **Clinical trials:** hypothesis testing, power analysis, multiple comparisons
- **Survival analysis:** Kaplan-Meier estimator, Cox proportional hazards
- **Bayesian clinical trials:** adaptive designs, posterior probability of efficacy
- **Image reconstruction:** Bayesian inference with spatial priors

---

## Summary of Key Theorems

| Theorem | Statement (abbreviated) | Significance |
|---------|------------------------|--------------|
| Strong LLN | X̄_n → μ a.s. (i.i.d., finite mean) | Sample means converge |
| CLT | √n(X̄_n - μ)/σ →_d N(0,1) | Universal Gaussian limit |
| Martingale Convergence | L^1-bounded martingale converges a.s. | Foundation of martingale theory |
| Cramer-Rao | Var(T) ≥ 1/I(θ) for unbiased T | Efficiency lower bound |
| Neyman-Pearson | LRT is most powerful at given size | Optimal simple hypothesis test |
| Ito's Formula | df = f'dX + (1/2)f''(dX)^2 | Chain rule for stochastic calculus |
| Donsker | Rescaled random walk → Brownian motion | Functional CLT |

---

*Last updated: 2026-03-22*
