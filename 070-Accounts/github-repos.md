---
title: "GitHub Repository Details — Per-Repo Documentation"
type: reference
status: active
created: 2026-03-22
updated: 2026-03-22
tags: [github, repos, reference, detailed]
---

# GitHub Repository Details

> Per-repo documentation with file structures, stacks, and key files.
> For the concise index, see [[../030-Projects/github-repos|GitHub Repos Index]].

Audited: 2026-03-22

## User: DanielBrMz

25 total repositories (23 original, 2 forks)

## Organization: Sidepocketinc

29 repos accessible: stratz, auth, redis, sidepocket-mobile-app, sp_wordpress, accounts, postgres_db, lambda_stratz_update, app-backend, SP-Web-App, beta-react, validate, sidepocket-admin, util, billing, events, cash, portfolio, keycloak_flask, cloudmapper, dynamodblocal, dotfiles, webapp, endorser-cms, earthfile, github-release, backend-api-testing, sp-endorser-cms, website, features

---

## Personal Repos (Original Code)

### Research / BCH / MRI

#### vanguard-mri-harmonization
- **Language:** Python | **Stars:** 0 | **Updated:** 2025-09-24
- **Description:** VANGUARD - Variational Anatomical Neural Generator for Unified and Adaptive Reconstruction in Diverse imaging. Bayesian deep learning for cross-site MRI harmonization with uncertainty quantification.
- **Stack:** PyTorch 2.0+, Python 3.8+, Conda, Docker
- **Status:** Under active development
- **Key files:**
  ```
  src/vanguard/core/bayesian_layers.py
  src/vanguard/core/uncertainty_quantification.py
  src/vanguard/core/mathematical_utils.py
  configs/model/vanguard_base.yaml
  configs/data/synthetic_validation.yaml
  tests/ (unit, integration, mathematical)
  ```

#### iguane_harmonization_t2
- **Language:** Python | **Stars:** 0 | **Updated:** 2025-11-04
- **Description:** 3D generalizable CycleGAN for multicenter harmonization of brain MR images. Adapted for T2-weighted fetal brain MRI.
- **Stack:** TensorFlow, CycleGAN, NIfTI processing
- **Contains:** iguane_original/ (3D T1 adult) + iguane_2d/ (2D fetal T2, in development)
- **Key files:**
  ```
  iguane_2d/training/train_fetal_2d_cyclegan.py
  iguane_2d/evaluation/ (multiple evaluation scripts)
  iguane_2d/harmonization/harmonize_and_enhance.py
  iguane_2d/preprocessing/
  iguane_original/all_in_one.py
  iguane_original/harmonization/
  iguane_original/prediction/
  ```

### Flagship Projects

#### Phoenix
- **Language:** TypeScript | **Stars:** 2 | **Updated:** 2024-09-14
- **Description:** AI wildfire prevention and tracking web app. 3D mapping with Mapbox, real-time alerts, fire spread prediction (95% satellite image accuracy). NASA Space Apps Global Finalist.
- **Stack:** Next.js, TypeScript, tRPC, Mapbox, deck.gl, Zustand, Tailwind CSS, Prisma
- **Key files:**
  ```
  src/Components/MyMap.tsx
  src/Components/Layers/ServicesLayer.tsx
  src/Components/Alerts/EmergencyAlerts.tsx
  src/server/api/routers/fire_prediction.ts
  src/store/ (alertsStore, layersStore, wildfiresStore)
  src/utils/mapUtils/
  src/pages/MenuPages/PredictionPages/
  ```

#### PocketDoctor
- **Language:** PHP (Backend) + Dart (Frontend) | **Stars:** 1 | **Updated:** 2023-10-27
- **Description:** Medical booking app with doctor appointment management.
- **Stack:** Laravel (Jetstream, Sanctum, Fortify), Flutter (Dart), SQLite
- **Key files:**
  ```
  Backend/app/Http/Controllers/AppointmentsController.php
  Backend/app/Http/Controllers/DocsController.php
  Backend/app/Models/ (User, Doctor, Appointments, Reviews)
  Frontend/lib/screens/ (home, booking, doctor_details, appointment)
  Frontend/lib/providers/dio_provider.dart
  ```

#### ITCademy
- **Language:** Python (Backend) + TypeScript (Frontend) | **Stars:** 3 | **Updated:** 2024-05-29
- **Description:** Education platform.
- **Stack:** Django backend (Docker), Next.js frontend (Tailwind, Yarn)
- **Key files:**
  ```
  backend/core/settings.py
  backend/core/urls.py
  backend/templates/email/
  frontend/src/app/
  ```

### Data Structures & Algorithms

#### DSA
- **Language:** C++ | **Stars:** 0 | **Updated:** 2025-02-17
- **Description:** "Disappointment to Success Archive" - Comprehensive DSA implementations.
- **Covers:** Arrays (circular, dynamic, sparse, multi-dimensional, matrix), LinkedLists (singly, doubly, circular, skip, unrolled, XOR), Queues (circular, deque, priority, thread-safe), Stacks (min, thread-safe), Trees (BST, AVL, splay, scapegoat, cartesian, threaded, B-tree, B+tree)
- **Key files:**
  ```
  DataStructures/CPP/Linear/Arrays/
  DataStructures/CPP/Linear/LinkedLists/
  DataStructures/CPP/Linear/Queue/
  DataStructures/CPP/Linear/Stack/
  DataStructures/CPP/Trees/Binary/
  DataStructures/CPP/Trees/MultiWay/
  ```

### Mobile App Clones

#### Pulsar
- **Language:** TypeScript | **Stars:** 2 | **Updated:** 2024-05-13
- **Description:** Mobile app clones (Uber clone implemented).
- **Stack:** React Native (Expo), TypeScript, Google Maps
- **Key files:**
  ```
  custom-uber/src/screens/HomeScreen.tsx
  custom-uber/src/screens/RequestScreen.tsx
  custom-uber/src/navigation/ (Drawer, Root, Stack Navigators)
  custom-uber/src/global/ (data, mapStyle, styles)
  ```

### Game Development

#### Red-Antenna
- **Language:** ShaderLab/C# | **Stars:** 0 | **Updated:** 2024-05-21
- **Description:** 2D Unity game with WebGL build.
- **Key files:**
  ```
  Assets/scripts/playerController.cs
  Assets/scripts/projectileSpawner.cs
  Assets/scripts/coinScript.cs
  Assets/scripts/GUIMenu.cs
  Assets/Projectile.cs
  Build/ (WebGL deployment)
  ```

### Web / Portfolio

#### portfolio-website
- **Language:** TypeScript | **Stars:** 0 | **Updated:** 2023-09-17
- **Description:** Personal portfolio website.
- **Stack:** Next.js, Tailwind CSS
- **Key files:** `app/page.tsx`, `app/layout.tsx`

#### DanielBrMz (Profile README)
- **Updated:** 2025-10-27
- **Contains:** GitHub profile README with bio, tech stack, achievements

### R / Bioinformatics

#### Automaton-Project
- **Language:** R | **Stars:** 0 | **Updated:** 2024-05-27
- **Contains:** WhatsApp chat analyzer, R data converter
- **Key files:** `WhatsApp Analyzer/main.R`, `Converter/Project3.R`

#### R-snippets
- **Language:** R | **Stars:** 1 | **Updated:** 2025-04-03
- **Description:** Bioinformatics R code - virus databases (NCBI), phylogenetic trees, molecular biology
- **Key files:**
  ```
  Base de datos de virus de NCBI/ (Dengue, SARS-COV-2, Zika FASTA)
  Arboles Filogeneticos en R/
  biomol/R_biomol.Rmd
  Evidencia/
  ```

### Course Repos (Tec de Monterrey)

#### TC1031 (Data Structures - Baldo)
- **Language:** Python/C++ | **Stars:** 8 | **Updated:** 2024-08-19
- **Content:** Sorting, searching, linked lists, stacks, queues, BST, hash tables, graphs, priority queues
- **Key dirs:** `C++/` (activities 1.1-5.2), `Python/` (activities 1.1-5.2)

#### TC2005B (Web Development)
- **Language:** HTML/JS/TypeScript | **Stars:** 0 | **Updated:** 2024-06-10
- **Content:** Calculator, Caesar cipher, Poke-Project (React+TypeScript Pokedex), MusicApp (Spotify API), user-integration (full-stack with Nearbyy RAG, OpenAI, Shadcn/UI)
- **Key projects:** `Poke-Project/`, `user-integration/`, `MusicApp/`, `server_start/`

#### TC2007B (Mobile Development)
- **Language:** TypeScript/Kotlin | **Stars:** 0 | **Updated:** 2024-11-11
- **Content:** React Native Expo apps (Firebase DB access, persistent data, multimedia player), Android Kotlin (UI Development with Jetpack Compose)
- **Key dirs:** `Acceso_Base_Datos/`, `Manejo_Datos_Persistentes/`, `Multimedia/`, `UI_Development/`

#### TC2008B (Multiagent Systems - Dounce)
- **Language:** Python/C# | **Stars:** 1 | **Updated:** 2024-09-09
- **Content:** Unity multiagent simulations, computational vision server, Mesa agent framework, traffic simulation
- **Key dirs:** `Arhivos_Unity_Reto/`, `Python/Mesa/`

#### TC2037 (Compilers/Languages - Ceja)
- **Language:** Rust | **Stars:** 1 | **Updated:** 2024-04-25
- **Content:** Expression parser, lexical highlighter (Rust)
- **Key files:** `Project 1/src/main.rs`, `project_2_lexical_highlighter/src/main.rs`

#### TC2038B (Advanced Algorithms - Reyes)
- **Language:** C++ | **Stars:** 0 | **Updated:** 2024-12-03
- **Content:** Merge sort, dynamic programming, greedy algorithms, hash tables, graph algorithms
- **Key dirs:** `Act1.1/`-`Act1.3/`, `E1/`, `E2/`, `Support/` (HashTable with SHA3, memoization)

#### TC3004-5B.M5 (Design Patterns)
- **Language:** Python | **Stars:** 0 | **Updated:** 2025-04-11
- **Content:** Abstract Factory, Decorator Pattern, Builder Pattern (Pygame game)
- **Key dirs:** `AbstractFacotory/`, `DecoratorPattern/`, `Game/`

#### TC3004B (Cloud/Modules)
- **Language:** TypeScript/Java/Python | **Stars:** 0 | **Updated:** 2025-05-06
- **Content:** M5 (design patterns), M6 (React movie app with Firebase), M11 (Spring Boot OCI microservice with Oracle DB)
- **Key dirs:** `M5/`, `M6/`, `M11/`

#### TC3005B (Software Engineering)
- **Language:** TypeScript/Java | **Stars:** 0 | **Updated:** 2025-06-10
- **Content:** M6 (game-hub + online-store, both React+TypeScript+Firebase), M11 (Java Paint App with Swing)
- **Key dirs:** `M6/game-hub/`, `M6/online-store/`, `M11/JavaPaintApp/`

### Other

#### Matlab-Scripts
- **Language:** MATLAB | **Stars:** 0 | **Updated:** 2024-05-13
- **Description:** Physics and engineering MATLAB scripts
- **Dirs:** `F-1004B/`, `F-1005B/`, `F-1008/`, `F-1013/`, `F-1014/`, `TC-1003B/`, `Pruebas/`

#### React-topics
- **Language:** TypeScript | **Stars:** 2 | **Updated:** 2024-06-09
- **Description:** React learning snippets covering basics, context, memoization, reducers, redux, routes
- **Key dirs:** `React-basics/`, `React-context/`, `React-memoization/`, `React-reducers/`, `React-redux/`, `React-routes/`

---

## Forked Repos

| Repo | Original | Language | Description |
|------|----------|----------|-------------|
| c302 | openworm/c302 | Python | The c302 framework (neural modeling) |
| TC1002S | (unknown) | Jupyter Notebook | Course repo |

---

## Language Distribution

| Language | Repos |
|----------|-------|
| TypeScript | 8 (Phoenix, portfolio-website, Pulsar, React-topics, TC2005B, TC2007B, TC3004B, TC3005B) |
| Python | 6 (iguane_harmonization_t2, ITCademy, TC1031, TC2008B, TC3004-5B.M5, vanguard-mri-harmonization) |
| C++ | 3 (DSA, TC2038B, TC1031) |
| R | 2 (Automaton-Project, R-snippets) |
| Rust | 1 (TC2037) |
| MATLAB | 1 (Matlab-Scripts) |
| PHP/Dart | 1 (PocketDoctor) |
| ShaderLab/C# | 1 (Red-Antenna) |
| HTML | 1 (TC2005B) |
| Jupyter | 1 (TC1002S) |

---

## Highlights by Impact

| Achievement | Repo |
|------------|------|
| NASA Space Apps Global Finalist | Phoenix |
| Most starred (8) | TC1031 |
| Active research (BCH/HMS) | vanguard-mri-harmonization, iguane_harmonization_t2 |
| Most comprehensive DSA | DSA (30+ data structure implementations) |
| Full-stack showcase | PocketDoctor, ITCademy, TC2005B user-integration |

> See also: [[../030-Projects/github-repos|GitHub Repos Overview]]
