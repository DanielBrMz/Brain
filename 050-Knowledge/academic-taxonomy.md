---
title: "Universal Knowledge & Science Taxonomy"
type: reference
status: active
created: 2026-03-22
updated: 2026-03-23
tags: [knowledge, taxonomy, curriculum, universal, sciences, humanities, philosophy]
---

# Universal Knowledge & Science Taxonomy

> Hierarchical map of all human knowledge — showing what builds on what, and how fields connect.
>
> **Legend:** `→` prerequisite · `↔` deeply related · `⇢` applies to · `[[link]]` = full course note exists

---

## I. Formal Sciences (Structural & Abstract Systems)

> The language every other science speaks. Independent of empirical observation.

### 1. Mathematics

#### 1.1 Foundations
    Arithmetic
    └─→ [[courses/logic-proof-theory|Logic & Proof Theory]]
        ├─→ [[courses/set-theory|Set Theory]]
        │   └─→ [[courses/category-theory|Category Theory]]  (also requires Abstract Algebra)
        └─→ all proof-based mathematics

#### 1.2 Algebra
    Elementary Algebra
    └─→ [[courses/linear-algebra|Linear Algebra]]
        ├─→ [[courses/abstract-algebra|Abstract Algebra]]
        │   ├─→ [[courses/commutative-algebra|Commutative Algebra]]
        │   │   └─→ [[courses/algebraic-geometry|Algebraic Geometry]]  (also requires Homological Algebra)
        │   ├─→ [[courses/homological-algebra|Homological Algebra]]  (also requires Category Theory)
        │   ├─→ [[courses/lie-algebras|Lie Algebras]]  → Mathematical Physics, Representation Theory
        │   └─→ Algebraic Number Theory, Algebraic Topology
        ├─→ Functional Analysis, Optimization, Differential Geometry
        └─⇢ Machine Learning, Quantum Mechanics, Economics

#### 1.3 Analysis
    Calculus
    └─→ [[courses/real-analysis|Real Analysis]]
        ├─→ [[courses/complex-analysis|Complex Analysis]]  → Analytic Number Theory, String Theory
        ├─→ [[courses/functional-analysis|Functional Analysis]]  (also requires Linear Algebra)
        │   └─→ Quantum Mechanics, PDE theory, Spectral Theory
        └─→ [[courses/harmonic-analysis|Harmonic Analysis]]  → Signal Processing, Wavelets

#### 1.4 Topology  ([[courses/topology|Survey]])
    Set Theory + Real Analysis
    └─→ [[courses/point-set-topology|Point-Set Topology]]
        ├─→ [[courses/algebraic-topology|Algebraic Topology]]  (also requires Abstract Algebra)
        │   └─→ [[courses/knot-theory|Knot Theory]]  → QFT, DNA topology
        ├─→ [[courses/differential-topology|Differential Topology]]  → Morse Theory, Cobordism
        └─→ Differential Geometry, Functional Analysis

#### 1.5 Geometry
    Calculus + Linear Algebra + Topology
    └─→ [[courses/differential-geometry|Differential Geometry]]
        ├─→ [[courses/projective-geometry|Projective Geometry]]  → Computer Vision, Algebraic Geometry
        ├─→ [[courses/hyperbolic-geometry|Hyperbolic Geometry]]  → Geometric Group Theory, 3-Manifolds
        ├─→ [[courses/symplectic-geometry|Symplectic Geometry]]  → Hamiltonian Mechanics
        └─⇢ General Relativity, Gauge Theory, Computer Graphics

#### 1.6 Number Theory  ([[courses/number-theory|Survey]])
    Abstract Algebra
    └─→ [[courses/elementary-number-theory|Elementary Number Theory]]
        ├─→ [[courses/analytic-number-theory|Analytic Number Theory]]  (requires Complex Analysis)
        │   └─→ Distribution of primes, Riemann Hypothesis, L-functions
        ├─→ [[courses/algebraic-number-theory|Algebraic Number Theory]]  (requires Commutative Algebra)
        │   └─→ Class Field Theory, Langlands Program
        └─→ [[courses/cryptographic-number-theory|Cryptographic Number Theory]]  (requires both Analytic + Algebraic NT)
            └─⇢ Security, Blockchain, Post-Quantum Crypto

#### 1.7 Combinatorics & Discrete Mathematics
    Logic + Elementary Algebra
    └─→ [[courses/enumerative-combinatorics|Enumerative Combinatorics]]
        ├─→ [[courses/graph-theory|Graph Theory]]  → Network Science, Algorithms, Social Networks
        ├─→ [[courses/coding-theory|Coding Theory]]  (also requires Linear Algebra) → Telecom, Quantum Error Correction
        └─→ [[courses/combinatorial-optimization|Combinatorial Optimization]]  (also requires Linear Algebra)
            └─⇢ Operations Research, Algorithm Design

#### 1.8 Probability & Statistics  ([[courses/probability-statistics|Survey]])
    Real Analysis
    └─→ [[courses/probability-theory|Probability Theory]]
        ├─→ [[courses/mathematical-statistics|Mathematical Statistics]]
        │   ├─→ [[courses/bayesian-statistics|Bayesian Statistics]]  → ML, Clinical Trials
        │   └─→ [[courses/causal-inference|Causal Inference]]  (also requires Bayesian) → Epidemiology, Policy
        ├─→ [[courses/stochastic-processes|Stochastic Processes]]
        │   └─→ [[courses/time-series|Time Series]]  → Econometrics, Signal Processing, Finance
        └─⇢ Statistical Mechanics, Machine Learning, Econometrics, Epidemiology

#### 1.9 Applied Mathematics
    Calculus + Linear Algebra
    ├─→ [[courses/numerical-analysis|Numerical Analysis]]  → Scientific Computing, FEM, CFD
    ├─→ [[courses/optimization|Optimization]]  → Machine Learning, Operations Research, Control Theory
    ├─→ [[courses/differential-equations|Differential Equations]]
    │   └─→ [[courses/dynamical-systems|Dynamical Systems]]  → Chaos, Climate Models, Neuroscience
    ├─→ [[courses/mathematical-physics|Mathematical Physics]]  (requires Diff Geo + Functional Analysis)
    │   └─→ QM, GR, Gauge Theory, Path Integrals
    └─→ [[courses/information-theory|Information Theory]]  (requires Probability)
        └─→ Coding Theory, ML, Neuroscience, Cryptography

---

### 2. Logic

> Valid reasoning — bridges math, philosophy, and computation.

    [[courses/logic-proof-theory|Formal & Mathematical Logic]]
    ├─→ Set Theory, Computability, Model Theory
    ├─⇢ Philosophy (Epistemology, Phil of Science)
    └─⇢ CS (Automata Theory, Formal Verification)

    [[courses/automata-computation|Computational Logic & Decidability]]
    └─→ Compilers, Complexity Theory, Formal Verification

    Informal & Syllogistic Reasoning
    └─→ Rhetoric, Critical Thinking, Philosophy

---

### 3. Theoretical Computer Science

    Discrete Math + Logic
    ├─→ [[courses/automata-computation|Theory of Computation]]  → Compilers, Complexity
    ├─→ [[courses/data-structures-algorithms|Algorithms & Data Structures]]  → System Design, ML
    ├─→ [[courses/information-theory|Information Theory]]  (requires Probability) → Coding, ML, Crypto
    ├─→ [[courses/quantum-computing|Quantum Computing]]  (requires Linear Algebra + Automata)
    └─→ [[courses/formal-verification|Formal Verification]]  (requires Logic + Automata) → Safety-critical systems

---

## II. Natural Sciences (The Physical Universe)

> Empirical sciences studying matter, energy, life, and the Earth. **Built on** Formal Sciences (especially Calculus, Linear Algebra, Probability, DiffEq).

### How Natural Sciences Connect

    Physics (fundamental laws)
    ├─→ Chemistry (matter and reactions)  ← applies quantum mechanics
    │   └─→ Biology (living systems)  ← applies biochemistry
    │       └─→ Medicine  ← applies physiology, genetics, immunology
    ├─→ Earth Sciences  ← applies fluid mechanics, thermodynamics
    └─→ Engineering  ← applies classical mechanics, EM, thermo

### 4. Physics

#### 4.1 Core (Classical → Modern)
    [[courses/classical-mechanics|Classical Mechanics]]  (requires Calculus, Linear Algebra, DiffEq)
    ├─→ [[courses/electromagnetism|Electromagnetism]]
    │   ├─→ [[courses/optics|Optics]]  → Lasers, Fiber Optics, Medical Imaging
    │   └─→ Special Relativity → General Relativity
    ├─→ [[courses/statistical-mechanics|Thermodynamics & Statistical Mechanics]]  (also requires Probability)
    │   └─⇢ Physical Chemistry, Condensed Matter, Astrophysics
    ├─→ [[courses/quantum-mechanics|Quantum Mechanics]]  (also requires Linear Algebra, PDEs)
    │   ├─→ [[courses/particle-physics|Particle Physics & QFT]]  (also requires Special Relativity, Group Theory)
    │   ├─→ [[courses/condensed-matter|Condensed Matter]]  (also requires Stat Mech)
    │   │   └─⇢ Materials Science, Semiconductor Physics, Superconductivity
    │   └─⇢ Physical Chemistry, Quantum Computing
    └─→ [[courses/fluid-mechanics|Fluid Mechanics]]  (also requires PDEs)
        └─⇢ Aerospace Engineering, Meteorology, CFD

#### 4.2 Intersections
    [[courses/general-relativity|General Relativity & Cosmology]]  (requires Differential Geometry, EM)
    └─→ [[courses/astrophysics|Astrophysics]]  (also requires Stat Mech, Nuclear Physics)

    [[courses/biophysics|Biophysics]]  (QM + Stat Mech + Biology)
    └─→ Protein Folding, Molecular Motors, Medical Physics

---

### 5. Chemistry

> Matter and its transformations. **Built on** physics (especially QM). **Feeds into** biology, medicine, materials.

    [[courses/general-chemistry|General Chemistry]]  (requires Algebra, basic Physics)
    ├─→ [[courses/physical-chemistry|Physical Chemistry]]  (requires Calculus, QM)
    │   └─⇢ Spectroscopy, Reaction Engineering, Materials Science
    ├─→ [[courses/organic-chemistry|Organic Chemistry]]
    │   └─→ [[courses/biochemistry|Biochemistry]]  ↔ Cell Biology
    │       └─⇢ Molecular Biology, Pharmacology, Medicine
    ├─→ [[courses/inorganic-chemistry|Inorganic Chemistry]]
    │   └─⇢ Materials Science, Catalysis, Bioinorganic
    └─→ [[courses/analytical-chemistry|Analytical Chemistry]]  (also requires Statistics)
        └─⇢ Forensics, Environmental Monitoring, Quality Control

    [[courses/materials-science|Materials Science]]  (Physical Chemistry + Condensed Matter)
    └─⇢ Engineering (all branches), Nanotechnology

---

### 6. Biology

> The science of life. **Built on** chemistry. **Feeds into** medicine, ecology, neuroscience.

    [[courses/biochemistry|Biochemistry]]
    └─→ [[courses/cell-biology|Cell Biology]]
        ├─→ [[courses/molecular-biology|Molecular Biology]]
        │   ├─→ [[courses/genetics|Genetics]]  (also requires Statistics)
        │   │   ├─→ [[courses/evolutionary-biology|Evolutionary Biology]]
        │   │   │   └─→ [[courses/ecology|Ecology]]  → Environmental Science, Conservation
        │   │   └─⇢ Genomics, GWAS, Biotechnology
        │   └─→ Microbiology → Infectious Disease, Microbiome
        ├─→ [[courses/physiology|Physiology]]
        │   ├─→ [[courses/neuroscience|Neuroscience]]  (also requires Electrophysics)
        │   │   └─⇢ Psychology, AI, Brain-Computer Interfaces
        │   └─⇢ Medicine, Pharmacology
        └─→ [[courses/immunology|Immunology]]
            └─⇢ Vaccines, Immunotherapy, Autoimmune disease

---

### 7. Earth Sciences

> The Earth as a physical-chemical-biological system. **Built on** physics, chemistry, biology.

    [[courses/geology|Geology]]  (requires Chemistry, Physics)
    ├─→ [[courses/oceanography|Oceanography]]  (also requires Fluid Mechanics, Chemistry)
    ├─→ [[courses/paleontology|Paleontology]]  (also requires Evolutionary Biology)
    └─→ [[courses/hydrology|Hydrology]]  (also requires Fluid Mechanics)

    [[courses/meteorology|Meteorology]]  (requires Fluid Mechanics, Thermodynamics)
    └─→ Climate Science → Environmental Science

    [[courses/environmental-science|Environmental Science]]  (requires Ecology, Chemistry, Meteorology)
    └─⇢ Policy, Conservation, Sustainability

---

## III. Social Sciences (Human Systems & Behavior)

> Systematic study of human behavior and institutions. **Built on** statistics and philosophy. **Feeds into** policy, law, economics.

### How Social Sciences Connect

    Neuroscience → Psychology → Sociology → Political Science
                       ↓             ↓
                   Economics ←→ Anthropology
                       ↓
                    Finance

### 8. Psychology

    [[courses/cognitive-psychology|Cognitive Psychology]]  (requires Statistics, Neuroscience basics)
    ├─→ [[courses/clinical-psychology|Clinical Psychology]]  → Psychiatry, Public Health
    ├─→ [[courses/developmental-psychology|Developmental Psychology]]  → Education, Pediatrics
    ├─→ [[courses/social-psychology|Social Psychology]]  → Sociology, Marketing, Behavioral Econ
    └─→ [[courses/behavioral-neuroscience|Behavioral Neuroscience]]  (also requires Neuroscience)
        └─→ Psychopharmacology, Neuropsychology

    ↔ Neuroscience (biological basis)
    ↔ Philosophy of Mind (consciousness, qualia)
    ⇢ AI/ML (cognitive models), UX/HCI, Education

### 9. Sociology

    [[courses/sociology|Sociology]]  (requires Social Psychology, Statistics)
    ├─→ [[courses/criminology|Criminology]]  → Criminal Justice, Policy
    ├─→ Demography → Public Health, Urban Planning
    └─→ Urban & Rural Sociology → Gentrification, Community Studies

    ↔ Economics (markets as social structures)
    ↔ Political Science (power, social movements)
    ⇢ Public Policy, Anthropology

### 10. Economics

    [[courses/microeconomics|Microeconomics]]  (requires Calculus, Optimization)
    ├─→ Game Theory, Mechanism Design
    ├─→ Behavioral Economics  (also requires Psychology)
    └─→ Labor Economics, Development Economics

    [[courses/macroeconomics|Macroeconomics]]  (requires Microeconomics, Statistics)
    └─→ Monetary Policy, Growth Theory, Public Policy

    [[courses/econometrics|Econometrics]]  (requires Statistics, Linear Algebra)
    └─→ Empirical Economics, Finance, Causal Inference

    ↔ Finance (applied economics of money and risk)
    ↔ Political Science (political economy)
    ⇢ Public Policy, Central Banking, International Development

### 11. Political Science

    [[courses/political-science|Comparative Politics]]  (requires Sociology, History)
    └─→ Democratization, Electoral Systems, Policy

    [[courses/international-relations|International Relations]]  (requires Comparative Politics, Economics)
    └─→ Diplomacy, Security Studies, International Organizations

    [[courses/political-theory|Political Theory]]  (requires Philosophy: Ethics, Epistemology)
    └─→ Constitutional Law, Justice, Civil Disobedience

    Public Policy & Administration  (requires Economics, Sociology)
    └─→ Governance, Regulation, Public Management

### 12. Anthropology & Archaeology

    [[courses/cultural-anthropology|Cultural Anthropology]]  (requires Sociology, Linguistics)
    └─→ Ethnography, Globalization Studies

    Physical/Biological Anthropology  (requires Biology, Genetics)
    └─→ Human Evolution, Forensic Anthropology

    Linguistic Anthropology  (requires Linguistics)
    └─→ Language and Culture, Endangered Languages

    [[courses/archaeology|Archaeology]]  (requires Geology, Cultural Anthropology)
    └─→ Dating Techniques, Material Culture, Settlement Patterns

---

## IV. Philosophy

> Foundational questions underlying all other fields. Every discipline has a "philosophy of X."

    Ancient (Plato, Aristotle)
    ├─→ [[courses/epistemology|Epistemology]] (What is knowledge?)
    │   ├─→ [[courses/philosophy-of-science|Philosophy of Science]]  ↔ Natural Sciences
    │   └─→ Social Epistemology, Epistemic Injustice
    ├─→ [[courses/ethics|Ethics]] (What is right?)
    │   ├─→ [[courses/political-philosophy|Political Philosophy]]  ↔ Political Science
    │   ├─→ [[courses/bioethics|Bioethics]]  ↔ Medicine, Biology
    │   └─→ AI Ethics  ↔ Computer Science
    ├─→ [[courses/metaphysics|Metaphysics]] (What is real?)
    │   └─→ [[courses/philosophy-of-mind|Philosophy of Mind]]  ↔ Neuroscience, AI
    │       └─→ Consciousness, Qualia, Extended Mind
    └─→ [[courses/aesthetics|Aesthetics]] (What is beautiful?)
        └─→ Philosophy of Art, Music, Film, Literature

    Key timeline: Socrates → Plato → Aristotle → ... → Descartes → Hume → Kant → ... →
    Hegel → Mill → Nietzsche → ... → Russell → Wittgenstein → Rawls → ... → Chalmers, Parfit

---

## V. Applied Sciences & Professional Fields

> Fields that **apply** formal and natural sciences to solve real-world problems.

### Dependency Flow

    Mathematics ──→ Computer Science ──→ Data Science
    Mathematics ──→ Engineering
    Mathematics ──→ Finance
    Physics    ──→ Engineering
    Chemistry  ──→ Engineering
    Biology    ──→ Medicine
    Chemistry  ──→ Medicine
    Psychology ──→ Medicine (Psychiatry)
    Statistics ──→ Data Science, Finance, Epidemiology

### 14. Computer Science (Applied)

#### 14.1 Systems & Infrastructure
    Computer Architecture
    └─→ [[courses/operating-systems|Operating Systems]]
        ├─→ [[courses/computer-networks|Computer Networks]]  → Distributed Systems, Security
        └─→ [[courses/distributed-systems|Distributed Systems]]  (also requires Networks, Databases)
            └─→ [[courses/system-design|System Design]]  → Cloud Architecture, SRE

    [[courses/compilers|Compilers]]  (requires Automata Theory, Data Structures)
    └─→ Language Design, JIT, VM internals

    [[courses/databases|Databases]]  (requires Data Structures)
    └─→ Data Engineering, System Design

#### 14.2 AI & Machine Learning
    Linear Algebra + Probability + Optimization + Calculus
    └─→ [[courses/machine-learning|Machine Learning]]
        └─→ [[courses/deep-learning|Deep Learning]]
            ├─→ [[courses/nlp|Natural Language Processing]]  (also requires Linguistics)
            │   └─→ LLMs, RLHF, Information Retrieval
            ├─→ [[courses/computer-vision|Computer Vision]]  → Autonomous Vehicles, Robotics
            ├─→ [[courses/reinforcement-learning|Reinforcement Learning]]  → Robotics, Game AI, RLHF
            └─→ [[courses/medical-imaging|Medical Imaging AI]]  (also requires MRI Physics)
                └─⇢ Fetal Brain Research, Clinical Diagnosis

    [[courses/mri-physics|MRI Physics]]  (requires EM, QM)
    └─→ Medical Imaging AI, Biomedical Engineering

#### 14.3 Security & Practice
    [[courses/security-cryptography|Cryptography & Security]]  (requires Number Theory, Probability)
    └─⇢ Web Security, Blockchain, Network Security

    [[courses/software-engineering|Software Engineering]]  (requires Programming, Data Structures)
    └─→ [[courses/web-development|Web Development]]  → Full-Stack, PWAs

---

### 15. Engineering

> Physics + Math **applied** to design, build, and optimize.

    [[courses/electrical-engineering|Electrical Engineering]]  (requires EM, Calculus, Linear Algebra)
    └─→ Signal Processing, Control Systems, Robotics, Power Systems

    [[courses/mechanical-engineering|Mechanical Engineering]]  (requires Classical Mechanics, Thermo, Materials)
    └─→ Machine Design, Robotics, HVAC, FEA

    [[courses/civil-engineering|Civil Engineering]]  (requires Mechanics, Fluid Mechanics, Materials)
    └─→ Structural Design, Geotechnical, Transportation, Infrastructure

    [[courses/chemical-engineering|Chemical Engineering]]  (requires Physical Chemistry, Thermo, Fluids)
    └─→ Process Design, Reaction Engineering, Separations

    [[courses/aerospace-engineering|Aerospace Engineering]]  (requires Fluid Mechanics, Control Systems, Materials)
    └─→ Aerodynamics, Propulsion, Orbital Mechanics, Flight Dynamics

    [[courses/biomedical-engineering|Biomedical Engineering]]  (requires Biology, EE, Signal Processing)
    └─→ Medical Devices, Imaging (MRI/CT/US), Prosthetics, Tissue Engineering

    Nuclear Engineering  (requires QM, Thermo)
    └─→ Reactor Physics, Radiation Shielding, Fuel Cycle, Fusion

    Environmental Engineering  (requires Chemistry, Fluid Mechanics, Ecology)
    └─→ Water Treatment, Air Quality, Remediation

---

### 16. Finance

> Economics + Mathematics **applied** to money, risk, and markets.

#### 16.1 Classical Finance
    [[courses/accounting|Accounting]]
    ├─→ [[courses/corporate-finance|Corporate Finance]]  (also requires Microeconomics)
    │   └─→ [[courses/equity-analysis|Equity Analysis]]  → Investing, Portfolio Management
    └─→ [[courses/banking|Banking]]  (also requires Macroeconomics)
        └─→ [[courses/fixed-income|Fixed Income]]  → Interest Rate Models, Credit Risk

#### 16.2 Portfolio Theory  ([[courses/portfolio-theory|Survey]])
    [[courses/modern-portfolio-theory|Modern Portfolio Theory]]  (requires Linear Algebra, Statistics)
    ├─→ [[courses/factor-models|Factor Models]]  (also requires Econometrics)
    ├─→ [[courses/asset-allocation|Asset Allocation]]  (also requires Optimization)
    └─→ [[courses/alternative-investments|Alternative Investments]]  (PE, Hedge Funds, Real Estate)

#### 16.3 Quantitative Finance  ([[courses/quantitative-finance|Survey]])
    [[courses/stochastic-calculus|Stochastic Calculus]]  (requires Probability Theory, Real Analysis)
    └─→ [[courses/derivatives|Derivatives]]  (Black-Scholes, Greeks, Exotic Options)
        ├─→ [[courses/interest-rate-models|Interest Rate Models]]  (also requires Fixed Income)
        ├─→ [[courses/credit-risk|Credit Risk]]  → CDS, CDO, CVA
        └─→ [[courses/risk-management|Risk Management]]  → VaR, Stress Testing, Basel

    [[courses/market-microstructure|Market Microstructure]]  (requires Statistics, Stochastic Processes)
    └─→ HFT, Algorithmic Execution, Order Book Dynamics

    [[courses/mathematical-finance|Mathematical Finance]]  (Stochastic Control, Optimal Stopping, Monte Carlo)

---

### 17. Medicine & Health Sciences

> Biology + Chemistry **applied** to human health.

    [[courses/anatomy|Anatomy]] + [[courses/physiology|Physiology]] + [[courses/biochemistry|Biochemistry]]
    └─→ [[courses/pathology|Pathology]]  (also requires Immunology)
        └─→ Clinical Diagnosis, Oncology

    [[courses/pharmacology|Pharmacology]]  (requires Biochemistry, Physiology)
    └─→ Drug Development, Clinical Medicine

    [[courses/epidemiology|Epidemiology]]  (requires Biostatistics)
    └─→ [[courses/public-health|Public Health]]  → Health Policy, Global Health

    [[courses/psychiatry|Psychiatry]]  (requires Pathology, Pharmacology, Psychology)
    └─→ Psychopharmacology, Psychotherapy

---

### 18. Data Science

> Statistics + CS **applied** to extracting knowledge from data.

    Statistics + Python + SQL
    └─→ [[courses/data-science|Data Science Foundations]]
        ├─→ Predictive Modeling  (requires ML)
        ├─→ Data Engineering  (requires Databases, Distributed Systems)
        └─→ Data Visualization  → Dashboards, Storytelling

---

## VI. Humanities & Arts

> Human culture, expression, and meaning.

### 19. Literature & Language

    [[courses/linguistics|Linguistics]]  → NLP, Anthropology, Language Teaching
    [[courses/literary-theory|Literary Theory]]  → Criticism, Cultural Studies
    [[courses/world-literature|World Literature]]  — Borges, García Márquez, Rulfo, Dostoevsky, Kafka, Joyce
    [[courses/poetry|Poetry]]  — Forms, prosody, imagery; Neruda, Paz, Dickinson, Rilke
    [[courses/creative-writing|Creative Writing]]  — Narrative, character, revision; Gardner, King
    [[courses/rhetoric|Rhetoric]]  — Argumentation, persuasion, fallacies; Aristotle, Burke

### 20. Music

    [[courses/music-theory|Music Theory]]  → Composition, Arranging
    └─→ [[courses/songwriting|Songwriting]]  → Performance, Production

    [[courses/music-history|Music History]]  — Medieval → Classical → Jazz → Rock → Electronic → Latin

---

## VII. Cross-Disciplinary Intersections

> Fields that emerge **at the boundaries** — often the most fertile ground.

    Biology ────── + Philosophy ──→ [[courses/bioethics|Bioethics]]
    Geography ──── + Political Sci → Geopolitics
    Neuroscience ─ + Economics ───→ [[courses/neuroeconomics|Neuroeconomics]]
    Biology ────── + Physics ─────→ [[courses/biophysics|Biophysics]]
    CS ──────────── + Humanities ──→ Digital Humanities
    Mathematics ── + Finance ────→ [[courses/mathematical-finance|Mathematical Finance]]
    Psychology ─── + CS + Neuro ──→ Cognitive Science
    CS ──────────── + Medicine ───→ Biomedical Informatics
    Sociology ──── + Hist of Sci → Science & Technology Studies (STS)

---

## Syllabi Index

| Division | Syllabus | Courses |
|----------|----------|---------|
| I. Formal Sciences | [[math-syllabus]], [[cs-syllabus]] | ~45 |
| II. Natural Sciences | [[sciences-syllabus]], [[earth-sciences-syllabus]] | ~30 |
| III. Social Sciences | [[social-sciences-syllabus]] | ~15 |
| IV. Philosophy | [[philosophy-syllabus]] | ~7 |
| V. Applied Sciences | [[engineering-syllabus]], [[medicine-syllabus]], [[finance-syllabus]] | ~45 |
| VI. Humanities | [[literature-syllabus]] | ~10 |

**Total: 150+ curriculum entries · 111 full course notes in `courses/`**

---

## Related

- [[knowledge-index|Knowledge Index]]
- [[../040-Roles/research-engineer-bch|BCH Research Role]]
- [[../040-Roles/sr-fullstack-sidepocket|Sidepocket Role]]
- [[../030-Projects/projects-index|Projects Index]]
