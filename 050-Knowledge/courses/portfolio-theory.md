---
title: "Survey: Portfolio Theory & Asset Management"
type: course
subtype: survey
status: active
created: 2026-03-22
tags: [knowledge, course, finance, portfolio-theory, investments, survey]
prerequisites: [linear-algebra, statistics, corporate-finance]
---

# Portfolio Theory & Asset Management (Survey)

> [[../finance-syllabus|Finance Syllabus]] | Related: [[corporate-finance]], [[quantitative-finance]], [[econometrics]]

> [!info] Detailed Sub-Courses
> This is the **overview survey**. For in-depth treatment, see:
> - [[modern-portfolio-theory|Modern Portfolio Theory]] — Mean-variance, efficient frontier, CAPM, APT
> - [[factor-models|Factor Models]] — Fama-French, Carhart, Barra, cross-sectional regression
> - [[asset-allocation|Asset Allocation]] — Risk parity, Black-Litterman, liability-driven investing
> - [[alternative-investments|Alternative Investments]] — Private equity, hedge funds, real estate, commodities

## Motivation

Portfolio theory provides the mathematical framework for constructing investment portfolios that optimally trade off risk and return. From Markowitz's foundational insight that diversification is "the only free lunch in finance" to modern multi-factor models and risk parity strategies, these tools are used daily by asset managers overseeing trillions of dollars. Whether you are building a personal retirement portfolio or managing a pension fund, understanding these principles is essential.

## Prerequisites

- [[linear-algebra]] (matrix operations, eigenvalues)
- Probability and statistics (distributions, covariance, regression)
- [[corporate-finance]] (WACC, cost of equity, basic valuation)
- Calculus (optimization, Lagrange multipliers)

---

## I. Mean-Variance Optimization (Markowitz, 1952)

### Setup

For N assets with:
- **Expected returns vector:** $\boldsymbol{\mu} = [\mu_1, \mu_2, \ldots, \mu_N]^T$
- **Covariance matrix:** $\boldsymbol{\Sigma}$ (N×N, symmetric positive semi-definite)
- **Portfolio weights:** $\mathbf{w} = [w_1, w_2, \ldots, w_N]^T$

**Portfolio return:** $\mu_p = \mathbf{w}^T \boldsymbol{\mu}$

**Portfolio variance:** $\sigma_p^2 = \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}$

### Optimization Problem

Minimize $\frac{1}{2}\mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w}$ subject to:
- $\mathbf{w}^T \boldsymbol{\mu} = \mu_{\text{target}}$
- $\mathbf{w}^T \mathbf{1} = 1$

Solved via Lagrange multipliers → closed-form solution involving $\boldsymbol{\Sigma}^{-1}$.

### Two-Fund Separation Theorem

Any minimum-variance portfolio can be expressed as a linear combination of any two distinct minimum-variance portfolios. This means all investors hold combinations of the same two "funds."

### Practical Issues

- **Estimation error:** Sample means are notoriously noisy; covariance estimation degrades with dimensionality
- **Concentration:** Unconstrained MVO produces extreme, unstable weights
- **Remedies:** Shrinkage estimators (Ledoit-Wolf), resampled efficient frontier, robust optimization, constraints (max weight, sector limits)

---

## II. Efficient Frontier

### Key Portfolios

- **Global Minimum Variance (GMV) portfolio:** Leftmost point on the frontier; minimizes risk regardless of return
  $$\mathbf{w}_{GMV} = \frac{\boldsymbol{\Sigma}^{-1}\mathbf{1}}{\mathbf{1}^T \boldsymbol{\Sigma}^{-1}\mathbf{1}}$$

- **Tangency (maximum Sharpe ratio) portfolio:** Point where the Capital Market Line is tangent to the efficient frontier
  $$\mathbf{w}_{tan} = \frac{\boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu} - r_f \mathbf{1})}{\mathbf{1}^T \boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu} - r_f \mathbf{1})}$$

### Capital Market Line (CML)

$$\mu_p = r_f + \frac{\mu_{tan} - r_f}{\sigma_{tan}} \sigma_p$$

With a risk-free asset, all efficient portfolios lie on the CML — combinations of the risk-free asset and the tangency portfolio.

---

## III. Capital Asset Pricing Model (CAPM)

### Derivation

If all investors use mean-variance optimization with identical expectations, in equilibrium:
- The tangency portfolio = the market portfolio (all risky assets, value-weighted)
- Every asset's expected excess return is proportional to its covariance with the market

### CAPM Equation

$$E[r_i] - r_f = \beta_i (E[r_m] - r_f)$$

Where:
$$\beta_i = \frac{Cov(r_i, r_m)}{Var(r_m)}$$

### Security Market Line (SML)

- Plots expected return vs. beta (not sigma)
- Assets above the SML are undervalued (positive alpha); below are overvalued
- Alpha: $\alpha_i = E[r_i] - [r_f + \beta_i(E[r_m] - r_f)]$

### Assumptions & Critiques

- Homogeneous expectations, single-period, no taxes/transaction costs
- Roll's critique: The true market portfolio is unobservable
- Empirical evidence: Low-beta anomaly, size effect, value effect → motivate multi-factor models

---

## IV. Performance Measures

### Risk-Adjusted Return Metrics

**Sharpe Ratio:**
$$SR = \frac{r_p - r_f}{\sigma_p}$$
Reward per unit of total risk. Best for evaluating a standalone portfolio.

**Sortino Ratio:**
$$\text{Sortino} = \frac{r_p - r_f}{\sigma_{\text{downside}}}$$
Uses downside deviation (only penalizes negative returns). Better for asymmetric return distributions.

**Treynor Ratio:**
$$TR = \frac{r_p - r_f}{\beta_p}$$
Reward per unit of systematic risk. For well-diversified portfolios.

**Information Ratio:**
$$IR = \frac{\alpha_p}{\sigma(\epsilon_p)} = \frac{r_p - r_b}{\text{Tracking Error}}$$
Active return per unit of active risk relative to a benchmark.

**Jensen's Alpha:**
$$\alpha_p = r_p - [r_f + \beta_p(r_m - r_f)]$$

### The Fundamental Law of Active Management (Grinold & Kahn)

$$IR \approx IC \times \sqrt{BR}$$

- IC = Information Coefficient (correlation of forecasts with outcomes)
- BR = Breadth (number of independent bets per year)
- Implies: either be very skilled (high IC) or make many independent bets (high BR)

---

## V. Factor Models

### Single-Factor (Market Model)

$$r_i - r_f = \alpha_i + \beta_i(r_m - r_f) + \epsilon_i$$

### Fama-French Three-Factor Model (1993)

$$r_i - r_f = \alpha_i + \beta_{i,MKT}(r_m - r_f) + \beta_{i,SMB} \cdot SMB + \beta_{i,HML} \cdot HML + \epsilon_i$$

- **SMB (Small Minus Big):** Size premium
- **HML (High Minus Low):** Value premium (high B/M minus low B/M)

### Carhart Four-Factor Model (1997)

Adds **UMD (Up Minus Down):** Momentum factor (past 12-month winners minus losers, skipping most recent month).

### Fama-French Five-Factor Model (2015)

Adds:
- **RMW (Robust Minus Weak):** Profitability factor
- **CMA (Conservative Minus Aggressive):** Investment factor

Note: The five-factor model subsumes the value factor (HML) in many tests. Momentum is conspicuously absent.

### Arbitrage Pricing Theory (APT) — Ross, 1976

$$E[r_i] = r_f + \sum_{k=1}^{K} \beta_{ik} \lambda_k$$

- No-arbitrage condition: factor risk premiums $\lambda_k$ must price all assets consistently
- Factors are unspecified (statistical or macroeconomic)
- More general than CAPM but less prescriptive

### Practical Factor Investing

- Long-short factor portfolios vs. long-only smart beta
- Factor crowding and capacity constraints
- Transaction costs erode factor premia
- Factor timing vs. static factor allocation

---

## VI. Black-Litterman Model (1992)

### Problem Solved

MVO is highly sensitive to expected return inputs. BL provides a Bayesian framework to combine market equilibrium returns with investor views.

### Steps

1. **Implied equilibrium returns:** Back out from market-cap weights and covariance matrix:
   $$\boldsymbol{\Pi} = \delta \boldsymbol{\Sigma} \mathbf{w}_{mkt}$$
   Where $\delta$ = risk aversion parameter.

2. **Express views:** Matrix P (pick matrix), vector Q (view returns), uncertainty Ω.

3. **Posterior returns:**
   $$\boldsymbol{\mu}_{BL} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{P}^T \boldsymbol{\Omega}^{-1} \mathbf{P}]^{-1} [(\tau\boldsymbol{\Sigma})^{-1}\boldsymbol{\Pi} + \mathbf{P}^T \boldsymbol{\Omega}^{-1}\mathbf{Q}]$$

4. **Optimize:** Use $\boldsymbol{\mu}_{BL}$ in standard MVO — produces stable, intuitive portfolios.

### Advantages

- Starts from a diversified equilibrium baseline
- Allows partial views (not all assets need a view)
- Confidence-weighted: uncertain views shift weights less
- Portfolios are more stable and concentrated on expressed views

---

## VII. Risk Parity

### Core Idea

Allocate so that each asset (or asset class) contributes equally to total portfolio risk, rather than equal capital allocation.

### Risk Contribution

For asset i:
$$RC_i = w_i \cdot \frac{(\boldsymbol{\Sigma}\mathbf{w})_i}{\sigma_p} = w_i \cdot MRC_i$$

Risk parity: $RC_1 = RC_2 = \cdots = RC_N$

### Implementation

- Typically requires leveraging low-risk assets (bonds) to match return targets
- Bridgewater's All Weather Fund is the canonical example
- Performs well in diverse macro regimes but underperforms in strong bull equity markets
- Critiques: leverage costs, tail-risk correlation, look-back bias in covariance estimation

---

## VIII. Asset Allocation

### Strategic Asset Allocation (SAA)

- Long-term target weights based on investor objectives, risk tolerance, time horizon
- Driven by capital market assumptions (expected returns, risks, correlations)
- Rebalanced periodically to maintain targets
- Liability-driven investing (LDI) for pensions: match duration of assets to liabilities

### Tactical Asset Allocation (TAA)

- Short-to-medium term deviations from SAA to exploit mispricings
- Signals: valuation (CAPE, yield spreads), momentum, macro indicators, sentiment
- Risk budgeting: limit tracking error vs. SAA

### Lifecycle/Glide Path

- Young investors: high equity, high risk capacity
- Approaching retirement: shift to bonds, annuities
- Target-date funds automate this

### Alternative Asset Classes

See also [[quantitative-finance]] for derivatives-based strategies.

- **Private Equity:** Buyout, venture capital, growth equity. Illiquidity premium, J-curve, IRR/MOIC measurement.
- **Hedge Funds:** Long/short equity, global macro, event-driven, quantitative. 2/20 fee structure, survivorship bias, capacity limits.
- **Real Estate:** Direct ownership, REITs, real estate debt. Inflation hedge, income generation.
- **Commodities:** Futures-based exposure, roll yield, backwardation vs. contango.
- **Infrastructure, farmland, collectibles.**

---

## IX. Performance Attribution

### Brinson-Hood-Beebower Model (BHB, 1986)

Decomposes portfolio return relative to benchmark into:

**Allocation effect:** Over/underweighting sectors that outperform/underperform.
$$A_i = (w_{p,i} - w_{b,i}) \cdot (r_{b,i} - r_b)$$

**Selection effect:** Picking better/worse securities within each sector.
$$S_i = w_{b,i} \cdot (r_{p,i} - r_{b,i})$$

**Interaction effect:**
$$I_i = (w_{p,i} - w_{b,i}) \cdot (r_{p,i} - r_{b,i})$$

**Total active return:** $\sum_i (A_i + S_i + I_i)$

### Multi-Period Attribution

- Linking single-period attributions across time
- Geometric vs. arithmetic methods; Carino smoothing

### Factor-Based Attribution

- Decompose returns by factor exposures rather than sector weights
- More relevant for quant strategies and factor-based investing

---

## X. Behavioral Finance and Market Efficiency

### Efficient Market Hypothesis (EMH)

- **Weak form:** Prices reflect all past trading information
- **Semi-strong form:** Prices reflect all publicly available information
- **Strong form:** Prices reflect all information (including private)

### Anomalies

- Size effect, value effect, momentum, low volatility
- Post-earnings announcement drift, accruals anomaly
- January effect, turn-of-month effect

### Behavioral Biases

- Overconfidence, anchoring, loss aversion, herding, disposition effect
- Limits to arbitrage: noise trader risk, implementation costs, model risk
- See [[microeconomics]] for prospect theory foundations

---

## Key References

1. Markowitz, H. (1952). "Portfolio Selection." *Journal of Finance*.
2. Sharpe, W. (1964). "Capital Asset Prices." *Journal of Finance*.
3. Fama, E. & French, K. (1993). "Common Risk Factors in the Returns on Stocks and Bonds." *JFE*.
4. Black, F. & Litterman, R. (1992). "Global Portfolio Optimization." *Financial Analysts Journal*.
5. Grinold, R. & Kahn, R. *Active Portfolio Management* (2nd ed.). McGraw-Hill.
6. Ilmanen, A. *Expected Returns*. Wiley. — Comprehensive empirical overview.
7. Ang, A. *Asset Management: A Systematic Approach to Factor Investing*. Oxford.
8. Bodie, Z., Kane, A. & Marcus, A. *Investments* (12th ed.). McGraw-Hill. — Standard textbook.
9. Maillard, S., Roncalli, T. & Teiletche, J. (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *JoPM*.

---

*Last updated: 2026-03-22*
