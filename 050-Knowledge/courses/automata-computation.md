---
title: "Course: Automata & Computation"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, cs, automata, computation, complexity, theory]
prerequisites: [discrete-math, mathematical-proofs]
---

# Automata & Computation

> Back to [[../cs-syllabus|CS Syllabus]] | Related: [[compilers]], [[security-cryptography]]

## Motivation

The theory of computation answers the most fundamental questions in computer science: What can be computed? How efficiently? What are the inherent limits of any algorithm? These questions, far from being purely academic, have practical consequences — from the design of programming languages and compilers to the security of cryptographic systems (which rely on problems being hard to solve). This course traces the hierarchy of computational models from finite automata through Turing machines, and explores complexity theory, decidability, and the frontiers of quantum computation.

## Prerequisites

- Discrete mathematics: sets, functions, relations, proof techniques
- Mathematical maturity: comfort with formal definitions and proofs (induction, contradiction, construction)
- Basic programming experience (for intuition, not required formally)

---

## 1. Finite Automata

### 1.1 Deterministic Finite Automata (DFA)
- **Definition:** 5-tuple (Q, Σ, δ, q₀, F)
  - Q: finite set of states
  - Σ: finite input alphabet
  - δ: Q × Σ → Q (transition function — exactly one next state per symbol)
  - q₀ ∈ Q: start state
  - F ⊆ Q: set of accept states
- **Computation:** Read input left to right; follow transitions; accept if final state ∈ F
- **Example:** DFA for binary strings divisible by 3
  - States: {q₀, q₁, q₂} representing remainder mod 3
  - On digit d in state qᵢ: transition to q₍₂ᵢ₊ₐ₎ mod 3

### 1.2 Nondeterministic Finite Automata (NFA)
- **Definition:** Same 5-tuple but δ: Q × (Σ ∪ {ε}) → P(Q) (power set — multiple possible next states)
- **ε-transitions:** Move without consuming input
- **Acceptance:** Accept if any computation path leads to an accept state
- **Intuition:** NFA "guesses" the right path; all paths explored in parallel

### 1.3 DFA-NFA Equivalence
- **Theorem:** Every NFA has an equivalent DFA (recognizes the same language)
- **Subset construction:** DFA states are sets of NFA states; DFA simulates all parallel NFA paths
- **Cost:** NFA with n states → DFA with up to 2ⁿ states (exponential blowup, but often manageable)
- **Implication:** Nondeterminism does not add power for finite automata

### 1.4 DFA Minimization
- **Myhill-Nerode theorem:** Number of states in minimal DFA equals the number of equivalence classes of the indistinguishability relation
- **Hopcroft's algorithm:** Partition states by distinguishability; O(n log n)
- **Uniqueness:** Minimal DFA is unique (up to isomorphism) for any regular language

---

## 2. Regular Languages

### 2.1 Regular Expressions
- Base cases: ∅ (empty language), ε (empty string), a (single character)
- Operations: union (R₁ ∪ R₂), concatenation (R₁R₂), Kleene star (R*)
- Extended operations: R⁺ (one or more), R? (zero or one), character classes [a-z]
- **Equivalence:** Regular expressions describe exactly the regular languages (same as DFA/NFA)

### 2.2 Conversions
- **Regex → NFA:** Thompson's construction (systematic, ε-transitions for operators)
- **NFA → DFA:** Subset construction
- **DFA → Regex:** State elimination method (remove states one by one, label transitions with regexes)
- **Regex → DFA directly:** Derivatives of regular expressions (Brzozowski)

### 2.3 Closure Properties
- Regular languages are closed under: union, intersection, complement, concatenation, Kleene star, reversal, homomorphism
- Product construction: intersection/union of two DFAs by running them in parallel

### 2.4 Pumping Lemma for Regular Languages
- **Statement:** For any regular language L, there exists p (pumping length) such that any string s ∈ L with |s| ≥ p can be written as s = xyz where:
  1. |y| > 0 (y is non-empty)
  2. |xy| ≤ p
  3. For all i ≥ 0, xyⁱz ∈ L (y can be pumped)
- **Usage:** Prove a language is NOT regular by contradiction
  - Assume regular → pumping lemma applies → find a string that can't be pumped → contradiction
- **Example:** L = {aⁿbⁿ | n ≥ 0} is not regular
  - Choose s = aᵖbᵖ; y must be within first p characters (all a's); pumping adds a's without b's → not in L

---

## 3. Context-Free Languages

### 3.1 Context-Free Grammars (CFGs)
- **Definition:** 4-tuple (V, Σ, R, S)
  - V: set of variables (non-terminals)
  - Σ: set of terminals (disjoint from V)
  - R: set of production rules V → (V ∪ Σ)*
  - S ∈ V: start variable
- **Derivation:** Repeatedly replace a variable with the right side of a production
  - Leftmost derivation: always expand leftmost variable
  - Rightmost derivation: always expand rightmost variable
- **Parse tree:** Tree representation of a derivation; internal nodes are variables, leaves are terminals
- **Ambiguity:** A grammar is ambiguous if some string has two different parse trees
  - Some CFLs are inherently ambiguous (no unambiguous grammar exists)
- **Example:** S → aSb | ε generates L = {aⁿbⁿ | n ≥ 0}

### 3.2 Chomsky Normal Form (CNF)
- Every production is of the form A → BC or A → a (or S → ε if ε ∈ L)
- Any CFG can be converted to CNF (remove ε-productions, unit productions, useless symbols)
- CNF is required for the CYK parsing algorithm

### 3.3 CYK Algorithm
- Dynamic programming algorithm for parsing CFGs in CNF
- Time complexity: O(n³ · |G|) where n = input length, |G| = grammar size
- Fills a triangular table: cell [i, j] contains variables that can generate substring from i to j
- Decides membership and can reconstruct parse tree

### 3.4 Pushdown Automata (PDA)
- **Definition:** 6-tuple (Q, Σ, Γ, δ, q₀, F)
  - Γ: stack alphabet; δ: Q × (Σ ∪ {ε}) × (Γ ∪ {ε}) → P(Q × (Γ ∪ {ε}))
- **Stack:** Unbounded LIFO storage; can push, pop, or read top
- **Acceptance:** By final state or by empty stack (equivalent power)
- **Equivalence:** PDAs recognize exactly the context-free languages
- **Key difference from FA:** Stack provides memory; enables matching (e.g., aⁿbⁿ)
- **Nondeterminism matters:** Deterministic PDAs (DPDAs) recognize a strict subset of CFLs
  - DPDAs: LR-parsable languages; important for compiler design (see [[compilers]])

### 3.5 Pumping Lemma for CFLs
- **Statement:** For any CFL L, there exists p such that any s ∈ L with |s| ≥ p can be written as s = uvxyz where:
  1. |vy| > 0 (v and y are not both empty)
  2. |vxy| ≤ p
  3. For all i ≥ 0, uvⁱxyⁱz ∈ L
- **Example:** L = {aⁿbⁿcⁿ | n ≥ 0} is not context-free
  - Choose s = aᵖbᵖcᵖ; v and y can cover at most two of the three symbols; pumping creates imbalance

### 3.6 Closure Properties of CFLs
- Closed under: union, concatenation, Kleene star, reversal, substitution
- NOT closed under: intersection, complement (major difference from regular languages)
- Intersection with a regular language IS context-free (useful proof technique)

---

## 4. Turing Machines

### 4.1 Definition
- **7-tuple:** (Q, Σ, Γ, δ, q₀, q_accept, q_reject)
  - Γ: tape alphabet (includes blank symbol ⊔)
  - δ: Q × Γ → Q × Γ × {L, R} (deterministic TM)
  - Infinite tape (one-way or two-way); read/write head
- **Computation:** Read symbol under head; write new symbol, move head, change state
- **Halting:** Machine halts when entering q_accept or q_reject
  - May also loop forever (never halt) — this is the fundamental problem

### 4.2 Variants (All Equivalent)
- Multi-tape TM: multiple tapes with independent heads → single tape TM (polynomial slowdown)
- Nondeterministic TM: multiple possible transitions → deterministic TM (exponential slowdown)
- Two-way infinite tape, multi-dimensional tape, multi-head: all equivalent
- **Church-Turing Thesis:** Any effectively computable function can be computed by a Turing machine
  - Not a theorem (cannot be proven); universally accepted; no counterexample found

### 4.3 Universal Turing Machine
- A TM that simulates any other TM given its description as input
- Input: ⟨M, w⟩ — encoding of TM M and input w
- Foundation of stored-program computers and interpreters

---

## 5. Decidability

### 5.1 Decidable Languages (Recursive)
- A language is decidable if some TM always halts and correctly accepts/rejects
- Examples:
  - A_DFA = {⟨B, w⟩ | B is a DFA that accepts w} — simulate B on w
  - A_CFG = {⟨G, w⟩ | G is a CFG that generates w} — CYK algorithm
  - E_DFA = {⟨A⟩ | A is a DFA with L(A) = ∅} — check if any accept state is reachable
  - EQ_DFA = {⟨A, B⟩ | A, B are DFAs with L(A) = L(B)} — symmetric difference is empty

### 5.2 The Halting Problem
- A_TM = {⟨M, w⟩ | M is a TM that accepts w}
- **Theorem (Turing, 1936):** A_TM is undecidable
- **Proof by diagonalization:**
  1. Assume decider H exists: H(⟨M, w⟩) accepts if M accepts w, rejects if M doesn't accept w
  2. Construct D: on input ⟨M⟩, run H(⟨M, ⟨M⟩⟩); if H accepts, D rejects; if H rejects, D accepts
  3. Run D on ⟨D⟩: D accepts ⟨D⟩ iff H rejects ⟨D, ⟨D⟩⟩ iff D doesn't accept ⟨D⟩ — contradiction
- A_TM is recognizable (semidecidable): simulate M on w; accept if M accepts (but may loop if M doesn't)

### 5.3 Rice's Theorem
- **Statement:** Every non-trivial property of the language recognized by a TM is undecidable
- "Non-trivial": some TMs have the property and some don't
- Examples of undecidable questions: Does TM M accept the empty string? Is L(M) finite? Is L(M) regular? Is L(M) = Σ*?
- Does NOT apply to properties of the TM itself (e.g., "does M have 5 states?" is decidable)

### 5.4 Recognizable and Co-Recognizable Languages
- **Recognizable (RE):** TM accepts strings in L; may loop on strings not in L
- **Co-recognizable (coRE):** Complement is recognizable
- **Theorem:** L is decidable iff L is both recognizable and co-recognizable
  - Run TMs for L and complement in parallel; one must halt
- A_TM is recognizable but not co-recognizable; complement of A_TM is not recognizable

---

## 6. Reductions

### 6.1 Mapping Reductions
- A ≤_m B ("A reduces to B"): there exists computable function f such that w ∈ A iff f(w) ∈ B
- If A ≤_m B and B is decidable, then A is decidable
- Contrapositive: if A is undecidable and A ≤_m B, then B is undecidable
- Used to prove undecidability by reducing from known undecidable problems (usually A_TM or HALT)

### 6.2 Common Reductions
- HALT_TM (does M halt on w?) — undecidable; reduce from A_TM
- E_TM (is L(M) = ∅?) — undecidable; reduce from A_TM
- EQ_TM (do two TMs recognize the same language?) — undecidable
- ALL_TM (does M accept all strings?) — undecidable; not even recognizable

### 6.3 Polynomial-Time Reductions
- A ≤_p B: reduction function f is computable in polynomial time
- Used in complexity theory (NP-completeness)
- If A ≤_p B and B ∈ P, then A ∈ P

---

## 7. Complexity Classes

### 7.1 Time Complexity
- **O-notation:** Asymptotic upper bound on running time as function of input size
- **TIME(f(n)):** Set of languages decidable by a TM in O(f(n)) time

### 7.2 P (Polynomial Time)
- P = ∪_k TIME(n^k) — decidable in polynomial time by a deterministic TM
- Informally: "efficiently solvable" problems
- Examples: sorting, shortest path, primality testing (AKS), linear programming, 2-SAT, matching

### 7.3 NP (Nondeterministic Polynomial Time)
- **Definition 1:** Decidable in polynomial time by a nondeterministic TM
- **Definition 2 (equivalent):** A language L is in NP if there exists a polynomial-time verifier V such that w ∈ L iff there exists a certificate c with |c| = poly(|w|) and V(w, c) accepts
- Examples: SAT, graph coloring, Hamiltonian path, subset sum, traveling salesman (decision version)
- P ⊆ NP (trivially; P problems need no certificate)
- **P = NP?** The most important open question in computer science; widely believed P ≠ NP

### 7.4 coNP
- coNP = {L | complement of L is in NP}
- Examples: tautology (is a formula true for ALL assignments?), graph non-isomorphism
- P ⊆ NP ∩ coNP; if P = NP then NP = coNP

### 7.5 NP-Completeness
- A language L is NP-complete if:
  1. L ∈ NP
  2. Every language in NP is polynomial-time reducible to L (L is NP-hard)
- **Cook-Levin Theorem:** SAT (Boolean satisfiability) is NP-complete
  - Proof: encode computation of any NP verifier as a Boolean formula
- **Proving NP-completeness:** Show L ∈ NP, then reduce a known NP-complete problem to L

### 7.6 Common NP-Complete Problems and Reductions
```
SAT
├── 3-SAT (restrict clauses to 3 literals)
│   ├── Independent Set
│   │   ├── Vertex Cover (complement)
│   │   └── Clique (complement graph)
│   ├── Graph Coloring (3-COLOR)
│   ├── Hamiltonian Path
│   │   └── Traveling Salesman (decision)
│   └── Subset Sum
│       └── Partition
│           └── Bin Packing
└── Circuit-SAT
```

### 7.7 PSPACE
- PSPACE = ∪_k SPACE(n^k) — decidable using polynomial space
- P ⊆ NP ⊆ PSPACE ⊆ EXPTIME (all containments believed strict)
- PSPACE-complete: TQBF (True Quantified Boolean Formula), generalized chess/Go
- PSPACE = NPSPACE (Savitch's theorem: nondeterministic space can be simulated deterministically with a square)

### 7.8 EXPTIME
- EXPTIME = ∪_k TIME(2^(n^k)) — exponential time
- P ⊊ EXPTIME (strict containment — provably different by time hierarchy theorem)
- EXPTIME-complete: generalized chess (n×n board), certain planning problems

---

## 8. Quantum Computing Basics

### 8.1 Qubits
- Classical bit: 0 or 1; Qubit: |ψ⟩ = α|0⟩ + β|1⟩ where |α|² + |β|² = 1
- Superposition: qubit in multiple states simultaneously
- Measurement: collapses to |0⟩ with probability |α|² or |1⟩ with probability |β|²
- Entanglement: two qubits correlated; measuring one affects the other (Bell states)
- n qubits: 2ⁿ-dimensional state vector; exponential information density

### 8.2 Quantum Gates
- Unitary operations on qubit state vectors
- **Hadamard (H):** Creates superposition: H|0⟩ = (|0⟩ + |1⟩)/√2
- **Pauli gates:** X (NOT), Y, Z (phase flip)
- **CNOT:** Controlled-NOT; two-qubit gate; entangles qubits
- **Toffoli (CCNOT):** Universal for classical computation
- Quantum circuits: sequence of gates applied to qubits

### 8.3 Shor's Algorithm
- Factors integers in polynomial time: O((log N)³)
- Classical best: sub-exponential (general number field sieve)
- Implication: breaks RSA and discrete-log-based cryptography
- Core technique: quantum Fourier transform to find period of modular exponentiation
- Post-quantum cryptography: lattice-based (Kyber/ML-KEM), hash-based (SPHINCS+) — see [[security-cryptography]]

### 8.4 Grover's Algorithm
- Searches unsorted database of N items in O(√N) time (classical: O(N))
- Quadratic speedup; applies to any NP search problem
- Implication for cryptography: effectively halves symmetric key strength (AES-256 → 128-bit quantum security)

### 8.5 Complexity Class BQP
- Bounded-error Quantum Polynomial time
- Problems solvable by quantum computer in polynomial time with error probability < 1/3
- P ⊆ BQP ⊆ PSPACE (believed but not proven: BQP ⊄ NP and NP ⊄ BQP)
- Factoring ∈ BQP but believed not in P; not known to be NP-complete

---

## 9. The Chomsky Hierarchy

| Type | Grammar           | Automaton              | Example Language    | Closed Under |
|------|-------------------|------------------------|---------------------|-------------|
| 3    | Regular           | DFA / NFA              | a*b*                | ∪ ∩ * comp  |
| 2    | Context-free      | Pushdown automaton     | aⁿbⁿ               | ∪ * (not ∩ comp) |
| 1    | Context-sensitive | Linear-bounded automaton | aⁿbⁿcⁿ            | ∪ ∩ comp    |
| 0    | Unrestricted      | Turing machine         | {⟨M⟩ | M halts on ε} | ∪ ∩ (not comp) |

- Strict hierarchy: Type 3 ⊊ Type 2 ⊊ Type 1 ⊊ Type 0
- Practical relevance: lexers use Type 3, parsers use Type 2, type checkers and static analyzers often deal with undecidable problems (Type 0)

---

## 10. Practical Applications

### 10.1 Compilers
- Lexical analysis uses DFA (regular languages) — see [[compilers]]
- Parsing uses PDA/CFGs (context-free languages)
- Type checking can be undecidable in general (but restricted type systems ensure decidability)

### 10.2 Regular Expressions in Practice
- grep, sed, programming language regex engines
- Backreferences make practical regex more powerful than formal regular expressions (context-sensitive)
- Catastrophic backtracking: pathological regex can cause exponential matching time (ReDoS attacks — see [[security-cryptography]])

### 10.3 Decidability in Software
- Many program analysis questions are undecidable (Rice's theorem)
- Static analyzers use sound approximations (over-approximate or under-approximate)
- Type systems are decidable restrictions on general program behavior analysis
- Termination checking: undecidable in general; decidable for restricted programs (total functional programming)

---

## Key Concepts Summary

1. **DFA = NFA = Regular Expressions** in computational power; these define regular languages
2. **Pumping lemma** is a tool for proving languages are NOT regular (or not context-free)
3. **PDAs add a stack** to finite automata and recognize context-free languages
4. **Turing machines** are the most powerful computational model (Church-Turing thesis)
5. **The Halting Problem** is the canonical undecidable problem; Rice's theorem generalizes it
6. **P vs. NP** asks whether every problem whose solution can be verified quickly can also be solved quickly
7. **NP-completeness** identifies the hardest problems in NP; if any one is in P, then P = NP
8. **Quantum computing** threatens current cryptography (Shor's) but doesn't solve NP-complete problems efficiently

---

## References

- Sipser, M. *Introduction to the Theory of Computation* (3rd ed., 2012) — the standard textbook
- Hopcroft, J., Motwani, R., Ullman, J. *Introduction to Automata Theory, Languages, and Computation* (3rd ed., 2006)
- Arora, S. & Barak, B. *Computational Complexity: A Modern Approach* (2009) — advanced complexity theory
- Aaronson, S. *Quantum Computing Since Democritus* (2013) — accessible quantum computing
- [Complexity Zoo](https://complexityzoo.net/) — encyclopedia of complexity classes
- Nielsen, M. & Chuang, I. *Quantum Computation and Quantum Information* (10th anniv. ed., 2010)
- [Scott Aaronson's Blog](https://scottaaronson.blog/) — approachable complexity theory
