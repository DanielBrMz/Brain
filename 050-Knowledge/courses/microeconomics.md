---
title: "Course: Microeconomics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, economics, microeconomics, game-theory]
prerequisites: [calculus, linear-algebra]
---

# Microeconomics

> [[../finance-syllabus|Finance Syllabus]] | Related: [[corporate-finance]], [[econometrics]]

## Motivation

Microeconomics studies how individual agents — consumers, firms, and governments — make decisions under scarcity and how those decisions interact in markets. It provides the analytical foundation for virtually all of applied economics and finance: from understanding why firms price discriminate, to predicting auction outcomes, to designing incentive-compatible mechanisms, to evaluating policy interventions. Game theory, developed within this tradition, has become the universal language for analyzing strategic interaction across economics, political science, computer science, and biology.

## Prerequisites

- Multivariable calculus (partial derivatives, constrained optimization, Lagrange multipliers)
- [[linear-algebra]] (useful for game theory and general equilibrium)
- Basic probability (for expected utility, mixed strategies)

---

## I. Consumer Theory

### Preferences and Utility

- **Axioms of rational preference:** Completeness, transitivity, continuity
- **Utility function:** $u: \mathbb{R}^n_+ \to \mathbb{R}$ representing preferences (ordinal, not cardinal)
- **Monotonicity:** More is better
- **Convexity:** Averages preferred to extremes → diminishing marginal rate of substitution

### Indifference Curves

- Level sets of $u(x_1, x_2) = \bar{u}$
- Slope = Marginal Rate of Substitution: $MRS_{12} = -\frac{dx_2}{dx_1}\bigg|_{\bar{u}} = \frac{MU_1}{MU_2}$
- Convex to the origin for "well-behaved" preferences

### Common Utility Functions

- **Cobb-Douglas:** $u = x_1^a x_2^b$ — smooth substitution, constant expenditure shares
- **Perfect substitutes:** $u = ax_1 + bx_2$ — linear indifference curves
- **Perfect complements (Leontief):** $u = \min(ax_1, bx_2)$ — L-shaped curves
- **Quasi-linear:** $u = v(x_1) + x_2$ — no income effects for good 1
- **CES:** $u = (a x_1^\rho + b x_2^\rho)^{1/\rho}$ — elasticity of substitution $\sigma = \frac{1}{1-\rho}$

### Utility Maximization

$$\max_{x_1, x_2} u(x_1, x_2) \quad \text{s.t.} \quad p_1 x_1 + p_2 x_2 = m$$

**Optimality (interior solution):** $\frac{MU_1}{p_1} = \frac{MU_2}{p_2}$ (equal bang for the buck)

**Marshallian demand:** $x_i^*(p_1, p_2, m)$ — quantity demanded as function of prices and income

### Income and Substitution Effects (Slutsky Decomposition)

$$\frac{\partial x_i}{\partial p_j} = \underbrace{\frac{\partial h_i}{\partial p_j}}_{\text{substitution}} - \underbrace{x_j \frac{\partial x_i}{\partial m}}_{\text{income}}$$

Where $h_i$ is the Hicksian (compensated) demand.

- **Normal good:** $\partial x/\partial m > 0$
- **Inferior good:** $\partial x/\partial m < 0$
- **Giffen good:** Inferior + income effect dominates → upward-sloping demand (rare)

### Duality

- **Indirect utility:** $v(p, m) = \max u(x)$ s.t. $p \cdot x \leq m$
- **Expenditure function:** $e(p, \bar{u}) = \min p \cdot x$ s.t. $u(x) \geq \bar{u}$
- **Roy's identity:** $x_i^* = -\frac{\partial v/\partial p_i}{\partial v/\partial m}$
- **Shephard's lemma:** $h_i = \frac{\partial e}{\partial p_i}$

---

## II. Producer Theory

### Production Functions

- $Q = f(K, L)$ — output as function of capital and labor
- **Marginal product:** $MP_L = \partial f/\partial L$; diminishing marginal product
- **Returns to scale:** $f(tK, tL)$ vs. $tf(K, L)$: increasing, constant, or decreasing
- **Common forms:** Cobb-Douglas $Q = AK^\alpha L^\beta$; CES; Leontief

### Isoquants and MRTS

$MRTS_{LK} = \frac{MP_L}{MP_K}$ — rate at which capital can substitute for labor.

### Cost Minimization

$$\min_{K,L} wL + rK \quad \text{s.t.} \quad f(K,L) = Q$$

**Optimality:** $\frac{MP_L}{w} = \frac{MP_K}{r}$

### Cost Functions

- **Total cost:** $C(Q) = FC + VC(Q)$
- **Average cost:** $AC = C/Q$; **Average variable cost:** $AVC = VC/Q$
- **Marginal cost:** $MC = dC/dQ$
- **U-shaped average cost:** MC crosses AC at its minimum
- **Long-run:** All inputs variable; long-run AC envelope of short-run AC curves
- **Economies of scale:** AC decreasing in Q; **Economies of scope:** joint production cheaper

### Profit Maximization

$$\max_Q \pi = PQ - C(Q) \implies P = MC(Q) \text{ (for price-taker)}$$

**Supply curve = MC above AVC** (short-run); above AC (long-run)

---

## III. Market Structures

### Perfect Competition

- Many firms, homogeneous product, free entry/exit, price-takers
- Short-run: P = MC; firms may earn positive or negative economic profit
- Long-run equilibrium: P = MC = min AC; zero economic profit
- Efficient: P = MC → no deadweight loss

### Monopoly

- Single seller, barriers to entry, price-maker
- **MR = MC** for profit maximization; $MR = P(1 - 1/|\epsilon_d|)$
- **Deadweight loss:** Output restricted below competitive level
- **Lerner Index:** $L = \frac{P - MC}{P} = \frac{1}{|\epsilon_d|}$

**Price Discrimination:**
- **First-degree:** Charge each consumer their WTP (perfect — captures all surplus)
- **Second-degree:** Self-selection (quantity discounts, bundling, versioning)
- **Third-degree:** Segment by observable characteristic (student discounts, geography)

### Monopolistic Competition

- Many firms, differentiated products, free entry
- Short-run: behaves like monopolist for its variety
- Long-run: entry drives economic profit to zero; tangency with AC curve
- Excess capacity (produces left of min AC)

### Oligopoly

- **Cournot (quantity competition):** Firms simultaneously choose quantities; Nash equilibrium
  - $n$ identical firms: $Q^* = \frac{n}{n+1}Q_{comp}$; converges to perfect competition as $n \to \infty$

- **Bertrand (price competition):** Firms simultaneously choose prices
  - Homogeneous goods: P = MC even with just 2 firms (Bertrand paradox)
  - Differentiated goods: Prices above MC

- **Stackelberg (sequential quantity):** Leader commits to quantity first; first-mover advantage

- **Collusion and cartels:** Joint profit maximization; unstable without enforcement
  - Prisoners' dilemma structure: incentive to deviate

---

## IV. Game Theory

### Normal Form Games

- Players, strategies, payoffs (bimatrix for 2 players)
- **Dominant strategy:** Best regardless of opponent's choice
- **Dominated strategy:** Never optimal; iterated elimination (IESDS)

### Nash Equilibrium

A strategy profile where no player can profitably deviate unilaterally:
$$u_i(s_i^*, s_{-i}^*) \geq u_i(s_i, s_{-i}^*) \quad \forall s_i, \forall i$$

- Existence guaranteed in finite games (Nash, 1950) — possibly in mixed strategies
- May be multiple equilibria → refinements needed

### Mixed Strategies

Player $i$ randomizes: $\sigma_i \in \Delta(S_i)$.

At a mixed-strategy NE, each player is indifferent over the strategies in their support:
$$\mathbb{E}[u_i(s_i, \sigma_{-i})] = \mathbb{E}[u_i(s_i', \sigma_{-i})] \quad \forall s_i, s_i' \in \text{support}(\sigma_i)$$

### Canonical Games

- **Prisoners' Dilemma:** Individual rationality leads to collective suboptimality
- **Battle of the Sexes:** Coordination game with multiple equilibria
- **Matching Pennies:** No pure strategy NE; unique mixed NE
- **Stag Hunt:** Risk-dominated vs. payoff-dominated equilibria
- **Chicken/Hawk-Dove:** Anti-coordination game

### Extensive Form Games

- Game trees: nodes, branches, information sets
- **Subgame Perfect Equilibrium (SPE):** NE in every subgame; found by backward induction
- **Credible threats:** Only SPE strategies are credible
- **Information sets:** Perfect vs. imperfect information

### Repeated Games

- **Finitely repeated:** Backward induction from last period; cooperation difficult
- **Infinitely repeated:** Cooperation sustainable via trigger strategies
- **Folk Theorem:** Any feasible, individually rational payoff is achievable in an SPE for sufficiently patient players ($\delta$ close to 1)
- **Grim trigger, tit-for-tat** strategies

### Bayesian Games (Incomplete Information)

- Players have private types drawn from known distributions
- **Bayesian Nash Equilibrium:** Strategies are functions of type; best response given beliefs
- **Harsanyi transformation:** Nature moves first, assigning types

### Mechanism Design

The "inverse" of game theory: design the game (mechanism) to achieve desired outcomes.

- **Revelation Principle:** Any mechanism's outcome can be replicated by a direct, incentive-compatible mechanism
- **Incentive compatibility:** Truthful reporting is optimal
- **Individual rationality:** Participation is voluntary
- **Vickrey-Clarke-Groves (VCG) mechanism:** Efficient + incentive-compatible
- **Impossibility results:** Arrow's theorem, Gibbard-Satterthwaite, Myerson-Satterthwaite

### Auction Theory

- **Types:** English (ascending), Dutch (descending), sealed-bid first-price, sealed-bid second-price (Vickrey)
- **Revenue Equivalence Theorem (Myerson, 1981):** Under IPV, symmetric bidders, risk neutrality → all standard auctions yield same expected revenue
- **Vickrey auction:** Dominant strategy to bid true value
- **First-price sealed-bid:** Bid shading; equilibrium bid = expected value of highest competing bidder
- **Winner's curse** in common-value auctions
- **Optimal auction design (Myerson):** Revenue-maximizing with reserve prices

---

## V. General Equilibrium

### Walrasian Equilibrium

A price vector $\mathbf{p}^*$ and allocation $\mathbf{x}^*$ such that:
1. Every consumer maximizes utility at $\mathbf{p}^*$
2. Every firm maximizes profit at $\mathbf{p}^*$
3. Markets clear: aggregate demand = aggregate supply for all goods

### Existence

- Arrow-Debreu (1954): Under convexity, continuity, and non-satiation, a competitive equilibrium exists
- Uses Kakutani fixed point theorem

### Edgeworth Box

- Two consumers, two goods; visualize all feasible allocations
- Contract curve: Set of Pareto efficient allocations
- Core: Allocations that no coalition can block

---

## VI. Welfare Economics

### Fundamental Theorems

**First Welfare Theorem:** Every competitive equilibrium is Pareto efficient.
- Requires: complete markets, no externalities, no market power, no asymmetric information

**Second Welfare Theorem:** Every Pareto efficient allocation can be achieved as a competitive equilibrium with appropriate lump-sum transfers.
- Justifies redistribution via transfers rather than market intervention

### Market Failures

- **Externalities:** Pigouvian taxes/subsidies, Coase theorem (with low transaction costs)
- **Public goods:** Non-rival, non-excludable; free-rider problem; Lindahl pricing
- **Asymmetric information:** Adverse selection (Akerlof's lemons), moral hazard, signaling (Spence), screening
- **Market power:** Monopoly, oligopoly → regulation, antitrust

### Social Choice

- **Arrow's Impossibility Theorem:** No voting rule satisfies unanimity, independence of irrelevant alternatives, and non-dictatorship simultaneously
- **Utilitarian vs. Rawlsian vs. libertarian** welfare criteria

---

## VII. Behavioral Economics

### Prospect Theory (Kahneman & Tversky, 1979)

- **Reference dependence:** Utility over gains and losses relative to a reference point
- **Loss aversion:** Losses hurt ~2x as much as equivalent gains feel good
- **Diminishing sensitivity:** Concave for gains, convex for losses
- **Probability weighting:** Overweight small probabilities, underweight large ones

### Bounded Rationality (Simon)

- Satisficing vs. optimizing
- Heuristics and biases: anchoring, availability, representativeness
- Choice architecture and nudges (Thaler & Sunstein)

### Time Inconsistency

- **Hyperbolic discounting:** Present bias; $\beta$-$\delta$ model
- **Commitment devices:** Restricting future choices to align with long-run preferences
- **Procrastination and self-control** problems

### Other Key Phenomena

- Endowment effect, status quo bias
- Framing effects
- Social preferences: fairness, reciprocity, inequality aversion (Fehr-Schmidt)
- Mental accounting

---

## VIII. Information Economics

### Adverse Selection

- Pre-contractual hidden information
- Akerlof (1970): Market for lemons → market unraveling
- Solutions: signaling, screening, warranties, regulation

### Moral Hazard

- Post-contractual hidden action
- Principal-agent problem: design contracts to align incentives
- Trade-off: risk sharing vs. incentive provision
- Multi-task moral hazard (Holmström-Milgrom)

### Signaling (Spence, 1973)

- Education as signal of ability (not necessarily human capital)
- Separating vs. pooling equilibria
- Signal must be costly and differentially so by type

---

## Key References

1. Mas-Colell, A., Whinston, M. & Green, J. *Microeconomic Theory*. Oxford. — The graduate bible.
2. Varian, H. *Intermediate Microeconomics* (9th ed.). Norton. — Best intermediate text.
3. Varian, H. *Microeconomic Analysis* (3rd ed.). Norton. — Graduate companion.
4. Tirole, J. *The Theory of Industrial Organization*. MIT Press. — IO and market structure.
5. Osborne, M. & Rubinstein, A. *A Course in Game Theory*. MIT Press.
6. Fudenberg, D. & Tirole, J. *Game Theory*. MIT Press. — Advanced.
7. Kahneman, D. *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
8. Akerlof, G. (1970). "The Market for 'Lemons'." *QJE*.
9. Krishna, V. *Auction Theory* (2nd ed.). Academic Press.

---

*Last updated: 2026-03-22*
