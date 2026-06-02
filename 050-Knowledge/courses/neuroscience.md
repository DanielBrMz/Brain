---
title: "Course: Neuroscience"
type: course
status: active
created: 2026-03-22
tags: [knowledge, course, neuroscience, brain, fetal-development, neuroimaging]
prerequisites: [biochemistry, cell-biology, basic-anatomy]
---

# Neuroscience

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
> *See also: [[mri-physics]], [[quantum-mechanics]], [[biochemistry]], [[biomedical-engineering]]*

## Motivation

Neuroscience is directly relevant to Daniel's research at Boston Children's Hospital. Understanding the developing fetal brain — from neural tube closure to gyrification — is essential for interpreting MRI data, designing segmentation algorithms, and understanding the clinical significance of anomalies like ventriculomegaly and the neurological effects of congenital heart disease. This course covers cellular neuroscience, systems neuroscience, development, clinical neuroanatomy, and neuroimaging analysis methods.

## Prerequisites

- **Biochemistry:** Amino acids, proteins, cell signaling, ion channels (see [[biochemistry]]).
- **Cell biology:** Cell membrane structure, membrane potential, transport.
- **Basic anatomy:** Organ systems, tissue types.
- **For neuroimaging sections:** MRI physics (see [[mri-physics]]), signal processing (see [[biomedical-engineering]]).

---

## I. Cellular Neuroscience

### 1.1 The Neuron

- **Structure:**
  - Cell body (soma): nucleus, organelles, protein synthesis.
  - Dendrites: receive input. Dendritic spines as sites of excitatory synapses.
  - Axon: conducts action potentials. Axon hillock (initiation zone), nodes of Ranvier, axon terminals (boutons).
  - Myelin sheath: oligodendrocytes (CNS), Schwann cells (PNS). Saltatory conduction.
- **Types of neurons:**
  - By function: sensory (afferent), motor (efferent), interneurons.
  - By morphology: pyramidal (cortex), Purkinje (cerebellum), granule cells, stellate cells.
  - By neurotransmitter: glutamatergic, GABAergic, dopaminergic, serotonergic, cholinergic.
- **Size and numbers:** ~86 billion neurons in the adult human brain. ~85 billion non-neuronal cells (glia).

### 1.2 Glial Cells

- **Astrocytes:** Blood-brain barrier maintenance, metabolic support, glutamate uptake, synapse regulation, gliotransmission. Star-shaped, GFAP marker.
- **Oligodendrocytes:** CNS myelination. Each wraps multiple axon segments.
- **Microglia:** Resident immune cells. Synaptic pruning during development. Activated in neuroinflammation.
- **Ependymal cells:** Line ventricles, produce/circulate CSF. Cilia.
- **Schwann cells:** PNS myelination. One per internode.
- **Radial glia:** Serve as scaffolding for neuronal migration during development. Neural progenitor cells.

### 1.3 Resting Membrane Potential

- Nernst equation: $E_{\text{ion}} = \frac{RT}{zF}\ln\frac{[\text{ion}]_{\text{out}}}{[\text{ion}]_{\text{in}}}$.
- Goldman-Hodgkin-Katz equation: $V_m$ depends on permeabilities and concentrations of K$^+$, Na$^+$, Cl$^-$.
- Resting potential: $\approx -70$ mV. Dominated by K$^+$ leak channels.
- Na$^+$/K$^+$-ATPase: 3 Na$^+$ out, 2 K$^+$ in. Electrogenic pump.

### 1.4 The Action Potential

- **Hodgkin-Huxley model:**
  - $C_m \frac{dV}{dt} = -g_{\text{Na}} m^3 h (V - E_{\text{Na}}) - g_K n^4 (V - E_K) - g_L (V - E_L) + I_{\text{ext}}$
  - Voltage-gated Na$^+$ channels: activation ($m$) and inactivation ($h$) gates.
  - Voltage-gated K$^+$ channels: activation ($n$) gate.
  - $m$, $h$, $n$ satisfy first-order kinetics: $\frac{dx}{dt} = \alpha_x(V)(1-x) - \beta_x(V)x$.
- **Phases:**
  1. Threshold (~-55 mV): Na$^+$ channels begin opening (positive feedback).
  2. Depolarization: rapid Na$^+$ influx → $V$ approaches $E_{\text{Na}}$ (+50 mV).
  3. Repolarization: Na$^+$ inactivation + delayed K$^+$ activation.
  4. Hyperpolarization (undershoot): K$^+$ channels still open.
  5. Refractory period: absolute (Na$^+$ inactivated) and relative.
- **Propagation:** Continuous in unmyelinated axons. Saltatory in myelinated axons (node to node).
- **Conduction velocity:** Increases with axon diameter and myelination. Myelinated: ~100 m/s. Unmyelinated: ~1 m/s.

### 1.5 Ion Channels

- Voltage-gated: Na$^+$, K$^+$, Ca$^{2+}$. Selectivity filter, gating mechanisms.
- Ligand-gated: ionotropic receptors (nAChR, GABA$_A$, AMPA, NMDA).
- Mechanically gated. Leak channels.
- Channelopathies: genetic mutations causing epilepsy, cardiac arrhythmias, myotonia.

### 1.6 Synaptic Transmission

- **Chemical synapse:**
  1. Action potential arrives at presynaptic terminal.
  2. Voltage-gated Ca$^{2+}$ channels open. Ca$^{2+}$ influx.
  3. Ca$^{2+}$ triggers vesicle fusion (SNARE complex: synaptobrevin, syntaxin, SNAP-25).
  4. Neurotransmitter release into synaptic cleft.
  5. Binding to postsynaptic receptors. Ion channels open.
  6. Postsynaptic potential (EPSP or IPSP).
  7. Neurotransmitter cleared: reuptake, enzymatic degradation, diffusion.
- **Excitatory postsynaptic potentials (EPSP):** Depolarizing. Glutamate → AMPA/NMDA receptors → Na$^+$/Ca$^{2+}$ influx.
- **Inhibitory postsynaptic potentials (IPSP):** Hyperpolarizing or shunting. GABA → GABA$_A$ receptors → Cl$^-$ influx.
- **Integration:** Spatial summation (multiple synapses), temporal summation (rapid succession).
- **Electrical synapse (gap junctions):** Direct ionic coupling. Fast, bidirectional. Less common.

### 1.7 Neurotransmitter Systems

| Neurotransmitter | Type | Key Functions |
|-----------------|------|---------------|
| Glutamate | Amino acid (excitatory) | Primary excitatory NT. Learning (LTP via NMDA). Excitotoxicity |
| GABA | Amino acid (inhibitory) | Primary inhibitory NT (cortex). Anxiolysis. Seizure control |
| Glycine | Amino acid (inhibitory) | Inhibition in spinal cord and brainstem |
| Acetylcholine | Small molecule | NMJ, autonomic, basal forebrain (attention, memory) |
| Dopamine | Monoamine | Reward, motivation, motor control. VTA, substantia nigra |
| Serotonin (5-HT) | Monoamine | Mood, sleep, appetite. Raphe nuclei |
| Norepinephrine | Monoamine | Arousal, attention, fight-or-flight. Locus coeruleus |
| Endorphins | Neuropeptide | Pain modulation, reward |

### 1.8 Synaptic Plasticity

- **Long-term potentiation (LTP):** Persistent strengthening. NMDA receptor-dependent (Hebbian: "fire together, wire together"). Ca$^{2+}$ → CaMKII → AMPA receptor insertion.
- **Long-term depression (LTD):** Persistent weakening. Low-frequency stimulation.
- **Spike-timing-dependent plasticity (STDP):** Direction of change depends on relative timing of pre/post spikes.
- **Homeostatic plasticity:** Synaptic scaling to maintain stability.

---

## II. Systems Neuroscience

### 2.1 Sensory Systems

**Visual system:**
- Retina: photoreceptors (rods, cones) → bipolar cells → retinal ganglion cells (RGCs).
- ON/OFF center-surround receptive fields.
- Optic nerve → optic chiasm (partial decussation) → LGN (thalamus) → primary visual cortex (V1, area 17).
- V1: orientation columns, ocular dominance columns, simple/complex cells (Hubel & Wiesel).
- Ventral stream ("what"): V1 → V2 → V4 → IT (object recognition).
- Dorsal stream ("where/how"): V1 → V2 → MT/V5 → posterior parietal (spatial, motion).

**Auditory system:**
- Cochlea: tonotopic mapping (base = high frequency, apex = low).
- Hair cells → auditory nerve → cochlear nucleus → superior olive → inferior colliculus → MGB → A1 (Heschl's gyrus).
- Tonotopic organization preserved through pathway.
- Sound localization: interaural time and level differences.

**Somatosensory system:**
- Mechanoreceptors: Meissner (touch), Pacinian (vibration), Merkel (pressure), Ruffini (stretch).
- Dorsal column-medial lemniscus pathway: fine touch, proprioception.
- Spinothalamic tract: pain, temperature.
- Somatosensory cortex (S1): somatotopic map (homunculus). Brodmann areas 1, 2, 3.

### 2.2 Motor Systems

- **Motor cortex:** Primary motor cortex (M1, area 4). Premotor (area 6). SMA.
- **Corticospinal tract:** Direct pathway for voluntary movement. Lateral CST crosses at pyramidal decussation.
- **Basal ganglia:**
  - Striatum (caudate + putamen): input. Receives cortical glutamatergic input.
  - Globus pallidus (internal/external), subthalamic nucleus, substantia nigra (pars compacta/reticulata).
  - Direct pathway (facilitates movement): Cortex → Striatum (D1) → GPi/SNr (inhibition) → Thalamus (disinhibition) → Cortex.
  - Indirect pathway (inhibits movement): Cortex → Striatum (D2) → GPe → STN → GPi/SNr → Thalamus.
  - Dopamine from SNc modulates: D1 excites direct, D2 inhibits indirect.
  - Parkinson's disease: loss of SNc dopamine neurons → akinesia, rigidity, tremor.
  - Huntington's disease: striatal degeneration → chorea.
- **Cerebellum:**
  - Cerebellar cortex: molecular layer, Purkinje cell layer, granule cell layer.
  - Input: climbing fibers (inferior olive), mossy fibers (pontine nuclei).
  - Output: deep cerebellar nuclei → thalamus → cortex.
  - Functions: motor coordination, timing, error correction, motor learning.
  - Cerebellar lesions: ataxia, dysmetria, intention tremor.
  - Zones: vermis (axial), intermediate (limb), lateral (planning).

### 2.3 Limbic System

- Hippocampus: episodic memory formation, spatial navigation (place cells, grid cells). CA1-CA3 regions, dentate gyrus.
- Amygdala: emotional processing, fear conditioning, emotional memory.
- Cingulate cortex: anterior (conflict monitoring, pain), posterior (self-referential, default mode).
- Hypothalamus: homeostasis (temperature, hunger, thirst, circadian rhythm), autonomic control, hormone release.
- Fornix, mammillary bodies, septal nuclei.

### 2.4 Association Cortex and Higher Functions

- Prefrontal cortex: executive function, working memory, decision-making, planning.
- Broca's area (left inferior frontal, area 44/45): speech production.
- Wernicke's area (left posterior superior temporal, area 22): speech comprehension.
- Arcuate fasciculus: connects Broca's and Wernicke's.
- Parietal association cortex: spatial awareness, attention, integration.
- Default mode network: medial PFC, PCC, precuneus, angular gyrus. Active at rest.

---

## III. Neurodevelopment

### 3.1 Neural Tube Formation (Neurulation)

- Week 3: neural plate forms from ectoderm (induced by notochord).
- Neural folds elevate and fuse → neural tube (days 21-28).
- Anterior: brain vesicles. Posterior: spinal cord.
- Neural crest cells: migrate to form PNS, melanocytes, craniofacial structures.
- **Neural tube defects:** Anencephaly (anterior failure), spina bifida (posterior failure). Folic acid prevention.

### 3.2 Brain Vesicle Formation

- Three primary vesicles: prosencephalon (forebrain), mesencephalon (midbrain), rhombencephalon (hindbrain).
- Five secondary vesicles:
  - Telencephalon → cerebral hemispheres, basal ganglia.
  - Diencephalon → thalamus, hypothalamus.
  - Mesencephalon → midbrain (tectum, tegmentum).
  - Metencephalon → pons, cerebellum.
  - Myelencephalon → medulla oblongata.

### 3.3 Neurogenesis

- Ventricular zone (VZ) and subventricular zone (SVZ): neural progenitor proliferation.
- Symmetric division: expands progenitor pool (early).
- Asymmetric division: one progenitor + one neuron (later, neurogenic).
- Timing: peak cortical neurogenesis ~GW 12-20 in humans.
- Radial unit hypothesis (Rakic): columns of cortical neurons derive from common progenitors.

### 3.4 Neuronal Migration

- **Radial migration:** Neurons climb radial glial fibers from VZ to cortical plate. Inside-out pattern (later neurons migrate past earlier ones → Layer II outermost, Layer VI innermost).
- **Tangential migration:** Interneurons (GABAergic) from ganglionic eminences migrate tangentially into cortex.
- **Migration disorders:**
  - Lissencephaly: smooth brain, failed migration.
  - Heterotopia: neurons stuck in wrong location (periventricular, subcortical band).
  - Polymicrogyria: excessive small folds, possible late migration/organization defect.
  - Schizencephaly: cleft from ventricle to surface.

### 3.5 Cortical Layering

- Six-layer neocortex (isocortex):
  - Layer I (molecular): few neurons, mostly dendrites and axons.
  - Layer II (external granular): small pyramidal and stellate cells.
  - Layer III (external pyramidal): medium pyramidal cells. Corticocortical connections.
  - Layer IV (internal granular): stellate cells. Primary input from thalamus. Prominent in sensory cortex.
  - Layer V (internal pyramidal): large pyramidal cells (Betz cells in M1). Output to subcortical structures.
  - Layer VI (multiform/polymorphic): Corticothalamic projections.
- Transient fetal layers:
  - **Subplate:** Below cortical plate. Crucial for establishing thalamocortical connections. Contains waiting afferents. Vulnerable to hypoxia-ischemia.
  - **Marginal zone:** Becomes Layer I. Cajal-Retzius cells, reelin signaling.

### 3.6 Gyrification and Sulcation

- **Why does the cortex fold?** Differential expansion hypothesis: cortical surface area grows faster than underlying white matter volume → mechanical buckling.
- **Timing of sulcal development** (see [[mri-physics]] Section IX.4):
  - Primary sulci: ~14-28 GW (Sylvian fissure first, ~14 GW).
  - Secondary sulci: ~28-36 GW.
  - Tertiary sulci: ~36 GW to postnatal.
- **Gyrification index (GI):** Ratio of total cortical surface to exposed (outer hull) surface. Increases with gestational age. Adult GI ~2.5.
- **Sulcal depth:** Measured from outer hull to sulcal fundus. Increases during development.
- **Abnormal gyrification:**
  - Lissencephaly (agyria): absent/reduced folding.
  - Pachygyria: broad, flat gyri.
  - Polymicrogyria: excessive small folds.
  - Simplified gyral pattern: seen in congenital heart disease, chromosomal anomalies.

### 3.7 Myelination

- Onset: ~2nd trimester, accelerates in 3rd trimester and first 2 postnatal years.
- Sequence: caudal to rostral, central to peripheral, sensory before motor.
  - Brainstem and cerebellar peduncles: 2nd-3rd trimester.
  - Posterior limb of internal capsule: ~36 GW.
  - Corpus callosum: birth to ~1 year.
  - Association fibers: continue through adolescence.
- MRI appearance: myelinated WM is bright on T1, dark on T2 (reversed in unmyelinated infant brain → "T1/T2 reversal").
- Delayed myelination: marker of brain injury or developmental delay.

### 3.8 Synaptogenesis and Pruning

- Synaptogenesis: massive overproduction of synapses (peaks at ~2 years in cortex).
- Pruning: activity-dependent elimination of weak synapses. Critical periods.
- Refinement continues through adolescence (prefrontal cortex last to mature).

---

## IV. Cortical Anatomy

### 4.1 Lobes and Major Landmarks

- **Frontal lobe:** Anterior to central sulcus. Motor cortex, premotor, prefrontal, Broca's area.
- **Parietal lobe:** Between central and parieto-occipital sulci. Somatosensory, spatial processing.
- **Temporal lobe:** Below lateral (Sylvian) fissure. Auditory cortex, Wernicke's, hippocampus, fusiform face area.
- **Occipital lobe:** Posterior. Visual cortex.
- **Insular cortex:** Deep to lateral fissure. Interoception, disgust, pain.
- **Limbic lobe:** Cingulate gyrus, parahippocampal gyrus.

### 4.2 Brodmann Areas

- Cytoarchitectonic parcellation based on cellular composition.
- Key areas: 4 (M1), 1/2/3 (S1), 17 (V1), 41/42 (A1), 44/45 (Broca's), 22 (Wernicke's), 6 (premotor/SMA).
- Modern parcellations: Desikan-Killiany, Destrieux, HCP multimodal (Glasser 360-region).

### 4.3 White Matter Tracts

- **Commissural:** Corpus callosum (largest; genu, body, splenium), anterior commissure.
- **Association:**
  - Superior longitudinal fasciculus (SLF) / arcuate fasciculus: frontoparietal-temporal.
  - Inferior longitudinal fasciculus (ILF): occipitotemporal.
  - Uncinate fasciculus: frontal-temporal.
  - Cingulum: limbic.
  - Inferior fronto-occipital fasciculus (IFOF).
- **Projection:** Corticospinal tract, corona radiata, internal capsule (anterior limb, genu, posterior limb), optic radiations, thalamocortical fibers.
- Visualized with DTI tractography (see [[mri-physics]]).

### 4.4 Ventricular System

- Lateral ventricles (paired): frontal horn, body, atrium (trigone), temporal horn, occipital horn.
- Third ventricle (midline diencephalon). Foramen of Monro connects to lateral ventricles.
- Cerebral aqueduct (midbrain).
- Fourth ventricle (between pons/medulla and cerebellum). Exits: foramen of Magendie (midline), foramina of Luschka (lateral).
- CSF production: choroid plexus. CSF volume: ~150 mL (adult). Turnover: ~3x/day.
- CSF circulation: lateral ventricles → third → aqueduct → fourth → subarachnoid space → arachnoid granulations → venous sinuses.
- **Hydrocephalus:** Obstructive (non-communicating) vs. communicating. Causes: aqueductal stenosis, hemorrhage, infection, tumor.

---

## V. Clinical Neuroscience — Conditions Relevant to Research

### 5.1 Ventriculomegaly

- Atrial diameter > 10 mm on ultrasound or MRI.
- Mild (10-12 mm), moderate (12-15 mm), severe (>15 mm).
- Isolated vs. associated with other anomalies (agenesis of corpus callosum, cortical malformations).
- Prognosis depends on degree, associated findings, progression.
- Fetal MRI role: detect associated anomalies not seen on US, monitor progression.

### 5.2 Congenital Heart Disease (CHD) and Brain Development

- **Key finding:** Fetuses and neonates with CHD show delayed brain maturation.
- Reduced total brain volume, smaller cortical surface area, delayed sulcation.
- White matter injury: periventricular leukomalacia (PVL), punctate lesions.
- Mechanism: altered hemodynamics → reduced cerebral oxygen delivery → impaired brain growth.
- Specific lesions: single-ventricle physiology (HLHS) shows greatest effects.
- **Daniel's research context:** Cortical surface analysis comparing CHD fetal brains to healthy controls.

### 5.3 Heterotaxy

- Abnormal arrangement of thoraco-abdominal organs (situs inversus, situs ambiguus).
- Associated with complex CHD (especially in right atrial isomerism).
- Potential brain lateralization effects (research question).

### 5.4 Autism Spectrum Disorder (ASD)

- Neurodevelopmental disorder: social communication deficits, restricted/repetitive behaviors.
- Neuroimaging findings: early brain overgrowth, altered cortical thickness and gyrification, reduced long-range connectivity, increased local connectivity.
- Genetic heterogeneity. Environmental risk factors.
- Neuroanatomical correlates: amygdala, fusiform gyrus, superior temporal sulcus, prefrontal cortex.

### 5.5 Other Fetal Brain Anomalies

- **Agenesis of corpus callosum:** Complete or partial. Colpocephaly. Variable outcomes.
- **Dandy-Walker malformation:** Posterior fossa cyst, vermian hypoplasia, elevated tentorium.
- **Chiari malformations:** Tonsillar (I) or cerebellar/brainstem (II, with myelomeningocele) herniation.
- **Cortical malformations:** Focal cortical dysplasia, tuberous sclerosis.

---

## VI. Neuroimaging Methods

### 6.1 Structural MRI

- T1-weighted, T2-weighted, FLAIR sequences (see [[mri-physics]]).
- Volumetric analysis: brain segmentation (FreeSurfer, FSL, ANTs).
- Tissue classification: GM, WM, CSF.
- Atlas-based parcellation.

### 6.2 Cortical Surface Analysis

- **Surface reconstruction:** Extract inner (white/gray boundary) and outer (pial) surfaces.
  - Adult: FreeSurfer (recon-all), CAT12, CIVET.
  - Fetal: dHCP pipeline, DrawEM, custom pipelines on SVR-reconstructed volumes.
- **Surface metrics:**
  - **Cortical thickness:** Distance between inner and outer surfaces. ~2.5-4 mm in adults. Thinner in sulci, thicker on gyral crowns.
  - **Surface area:** Measured per vertex or per parcel. Related to tangential expansion.
  - **Curvature:** Mean curvature (negative in sulci, positive on gyri). Gaussian curvature. Curvature index.
  - **Sulcal depth:** Distance from outer hull. Quantifies folding depth.
  - **Gyrification index (GI):** Local (lGI) or global ratio of cortical to hull surface area.
  - **Fractal dimensionality:** Complexity measure of folding pattern.
- **Surface-based registration:** Align cortical surfaces across subjects using sulcal/gyral features (FreeSurfer's spherical registration, MSM).
- **Surface-based statistics:** Vertex-wise analysis. Correct for multiple comparisons (random field theory, Monte Carlo).

### 6.3 Diffusion Imaging and Tractography

- DTI, HARDI, CSD — see [[mri-physics]] Section VI.7.
- Tract-based spatial statistics (TBSS): voxel-wise analysis of FA, MD along white matter skeleton.
- Connectomics: structural connectivity matrices from tractography. Graph theory metrics (degree, clustering, modularity, small-world).

### 6.4 Functional MRI

- BOLD fMRI: task-based and resting-state (see [[mri-physics]] Section XII.1).
- Functional connectivity: correlation between time series of brain regions.
- Independent component analysis (ICA): data-driven network identification.
- Default mode network, salience network, central executive network, sensorimotor network.

---

## VII. Computational Neuroscience

### 7.1 Neural Network Models (Biological)

- Integrate-and-fire models (simplification of Hodgkin-Huxley).
- Rate models: firing rate as continuous variable.
- Attractor networks: memory retrieval, decision-making.
- Balanced excitation-inhibition: cortical dynamics.

### 7.2 Connectomics

- Structural connectome: complete wiring diagram.
- C. elegans: 302 neurons, fully mapped.
- Human: macroscale (MRI tractography), mesoscale (Allen Brain Atlas), microscale (electron microscopy, ongoing).
- Graph theory applied to brain networks: hubs, modules, rich clubs.

### 7.3 Brain Parcellation

- **Cytoarchitectonic:** Based on cellular organization (Brodmann).
- **Connectivity-based:** Regions defined by similar connectivity profiles.
- **Multimodal:** Combine structural, functional, connectivity data (HCP Glasser parcellation: 180 areas per hemisphere).
- **Fetal parcellations:** Age-specific atlases required (transient zones, different proportions).
  - CRL fetal brain atlas.
  - Gholipour et al. spatiotemporal atlas.

---

## Key Concepts Summary

| Concept | Significance |
|---------|-------------|
| Hodgkin-Huxley model | Quantitative foundation of neural excitability |
| Synaptic transmission | Communication between neurons; target of most drugs |
| Cortical layering | Six-layer structure with specific connectivity patterns |
| Neural migration | Inside-out cortical construction; disruption → malformations |
| Gyrification | Cortical folding as marker of brain development; quantifiable on MRI |
| Myelination | Progressive; sequence is a biomarker of maturation |
| Subplate | Transient fetal zone critical for circuit formation; vulnerable to injury |
| Ventriculomegaly | Common fetal finding; MRI helps determine significance |
| CHD brain effects | Altered hemodynamics → delayed brain maturation |
| Cortical surface analysis | Thickness, curvature, sulcal depth, GI — key research tools |
| Connectomics | Network-level brain organization |

---

## Recommended References

1. **Kandel, Schwartz, Jessell, Siegelbaum, Hudspeth** — *Principles of Neural Science* (6th ed.). The definitive neuroscience textbook.
2. **Bear, Connors, Paradiso** — *Neuroscience: Exploring the Brain* (4th ed.). Accessible undergraduate text.
3. **Purves et al.** — *Neuroscience* (6th ed.). Clear, well-illustrated.
4. **Volpe** — *Volpe's Neurology of the Newborn* (6th ed.). Essential reference for neonatal/fetal neurology.
5. **Stiles & Jernigan** — "The Basics of Brain Development" (Neuropsychology Review, 2010). Concise developmental review.
6. **Kostovic & Jovanov-Milosevic** — "The Development of Cerebral Connections During the First 20-45 Weeks' Gestation" (Seminars in Fetal & Neonatal Medicine, 2006).
7. **Fischl** — "FreeSurfer" (NeuroImage, 2012). Cortical surface analysis methods.
8. **Gholipour et al.** — "A Normative Spatiotemporal MRI Atlas of the Fetal Brain" (Scientific Reports, 2017).
9. **Sun et al.** — "Benchmarking Surface Reconstruction for Fetal Brain MRI" (MICCAI, 2023).

---

> *Back to [[../sciences-syllabus|Sciences Syllabus]]*
