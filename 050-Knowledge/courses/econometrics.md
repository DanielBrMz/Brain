---
title: "Course: Econometrics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, economics, econometrics, statistics]
prerequisites: [linear-algebra, statistics, probability]
---

# Econometrics

> [[../finance-syllabus|Finance Syllabus]] | Related: [[corporate-finance]], [[portfolio-theory]], [[quantitative-finance]], [[microeconomics]]

## Motivation

Econometrics is the application of statistical methods to economic and financial data to test theories, estimate relationships, and forecast. It is the empirical backbone of economics: every claim about "the effect of X on Y" — whether minimum wage on employment, education on earnings, or interest rates on investment — must ultimately be evaluated with econometric tools. This course covers the core methods from OLS through modern causal inference, equipping you to both produce and critically evaluate empirical research.

## Prerequisites

- [[linear-algebra]] (matrix algebra, projections, rank)
- Probability and statistics (distributions, hypothesis testing, confidence intervals)
- Calculus (partial derivatives, optimization)
- Some exposure to economic theory ([[microeconomics]])

---

## I. Ordinary Least Squares (OLS)

### The Linear Model

$$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}$$

Where $\mathbf{y}$ is n×1, $\mathbf{X}$ is n×k, $\boldsymbol{\beta}$ is k×1, $\boldsymbol{\epsilon}$ is n×1.

### OLS Estimator

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

Minimizes $\sum_i e_i^2 = (\mathbf{y} - \mathbf{X}\hat{\boldsymbol{\beta}})^T(\mathbf{y} - \mathbf{X}\hat{\boldsymbol{\beta}})$.

### Classical Assumptions (Gauss-Markov)

1. **Linearity:** $y = X\beta + \epsilon$
2. **Full rank:** $\text{rank}(\mathbf{X}) = k$ (no perfect multicollinearity)
3. **Exogeneity:** $\mathbb{E}[\boldsymbol{\epsilon} | \mathbf{X}] = \mathbf{0}$ (strict exogeneity)
4. **Spherical errors:** $\text{Var}(\boldsymbol{\epsilon} | \mathbf{X}) = \sigma^2 \mathbf{I}$ (homoskedasticity + no autocorrelation)
5. (For inference) **Normality:** $\boldsymbol{\epsilon} | \mathbf{X} \sim N(\mathbf{0}, \sigma^2\mathbf{I})$

Under 1-4: OLS is BLUE (Best Linear Unbiased Estimator) — Gauss-Markov theorem.

### Properties

- **Unbiasedness:** $\mathbb{E}[\hat{\boldsymbol{\beta}}] = \boldsymbol{\beta}$ (requires exogeneity)
- **Consistency:** $\hat{\boldsymbol{\beta}} \xrightarrow{p} \boldsymbol{\beta}$ as $n \to \infty$
- **Asymptotic normality:** $\sqrt{n}(\hat{\boldsymbol{\beta}} - \boldsymbol{\beta}) \xrightarrow{d} N(\mathbf{0}, \sigma^2 (\mathbf{X}^T\mathbf{X}/n)^{-1})$
- $R^2 = 1 - \frac{SSR}{SST}$; Adjusted $R^2 = 1 - \frac{SSR/(n-k)}{SST/(n-1)}$

### Diagnostics and Violations

**Heteroskedasticity:** $\text{Var}(\epsilon_i | \mathbf{x}_i) \neq \sigma^2$
- Tests: Breusch-Pagan, White
- Fix: Heteroskedasticity-robust (White) standard errors: $\hat{V} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \hat{\boldsymbol{\Omega}} \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}$
- Always use robust SEs in practice (or clustered SEs with grouped data)

**Autocorrelation:** $\text{Cov}(\epsilon_i, \epsilon_j) \neq 0$
- Tests: Durbin-Watson, Breusch-Godfrey
- Fix: Newey-West (HAC) standard errors

**Multicollinearity:** High correlation among regressors
- Inflates standard errors (high VIF); OLS still unbiased
- Diagnose with Variance Inflation Factors: $VIF_j = \frac{1}{1 - R_j^2}$

**Omitted Variable Bias:** If $y = \beta_1 x_1 + \beta_2 x_2 + \epsilon$ but you omit $x_2$:
$$\text{Bias} = \beta_2 \cdot \frac{\text{Cov}(x_1, x_2)}{\text{Var}(x_1)}$$

**Specification Tests:**
- Ramsey RESET: Tests functional form misspecification
- F-test for joint significance of regressors

---

## II. Generalized Least Squares (GLS)

When $\text{Var}(\boldsymbol{\epsilon} | \mathbf{X}) = \sigma^2 \boldsymbol{\Omega}$ (non-spherical errors):

$$\hat{\boldsymbol{\beta}}_{GLS} = (\mathbf{X}^T \boldsymbol{\Omega}^{-1} \mathbf{X})^{-1} \mathbf{X}^T \boldsymbol{\Omega}^{-1} \mathbf{y}$$

- Equivalent to OLS on transformed data: $\boldsymbol{\Omega}^{-1/2}\mathbf{y} = \boldsymbol{\Omega}^{-1/2}\mathbf{X}\boldsymbol{\beta} + \boldsymbol{\Omega}^{-1/2}\boldsymbol{\epsilon}$
- **Feasible GLS (FGLS):** Estimate $\boldsymbol{\Omega}$ from data, then apply GLS
- **Weighted Least Squares (WLS):** Special case when $\boldsymbol{\Omega}$ is diagonal (heteroskedasticity only)

---

## III. Instrumental Variables (IV)

### The Endogeneity Problem

When $\text{Cov}(x, \epsilon) \neq 0$ (due to omitted variables, measurement error, or simultaneity), OLS is biased and inconsistent.

### IV Estimator

An instrument $z$ satisfies:
1. **Relevance:** $\text{Cov}(z, x) \neq 0$ (testable — first-stage F-statistic)
2. **Exclusion restriction:** $\text{Cov}(z, \epsilon) = 0$ (untestable — requires theoretical justification)

**Simple IV (Wald estimator):**
$$\hat{\beta}_{IV} = \frac{\text{Cov}(z, y)}{\text{Cov}(z, x)}$$

### Two-Stage Least Squares (2SLS)

1. **First stage:** Regress $x$ on $z$ (and controls): $x = \pi_0 + \pi_1 z + v$ → get $\hat{x}$
2. **Second stage:** Regress $y$ on $\hat{x}$ (and controls): $y = \beta_0 + \beta_1 \hat{x} + \epsilon$

Standard errors from the second stage must be adjusted (most software does this automatically).

### Weak Instruments

- If $\pi_1 \approx 0$, IV is biased toward OLS and has non-normal finite-sample distributions
- **Stock-Yogo rule of thumb:** First-stage F > 10 for single endogenous regressor
- Weak instrument-robust inference: Anderson-Rubin test, conditional likelihood ratio test

### Over-Identification

When there are more instruments than endogenous variables:
- **Sargan/Hansen J-test:** Test whether extra instruments are valid (orthogonal to errors)
- Rejection suggests at least one instrument is invalid

---

## IV. Panel Data

### Structure

Data indexed by unit $i$ and time $t$: $y_{it} = \mathbf{x}_{it}^T\boldsymbol{\beta} + \alpha_i + \epsilon_{it}$

Where $\alpha_i$ captures unobserved, time-invariant individual heterogeneity.

### Fixed Effects (FE)

- Demean within each unit: eliminate $\alpha_i$
- Equivalent to including unit dummies (LSDV)
- **Assumes:** $\text{Cov}(\alpha_i, \mathbf{x}_{it}) \neq 0$ is allowed (controls for time-invariant confounders)
- **Cannot estimate** coefficients on time-invariant regressors
- Cluster standard errors by unit

### Random Effects (RE)

- Treats $\alpha_i$ as random: $\alpha_i \sim (0, \sigma_\alpha^2)$ independent of $\mathbf{x}_{it}$
- More efficient than FE if assumption holds; estimated via GLS
- **Can estimate** coefficients on time-invariant regressors

### Hausman Test

$H_0$: RE is consistent (i.e., $\alpha_i$ uncorrelated with $\mathbf{x}_{it}$)

$$H = (\hat{\boldsymbol{\beta}}_{FE} - \hat{\boldsymbol{\beta}}_{RE})^T [\hat{V}_{FE} - \hat{V}_{RE}]^{-1} (\hat{\boldsymbol{\beta}}_{FE} - \hat{\boldsymbol{\beta}}_{RE}) \sim \chi^2_k$$

Rejection → use Fixed Effects.

### Extensions

- **First differences:** $\Delta y_{it} = \Delta \mathbf{x}_{it}^T \boldsymbol{\beta} + \Delta \epsilon_{it}$
- **Two-way FE:** Unit + time fixed effects
- **Dynamic panels:** Lagged dependent variable → Arellano-Bond GMM
- **Correlated random effects (Mundlak):** Add group means of time-varying regressors to RE

---

## V. Time Series Econometrics

### Stationarity

- **Strictly stationary:** Joint distribution invariant to time shifts
- **Weakly (covariance) stationary:** Constant mean, constant variance, autocovariance depends only on lag
- **Unit root tests:** Augmented Dickey-Fuller (ADF), Phillips-Perron, KPSS

### AR(p) — Autoregressive

$$y_t = c + \phi_1 y_{t-1} + \cdots + \phi_p y_{t-p} + \epsilon_t$$

Stationary if all roots of the characteristic polynomial lie outside the unit circle.

### MA(q) — Moving Average

$$y_t = c + \epsilon_t + \theta_1 \epsilon_{t-1} + \cdots + \theta_q \epsilon_{t-q}$$

Always stationary; invertible if roots outside unit circle.

### ARIMA(p,d,q)

Integrate (difference) $d$ times to achieve stationarity, then fit ARMA(p,q).

Model selection: AIC, BIC, or Ljung-Box test on residuals.

### VAR (Vector Autoregression)

$$\mathbf{y}_t = \mathbf{c} + \mathbf{A}_1 \mathbf{y}_{t-1} + \cdots + \mathbf{A}_p \mathbf{y}_{t-p} + \boldsymbol{\epsilon}_t$$

- Treats all variables as endogenous
- Impulse response functions (IRFs): Cholesky or structural identification
- Forecast error variance decomposition (FEVD)

### Cointegration

Two I(1) series may have a stationary linear combination (long-run equilibrium).

- **Engle-Granger two-step:** Estimate cointegrating regression; test residual for unit root
- **Johansen test:** Maximum likelihood; determines number of cointegrating vectors
- **Vector Error Correction Model (VECM):** Short-run dynamics + error correction toward equilibrium

### Granger Causality

$x$ Granger-causes $y$ if past values of $x$ help predict $y$ (controlling for past $y$).

- F-test on lagged $x$ coefficients in a VAR equation for $y$
- Predictive, not structural causality
- Sensitive to lag selection, omitted variables

---

## VI. Limited Dependent Variables

### Binary Response: Logit and Probit

$$P(y = 1 | \mathbf{x}) = F(\mathbf{x}^T\boldsymbol{\beta})$$

- **Logit:** $F$ = logistic CDF → $P = \frac{e^{\mathbf{x}^T\boldsymbol{\beta}}}{1 + e^{\mathbf{x}^T\boldsymbol{\beta}}}$
- **Probit:** $F$ = standard normal CDF → $P = \Phi(\mathbf{x}^T\boldsymbol{\beta})$
- Estimated by Maximum Likelihood
- Marginal effects: $\frac{\partial P}{\partial x_j} = f(\mathbf{x}^T\boldsymbol{\beta}) \cdot \beta_j$ (depends on evaluation point)
- Average marginal effects (AME) preferred for interpretation

### Ordered Response

Ordered logit/probit for ordinal outcomes (Likert scales, ratings).

### Multinomial

- **Multinomial logit:** Independence of irrelevant alternatives (IIA) assumption
- **Conditional logit (McFadden):** Characteristics of alternatives vary
- **Nested logit, mixed logit:** Relax IIA

### Tobit Model

For censored/corner solution data (e.g., hours worked, expenditure):
$$y_i^* = \mathbf{x}_i^T\boldsymbol{\beta} + \epsilon_i, \quad y_i = \max(0, y_i^*)$$

Estimated by MLE. Selection on the dependent variable → Heckman two-step.

### Count Data

- **Poisson:** $E[y|\mathbf{x}] = \exp(\mathbf{x}^T\boldsymbol{\beta})$; equidispersion assumption
- **Negative Binomial:** Relaxes equidispersion
- **Zero-inflated models** for excess zeros

---

## VII. Causal Inference

### The Fundamental Problem

We observe $Y_i(1)$ or $Y_i(0)$ but never both (Rubin causal model / potential outcomes).

**Average Treatment Effect (ATE):** $\mathbb{E}[Y(1) - Y(0)]$

**Selection bias:** $\mathbb{E}[Y|D=1] - \mathbb{E}[Y|D=0] = ATE + \text{selection bias}$

### Difference-in-Differences (DID)

$$\hat{\delta}_{DID} = (\bar{Y}_{treat,post} - \bar{Y}_{treat,pre}) - (\bar{Y}_{control,post} - \bar{Y}_{control,pre})$$

- **Parallel trends assumption:** In the absence of treatment, both groups would have followed the same trend
- Regression form: $y_{it} = \alpha + \beta \cdot \text{Treat}_i + \gamma \cdot \text{Post}_t + \delta(\text{Treat}_i \times \text{Post}_t) + \epsilon_{it}$
- **Staggered DID:** Callaway-Sant'Anna, Sun-Abraham methods for varying treatment timing
- Pre-trend testing: Event study plots

### Regression Discontinuity Design (RDD)

Treatment assigned by threshold: treated if $X_i \geq c$.

$$\hat{\tau}_{RDD} = \lim_{x \downarrow c} \mathbb{E}[Y|X=x] - \lim_{x \uparrow c} \mathbb{E}[Y|X=x]$$

- **Sharp RDD:** Treatment deterministic at cutoff
- **Fuzzy RDD:** Probability of treatment jumps at cutoff (IV interpretation)
- Bandwidth selection: Imbens-Kalyanaraman, Calonico-Cattaneo-Titiunik
- Local polynomial regression; manipulation testing (McCrary density test)

### Synthetic Control (Abadie, Diamond, Hainmueller)

- For comparative case studies with one treated unit and many controls
- Constructs a "synthetic" control as a weighted average of untreated units
- Weights chosen to match pre-treatment outcomes
- Inference via placebo tests (in-space and in-time)

### Matching and Propensity Score

- **Propensity score:** $p(\mathbf{x}) = P(D=1|\mathbf{x})$; reduces dimensionality
- **Matching:** Pair treated/control with similar $p(\mathbf{x})$; estimate ATT
- **Inverse probability weighting (IPW):** Weight by $1/p(\mathbf{x})$ or $1/(1-p(\mathbf{x}))$
- **Doubly robust estimators:** Combine regression and IPW

---

## VIII. GMM and Maximum Likelihood

### Generalized Method of Moments (GMM)

Given moment conditions $\mathbb{E}[\mathbf{g}(\mathbf{y}, \mathbf{x}, \boldsymbol{\theta})] = \mathbf{0}$:

$$\hat{\boldsymbol{\theta}}_{GMM} = \arg\min_{\boldsymbol{\theta}} \bar{\mathbf{g}}(\boldsymbol{\theta})^T \mathbf{W} \bar{\mathbf{g}}(\boldsymbol{\theta})$$

- **Two-step GMM:** First use identity weight matrix; estimate optimal $\mathbf{W} = \hat{\mathbf{S}}^{-1}$; re-estimate
- Encompasses OLS, IV, GLS as special cases
- Hansen J-test for over-identifying restrictions

### Maximum Likelihood Estimation (MLE)

$$\hat{\boldsymbol{\theta}}_{MLE} = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^n \ln f(y_i | \mathbf{x}_i, \boldsymbol{\theta})$$

- **Properties:** Consistent, asymptotically normal, asymptotically efficient (Cramér-Rao bound)
- **Information matrix:** $\mathcal{I}(\boldsymbol{\theta}) = -\mathbb{E}\left[\frac{\partial^2 \ln f}{\partial\boldsymbol{\theta}\partial\boldsymbol{\theta}^T}\right]$
- **Testing:** Wald test, Likelihood Ratio test, Lagrange Multiplier (Score) test — asymptotically equivalent
- **Quasi-MLE (QMLE):** Consistent even if distribution misspecified (under correct mean/variance)

---

## IX. Machine Learning in Econometrics (Brief Overview)

- **LASSO/Ridge/Elastic Net:** Variable selection and regularization; post-LASSO for valid inference
- **Random forests, boosting:** Prediction; less suited for causal inference without modification
- **Double/Debiased Machine Learning (Chernozhukov et al.):** Use ML for nuisance parameters while maintaining valid inference for causal parameters
- **Causal forests (Athey & Imbens):** Heterogeneous treatment effect estimation

---

## Key References

1. Wooldridge, J. *Introductory Econometrics: A Modern Approach* (7th ed.). Cengage. — Undergraduate standard.
2. Wooldridge, J. *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press. — Graduate standard.
3. Greene, W. *Econometric Analysis* (8th ed.). Pearson. — Comprehensive reference.
4. Angrist, J. & Pischke, J.-S. *Mostly Harmless Econometrics*. Princeton. — Causal inference bible.
5. Angrist, J. & Pischke, J.-S. *Mastering 'Metrics*. Princeton. — Accessible introduction.
6. Hamilton, J. *Time Series Analysis*. Princeton. — Definitive time series reference.
7. Cunningham, S. *Causal Inference: The Mixtape*. Yale. — Modern causal inference with code.
8. Imbens, G. & Rubin, D. *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge.
9. Cameron, A.C. & Trivedi, P. *Microeconometrics*. Cambridge. — Advanced methods.

---

*Last updated: 2026-03-22*
