---
title: "Finance — Complete Syllabus"
type: reference
status: active
created: 2026-03-22
tags: [knowledge, finance, quantitative-finance, syllabus]
---

# Finance — Complete Syllabus

> Comprehensive curriculum spanning classical finance through quantitative methods, financial engineering, and economics. Organized for progressive study with key formulas and concepts highlighted.

See also: [[academic-taxonomy]] | [[knowledge-index]]

---

## Course Notes

### Classical Finance
| Topic | Course Note |
|-------|------------|
| Corporate Finance | [[courses/corporate-finance\|Corporate Finance]] |
| Accounting | [[courses/accounting\|Accounting]] |
| Banking | [[courses/banking\|Banking]] |
| Fixed Income | [[courses/fixed-income\|Fixed Income]] |
| Equity Analysis | [[courses/equity-analysis\|Equity Analysis]] |

### Portfolio Theory
| Topic | Course Note |
|-------|------------|
| Modern Portfolio Theory | [[courses/modern-portfolio-theory\|Modern Portfolio Theory]] |
| Factor Models | [[courses/factor-models\|Factor Models]] |
| Asset Allocation | [[courses/asset-allocation\|Asset Allocation]] |
| Alternative Investments | [[courses/alternative-investments\|Alternative Investments]] |
| Survey | [[courses/portfolio-theory\|Portfolio Theory (Survey)]] |

### Quantitative Finance
| Topic | Course Note |
|-------|------------|
| Derivatives | [[courses/derivatives\|Derivatives]] |
| Stochastic Calculus | [[courses/stochastic-calculus\|Stochastic Calculus]] |
| Risk Management | [[courses/risk-management\|Risk Management]] |
| Market Microstructure | [[courses/market-microstructure\|Market Microstructure]] |
| Interest Rate Models | [[courses/interest-rate-models\|Interest Rate Models]] |
| Credit Risk | [[courses/credit-risk\|Credit Risk]] |
| Survey | [[courses/quantitative-finance\|Quantitative Finance (Survey)]] |

### Economics
| Topic | Course Note |
|-------|------------|
| Microeconomics | [[courses/microeconomics\|Microeconomics]] |
| Macroeconomics | [[courses/macroeconomics\|Macroeconomics]] |
| Econometrics | [[courses/econometrics\|Econometrics]] |

---

## 1. Classical Finance

### 1.1 Corporate Finance

#### 1.1.1 Time Value of Money
- Present value and future value: PV = FV / (1 + r)^n
- Annuities: PV = C * [1 - (1 + r)^(-n)] / r
- Perpetuities: PV = C / r
- Growing perpetuity: PV = C / (r - g)
- Effective annual rate vs nominal rate: EAR = (1 + r/m)^m - 1

#### 1.1.2 Capital Budgeting
- Net Present Value (NPV) — sum of discounted cash flows minus initial investment
- Internal Rate of Return (IRR) — discount rate where NPV = 0
- Modified IRR (MIRR) — addresses reinvestment rate assumption
- Payback period and discounted payback period
- Profitability index: PI = PV(future CFs) / initial investment
- Real options analysis — flexibility value in capital projects

#### 1.1.3 Capital Structure
- Modigliani-Miller Theorem — irrelevance propositions (I and II)
- Trade-off theory — tax shields vs bankruptcy costs
- Pecking order theory (Myers-Majluf) — internal funds > debt > equity
- WACC: r_wacc = (E/V)*r_e + (D/V)*r_d*(1 - T)
- Leverage effect on cost of equity: r_e = r_0 + (r_0 - r_d)*(D/E)
- Agency costs — conflicts between shareholders, managers, debtholders

#### 1.1.4 Valuation
- Discounted Cash Flow (DCF) — free cash flow to firm and equity
- Comparable company analysis (trading multiples: P/E, EV/EBITDA, P/B)
- Precedent transactions analysis
- Dividend discount model: P = D1 / (r - g)
- Leveraged buyout (LBO) modeling
- Sum-of-the-parts valuation

#### 1.1.5 Corporate Governance & M&A
- Hostile vs friendly acquisitions; tender offers, proxy fights
- Synergies — revenue, cost, financial
- Takeover defenses — poison pills, staggered boards, white knights
- Spin-offs, carve-outs, divestitures
- ESG integration and stakeholder theory

### 1.2 Accounting & Financial Statement Analysis

#### 1.2.1 Financial Statements
- Income statement — revenue recognition (ASC 606), expense matching
- Balance sheet — assets = liabilities + equity; classification rules
- Cash flow statement — operating (direct/indirect), investing, financing
- Statement of stockholders' equity
- Notes and MD&A — contingencies, off-balance-sheet items

#### 1.2.2 Ratio Analysis
- Profitability: ROE, ROA, ROIC, gross/operating/net margins
- DuPont decomposition: ROE = margin * turnover * leverage
- Liquidity: current ratio, quick ratio, cash ratio
- Solvency: debt-to-equity, interest coverage (EBIT/interest)
- Efficiency: inventory turnover, DSO, DPO, cash conversion cycle
- Altman Z-Score for bankruptcy prediction

#### 1.2.3 Advanced Accounting Topics
- Lease accounting (ASC 842 / IFRS 16) — right-of-use assets
- Goodwill and impairment testing
- Deferred tax assets/liabilities — temporary vs permanent differences
- Foreign currency translation (ASC 830) — functional vs reporting currency
- Revenue recognition across contract types
- Fair value hierarchy (Level 1, 2, 3 inputs)

### 1.3 Banking & Financial Institutions

#### 1.3.1 Commercial Banking
- Fractional reserve banking; money multiplier = 1 / reserve ratio
- Net interest margin (NIM) — spread between lending and deposit rates
- Loan origination, underwriting, securitization pipeline
- Basel III/IV — CET1, Tier 1, total capital ratios; liquidity coverage ratio (LCR)
- Stress testing frameworks (CCAR, DFAST)

#### 1.3.2 Investment Banking
- Equity capital markets (IPOs, follow-ons, SPACs)
- Debt capital markets (investment grade, high yield, leveraged loans)
- Advisory — M&A, restructuring, recapitalization
- Sales & trading — market-making, principal vs agency trades
- Prime brokerage services

### 1.4 Fixed Income

#### 1.4.1 Bond Fundamentals
- Bond pricing: P = sum of C/(1+y)^t + FV/(1+y)^n
- Yield measures: current yield, YTM, YTC, yield to worst
- Day count conventions (30/360, ACT/360, ACT/ACT)
- Accrued interest and clean vs dirty price
- Credit ratings (Moody's, S&P, Fitch) and migration matrices

#### 1.4.2 Term Structure & Duration
- Yield curve theories: expectations, liquidity preference, market segmentation
- Bootstrapping spot rates from par curve
- Forward rates: (1 + f_{t,t+1}) = (1 + s_{t+1})^(t+1) / (1 + s_t)^t
- Macaulay duration: D = sum of t * PV(CF_t) / P
- Modified duration: D_mod = D_mac / (1 + y/m)
- Convexity: C = (1/P) * d^2P/dy^2
- Price change approximation: dP/P ~ -D_mod * dy + 0.5 * C * (dy)^2
- Key rate durations and partial DV01s

#### 1.4.3 Structured Products
- Mortgage-backed securities (MBS) — pass-throughs, CMOs, tranching
- Prepayment models — PSA, CPR, SMM
- Asset-backed securities (ABS) — auto loans, credit cards, CLOs
- Waterfall structures and credit enhancement (subordination, overcollateralization)

### 1.5 Equity Markets

#### 1.5.1 Equity Valuation
- CAPM: E(r_i) = r_f + beta_i * (E(r_m) - r_f)
- Multi-stage DDM, H-model
- Free cash flow models (FCFF, FCFE)
- Residual income model: V = BV + sum of RI_t / (1+r)^t
- Earnings quality analysis — accruals, sustainability

#### 1.5.2 Market Structure
- Order types: market, limit, stop, iceberg, TWAP, VWAP
- Exchange vs OTC; lit vs dark pools
- Market makers and specialists; bid-ask spread components
- Circuit breakers and volatility halts
- Regulation: SEC, Reg NMS, MiFID II

---

## 2. Portfolio Theory & Asset Management

### 2.1 Modern Portfolio Theory (MPT)

#### 2.1.1 Mean-Variance Optimization
- Portfolio return: E(r_p) = sum of w_i * E(r_i)
- Portfolio variance: sigma_p^2 = w' * Sigma * w
- Two-asset case: sigma_p^2 = w1^2*s1^2 + w2^2*s2^2 + 2*w1*w2*s1*s2*rho
- Efficient frontier — minimum variance portfolios for each return level
- Global minimum variance portfolio
- Tangency portfolio and the capital market line (CML)
- Sharpe ratio: S = (E(r_p) - r_f) / sigma_p

#### 2.1.2 Practical Challenges
- Estimation error in means, variances, covariances
- Black-Litterman model — combining equilibrium with investor views
- Resampled efficient frontier (Michaud)
- Robust optimization approaches
- Shrinkage estimators (Ledoit-Wolf)

### 2.2 Factor Models

#### 2.2.1 Capital Asset Pricing Model (CAPM)
- Single-factor model; systematic vs idiosyncratic risk
- Security market line (SML): E(r_i) = r_f + beta_i * MRP
- Jensen's alpha: alpha = r_i - [r_f + beta_i * (r_m - r_f)]
- Roll's critique — unobservable true market portfolio

#### 2.2.2 Multi-Factor Models
- Fama-French three-factor: market, SMB (size), HML (value)
- Carhart four-factor: adds momentum (UMD)
- Fama-French five-factor: adds RMW (profitability), CMA (investment)
- APT (Ross) — arbitrage pricing theory; k-factor structure
- Barra risk models — style and industry factors
- AQR quality-minus-junk, betting-against-beta

### 2.3 Asset Allocation & Alternatives

#### 2.3.1 Strategic Asset Allocation
- Policy portfolio and long-term capital market assumptions
- Risk parity — equal risk contribution from each asset class
- Liability-driven investing (LDI) — pension fund matching
- Endowment model (Yale/Swensen) — heavy alternatives allocation
- Human capital and lifecycle investing

#### 2.3.2 Alternative Investments
- Private equity: venture capital, growth, buyout; J-curve, IRR vs MOIC
- Hedge funds: long/short, global macro, event-driven, relative value
- Real estate: direct, REITs, cap rates, NOI yield
- Commodities: futures curve (contango/backwardation), roll yield
- Infrastructure and real assets
- Fund-of-funds and co-investment structures

### 2.4 Performance Attribution
- Brinson-Fachler attribution: allocation + selection + interaction effects
- Multi-period linking (geometric vs arithmetic)
- Risk-adjusted measures: Sharpe, Sortino, Treynor, Information ratio
- Maximum drawdown and Calmar ratio
- GIPS compliance standards

---

## 3. Quantitative Finance

### 3.1 Derivatives Pricing

#### 3.1.1 Options Fundamentals
- Put-call parity: C - P = S - K*e^(-rT)
- Intrinsic vs time value; moneyness (ITM, ATM, OTM)
- American vs European; early exercise conditions
- Binomial tree model (Cox-Ross-Rubinstein): u = e^(sigma*sqrt(dt)), d = 1/u
- Risk-neutral pricing: p = (e^(r*dt) - d) / (u - d)

#### 3.1.2 Black-Scholes-Merton Framework
- Geometric Brownian Motion: dS = mu*S*dt + sigma*S*dW
- Black-Scholes PDE: dV/dt + 0.5*sigma^2*S^2*d^2V/dS^2 + r*S*dV/dS - r*V = 0
- Call: C = S*N(d1) - K*e^(-rT)*N(d2)
- d1 = [ln(S/K) + (r + sigma^2/2)*T] / (sigma*sqrt(T))
- d2 = d1 - sigma*sqrt(T)
- Greeks: Delta, Gamma, Theta, Vega, Rho
- Delta-gamma hedging; gamma scalping
- Implied volatility and the volatility smile/skew/surface

#### 3.1.3 Exotic Options
- Barrier options (knock-in, knock-out); Asian options (arithmetic, geometric average)
- Lookback, chooser, compound, quanto, rainbow options
- Variance and volatility swaps: payoff = N * (sigma_realized^2 - K_var)
- Binary/digital options

### 3.2 Stochastic Calculus

#### 3.2.1 Foundations
- Probability spaces, filtrations, sigma-algebras
- Brownian motion properties: continuous, independent increments, W_t ~ N(0,t)
- Quadratic variation: [W,W]_t = t
- Ito's Lemma: df = (df/dt + mu*df/dx + 0.5*sigma^2*d^2f/dx^2)*dt + sigma*(df/dx)*dW
- Ito isometry: E[(integral h dW)^2] = integral E[h^2] dt

#### 3.2.2 Advanced Stochastic Processes
- Girsanov's theorem — change of measure; Radon-Nikodym derivative
- Martingale representation theorem
- Feynman-Kac formula — PDE-expectation connection
- Stochastic volatility: Heston model dv = kappa*(theta - v)*dt + xi*sqrt(v)*dW_v
- SABR model for smile dynamics
- Jump-diffusion (Merton): dS/S = mu*dt + sigma*dW + J*dN

### 3.3 Risk Management

#### 3.3.1 Market Risk
- Value at Risk (VaR): parametric, historical simulation, Monte Carlo
- Expected Shortfall (CVaR): E[L | L > VaR_alpha]
- Coherent risk measures — monotonicity, subadditivity, homogeneity, translation invariance
- Stress testing and scenario analysis
- Extreme value theory (EVT) — Generalized Pareto Distribution for tails

#### 3.3.2 Credit Risk
- Structural models (Merton) — equity as call on firm assets
- Reduced-form models (Jarrow-Turnbull, Duffie-Singleton) — hazard rate approach
- Credit default swaps (CDS): spread = (1-R) * lambda (approx)
- CVA/DVA/FVA — counterparty valuation adjustments
- Copula models for default correlation (Gaussian copula, t-copula)

#### 3.3.3 Operational and Liquidity Risk
- Basel operational risk frameworks (basic indicator, standardized, AMA)
- Key risk indicators (KRIs) and loss distribution approach
- Liquidity risk: funding vs market liquidity
- Liquidity-adjusted VaR; bid-ask spread modeling

### 3.4 Market Microstructure
- Kyle model — informed trading; lambda as market depth
- Glosten-Milgrom — sequential trade model; adverse selection
- Roll model for effective spread estimation
- Price impact models: permanent vs temporary impact
- Almgren-Chriss optimal execution: minimize impact + risk cost
- Order flow toxicity: VPIN (volume-synchronized probability of informed trading)
- Latency arbitrage and high-frequency trading dynamics

### 3.5 Statistical Arbitrage & Systematic Trading
- Pairs trading — cointegration (Engle-Granger, Johansen)
- Mean reversion: Ornstein-Uhlenbeck process dX = theta*(mu - X)*dt + sigma*dW
- Half-life of mean reversion: t_half = ln(2) / theta
- Momentum strategies — cross-sectional and time-series
- Signal construction, z-scoring, portfolio construction
- Transaction cost modeling and turnover constraints
- Regime detection (Markov switching models)

### 3.6 Machine Learning in Finance
- Supervised: regression (returns prediction), classification (direction)
- Feature engineering from financial data (technical, fundamental, alternative)
- Cross-validation pitfalls: purged k-fold, embargo periods
- Ensemble methods: random forests, gradient boosting (XGBoost, LightGBM)
- Deep learning: LSTMs for sequences, transformer models, attention mechanisms
- Reinforcement learning for portfolio optimization and execution
- NLP: sentiment analysis, earnings call parsing, news analytics
- Backtesting frameworks and overfitting risks (deflated Sharpe ratio)
- Interpretability: SHAP values, feature importance

---

## 4. Financial Engineering

### 4.1 Interest Rate Models
- Short-rate models: Vasicek, CIR, Hull-White, BDT
- Vasicek: dr = a*(b - r)*dt + sigma*dW (mean-reverting, Gaussian)
- CIR: dr = a*(b - r)*dt + sigma*sqrt(r)*dW (no negative rates)
- HJM framework — forward rate dynamics; drift condition
- LIBOR/SOFR Market Model (BGM) — lognormal forward rates
- Swaption pricing and Bermudan swaptions
- Transition from LIBOR to SOFR/RFR benchmarks

### 4.2 Credit Risk Modeling
- Intensity-based models — inhomogeneous Poisson process for default
- CreditMetrics — transition-matrix-based portfolio credit risk
- CreditRisk+ — actuarial approach; Poisson mixture
- CDO pricing — base correlation, tranche sensitivity
- Wrong-way risk — correlation between exposure and counterparty default

### 4.3 Numerical Methods
- Monte Carlo simulation — variance reduction (antithetic, control variates, importance sampling)
- Finite difference methods — explicit, implicit, Crank-Nicolson schemes
- Lattice methods — binomial, trinomial trees; recombining vs non-recombining
- Longstaff-Schwartz algorithm — American option pricing via regression
- Fourier transform methods — characteristic function pricing (Carr-Madan, COS method)
- Quasi-Monte Carlo — Sobol and Halton low-discrepancy sequences

### 4.4 Crypto & Decentralized Finance (DeFi)
- Blockchain consensus: proof of work, proof of stake, BFT variants
- Smart contracts — Solidity, EVM, gas optimization
- Automated market makers (AMMs): Uniswap (x*y=k), Curve (StableSwap)
- Impermanent loss: IL = 2*sqrt(p)/(1+p) - 1 where p = price ratio
- Yield farming, liquidity mining, staking mechanics
- DeFi lending protocols (Aave, Compound) — utilization-based rate curves
- MEV (maximal extractable value) — frontrunning, sandwich attacks, flashbots
- Token economics and governance design
- Regulatory landscape — MiCA, SEC classification frameworks

---

## 5. Economics

### 5.1 Microeconomics

#### 5.1.1 Consumer & Producer Theory
- Utility maximization: MRS = -dU/dx1 / dU/dx2 = p1/p2
- Slutsky equation: substitution + income effects
- Producer theory: cost minimization, profit maximization
- Market structures: perfect competition, monopoly, oligopoly, monopolistic competition
- Welfare economics: Pareto efficiency, deadweight loss, surplus analysis

#### 5.1.2 Game Theory
- Normal form games; Nash equilibrium — no unilateral deviation incentive
- Extensive form and subgame perfect equilibrium (backward induction)
- Mixed strategies — indifference condition
- Repeated games — Folk theorem; trigger strategies
- Bayesian games — incomplete information; Bayesian Nash equilibrium
- Signaling and screening (Spence job market signaling)
- Cooperative games — Shapley value, core, nucleolus
- Evolutionary game theory — ESS, replicator dynamics

#### 5.1.3 Mechanism Design & Auction Theory
- Revelation principle — any outcome achievable by a direct truthful mechanism
- Vickrey-Clarke-Groves (VCG) mechanism
- Auction formats: English, Dutch, first-price sealed, second-price (Vickrey)
- Revenue equivalence theorem
- Optimal auction design (Myerson) — virtual valuation, reserve prices
- Combinatorial auctions and algorithmic mechanism design

#### 5.1.4 Behavioral Economics
- Prospect theory (Kahneman-Tversky) — loss aversion, reference dependence
- Value function: concave for gains, convex for losses, steeper for losses
- Probability weighting — overweighting small probabilities
- Heuristics: anchoring, availability, representativeness
- Bounded rationality (Simon); satisficing vs optimizing
- Nudge theory (Thaler-Sunstein); choice architecture
- Mental accounting and framing effects
- Time inconsistency — hyperbolic discounting, present bias

### 5.2 Macroeconomics

#### 5.2.1 Monetary Policy & Central Banking
- Taylor rule: i = r* + pi + 0.5*(pi - pi*) + 0.5*(y - y*)
- Quantity theory of money: MV = PY
- IS-LM model — goods and money market equilibrium
- Mundell-Fleming model — open economy extension
- Zero lower bound and unconventional policy (QE, forward guidance, YCC)
- Money supply process — open market operations, reserve requirements, discount window
- Transmission mechanisms — interest rate, credit, exchange rate, asset price channels

#### 5.2.2 Growth Theory
- Solow model: Y = A * K^alpha * L^(1-alpha); steady state k* where sf(k*) = (n+delta)*k*
- Golden rule: MPK = n + delta (consumption-maximizing)
- Endogenous growth — Romer (knowledge), Lucas (human capital)
- AK models — constant returns to capital, no diminishing returns
- Convergence debate — conditional vs unconditional
- Total factor productivity and growth accounting

#### 5.2.3 Business Cycles & Fiscal Policy
- Real business cycle (RBC) theory — technology shocks
- New Keynesian DSGE models — sticky prices, Calvo pricing
- Phillips curve: pi = pi_e - beta*(u - u*) + supply shocks
- Fiscal multipliers — spending vs tax multipliers
- Ricardian equivalence — conditions and violations
- Government debt sustainability — r vs g dynamics
- Automatic stabilizers vs discretionary policy

### 5.3 Econometrics

#### 5.3.1 Foundations
- OLS estimation: beta_hat = (X'X)^(-1) * X'y
- Gauss-Markov assumptions and BLUE property
- Hypothesis testing: t-tests, F-tests, Wald tests
- Heteroskedasticity — White robust standard errors, GLS
- Multicollinearity — VIF diagnostics
- Endogeneity — instrumental variables; 2SLS; GMM

#### 5.3.2 Time Series Econometrics
- Stationarity — strict vs weak; unit root tests (ADF, Phillips-Perron, KPSS)
- ARMA(p,q) models — Box-Jenkins methodology
- GARCH family: sigma_t^2 = omega + alpha*e_{t-1}^2 + beta*sigma_{t-1}^2
- EGARCH, GJR-GARCH — asymmetric volatility (leverage effect)
- Cointegration — Engle-Granger two-step, Johansen trace/max eigenvalue tests
- Vector autoregression (VAR) — Granger causality, impulse response functions
- State-space models and Kalman filter

#### 5.3.3 Applied & Modern Methods
- Panel data: fixed effects, random effects; Hausman test for selection
- Difference-in-differences; regression discontinuity; synthetic control
- Maximum likelihood estimation; EM algorithm
- Bayesian econometrics — priors, posteriors, MCMC sampling
- High-dimensional methods — LASSO, ridge, elastic net for variable selection
- Causal inference — DAGs, do-calculus, potential outcomes framework

### 5.4 International Finance & Trade
- Balance of payments — current account, capital/financial account
- Interest rate parity: covered (F/S = (1+r_d)/(1+r_f)) and uncovered
- Purchasing power parity — absolute and relative; Big Mac Index
- Exchange rate models: monetary, portfolio balance, Dornbusch overshooting
- Impossible trinity (Mundell) — fixed exchange rate, free capital flow, independent monetary policy
- Sovereign debt crises — original sin, sudden stops, currency crises
- Trade theory: comparative advantage, Heckscher-Ohlin, new trade theory (Krugman)
- Global financial architecture — IMF, World Bank, BIS, FSB

---

## Reading List & Resources

### Foundational Texts
- *Principles of Corporate Finance* — Brealey, Myers, Allen
- *Options, Futures, and Other Derivatives* — Hull
- *Stochastic Calculus for Finance I & II* — Shreve
- *Advances in Financial Machine Learning* — de Prado
- *Microeconomic Theory* — Mas-Colell, Whinston, Green
- *Macroeconomics* — Romer (graduate), Mankiw (undergraduate)

### Quantitative & Technical
- *Paul Wilmott on Quantitative Finance* — Wilmott
- *Market Microstructure Theory* — O'Hara
- *Econometrics* — Hayashi (graduate), Wooldridge (undergraduate)
- *The Concepts and Practice of Mathematical Finance* — Joshi
- *Active Portfolio Management* — Grinold, Kahn

### Certifications & Programs
- CFA (Chartered Financial Analyst) — Levels I, II, III
- FRM (Financial Risk Manager) — Part I, Part II
- CAIA (Chartered Alternative Investment Analyst)
- CQF (Certificate in Quantitative Finance)

---

*Last updated: 2026-03-22*
*Cross-reference: [[academic-taxonomy]] | [[knowledge-index]]*
