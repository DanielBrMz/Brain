---
title: "Course: Biochemistry"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, biology, biochemistry, molecular-biology]
prerequisites: [general-chemistry, organic-chemistry, cell-biology]
---

# Biochemistry

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[neuroscience]], [[statistical-mechanics]], [[biomedical-engineering]]*

## Motivation

Biochemistry provides the molecular-level understanding of life processes. Protein structure determines enzyme function, metabolism supplies cellular energy, and gene expression controls development and disease. For neuroscience, understanding ion channels, receptor pharmacology, and neurotransmitter metabolism requires biochemistry. For MRI, tissue relaxation times depend on molecular dynamics and macromolecular composition. Biochemistry connects physics and chemistry to the biology of living systems.

## Prerequisites

- **General chemistry:** Atomic structure, chemical bonding, equilibrium, acids/bases, thermodynamics.
- **Organic chemistry:** Functional groups, stereochemistry, reaction mechanisms, carbonyl chemistry.
- **Cell biology:** Cell structure, membrane biology, organelles.

---

## I. Amino Acids and Protein Structure

### 1.1 Amino Acids

- General structure: amino group (NH$_3^+$), carboxyl group (COO$^-$), R group, alpha carbon. Chiral (L-amino acids in biology).
- **20 standard amino acids.** Classification by R group:
  - Nonpolar/hydrophobic: Gly, Ala, Val, Leu, Ile, Pro, Phe, Trp, Met.
  - Polar/uncharged: Ser, Thr, Cys, Tyr, Asn, Gln.
  - Positively charged (basic): Lys, Arg, His (pKa ~6, titratable at physiological pH).
  - Negatively charged (acidic): Asp, Glu.
- Acid-base properties: zwitterion at physiological pH. pI (isoelectric point).
- The peptide bond: planar, partial double-bond character, trans configuration. Formed by dehydration (ribosome).

### 1.2 Protein Structure Levels

- **Primary structure:** Amino acid sequence. Encoded by DNA.
- **Secondary structure:**
  - Alpha helix: 3.6 residues/turn, H-bonds between C=O of residue $i$ and N-H of residue $i+4$. Right-handed. ~1.5 A rise/residue.
  - Beta sheet: parallel and antiparallel. H-bonds between strands. Pleated.
  - Turns and loops: connect secondary elements. Beta turns often contain Pro, Gly.
  - Ramachandran plot: allowed $\phi, \psi$ backbone dihedral angles.
- **Tertiary structure:** Overall 3D fold of single polypeptide.
  - Stabilized by: hydrophobic interactions (dominant), hydrogen bonds, ionic interactions (salt bridges), disulfide bonds (Cys-Cys), van der Waals.
  - Hydrophobic core: nonpolar residues buried inside.
  - Protein domains: independently folding units (e.g., SH2, SH3, PH domains).
- **Quaternary structure:** Arrangement of multiple polypeptide subunits.
  - Hemoglobin: $\alpha_2\beta_2$ tetramer. Cooperativity.
  - Homo- and heteromeric complexes.

### 1.3 Protein Folding

- Anfinsen's dogma: sequence determines structure (thermodynamic hypothesis).
- Levinthal's paradox: impossibility of random conformational search.
- Folding funnel (energy landscape): progressive reduction of conformational entropy.
- Chaperones: Hsp70 (binds exposed hydrophobic regions), Hsp60/GroEL-GroES (folding chamber).
- Misfolding diseases: Alzheimer's (amyloid beta, tau), Parkinson's (alpha-synuclein), prions.
- **AlphaFold / computational structure prediction:** Solved the "protein structure problem" at high accuracy (CASP14, 2020).

### 1.4 Protein Function

- Enzymes (catalysis), structural proteins (collagen, keratin), transport (hemoglobin, albumin), signaling (receptors, hormones), immune (antibodies), motor (myosin, kinesin).
- Structure-function relationship: active site geometry, binding specificity.
- Post-translational modifications: phosphorylation, glycosylation, acetylation, ubiquitination, methylation.

---

## II. Enzyme Kinetics

### 2.1 Enzyme Fundamentals

- Enzymes lower activation energy ($\Delta G^\ddagger$) without altering equilibrium.
- Active site: complementary to transition state (Pauling's insight).
- Enzyme classes: oxidoreductases, transferases, hydrolases, lyases, isomerases, ligases.
- Cofactors (metal ions), coenzymes (organic molecules: NAD$^+$, FAD, CoA, PLP, TPP).

### 2.2 Michaelis-Menten Kinetics

- Model: $E + S \xrightleftharpoons{k_1/k_{-1}} ES \xrightarrow{k_{\text{cat}}} E + P$.
- Steady-state assumption: $d[ES]/dt = 0$.
- **Michaelis-Menten equation:** $v = \frac{V_{\max}[S]}{K_M + [S]}$.
  - $V_{\max} = k_{\text{cat}}[E]_T$: maximum velocity.
  - $K_M = (k_{-1} + k_{\text{cat}})/k_1$: substrate concentration at half-$V_{\max}$.
  - $k_{\text{cat}}$: turnover number (reactions per enzyme per second).
  - $k_{\text{cat}}/K_M$: catalytic efficiency (specificity constant). Upper limit ~$10^8$-$10^9$ M$^{-1}$s$^{-1}$ (diffusion-controlled).
- Lineweaver-Burk plot: $1/v$ vs. $1/[S]$. Double reciprocal. Useful for determining $K_M$ and $V_{\max}$, though statistically suboptimal.

### 2.3 Enzyme Inhibition

- **Competitive:** Inhibitor binds active site. $K_M$ increases (apparent), $V_{\max}$ unchanged. Overcome by excess substrate.
- **Uncompetitive:** Inhibitor binds ES complex only. Both $K_M$ and $V_{\max}$ decrease.
- **Noncompetitive (mixed):** Inhibitor binds E and ES. $V_{\max}$ decreases, $K_M$ may change.
- **Irreversible inhibition:** Covalent modification (e.g., aspirin on COX, nerve agents on acetylcholinesterase).
- Drug design: many drugs are enzyme inhibitors (statins, ACE inhibitors, protease inhibitors).

### 2.4 Allosteric Regulation

- Allosteric site: distinct from active site. Binding causes conformational change affecting activity.
- Concerted model (MWC): T state (tense, low affinity) ↔ R state (relaxed, high affinity). Allosteric effector shifts equilibrium.
- Sequential model (KNF): Ligand binding induces conformational change transmitted to neighboring subunits.
- Sigmoidal kinetics: $v$ vs. $[S]$ curve is S-shaped (cooperative). Hill coefficient $n_H > 1$.
- Examples: hemoglobin (O$_2$ binding), ATCase (aspartate transcarbamoylase — CTP inhibition, ATP activation), phosphofructokinase-1.
- Feedback inhibition: end product of pathway inhibits an early enzyme.

### 2.5 Enzyme Mechanisms

- Acid-base catalysis: proton transfer.
- Covalent catalysis: transient covalent enzyme-substrate intermediate (e.g., serine proteases).
- Metal ion catalysis: Lewis acid, redox, electrostatic stabilization.
- Proximity and orientation effects.
- Transition state stabilization: oxyanion hole (serine proteases), strain.
- **Serine protease mechanism (chymotrypsin):** Catalytic triad (Ser-His-Asp). Acyl-enzyme intermediate. Tetrahedral transition state.

---

## III. Metabolism

### 3.1 Overview and Thermodynamics

- Catabolism: degradation, energy release (ATP generation).
- Anabolism: biosynthesis, energy consumption.
- ATP: universal energy currency. $\Delta G^\circ' = -30.5$ kJ/mol for hydrolysis.
- Phosphoryl transfer potential. High-energy compounds: PEP, 1,3-BPG, creatine phosphate.
- NAD$^+$/NADH and FAD/FADH$_2$: electron carriers.
- Metabolic regulation: allosteric control, covalent modification (phosphorylation), gene expression, compartmentalization.

### 3.2 Glycolysis

- Location: cytoplasm. Glucose → 2 pyruvate.
- 10 enzymatic steps. Net yield: 2 ATP (substrate-level phosphorylation) + 2 NADH.
- **Key regulatory enzymes:**
  - Hexokinase (step 1): inhibited by G6P.
  - Phosphofructokinase-1 (step 3, committed step): activated by AMP, fructose-2,6-bisphosphate; inhibited by ATP, citrate.
  - Pyruvate kinase (step 10): activated by F1,6BP; inhibited by ATP, alanine.
- Fate of pyruvate:
  - Aerobic: → acetyl-CoA (pyruvate dehydrogenase complex) → TCA cycle.
  - Anaerobic: → lactate (lactate dehydrogenase, regenerates NAD$^+$) or → ethanol (yeast).

### 3.3 Pyruvate Dehydrogenase Complex (PDC)

- Pyruvate + CoA + NAD$^+$ → acetyl-CoA + CO$_2$ + NADH.
- Three enzymes (E1, E2, E3), five coenzymes (TPP, lipoamide, CoA, FAD, NAD$^+$).
- Irreversible. Regulation: product inhibition (NADH, acetyl-CoA), phosphorylation (inactivation by PDH kinase).

### 3.4 Citric Acid Cycle (TCA / Krebs Cycle)

- Location: mitochondrial matrix.
- Acetyl-CoA + OAA → citrate → ... → OAA (regenerated).
- Per acetyl-CoA: 3 NADH + 1 FADH$_2$ + 1 GTP + 2 CO$_2$.
- **Key regulatory enzymes:**
  - Isocitrate dehydrogenase: activated by ADP; inhibited by NADH.
  - Alpha-ketoglutarate dehydrogenase: inhibited by succinyl-CoA, NADH.
  - Citrate synthase: inhibited by citrate, succinyl-CoA.
- Amphibolic: both catabolic and anabolic (provides biosynthetic precursors).
- Anaplerotic reactions: replenish TCA intermediates (pyruvate carboxylase: pyruvate → OAA).

### 3.5 Oxidative Phosphorylation

- Location: inner mitochondrial membrane.
- **Electron transport chain (ETC):**
  - Complex I (NADH → ubiquinone): pumps 4 H$^+$.
  - Complex II (succinate → ubiquinone / FADH$_2$): no proton pumping.
  - Complex III (ubiquinone → cytochrome c): Q cycle, pumps 4 H$^+$.
  - Complex IV (cytochrome c → O$_2$): pumps 2 H$^+$. $O_2 + 4H^+ + 4e^- → 2H_2O$.
- Proton motive force: $\Delta p = \Delta\psi - (2.3RT/F)\Delta pH$. ~200 mV.
- **ATP synthase (Complex V):** F$_0$ (proton channel, c-ring rotation) + F$_1$ ($\alpha_3\beta_3$ catalytic head).
  - Binding change mechanism (Boyer): rotation drives conformational changes in $\beta$ subunits (open → loose → tight).
  - ~3 H$^+$ per ATP. ~10 c-subunits (organism-dependent) → ~10/3 H$^+$/ATP.
- **ATP yield:** ~30-32 ATP per glucose (P/O ratios: ~2.5 for NADH, ~1.5 for FADH$_2$).
- Regulation: respiratory control (rate proportional to ADP availability).
- Uncoupling: proton leak dissipates gradient as heat. UCP1 in brown fat (thermogenesis). DNP.
- Reactive oxygen species (ROS): superoxide from Complex I, III. SOD, catalase, glutathione peroxidase defense.

### 3.6 Gluconeogenesis

- Glucose synthesis from non-carbohydrate precursors (lactate, amino acids, glycerol).
- Location: primarily liver, some kidney.
- Bypasses three irreversible glycolytic steps:
  - Pyruvate → OAA (pyruvate carboxylase, mitochondria) → PEP (PEPCK).
  - F1,6BP → F6P (fructose-1,6-bisphosphatase).
  - G6P → glucose (glucose-6-phosphatase, ER membrane).
- Cori cycle: lactate from muscle → liver → glucose → muscle.
- Reciprocal regulation with glycolysis (PFK-1 vs. FBPase-1, mediated by F2,6BP and AMP).

### 3.7 Glycogen Metabolism

- Glycogen: branched polymer of glucose ($\alpha$-1,4 and $\alpha$-1,6 linkages).
- Glycogenesis: glycogen synthase (adds glucose from UDP-glucose).
- Glycogenolysis: glycogen phosphorylase (releases glucose-1-phosphate). Debranching enzyme.
- Regulation: hormonal (insulin, glucagon, epinephrine) via cAMP cascade.
  - Phosphorylase kinase → activates phosphorylase.
  - Protein kinase A → phosphorylates/inactivates glycogen synthase.
- Glycogen storage diseases (von Gierke, McArdle, Pompe, etc.).

### 3.8 Fatty Acid Metabolism

- **Beta-oxidation:** Mitochondrial matrix. Fatty acyl-CoA → acetyl-CoA units.
  - Carnitine shuttle for long-chain FA transport across inner membrane.
  - Each cycle: oxidation (FAD), hydration, oxidation (NAD$^+$), thiolysis.
  - Palmitoyl-CoA (C16): 7 cycles → 8 acetyl-CoA + 7 FADH$_2$ + 7 NADH.
  - ATP yield: ~106 ATP per palmitate (minus 2 for activation).
  - Regulation: malonyl-CoA inhibits CPT-1 (prevents simultaneous synthesis and oxidation).
- **Fatty acid synthesis:** Cytoplasm. Acetyl-CoA → malonyl-CoA (ACC) → fatty acid synthase (FAS).
  - Citrate shuttle exports acetyl-CoA from mitochondria.
  - NADPH as reductant (from pentose phosphate pathway, malic enzyme).
  - FAS: multifunctional enzyme. ACP (acyl carrier protein) tethers intermediates.
- Ketone bodies: acetoacetate, beta-hydroxybutyrate, acetone. Produced in liver during fasting/starvation. Fuel for brain when glucose is scarce.

### 3.9 Amino Acid Metabolism

- Transamination: aminotransferases (PLP-dependent) transfer amino groups.
- Urea cycle: disposal of excess nitrogen. Liver. 2 NH$_4^+$ + CO$_2$ + 3 ATP → urea + 2 H$_2O$.
- Glucogenic amino acids: degraded to pyruvate, OAA, alpha-KG, succinyl-CoA, fumarate.
- Ketogenic amino acids: degraded to acetyl-CoA or acetoacetate (Leu, Lys exclusively).
- Inborn errors: PKU (phenylalanine hydroxylase deficiency), maple syrup urine disease, homocystinuria.

### 3.10 Pentose Phosphate Pathway

- Produces NADPH (for biosynthesis, glutathione reduction) and ribose-5-phosphate (for nucleotide synthesis).
- Oxidative phase: G6P → ribulose-5-P + 2 NADPH + CO$_2$. Glucose-6-phosphate dehydrogenase (G6PD deficiency → hemolytic anemia).
- Non-oxidative phase: interconversion of sugars (transketolase, transaldolase). Connects to glycolysis.

---

## IV. Nucleic Acids and Gene Expression

### 4.1 DNA and RNA Structure

- Nucleotides: base + sugar (ribose/deoxyribose) + phosphate.
- Bases: purines (A, G), pyrimidines (C, T/U).
- DNA double helix (Watson-Crick): antiparallel, right-handed (B-form). A-T (2 H-bonds), G-C (3 H-bonds).
- Major and minor grooves: protein recognition.
- A-DNA, B-DNA, Z-DNA conformations.
- RNA: single-stranded (usually), ribose, uracil replaces thymine. Extensive secondary structure (hairpins, pseudoknots).
- RNA types: mRNA, tRNA, rRNA, miRNA, siRNA, lncRNA, snRNA.

### 4.2 DNA Replication

- Semi-conservative (Meselson-Stahl experiment).
- Origin of replication. Replication fork: leading strand (continuous), lagging strand (Okazaki fragments).
- Key enzymes: helicase, primase, DNA polymerase III (E. coli) / pol epsilon and delta (eukaryotes), SSB, clamp loader, sliding clamp (PCNA), ligase, topoisomerase.
- Proofreading: 3'-5' exonuclease activity. Error rate: ~$10^{-9}$ per bp (after mismatch repair).
- Telomeres and telomerase: end-replication problem.

### 4.3 Transcription

- RNA polymerase reads template 3'→5', synthesizes mRNA 5'→3'.
- Prokaryotic: single RNAP, sigma factor for promoter recognition (-10 and -35 elements).
- Eukaryotic: RNAP II (mRNA). Promoter elements: TATA box, initiator. General transcription factors (TFIIA, B, D, E, F, H). Mediator complex.
- mRNA processing (eukaryotic):
  - 5' cap: 7-methylguanosine. Protects, aids ribosome recruitment.
  - 3' polyadenylation: poly(A) tail. Stability, export.
  - Splicing: removal of introns by spliceosome (snRNPs). Alternative splicing → proteome diversity.

### 4.4 Translation

- Ribosome: 70S (prokaryotic: 30S + 50S), 80S (eukaryotic: 40S + 60S). rRNA catalytic (ribozyme).
- Genetic code: 64 codons, 20 amino acids + stop. Degenerate, near-universal.
- tRNA: anticodon-codon pairing. Aminoacyl-tRNA synthetases: charge tRNA with correct amino acid (proofreading).
- Stages:
  - Initiation: small subunit + mRNA + initiator tRNA (Met/fMet) + initiation factors → start codon (AUG).
  - Elongation: aminoacyl-tRNA delivery (EF-Tu/eEF1A) → peptide bond formation (peptidyl transferase center, 23S rRNA) → translocation (EF-G/eEF2).
  - Termination: stop codon recognized by release factors → peptide released.
- Post-translational: folding (chaperones), modifications, targeting (signal peptide → ER).

### 4.5 Gene Regulation

- **Prokaryotic:**
  - Operon model (Jacob-Monod): lac operon. Repressor, inducer (allolactose/IPTG). Positive regulation (CAP-cAMP).
  - trp operon: attenuation, repression.
- **Eukaryotic:**
  - Chromatin remodeling: histone acetylation (HATs → open), deacetylation (HDACs → closed), methylation.
  - Transcription factors: activators and repressors. Enhancers, silencers.
  - Epigenetics: DNA methylation (CpG islands), histone modifications, non-coding RNA.
  - miRNA: post-transcriptional gene silencing (RISC complex, mRNA degradation or translational repression).
  - CRISPR-Cas9: genome editing tool derived from bacterial adaptive immunity.

---

## V. Signal Transduction

### 5.1 General Principles

- Ligand (signal) → receptor → intracellular signaling cascade → cellular response.
- Specificity, amplification, desensitization, integration.

### 5.2 G Protein-Coupled Receptors (GPCRs)

- Seven transmembrane helices. Largest receptor family.
- Heterotrimeric G proteins: $G_\alpha$ (GTPase), $G_\beta$, $G_\gamma$.
- $G_s$ pathway: activates adenylyl cyclase → cAMP → PKA → phosphorylation of targets.
- $G_q$ pathway: activates PLC → IP$_3$ + DAG → Ca$^{2+}$ release + PKC activation.
- $G_i$: inhibits adenylyl cyclase.
- Desensitization: receptor phosphorylation (GRKs) → arrestin binding → internalization.
- Examples: beta-adrenergic (epinephrine), muscarinic (ACh), opioid, olfactory, rhodopsin (vision).

### 5.3 Receptor Tyrosine Kinases (RTKs)

- Ligand binding → receptor dimerization → autophosphorylation of tyrosine residues.
- Adaptor proteins (Grb2, SOS) → Ras activation → Raf → MEK → ERK (MAPK cascade).
- PI3K → PIP$_3$ → Akt pathway (cell survival, growth).
- Examples: insulin receptor, EGFR, PDGFR, VEGFR.
- Oncogenic mutations: constitutive activation (HER2 in breast cancer, BCR-ABL in CML).

### 5.4 Other Signaling Pathways

- **JAK-STAT:** Cytokine receptors → JAK phosphorylation → STAT dimerization → gene expression.
- **Wnt/beta-catenin:** Development, cell fate. Dysregulation in cancer.
- **Notch:** Cell-cell contact signaling, lateral inhibition. Neural development.
- **Hedgehog:** Patterning in embryonic development.
- **Nuclear receptors:** Intracellular receptors for lipophilic ligands (steroids, thyroid hormone, retinoids). Directly regulate transcription.

### 5.5 Second Messengers

- cAMP, cGMP, Ca$^{2+}$, IP$_3$, DAG, PIP$_3$.
- Calmodulin: Ca$^{2+}$-binding protein → activates CaMKII, calcineurin, etc.
- NO (nitric oxide): gaseous messenger → activates soluble guanylyl cyclase → cGMP.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Protein folding | Structure determines function; misfolding causes disease |
| Michaelis-Menten | Quantitative framework for enzyme kinetics |
| Allosteric regulation | Metabolic control at molecular level |
| Central dogma | DNA → RNA → Protein (with exceptions) |
| Oxidative phosphorylation | Major ATP source; chemiosmotic coupling |
| Signal transduction | How cells sense and respond to environment |
| Gene regulation | How cells differentiate and respond; epigenetics |
| Metabolic integration | Hormonal and allosteric coordination of pathways |

---

## Recommended References

1. **Berg, Tymoczko, Gatto, Stryer** — *Biochemistry* (9th ed.). The standard undergraduate text. Clear, excellent figures.
2. **Voet & Voet** — *Biochemistry* (4th ed.). More detailed, graduate level.
3. **Nelson & Cox (Lehninger)** — *Principles of Biochemistry* (8th ed.). Comprehensive, well-organized.
4. **Alberts et al.** — *Molecular Biology of the Cell* (7th ed.). More cell biology focused but essential complement.
5. **Petsko & Ringe** — *Protein Structure and Function*. Concise structure/function text.
6. **Fersht** — *Structure and Mechanism in Protein Science*. Advanced enzyme kinetics and folding.

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
