---
title: "Course: Corporate Finance"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, finance, corporate-finance]
prerequisites: [financial-accounting, statistics, microeconomics]
---

# Corporate Finance

> [[../finance-syllabus|Finance Syllabus]] | Related: [[portfolio-theory]], [[quantitative-finance]], [[econometrics]]

## Motivation

Corporate finance answers the three fundamental questions every firm faces: **what to invest in** (capital budgeting), **how to finance it** (capital structure), and **how to return value to shareholders** (payout policy). Whether you are a CFO evaluating a $500M acquisition, a startup founder choosing between equity and debt, or an analyst modeling a leveraged buyout, the frameworks here are the analytical backbone. This course builds from first principles — the time value of money — through to the complex strategic decisions that shape modern corporations.

## Prerequisites

- Financial accounting (reading income statements, balance sheets, cash flow statements)
- Introductory statistics and probability
- Basic [[microeconomics]] (supply/demand, market equilibrium)
- Comfort with algebra and spreadsheet modeling

---

## I. Time Value of Money

### Core Principle

A dollar today is worth more than a dollar tomorrow because of opportunity cost, inflation, and risk.

### Key Formulas

**Future Value:**
$$FV = PV \times (1 + r)^n$$

**Present Value:**
$$PV = \frac{FV}{(1 + r)^n}$$

**Annuity (ordinary):**
$$PV = C \times \frac{1 - (1+r)^{-n}}{r}$$

**Perpetuity:**
$$PV = \frac{C}{r}$$

**Growing Perpetuity:**
$$PV = \frac{C}{r - g} \quad (r > g)$$

**Growing Annuity:**
$$PV = C \times \frac{1 - \left(\frac{1+g}{1+r}\right)^n}{r - g}$$

### Key Concepts

- **Compounding frequency:** Effective annual rate (EAR) vs. stated APR: $EAR = (1 + \frac{r}{m})^m - 1$
- **Continuous compounding:** $FV = PV \cdot e^{rn}$
- **Real vs. nominal rates:** Fisher equation: $(1 + r_{nom}) = (1 + r_{real})(1 + \pi)$

---

## II. Capital Budgeting

### Net Present Value (NPV)

$$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$

- The gold standard decision rule: accept if NPV > 0
- Accounts for time value, risk (through discount rate), and all cash flows
- Additive: NPV of combined projects = sum of individual NPVs

### Internal Rate of Return (IRR)

The discount rate that makes NPV = 0:
$$0 = \sum_{t=0}^{n} \frac{CF_t}{(1+IRR)^t}$$

- Accept if IRR > hurdle rate (cost of capital)
- **Problems:** Multiple IRRs with non-conventional cash flows, scale problem, reinvestment assumption
- **Modified IRR (MIRR):** Assumes reinvestment at cost of capital, not IRR itself

### Other Methods

- **Payback Period:** Time to recover initial investment. Simple but ignores TVM and post-payback CFs.
- **Discounted Payback:** Same but with discounted cash flows.
- **Profitability Index:** $PI = \frac{PV(\text{future CFs})}{\text{Initial Investment}}$. Useful for capital rationing.
- **Equivalent Annual Annuity (EAA):** Comparing projects with unequal lives.

### Estimating Cash Flows

- **Incremental cash flows only** — ignore sunk costs, include opportunity costs
- **Free Cash Flow to Firm (FCFF):** EBIT(1 - t) + Depreciation - CapEx - ΔNWC
- **Cannibalization and side effects**
- **Terminal value:** Growing perpetuity or exit multiple
- **Scenario analysis, sensitivity analysis, Monte Carlo simulation**
- **Real options:** Option to delay, expand, abandon, switch — value of managerial flexibility

---

## III. Cost of Capital

### Weighted Average Cost of Capital (WACC)

$$WACC = \frac{E}{V}r_E + \frac{D}{V}r_D(1 - t_c)$$

Where V = E + D, and $t_c$ is the corporate tax rate.

### Cost of Equity

**Capital Asset Pricing Model (CAPM):**
$$r_E = r_f + \beta(r_m - r_f)$$

- $r_f$: Risk-free rate (typically 10-year Treasury)
- $\beta$: Systematic risk relative to market
- $(r_m - r_f)$: Equity risk premium (historically ~5-7%)
- **Estimating beta:** Regression of stock returns on market returns; unlever/relever for comparables

**Arbitrage Pricing Theory (APT):**
$$r_E = r_f + \beta_1 \lambda_1 + \beta_2 \lambda_2 + \cdots + \beta_k \lambda_k$$

Multi-factor model; factors might include GDP growth, inflation, interest rate spreads, etc.

**Fama-French / Build-up methods:** See [[portfolio-theory]] for factor model details.

**Dividend Growth Model (backward-solve):**
$$r_E = \frac{D_1}{P_0} + g$$

### Cost of Debt

- Yield to maturity on existing debt, adjusted for tax shield
- Credit spreads, ratings, and default risk

### Beta

- **Asset (unlevered) beta:** $\beta_A = \frac{\beta_E}{1 + (1 - t_c)\frac{D}{E}}$ (Hamada equation)
- **Project beta:** Use comparable pure-play firms, unlever their betas, relever at target structure
- **Bottom-up beta** vs. regression beta

---

## IV. Capital Structure

### Modigliani-Miller Theorems

**Proposition I (no taxes):** Firm value is independent of capital structure.
$$V_L = V_U$$

**Proposition II (no taxes):** Cost of equity increases linearly with leverage.
$$r_E = r_A + (r_A - r_D)\frac{D}{E}$$

**With corporate taxes:**
$$V_L = V_U + t_c \cdot D$$

Tax shield of debt creates value — suggests 100% debt is optimal (unrealistic).

### Trade-off Theory

Optimal capital structure balances:
- **Tax shield benefit** of debt
- **Financial distress costs:** Direct (legal, administrative) and indirect (lost customers, underinvestment)
- **Agency costs:** Asset substitution, debt overhang, free cash flow problems

### Pecking Order Theory (Myers & Majluf, 1984)

Firms prefer financing in this order due to asymmetric information:
1. Internal funds (retained earnings)
2. Debt
3. Equity (last resort — signals overvaluation)

No target D/E ratio; leverage is a cumulative result of past financing needs.

### Other Considerations

- **Market timing theory:** Issue equity when stock is overvalued
- **Signaling:** Debt signals confidence in cash flows
- **Agency theory:** Debt disciplines managers (Jensen's free cash flow hypothesis)
- **Financial flexibility** as a strategic option

---

## V. Dividend Policy

### Irrelevance (M&M, 1961)

In perfect markets, dividend policy is irrelevant to firm value. Investors can create "homemade dividends" by selling shares.

### Why Dividends Might Matter

- **Tax clienteles:** Different investors prefer different payout policies based on tax treatment
- **Signaling:** Dividend increases signal management confidence
- **Agency costs:** Dividends reduce free cash flow available for wasteful spending
- **Bird-in-hand fallacy** (Gordon & Lintner) — debated

### Payout Methods

- **Regular dividends:** Implicit commitment; sticky
- **Special dividends:** One-time, no commitment
- **Share repurchases:** Flexible, tax-advantaged (capital gains vs. ordinary income), signal undervaluation
- **Dividend reinvestment plans (DRIPs)**

### Key Dates

- Declaration date → Ex-dividend date → Record date → Payment date
- Stock price drops by approximately the dividend amount on the ex-date

---

## VI. Mergers & Acquisitions

### Types

- **Horizontal:** Same industry (synergies, market power)
- **Vertical:** Supply chain integration
- **Conglomerate:** Unrelated diversification (generally value-destroying for shareholders)

### Valuation Methods

- **Comparable company analysis (comps):** EV/EBITDA, P/E, EV/Revenue multiples
- **Precedent transactions:** Multiples from similar M&A deals (include control premium)
- **Discounted Cash Flow (DCF):** Most rigorous; project FCFF, discount at WACC, add terminal value
- **Sum-of-the-parts (SOTP):** For diversified companies

### Synergies

- **Revenue synergies:** Cross-selling, market access (harder to realize)
- **Cost synergies:** Eliminate redundancies, economies of scale (more credible)
- Rule of thumb: acquirers typically overpay — "winner's curse"

### Leveraged Buyouts (LBOs)

- Acquisition primarily financed with debt (60-80% leverage)
- Returns driven by: debt paydown, EBITDA growth, multiple expansion
- Key metrics: IRR (target 20%+), MOIC, debt/EBITDA coverage ratios
- Ideal targets: stable cash flows, low capex, strong asset base, cost-cutting opportunities

### Deal Mechanics

- Hostile vs. friendly; tender offer vs. merger agreement
- Defenses: poison pill, staggered board, white knight, Pac-Man
- Regulatory: Hart-Scott-Rodino antitrust review

---

## VII. Working Capital Management

### Components

- **Current assets:** Cash, receivables, inventory
- **Current liabilities:** Payables, accrued expenses, short-term debt
- **Net Working Capital (NWC) = Current Assets - Current Liabilities**

### Cash Conversion Cycle

$$CCC = DSO + DIO - DPO$$

- **Days Sales Outstanding (DSO):** Average collection period
- **Days Inventory Outstanding (DIO):** How long inventory sits
- **Days Payable Outstanding (DPO):** How long you take to pay suppliers
- Shorter CCC → less capital tied up → more efficient

### Cash Management

- Motives for holding cash: transaction, precautionary, speculative
- Target cash balance models (Baumol, Miller-Orr)
- Short-term investments: T-bills, commercial paper, money market funds

### Credit Policy

- Credit standards, terms (e.g., 2/10 net 30), collection policy
- Trade-off: sales growth vs. bad debt expense and carrying costs
- Aging schedule analysis

---

## VIII. Financial Planning & Forecasting

### Pro Forma Financial Statements

- **Percent-of-sales method:** Project income statement and balance sheet items as percentage of revenue
- **External Financing Needed (EFN):**
$$EFN = \frac{A}{S}\Delta S - \frac{L}{S}\Delta S - PM \cdot S_1 \cdot (1 - d)$$

Where A/S = asset ratio, L/S = spontaneous liability ratio, PM = profit margin, d = dividend payout

### Sustainable Growth Rate

$$g^* = ROE \times b$$

Where b = retention ratio = (1 - dividend payout ratio) and ROE = NI/Equity.

### Internal Growth Rate

$$g_{int} = \frac{ROA \times b}{1 - ROA \times b}$$

### Financial Modeling Best Practices

- Three-statement model: IS → BS → CF statement (all linked)
- Separate operating assumptions from financial structure
- Scenario analysis: base, upside, downside
- Sensitivity tables (data tables) for key drivers

---

## IX. International Corporate Finance

- **Cross-border valuation:** Adjust for country risk premium, currency risk
- **Interest rate parity, purchasing power parity, international Fisher effect**
- **Foreign exchange risk:** Transaction, translation, economic exposure
- **Hedging:** Forwards, futures, options, natural hedges (matching currency revenues/costs)

---

## Key References

1. Berk, J. & DeMarzo, P. *Corporate Finance* (5th ed.). Pearson. — Primary textbook.
2. Brealey, R., Myers, S. & Allen, F. *Principles of Corporate Finance* (14th ed.). McGraw-Hill. — Classic alternative.
3. Damodaran, A. *Applied Corporate Finance* (4th ed.). Wiley. — Practical orientation.
4. Rosenbaum, J. & Pearl, J. *Investment Banking* (3rd ed.). Wiley. — LBO, M&A modeling.
5. Modigliani, F. & Miller, M. (1958). "The Cost of Capital, Corporation Finance, and the Theory of Investment." *AER*.
6. Myers, S. & Majluf, N. (1984). "Corporate Financing and Investment Decisions When Firms Have Information That Investors Do Not Have." *JFE*.
7. Jensen, M. (1986). "Agency Costs of Free Cash Flow, Corporate Finance, and Takeovers." *AER*.
8. Damodaran, A. *Damodaran Online* — http://pages.stern.nyu.edu/~adamodar/

---

*Last updated: 2026-03-22*
