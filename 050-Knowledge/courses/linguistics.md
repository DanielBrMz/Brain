---
title: "Course: Linguistics"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, language, linguistics, phonetics, syntax]
prerequisites: [none]
---

# Linguistics

> [[../literature-syllabus|Literature & Language Syllabus]] | Related: [[literary-theory]], [[music-theory]]

## Motivation

Linguistics is the scientific study of language — the most distinctively human capacity. It asks: What do you know when you "know" a language? How is that knowledge organized in the mind? How does it vary across communities and change over time? How can we formalize it computationally? Whether your interest is in understanding human cognition, learning new languages, building NLP systems, or appreciating literature at a deeper level, linguistics provides the foundational toolkit for analyzing the structure, meaning, and use of language.

## Prerequisites

- No formal prerequisites, though some mathematical maturity helps for phonology and formal semantics
- Curiosity about language is essential

---

## I. Phonetics

### What Phonetics Studies

The physical properties of speech sounds — how they are produced (articulatory), transmitted (acoustic), and perceived (auditory).

### The International Phonetic Alphabet (IPA)

- Universal notation system for representing speech sounds
- Every symbol = one sound (phone); every sound = one symbol
- Organized by place of articulation, manner of articulation, and voicing

### Articulatory Phonetics

**Consonants** classified by three parameters:

1. **Voicing:** Voiced (vocal folds vibrating: [b, d, g, z, v]) vs. voiceless ([p, t, k, s, f])

2. **Place of articulation:**
   - Bilabial [p, b, m] — both lips
   - Labiodental [f, v] — lower lip + upper teeth
   - Dental [θ, ð] — tongue tip + teeth
   - Alveolar [t, d, n, s, z, l, r] — tongue tip + alveolar ridge
   - Post-alveolar [ʃ, ʒ, tʃ, dʒ] — behind alveolar ridge
   - Palatal [j, ɲ] — body of tongue + hard palate
   - Velar [k, g, ŋ] — back of tongue + soft palate
   - Uvular [q, ʁ] — back of tongue + uvula
   - Glottal [h, ʔ] — vocal folds

3. **Manner of articulation:**
   - Stops/plosives [p, t, k, b, d, g] — complete closure
   - Fricatives [f, s, ʃ, h] — narrow constriction
   - Affricates [tʃ, dʒ] — stop + fricative release
   - Nasals [m, n, ŋ] — oral closure, air through nose
   - Approximants [w, j, l, r] — near contact
   - Laterals [l] — air around sides of tongue
   - Trills [r] — vibration of articulator
   - Flaps/taps [ɾ] — single brief contact

**Vowels** classified by:
- **Height:** High (close) → mid → low (open): [i, e, a]
- **Backness:** Front → central → back: [i, ɨ, u]
- **Rounding:** Rounded [o, u] vs. unrounded [a, e, i]
- **Tense/lax:** Tense [i, u] vs. lax [ɪ, ʊ]

### Acoustic Phonetics

- **Sound waves:** Fundamental frequency (F0, perceived as pitch), amplitude (loudness)
- **Formants:** Resonant frequencies of the vocal tract; F1 (inversely related to height), F2 (related to backness)
- **Spectrograms:** Time × frequency × intensity visualization
- **Voice Onset Time (VOT):** Distinguishes voicing categories across languages

### Suprasegmentals

- **Stress:** Prominence on a syllable (English is stress-timed)
- **Tone:** Pitch distinguishes word meaning (Mandarin, Yoruba, Nahuatl)
- **Intonation:** Sentence-level pitch patterns (questions, statements, focus)
- **Length:** Short vs. long vowels/consonants (Japanese, Finnish, Latin)

---

## II. Phonology

### Phonemes and Allophones

- **Phoneme:** Abstract, contrastive sound unit /p/, /b/
- **Allophone:** Concrete realization in context [pʰ], [p]
- **Minimal pairs:** Prove phonemic contrast (/p/ vs. /b/: "pat" vs. "bat")
- **Complementary distribution:** Allophones of the same phoneme appear in mutually exclusive environments

### Distinctive Features (Jakobson, Chomsky & Halle)

Binary features characterizing natural classes of sounds:
- [±voice], [±sonorant], [±continuant], [±nasal], [±lateral]
- [±anterior], [±coronal], [±high], [±back], [±round]
- Enable elegant statement of phonological rules

### Phonological Rules

Formal notation: A → B / C __ D (A becomes B in the environment after C and before D)

**Common processes:**
- **Assimilation:** Sound becomes more like a neighbor (nasalization, voicing assimilation)
- **Dissimilation:** Sound becomes less like a neighbor (Grassmann's Law in Greek/Sanskrit)
- **Deletion (elision):** Sound removed in certain environments
- **Insertion (epenthesis):** Sound added (English: "something" → [sʌmpθɪŋ])
- **Metathesis:** Sounds swap order
- **Lenition:** Weakening (stops → fricatives → approximants)
- **Fortition:** Strengthening

### Syllable Structure

- **Onset-Nucleus-Coda** (C)V(C) — nucleus typically a vowel
- **Sonority Sequencing Principle:** Sonority rises toward the nucleus
- Languages vary in permitted syllable types (Japanese: (C)V; English: complex onsets/codas)

### Optimality Theory (Prince & Smolensky, 1993)

- Replace ordered rules with ranked, violable constraints
- **GEN:** Generate all possible outputs
- **EVAL:** Select the candidate that minimally violates highest-ranked constraints
- **Markedness constraints** (penalize marked structures) vs. **faithfulness constraints** (penalize deviation from input)
- Language variation = different constraint rankings

---

## III. Morphology

### Core Concepts

- **Morpheme:** Smallest meaningful unit (free: "cat"; bound: "-s", "un-")
- **Allomorph:** Variant form of a morpheme (English plural: [-s], [-z], [-ɪz])
- **Root, stem, affix** (prefix, suffix, infix, circumfix)

### Word Formation

**Inflectional morphology:** Grammatical function; doesn't change category or core meaning
- English: plural (-s), past tense (-ed), progressive (-ing), comparative (-er)
- Typically productive and regular

**Derivational morphology:** Creates new words, may change category
- un- + happy → unhappy (Adj → Adj)
- happi- + -ness → happiness (Adj → N)
- Less predictable, may be semi-productive

### Morphological Typology

- **Isolating (analytic):** One morpheme per word (Mandarin, Vietnamese)
- **Agglutinating:** Transparent, concatenative morphemes (Turkish, Swahili, Quechua)
- **Fusional (inflectional):** Morphemes fused, encode multiple features (Spanish, Latin, Russian)
- **Polysynthetic:** Single words equivalent to whole sentences (Mohawk, Inuktitut)

### Morpheme Analysis

- Identify recurring forms with consistent meanings
- Morpheme segmentation: interlinear glossing
- Morphophonological alternations: when phonology interacts with morphology

---

## IV. Syntax

### Constituency

- Sentences have hierarchical structure, not just linear order
- **Constituency tests:** Substitution (pronominalization), movement, coordination, fragment answers
- **Phrase = constituent:** NP, VP, PP, AP, AdvP

### Phrase Structure Rules and Trees

Basic template: XP → (Specifier) X' → X' → X (Head) (Complement)

### X-bar Theory

Uniform phrase structure across categories:

```
        XP
       / \
    Spec   X'
          / \
         X   Complement
        (head)
```

- **Head:** Determines category and essential properties (N, V, A, P, etc.)
- **Complement:** Sister of head; selected by head (subcategorization)
- **Specifier:** Daughter of XP; e.g., Det in NP, Subject in TP (IP)
- **Adjunct:** Additional modifier; recursive attachment

### Transformational Grammar (Chomsky, 1957, 1965)

- **Deep structure** → transformations → **surface structure**
- Movement operations: wh-movement, NP-movement (passivization, raising)
- **Traces/copies:** Moved elements leave traces in original position

### Government and Binding (GB) Theory

- Modular: X-bar, theta theory, Case theory, binding theory, bounding theory, control theory
- **Binding Theory:**
  - Principle A: Anaphors (himself) must be bound in their local domain
  - Principle B: Pronouns (him) must be free in their local domain
  - Principle C: R-expressions (John) must be free everywhere
- **Case Filter:** Every overt NP must receive abstract Case

### Minimalist Program (Chomsky, 1995+)

- Reduce syntax to minimal computational operations
- **Merge:** Combine two elements into a set {α, β} — the core operation
- **Internal Merge (Move):** Merge an element already in the structure → displacement
- **Agree:** Feature checking between probe and goal
- **Phases:** Strong phases (CP, v*P) as units of computation; spell-out at phase edges
- No deep structure/surface structure distinction; single derivation

### Key Syntactic Phenomena

- **Argument structure:** Theta roles (agent, theme, experiencer, goal)
- **Passivization:** Theme promoted to subject; agent demoted/omitted
- **Raising vs. control:** "John seems to win" vs. "John tries to win"
- **Relative clauses:** "The book [that I read __]"
- **Island constraints:** Restrictions on extraction (complex NP, adjunct, coordinate structure)

---

## V. Semantics

### Lexical Semantics

- **Sense relations:** Synonymy, antonymy, hyponymy, meronymy
- **Polysemy** (related meanings) vs. **homonymy** (unrelated meanings)
- **Semantic fields and frames** (Fillmore's frame semantics)

### Formal (Compositional) Semantics

- **Principle of compositionality (Frege):** Meaning of a complex expression = function of meanings of parts + structure
- **Denotational semantics:** Expressions denote objects in a model
  - Proper nouns → individuals: ⟦John⟧ = j
  - Predicates → sets: ⟦sleeps⟧ = {x : x sleeps}
  - Sentences → truth values

### Truth Conditions

"Snow is white" is true iff snow is white (Tarski).

- **Entailment:** A entails B iff whenever A is true, B is true
- **Presupposition:** Background assumption; survives negation
- **Implicature (Grice):** Suggested but not entailed; cancellable

### Lambda Calculus in Semantics

- Functions as meanings: ⟦sleeps⟧ = λx.sleep(x)
- **Functional application:** ⟦John sleeps⟧ = [λx.sleep(x)](j) = sleep(j)
- Enables compositional derivation of sentence meaning

### Quantification

- ⟦Every student passed⟧ = ∀x[student(x) → passed(x)]
- ⟦Some student passed⟧ = ∃x[student(x) ∧ passed(x)]
- **Scope ambiguity:** "Every student read some book" — two readings
- **Generalized quantifiers** (Barwise & Cooper)

### Pragmatics

- **Speech acts (Austin, Searle):** Locution, illocution, perlocution
- **Grice's Maxims:** Quantity, quality, relation, manner → conversational implicature
- **Relevance Theory (Sperber & Wilson):** Communication guided by optimal relevance
- **Deixis:** Context-dependent reference (I, here, now, this)
- **Presupposition triggers:** Definite descriptions, factive verbs, cleft sentences

---

## VI. Sociolinguistics

### Language Variation

- **Dialect:** Regional variety (isoglosses, dialect continua)
- **Sociolect:** Social variety (class, ethnicity, age, gender)
- **Register/style:** Formal vs. informal; code-switching
- **Labov's department store study:** Social stratification of [r] in NYC
- **Variationist sociolinguistics:** Linguistic variable, envelope of variation, multivariate analysis

### Language and Society

- **Language attitudes and ideologies:** Standard language ideology, linguistic prejudice
- **Diglossia (Ferguson):** High variety vs. low variety for different functions
- **Multilingualism and code-switching:** Grammatical constraints on switching points
- **Language policy and planning:** Corpus planning, status planning, acquisition planning
- **Language endangerment and revitalization:** ~50% of world's 7000+ languages endangered

### Pidgins and Creoles

- **Pidgin:** Simplified contact language; no native speakers
- **Creole:** Nativized pidgin; full language with native speakers
- **Decreolization:** Creole moves toward lexifier language
- Bioprogram hypothesis (Bickerton): Universal grammar shapes creole structure

---

## VII. Historical Linguistics

### Language Change

- **Sound change:** Regular and exceptionless (Neogrammarian hypothesis)
  - Grimm's Law: PIE stops → Germanic fricatives
  - Great Vowel Shift: Middle English → Modern English vowel system
- **Morphological change:** Analogy, leveling, grammaticalization
- **Syntactic change:** Word order shifts, development of auxiliaries
- **Semantic change:** Broadening, narrowing, amelioration, pejoration, metaphor, metonymy

### The Comparative Method

1. Assemble cognates across related languages
2. Identify systematic sound correspondences
3. Reconstruct proto-forms using directionality principles
4. Establish a family tree (Stammbaum model)

### Language Families

- **Indo-European:** Largest studied family (Germanic, Romance, Slavic, Indo-Iranian, Celtic, etc.)
- **Sino-Tibetan, Austronesian, Niger-Congo, Afroasiatic, Uto-Aztecan**
- Proto-language reconstruction: Proto-Indo-European (PIE)

### Internal Reconstruction and Typology

- Use alternations within a single language to infer earlier stages
- **Linguistic universals (Greenberg):** Implicational universals, word order correlations
- SOV, SVO, VSO as dominant word orders

---

## VIII. Computational Linguistics / NLP Connection

### Formal Language Theory

- **Chomsky hierarchy:** Regular → context-free → context-sensitive → recursively enumerable
- Natural languages are mildly context-sensitive (TAG, CCG frameworks)
- Finite-state automata for morphology and phonology

### Core NLP Tasks

- **Tokenization, POS tagging, parsing** (constituency and dependency)
- **Named entity recognition, semantic role labeling**
- **Machine translation:** Rule-based → statistical → neural (transformer-based)
- **Speech recognition and synthesis:** Acoustic models, language models

### Language Models

- **N-gram models:** $P(w_n | w_1, \ldots, w_{n-1}) \approx P(w_n | w_{n-k}, \ldots, w_{n-1})$
- **Neural language models:** RNNs, LSTMs → Transformers (Vaswani et al., 2017)
- **Pre-trained models:** BERT, GPT family, T5 — transfer learning revolution
- **Linguistic competence vs. performance:** What LLMs learn vs. what humans know — active research debate

### Corpus Linguistics

- Empirical approach: large text collections as evidence
- Frequency, collocation, concordance
- Annotation: POS tags, syntactic trees (Penn Treebank), semantic roles (PropBank)

---

## Key References

1. Fromkin, V., Rodman, R. & Hyams, N. *An Introduction to Language* (12th ed.). Cengage. — Accessible introduction.
2. O'Grady, W., Archibald, J. & Katamba, F. *Contemporary Linguistics* (7th ed.). Pearson.
3. Chomsky, N. (1957). *Syntactic Structures*. Mouton.
4. Chomsky, N. (1995). *The Minimalist Program*. MIT Press.
5. Ladefoged, P. & Johnson, K. *A Course in Phonetics* (7th ed.). Cengage.
6. Heim, I. & Kratzer, A. *Semantics in Generative Grammar*. Blackwell. — Formal semantics.
7. Labov, W. (1966). *The Social Stratification of English in New York City*. — Foundational sociolinguistics.
8. Campbell, L. *Historical Linguistics* (4th ed.). MIT Press.
9. Jurafsky, D. & Martin, J. *Speech and Language Processing* (3rd ed.). — NLP standard.
10. Prince, A. & Smolensky, P. (1993/2004). *Optimality Theory*. Blackwell.

---

*Last updated: 2026-03-22*
