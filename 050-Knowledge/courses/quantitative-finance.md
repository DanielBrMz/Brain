---
title: "Survey: Quantitative Finance"
type: course
subtype: survey
status: active
created: 2026-03-22
tags: [knowledge, course, finance, quantitative-finance, derivatives, stochastic-calculus, survey]
prerequisites: [linear-algebra, probability, real-analysis, portfolio-theory]
---

# Quantitative Finance (Survey)

> [[../finance-syllabus|Finance Syllabus]] | Related: [[portfolio-theory]], [[corporate-finance]], [[econometrics]]

> [!info] Detailed Sub-Courses
> This is the **overview survey**. For in-depth treatment, see:
> - [[derivatives|Derivatives]] — Black-Scholes, Greeks, exotic options, volatility surfaces
> - [[stochastic-calculus|Stochastic Calculus]] — Itô calculus, Girsanov, martingale pricing
> - [[risk-management|Risk Management]] — VaR, CVaR, stress testing, Basel
> - [[market-microstructure|Market Microstructure]] — Order books, market making, HFT, execution
> - [[interest-rate-models|Interest Rate Models]] — Vasicek, CIR, Hull-White, HJM, LIBOR market model
> - [[credit-risk|Credit Risk]] — Merton, reduced form, CDS, CDO, CVA

## Motivation

Quantitative finance sits at the intersection of mathematics, statistics, and financial economics. It provides the rigorous machinery behind derivatives pricing, risk management, and algorithmic trading — the engine rooms of modern capital markets. From the Black-Scholes equation that enabled the explosive growth of options markets to the Monte Carlo methods used to stress-test bank portfolios, these tools are indispensable for anyone working in trading, structuring, risk management, or systematic investing.

## Prerequisites

- [[linear-algebra]] (matrix decompositions, eigenvalues)
- Probability theory (measure theory helpful but not required)
- Real analysis / advanced calculus
- [[portfolio-theory]] (CAPM, factor models)
- Programming (Python/R/C++ for implementation)

---

## I. Options Pricing: Black-Scholes

### Assumptions

- Geometric Brownian Motion (GBM) for the underlying: $dS = \mu S\,dt + \sigma S\,dW$
- Constant volatility $\sigma$, risk-free rate $r$
- No dividends (or continuous dividend yield $q$)
- Continuous trading, no transaction costs, no arbitrage
- European-style options

### The Black-Scholes PDE (Hedging Approach)

Construct a delta-hedged portfolio $\Pi = V - \Delta S$ where $V$ is the option value. By Itô's lemma and requiring the portfolio to earn the risk-free rate:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$

### Black-Scholes Formulas

**European Call:**
$$C = S_0 N(d_1) - Ke^{-rT}N(d_2)$$

**European Put:**
$$P = Ke^{-rT}N(-d_2) - S_0 N(-d_1)$$

Where:
$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

### Risk-Neutral Pricing

Under the risk-neutral measure $\mathbb{Q}$:
$$V_0 = e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{Payoff}(S_T)]$$

The drift of S under $\mathbb{Q}$ is $r$ (not $\mu$): $dS = rS\,dt + \sigma S\,dW^{\mathbb{Q}}$

This is the cornerstone of derivatives pricing — price = discounted expected payoff under the risk-neutral measure.

### Binomial Model (Cox-Ross-Rubinstein, 1979)

- Discrete-time approximation; converges to Black-Scholes as steps → ∞
- At each node: up factor $u = e^{\sigma\sqrt{\Delta t}}$, down factor $d = 1/u$
- Risk-neutral probability: $p = \frac{e^{r\Delta t} - d}{u - d}$
- **American options:** Check for early exercise at each node (backward induction)
- Practical for American options, dividends, exotic features

---

## II. The Greeks

Sensitivities of option value to model parameters:

| Greek | Formula (Call) | Interpretation |
|-------|---------------|----------------|
| **Delta** $\Delta$ | $N(d_1)$ | ∂V/∂S — hedge ratio |
| **Gamma** $\Gamma$ | $\frac{N'(d_1)}{S\sigma\sqrt{T}}$ | ∂²V/∂S² — convexity |
| **Vega** $\mathcal{V}$ | $S N'(d_1)\sqrt{T}$ | ∂V/∂σ — vol sensitivity |
| **Theta** $\Theta$ | $-\frac{SN'(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)$ | ∂V/∂t — time decay |
| **Rho** $\rho$ | $KTe^{-rT}N(d_2)$ | ∂V/∂r — rate sensitivity |

### Key Relationships

- **Delta-Gamma hedging:** Delta hedge neutralizes first-order; Gamma hedging adds second-order protection
- **Theta-Gamma trade-off:** Long gamma (positive convexity) costs theta (time decay)
- **Put-Call parity:** $C - P = S - Ke^{-rT}$ (European options)

---

## III. Exotic Options

- **Barrier options:** Knock-in/knock-out (up/down); path-dependent
- **Asian options:** Payoff depends on average price (arithmetic or geometric)
- **Lookback options:** Payoff depends on max or min price over life
- **Digital/Binary options:** Fixed payoff if condition met
- **Basket options:** On a portfolio of underlyings
- **Chooser options:** Holder chooses call or put at specified date
- **Compound options:** Option on an option
- **Cliquets/Ratchets:** Series of forward-starting options
- **Quanto options:** Foreign underlying, domestic payoff

Pricing: Closed-form solutions for some; Monte Carlo or PDE methods for most.

---

## IV. Volatility

### Implied Volatility

- The $\sigma$ that equates the Black-Scholes price to the market price
- Backed out numerically (Newton-Raphson on the BS formula)
- Not a forecast — it's a quoting convention and risk metric

### Volatility Smile and Skew

- **Smile:** OTM puts and calls have higher implied vol than ATM (common in FX)
- **Skew:** OTM puts have higher implied vol than OTM calls (equity markets post-1987)
- Reflects fat tails, jump risk, leverage effect, supply/demand for downside protection

### Volatility Surface

- Implied vol as a function of (strike, maturity): σ(K, T)
- Must be arbitrage-free: no calendar arbitrage, no butterfly arbitrage
- Parameterizations: SVI (Gatheral), SABR (Hagan et al.)

### Stochastic Volatility Models

- **Heston (1993):** $dv_t = \kappa(\theta - v_t)dt + \xi\sqrt{v_t}\,dW_t^v$; semi-closed form via characteristic functions
- **SABR:** Popular in rates; $\sigma$ follows CEV process
- **Local volatility (Dupire):** Deterministic $\sigma(S, t)$ calibrated to the full surface

### Realized/Historical Volatility

- Sample standard deviation of log returns
- Close-to-close, Parkinson (high-low), Garman-Klass, Yang-Zhang estimators
- **GARCH(1,1):** $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$ — volatility clustering
- **EWMA:** Special case of GARCH with α + β = 1 (RiskMetrics)

---

## V. Stochastic Calculus

### Brownian Motion (Wiener Process)

Properties: $W_0 = 0$; independent increments; $W_t - W_s \sim N(0, t-s)$; continuous but nowhere differentiable.

### Itô's Lemma

For $f(S_t, t)$ where $dS = \mu S\,dt + \sigma S\,dW$:

$$df = \left(\frac{\partial f}{\partial t} + \mu S\frac{\partial f}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 f}{\partial S^2}\right)dt + \sigma S \frac{\partial f}{\partial S}\,dW$$

The extra $\frac{1}{2}\sigma^2 S^2 f_{SS}$ term is the key difference from ordinary calculus — consequence of $(dW)^2 = dt$.

### Itô Integral

- Defined as limit of left-point Riemann sums (non-anticipating)
- $\mathbb{E}[\int_0^T f\,dW] = 0$ (martingale property)
- Itô isometry: $\mathbb{E}[(\int_0^T f\,dW)^2] = \mathbb{E}[\int_0^T f^2\,dt]$

### Girsanov Theorem

Allows change of probability measure. If $dW^{\mathbb{P}} = dW^{\mathbb{Q}} + \gamma\,dt$, then under the new measure $\mathbb{Q}$ (defined by the Radon-Nikodym derivative), $W^{\mathbb{Q}}$ is a Brownian motion.

This is how we move from the real-world measure $\mathbb{P}$ to the risk-neutral measure $\mathbb{Q}$ — the drift changes from $\mu$ to $r$, but volatility is preserved.

### Martingale Pricing

Under $\mathbb{Q}$, discounted asset prices are martingales:
$$\frac{S_t}{B_t} = \mathbb{E}^{\mathbb{Q}}\left[\frac{S_T}{B_T} \bigg| \mathcal{F}_t\right]$$

Where $B_t = e^{rt}$ is the money market account.

### Change of Numeraire

- Choose any traded asset as numeraire; under the associated measure, prices expressed in that numeraire are martingales
- **Forward measure:** Numeraire = zero-coupon bond → simplifies interest rate derivatives
- **Stock measure:** Numeraire = stock → simplifies certain equity derivatives

---

## VI. Risk Management

### Value at Risk (VaR)

The loss that is exceeded with probability $\alpha$ over horizon $h$:
$$P(L > \text{VaR}_\alpha) = \alpha$$

**Methods:**

1. **Historical simulation:** Use empirical return distribution; no distributional assumption
2. **Parametric (variance-covariance):** Assume normality; $\text{VaR}_\alpha = \mu_p - z_\alpha \sigma_p$
3. **Monte Carlo:** Simulate paths from a model; compute loss distribution

### Conditional VaR / Expected Shortfall (CVaR/ES)

$$CVaR_\alpha = \mathbb{E}[L \mid L > \text{VaR}_\alpha]$$

- Coherent risk measure (VaR is not — fails subadditivity)
- Better captures tail risk
- Basel III/IV uses ES at 97.5% instead of VaR at 99%

### Stress Testing

- Historical scenarios: 2008 financial crisis, COVID crash, dot-com bust
- Hypothetical scenarios: rate shock, vol spike, correlation breakdown
- Reverse stress testing: What scenario causes the fund to fail?

### Risk Decomposition

- Marginal VaR, component VaR, incremental VaR
- Factor risk decomposition
- Counterparty credit risk, CVA/DVA

---

## VII. Market Microstructure

### Order Books

- **Limit order book (LOB):** Queue of resting limit orders at each price level
- **Bid-ask spread:** Compensation for adverse selection, inventory risk, order processing
- **Market orders:** Execute immediately against resting liquidity; pay the spread
- **Limit orders:** Provide liquidity; risk of non-execution and adverse selection

### Market Making

- Continuous two-sided quoting; profit from spread, manage inventory risk
- **Avellaneda-Stoikov model:** Optimal bid/ask placement given inventory and volatility
- **Kyle's lambda:** Price impact coefficient — measures market depth

### Price Impact

- **Temporary impact:** Reverts after trade; cost of demanding liquidity
- **Permanent impact:** Information content of the trade shifts equilibrium price
- **Square-root law:** Impact ∝ $\sqrt{\text{volume}/\text{ADV}}$ (empirically robust)

### Execution Algorithms

- **TWAP (Time-Weighted Average Price):** Spread execution uniformly over time
- **VWAP (Volume-Weighted Average Price):** Match historical volume profile
- **Implementation Shortfall (IS):** Minimize slippage vs. decision price; front-loads execution
- **Optimal execution (Almgren-Chriss):** Trade-off between market impact and timing risk

### High-Frequency Trading (HFT)

- Latency arbitrage, statistical arbitrage at microsecond timescales
- Co-location, FPGA/hardware acceleration
- Market making as HFT strategy
- Regulatory concerns: flash crashes, fairness, market stability

---

## VIII. Statistical Arbitrage

### Pairs Trading

- Identify two cointegrated securities (see [[econometrics]] for cointegration)
- Trade the spread: long the underperformer, short the outperformer
- Mean reversion assumption; exit when spread reverts to equilibrium

### Cointegration (Engle-Granger)

Two I(1) series $X_t$, $Y_t$ are cointegrated if $Y_t - \beta X_t = \epsilon_t$ where $\epsilon_t$ is I(0).

- Augmented Dickey-Fuller test on the residual
- Johansen test for multivariate cointegration
- Error correction model for dynamics

### Mean Reversion

- **Ornstein-Uhlenbeck process:** $dX_t = \theta(\mu - X_t)dt + \sigma\,dW_t$
- Half-life of mean reversion: $h = \frac{\ln 2}{\theta}$
- Hurst exponent: H < 0.5 indicates mean-reverting; H > 0.5 trending

### Regime Switching

- **Hidden Markov Models (HMM):** Market operates in latent regimes (e.g., low/high volatility)
- Transition probabilities govern regime changes
- Hamilton filter for regime inference
- Strategy adaptation: different models/parameters per regime

### Other Stat Arb Strategies

- Cross-sectional momentum / mean reversion
- Factor-neutral portfolios
- PCA-based strategies (statistical factors)
- Machine learning approaches: regularized regression, random forests, neural networks

---

## IX. Interest Rate Models (Overview)

### Short-Rate Models

- **Vasicek:** $dr = a(b-r)dt + \sigma\,dW$ — mean-reverting, can go negative
- **CIR:** $dr = a(b-r)dt + \sigma\sqrt{r}\,dW$ — non-negative
- **Hull-White:** Time-dependent parameters; fits initial yield curve exactly

### HJM Framework

- Models the entire forward rate curve: $df(t,T) = \alpha(t,T)dt + \sigma(t,T)dW$
- No-arbitrage drift condition links $\alpha$ to $\sigma$

### LIBOR Market Model (BGM)

- Models discrete forward rates (LIBOR) directly
- Consistent with Black's formula for caps/floors
- Standard for pricing complex interest rate derivatives

---

## X. Numerical Methods

### Monte Carlo Simulation

- Simulate N paths of $S_T$ under risk-neutral measure; average discounted payoffs
- **Variance reduction:** Antithetic variates, control variates, importance sampling, stratified sampling
- **Least-squares Monte Carlo (Longstaff-Schwartz):** For American options — regress continuation value
- Convergence: $O(1/\sqrt{N})$ — slow but dimension-independent

### Finite Difference Methods

- Discretize the Black-Scholes PDE on a grid (S, t)
- **Explicit:** Simple but requires small time steps (stability constraint)
- **Implicit (Crank-Nicolson):** Unconditionally stable, more accurate
- Good for 1-2 dimensional problems; curse of dimensionality for higher

### Fast Fourier Transform (FFT)

- Carr-Madan method: Price options across all strikes simultaneously
- Requires characteristic function of log-price (available for Heston, VG, etc.)
- Very fast for calibration

---

## Key References

1. Hull, J. *Options, Futures, and Other Derivatives* (11th ed.). Pearson. — The standard reference.
2. Shreve, S. *Stochastic Calculus for Finance I & II*. Springer. — Rigorous mathematical treatment.
3. Wilmott, P. *Paul Wilmott on Quantitative Finance* (2nd ed.). Wiley. — Practical and readable.
4. Gatheral, J. *The Volatility Surface*. Wiley. — Volatility modeling.
5. Black, F. & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." *JPE*.
6. Almgren, R. & Chriss, N. (2001). "Optimal Execution of Portfolio Transactions." *JRFM*.
7. Avellaneda, M. & Lee, J.-H. (2010). "Statistical Arbitrage in the US Equities Market." *QF*.
8. Cont, R. (2001). "Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues." *QF*.
9. Glasserman, P. *Monte Carlo Methods in Financial Engineering*. Springer.
10. McNeil, A., Frey, R. & Embrechts, P. *Quantitative Risk Management*. Princeton.

---

*Last updated: 2026-03-22*
