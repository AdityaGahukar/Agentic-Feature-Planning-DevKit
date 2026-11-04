# Agentic Feature Planning DevKit — High-Level Design (HLD)

> **Document Version:** 1.0.0  
> **Status:** Ready for Review  
> **Traceability Target:** `specs/agentic_feature_planning_devkit_spec.md` (v0.2.0)  
> **Author:** Antigravity AI + Project Architecture Team  
> **Date:** 2026-11-04  

---

## Table of Contents

1. [Executive Summary & System Objectives](#1-executive-summary--system-objectives)
2. [Architectural Principles & Spec Alignment](#2-architectural-principles--spec-alignment)
3. [Overall System Architecture](#3-overall-system-architecture)
4. [Portable Core Layer vs. Harness Adapter Layer](#4-portable-core-layer-vs-harness-adapter-layer)
5. [Core Planning Orchestrator & Execution Pipeline](#5-core-planning-orchestrator--execution-pipeline)
6. [The Eight Planning Stages — Design & Contracts](#6-the-eight-planning-stages--design--contracts)
7. [Repository Intelligence & Classification Engine](#7-repository-intelligence--classification-engine)
8. [Evidence-Driven Framework & Convention Engine](#8-evidence-driven-framework--convention-engine)
9. [Human Intervention & Ambiguity Handling Engine](#9-human-intervention--ambiguity-handling-engine)
10. [Intermediate State Management & Lifecycle](#10-intermediate-state-management--lifecycle)
11. [Blueprint Artifact Generation & Storage Architecture](#11-blueprint-artifact-generation--storage-architecture)
12. [Quality Gate & Traceability Engine](#12-quality-gate--traceability-engine)
13. [Security, Safety & File Isolation Architecture](#13-security-safety--file-isolation-architecture)
14. [Harness Adapter Design: Antigravity MVP](#14-harness-adapter-design-antigravity-mvp)
15. [Generic Harness Adapter Contract (Future-Proofing)](#15-generic-harness-adapter-contract-future-proofing)
16. [Error Handling, Fault Recovery & Session Handoff](#16-error-handling-fault-recovery--session-handoff)
17. [Configuration & Extensibility](#17-configuration--extensibility)
18. [Traceability Matrix to Specification v0.2.0](#18-traceability-matrix-to-specification-v020)

---

## 1. Executive Summary & System Objectives

The **Agentic Feature Planning DevKit** (DevKit) is a plug-and-play developer productivity framework designed to transform a raw feature request into an actionable, repository-aware implementation blueprint without modifying application source code.

This High-Level Design (HLD) translates the approved functional specification (`specs/agentic_feature_planning_devkit_spec.md` v0.2.0) into a concrete, modular architecture. The design addresses the core challenge of conversational AI planning: **ephemeral context and hallucinated codebases**. By coupling structured repository reconnaissance with an evidence-driven decision rubric and deterministic Markdown planning templates, the DevKit produces a self-contained, version-controllable **Blueprint** suite stored directly within the target repository (`.devkit/plans/<feature-slug>/`).

### Primary Architectural Tenets for MVP:
1. **Harness-Agnostic Core:** The planning logic is defined in pure, portable Markdown instructions and schema definitions.
2. **Instruction-Based Execution:** No compiled CLI binary or background daemon required. Host agent harnesses execute the planning pipeline natively via file tools.
3. **Single-Agent Autonomous Pipeline:** All 8 planning stages run consecutively in a single session without requiring manual step-by-step developer prompts.
4. **Strict Source Code Non-Mutation:** Planning operations strictly write only inside `.devkit/`; target application source code remains untouched.
5. **Session & Conversation Independence:** Completed plans and intermediate checkpoint states can be picked up by a fresh agent session or a human developer without prior conversation logs.

---

## 2. Architectural Principles & Spec Alignment

The system architecture directly enforces the decisions established in Specification v0.2.0:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SPEC v0.2.0 ALIGNMENT MATRIX                          │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ Spec Requirement      │ HLD Architectural Realization                       │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ AD-1: Invocation      │ Instruction-based Core; zero mandatory CLI binary.  │
│ AD-2: Orchestration   │ Single-agent autonomous sequential pipeline.        │
│ AD-3: State Format    │ Hybrid run-state: in-memory reasoning + Markdown   │
│                       │ checkpoint summaries in .devkit/run-state/.         │
│ AD-4: Storage & ID    │ Slugified feature folders in .devkit/plans/<slug>/. │
│ AD-5: Decision Rubric │ 4-tier Evidence Rubric replacing numeric confidence.│
│ Harness Independence  │ Strict two-tier Core vs. Adapter separation.        │
│ Evidence-Driven Intel │ Empirical file/config analysis > framework defaults.│
│ Code Safety           │ Enforced sandboxing to .devkit/ output tree.        │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 3. Overall System Architecture

The DevKit architecture is partitioned into four major decoupled blocks: the **Harness Adapter Layer**, the **Core Planning Engine**, the **Execution State Store**, and the **Target Repository Boundaries**.

```
                      ┌─────────────────────────────────┐
                      │        Developer User           │
                      └────────────────┬────────────────┘
                                       │ 1. Invocation (Feature + Target Repo)
                                       ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                           HARNESS ADAPTER LAYER                               │
│  ┌─────────────────────────────┐         ┌─────────────────────────────────┐  │
│  │     Antigravity Adapter     │         │     Future Adapters             │  │
│  │ (MVP: Skill Definition,     │         │ (Cursor, Claude Code, Copilot,  │  │
│  │  File Tool Bindings, Prompt)│         │  CLI wrappers)                  │  │
│  └──────────────┬──────────────┘         └─────────────────────────────────┘  │
└─────────────────┼─────────────────────────────────────────────────────────────┘
                  │ 2. Canonical Parameters (repo, feature, stack, depth)
                  ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                     PORTABLE CORE PLANNING ENGINE                             │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                       Core Orchestrator Workflow                        │  │
│  │  (Reads Core Markdown Instructions, Drives Pipeline, Evaluates Gates)   │  │
│  └──────┬───────────────────────┬─────────────────────────┬─────────────┬──┘  │
│         │                       │                         │             │     │
│         ▼                       ▼                         ▼             ▼     │
│   [Stage 1: Intake]       [Stage 2: Recon]          [Stage 3: Arch]   [Stage 4: Spec]
│   • Input validation      • Repo-type detection     • Module maps     • Stories & ACs
│   • Ambiguity check       • Manifest/lock analysis  • Convention ext. • Assumptions   
│         │                       │                         │             │     │
│         ▼                       ▼                         ▼             ▼     │
│   [Stage 5: Impact/Risk]  [Stage 6: Tasks]          [Stage 7: Valid]  [Stage 8: Gates]
│   • Blast radius          • Phased atomic tasks     • Test mapping    • Path check    
│   • Security/migrations   • Mermaid DAG             • Fixtures/mocks  • Traceability  
└─────────┬───────────────────────┬─────────────────────────┬─────────────┬─────┘
          │                       │                         │             │
          │ Writes checkpoint summaries                     │ Writes final Blueprints
          ▼                                                 ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                         TARGET REPOSITORY WORKSPACE                           │
│                                                                               │
│  ┌────────────────────────────────────────┐ ┌──────────────────────────────┐  │
│  │ Application Code & Configs (READ-ONLY) │ │ .devkit/ Output Hierarchy    │  │
│  │  src/, tests/, package.json, etc.      │ │  ├── run-state/ (Temporary)  │  │
│  │  (Strictly protected against writes)   │ │  │   ├── intake.md           │  │
│  └────────────────────────────────────────┘ │   │   ├── repo-map.md         │  │
│                                             │   │   └── stage-log.md        │  │
│                                             │   └── plans/<feature-slug>/   │  │
│                                             │       ├── feature-spec.md     │  │
│                                             │       ├── task-breakdown.md   │  │
│                                             │       └── run-summary.md      │  │
│                                             └──────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Portable Core Layer vs. Harness Adapter Layer

To guarantee true harness-independence without sacrificing developer experience, the DevKit strictly separates planning intelligence from harness mechanics.

### 4.1 Boundary Definitions

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                             PORTABLE CORE LAYER                               │
│  Contains:                                                                    │
│  • Core Planning Stage Instructions (Markdown specifications).                │
│  • Canonical Input/Output Data Schemas.                                       │
│  • Evidence Rubric & Ambiguity Evaluation Rules.                              │
│  • Repository Type Classification Heuristics.                                 │
│  • Blueprint Markdown Output Templates & Front-Matter Schemas.                │
│  • Quality Gate Validation Invariants.                                        │
│  Zero knowledge of: Antigravity tools, proprietary APIs, vendor metadata.    │
└──────────────────────────────────────┬────────────────────────────────────────┘
                                       │ Standardized Adapter Contract
                                       ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                            HARNESS ADAPTER LAYER                              │
│  Contains:                                                                    │
│  • Harness-specific packaging (e.g., Antigravity `SKILL.md`).                 │
│  • Parameter extraction from user interaction (Slash commands / chat prompts).│
│  • Mapping agent host file tools (read, write, list) to pipeline operations.  │
│  • Facilitating user interaction during Stage 1 if Critical Ambiguity arises. │
│  • Presenting the final execution summary to the developer UI.                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 How Other Harnesses Consume the Core
When running on Antigravity, an adapter maps the core instructions to an Antigravity Skill. If a team adopts **Claude Code**, **Cursor**, or an internal CLI, they simply provide a thin adapter that:
1. Passes the repository path and feature prompt to the core instructions.
2. Directs the local LLM agent to follow the stage-by-stage instructions using its own native filesystem tools.
3. No planning logic, stage boundaries, or artifact schemas are duplicated or modified.

---

## 5. Core Planning Orchestrator & Execution Pipeline

The Core Orchestrator is an autonomous procedural state machine executed by the single agent. It processes inputs sequentially, evaluates conditional branches (such as ambiguities), generates intermediate checkpoints, and applies quality verification gates.

### 5.1 Pipeline Stage Flow and Data Transitions

```
[User Input: repo, feature, stack, depth]
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 1: Intake       │ ◄── Validates repo path, computes feature-slug,
       └───────────┬───────────┘     evaluates critical ambiguity.
                   │
         [Critical Ambiguity?]
         ├── YES ──► [Batched Q&A Interruption] ──► [User Responds]
         │                                                 │
         └── NO ───────────────────────────────────────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 2: Recon        │ ◄── Classifies repo type, parses manifests,
       └───────────┬───────────┘     maps directory trees (read-only).
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 3: Architecture │ ◄── Identifies module boundaries, infers arch,
       └───────────┬───────────┘     extracts empirical conventions.
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 4: Feature Spec │ ◄── Drafts User Stories, FRs, ACs, boundaries,
       └───────────┬───────────┘     assumptions.
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 5: Impact & Risk│ ◄── Computes blast radius, security, migration,
       └───────────┬───────────┘     backward compatibility.
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 6: Tasks        │ ◄── Creates dependency-ordered atomic tasks,
       └───────────┬───────────┘     verifies paths exist or marked [NEW FILE].
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 7: Validation   │ ◄── Maps every AC to unit/integration/e2e tests,
       └───────────┬───────────┘     defines fixtures and mock requirements.
                   │
                   ▼
       ┌───────────────────────┐
       │ Stage 8: Quality Gate │ ◄── Validates traceability, path existence,
       └───────────┬───────────┘     DAG cycles; writes final Blueprint suite.
                   │
                   ▼
[Final Output: .devkit/plans/<slug>/ + Developer Run Summary]
```

---

## 6. The Eight Planning Stages — Design & Contracts

Each planning stage operates as a deterministic transformation unit with explicit inputs, responsibilities, outputs, and failure modes.

### 6.1 Stage 1: Intake & Clarification
- **Objective:** Establish the planning envelope, derive feature identity, and filter blocking ambiguities.
- **Inputs:** `repo` (path/URL), `feature` (text), `stack` (optional), `depth` (auto/shallow/deep).
- **Execution Actions:**
  1. Validate directory read permissions.
  2. Normalize and compute `feature-slug` (see Section 11.3).
  3. Classify feature category: `new-feature`, `bug-fix`, `refactor`, `migration`, or `performance`.
  4. Evaluate requirements against the **Evidence Rubric** (Section 9).
  5. If a **Critical Ambiguity** is detected, compile a batched question set (maximum 5), pause for user response, and store answers.
- **Outputs:** `.devkit/run-state/intake.md`

### 6.2 Stage 2: Repository Reconnaissance
- **Objective:** Build an accurate factual inventory of codebase layout, dependencies, and infrastructure.
- **Inputs:** `.devkit/run-state/intake.md`, Target Repository Filesystem.
- **Execution Actions:**
  1. Detect repository archetype (Application, Library/SDK, Data Engineering, Infrastructure, Monorepo, Unknown).
  2. Parse package and dependency manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.).
  3. Catalog test runners, linter configurations, and CI/CD workflows.
  4. Identify core entry points, routing layers, and configuration schemes.
- **Outputs:** `.devkit/run-state/repo-map.md`, `.devkit/run-state/repo-type.md`

### 6.3 Stage 3: Architecture & Conventions Extraction
- **Objective:** Discern structural architectural paradigms and extract empirical coding standards.
- **Inputs:** `.devkit/run-state/repo-map.md`, relevant codebase source files.
- **Execution Actions:**
  1. Identify system pattern (MVC, Clean Architecture, Hexagonal, Event-Driven, Modular Slice). Tag all inferences as `[INFERRED]`.
  2. Map module boundaries, shared services, and domain data models.
  3. Perform empirical code-level convention extraction: file naming cases (kebab vs camel vs Pascal), directory placement rules, error handling structures, logging styles, and test idioms.
- **Outputs:** `.devkit/run-state/architecture.md`, `.devkit/run-state/conventions.md`

### 6.4 Stage 4: Feature Specification Formulation
- **Objective:** Formulate complete, verifiable functional and non-functional requirements.
- **Inputs:** Checkpoints from Stages 1, 2, and 3.
- **Execution Actions:**
  1. Expand feature statement into formal User Stories (`As a... I want... So that...`).
  2. Decompose stories into Functional Requirements (`FR-001..N`).
  3. Define verifiable, binary-pass Acceptance Criteria (`AC-001..N`) for every requirement.
  4. Formulate explicit In-Scope and Out-of-Scope boundaries.
  5. Catalog all assumptions with evidence links and risks (`[ASSUMPTION: <level>]`).
- **Outputs:** `.devkit/plans/<slug>/feature-spec.md`

### 6.5 Stage 5: Impact & Risk Analysis
- **Objective:** Quantify codebase blast radius, breaking changes, and operational hazards.
- **Inputs:** `feature-spec.md`, `architecture.md`, `repo-map.md`.
- **Execution Actions:**
  1. Isolate concrete file modification targets and prospective new files (`[NEW FILE]`).
  2. Assess backward compatibility of data schemas, APIs, and client contracts.
  3. Analyze cross-cutting impacts (auth, logging, transactions, caching).
  4. Construct the Risk Register: technical, integration, and security risks with likelihood, impact, and concrete mitigations.
- **Outputs:** Intermediate impact and risk analysis incorporated into `implementation-plan.md`.

### 6.6 Stage 6: Task Decomposition
- **Objective:** Translate specifications into a sequenced, dependency-ordered execution graph.
- **Inputs:** `feature-spec.md`, impact analysis, `conventions.md`.
- **Execution Actions:**
  1. Decompose implementation into atomic, testable tasks (`TASK-001..N`).
  2. Assign task metadata: Type (`infrastructure`, `feature`, `test`, `doc`), Complexity (`S`, `M`, `L`, `XL`), and prerequisite dependencies.
  3. Enforce **Path Grounding**: Every target file must either physically exist in `repo-map.md` or be explicitly tagged `[NEW FILE: <path>]`.
  4. Group tasks into logical execution phases.
  5. Generate a Mermaid Directed Acyclic Graph (DAG) visualizing dependencies.
- **Outputs:** `.devkit/plans/<slug>/task-breakdown.md`, `.devkit/plans/<slug>/implementation-plan.md`

### 6.7 Stage 7: Validation Planning
- **Objective:** Ensure automated and manual verification coverage for every requirement.
- **Inputs:** `feature-spec.md`, `task-breakdown.md`, `repo-map.md` (testing infrastructure).
- **Execution Actions:**
  1. Map every Acceptance Criterion (`AC-xxx`) to one or more explicit Test Cases (`TC-xxx`).
  2. Categorize test cases by scope: Unit, Integration, End-to-End, or Contract.
  3. Specify mock definitions, fixture requirements, and test environment prerequisites.
  4. Define explicit manual verification procedures for non-automatable criteria.
- **Outputs:** `.devkit/plans/<slug>/validation-plan.md`

### 6.8 Stage 8: Quality Gate & Plan Finalization
- **Objective:** Enforce plan consistency, requirement traceability, and factual accuracy.
- **Inputs:** All generated Blueprints and intermediate run-state files.
- **Execution Actions:**
  1. Verify 100% path accuracy (zero hallucinated paths).
  2. Verify acyclic task DAG (topological validation).
  3. Verify bidirectional traceability (FR ↔ TASK ↔ TC).
  4. Validate zero file modifications outside `.devkit/`.
  5. Produce `decisions.md` (ADRs + Open Questions + Assumptions).
  6. Generate `run-summary.md` and finalize `plan-run.log`.
  7. Set YAML front-matter status (`approved`, `draft`, or `incomplete`).
- **Outputs:** Finalized `.devkit/plans/<slug>/` artifact suite, consolidated log, temporary state cleanup.

---

## 7. Repository Intelligence & Classification Engine

The reconnaissance engine eliminates guesswork by categorizing repositories based on concrete codebase signals before architectural inference begins.

### 7.1 Archetype Detection Matrix

```
┌──────────────────┬─────────────────────────────────┬───────────────────────────────┐
│ Repository Type  │ Detection Signatures            │ Planning Pipeline Adaptation  │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Application      │ • Server entrypoints (main,app) │ Emphasize API routing, data   │
│                  │ • Web framework dependencies    │ persistence, security, and    │
│                  │ • Route controllers & UI views  │ end-user acceptance flows.    │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Library / SDK    │ • Export index (index.ts, lib.rs│ Emphasize public API contracts│
│                  │ • Packaging manifests & semver  │ backwards-compatibility,      │
│                  │ • High unit test coverage       │ zero-dependency footprints.   │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Data Engineering │ • DAG definitions (Airflow,dbt) │ Emphasize schema evolution,   │
│                  │ • ETL pipeline scripts & Spark  │ idempotency, data lineage,    │
│                  │ • Data warehouse schemas/queries│ batch/stream performance.     │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Infrastructure / │ • Terraform, Helm, K8s manifests│ Emphasize declarative state,  │
│ DevOps           │ • CloudFormation, Ansible       │ rollback plans, zero-downtime,│
│                  │ • Absence of app source code    │ security blast radius.        │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Monorepo         │ • Workspace manifests (pnpm, nx)│ Isolate affected packages,    │
│                  │ • Multiple package.json/cargo   │ evaluate inter-package deps,  │
│                  │ • packages/ or apps/ subtrees   │ enforce boundary separation.  │
├──────────────────┼─────────────────────────────────┼───────────────────────────────┤
│ Unknown / Mixed  │ • Non-standard directory layouts│ Log limitations in summary,   │
│                  │ • Multi-language hybrid setups  │ fall back to empirical file   │
│                  │                                 │ analysis, tag as draft plan.  │
└──────────────────┴─────────────────────────────────┴───────────────────────────────┘
```

### 7.2 Evidence Hierarchy
When the agent evaluates technical choices, it must follow an unwavering order of authority:
1. **Actual Implementation Source Files:** (Highest authority — how code is actually written).
2. **Repository Configuration & Manifests:** (`tsconfig.json`, `package.json`, `.env.example`).
3. **In-Repository Documentation & Tests:** (`README.md`, existing test patterns).
4. **General Framework Knowledge:** (Lowest authority — only advisory when codebase is silent).

---

## 8. Evidence-Driven Framework & Convention Engine

### 8.1 The Convention Precedence Rule
Framework conventions published online are frequently ignored or modified in real-world codebases. 
> **Rule of Precedence:**  
> The observed repository pattern **always** overrides standard framework guidelines. If an official React or Go guide recommends naming convention *A*, but the inspected codebase consistently adheres to convention *B*, the DevKit **must** adopt convention *B*. The deviation is documented in `decisions.md` as `[ASSUMPTION: evidence-supported]`.

### 8.2 Extraction Mechanics
The agent inspects existing files in Stage 3 across 7 explicit dimensions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CONVENTION EXTRACTION CHECKLIST                       │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Dimension        │ Extracted Attributes & Patterns                          │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ File Naming      │ kebab-case vs camelCase vs PascalCase vs snake_case      │
│ Directory Layout │ Flat vs Layered vs Feature-Sliced vs Hexagonal Ports     │
│ Import Style     │ Relative paths (../../) vs Path Aliases (@/components)   │
│ Error Handling   │ Try/catch blocks vs Result<T,E> types vs Error Envelopes │
│ Logging Patterns │ Console calls vs Winston/Pino structured JSON payloads   │
│ Testing Idioms   │ BDD describe/it blocks vs table-driven tests vs assert   │
│ API Structures   │ REST resource envelopes vs GraphQL schemas vs gRPC protos│
└──────────────────┴──────────────────────────────────────────────────────────┘
```

---

## 9. Human Intervention & Ambiguity Handling Engine

The DevKit minimizes developer friction by eliminating frequent, chatty interruptions.

### 9.1 The Four-Level Evidence Rubric
Every decision made during planning must be classified into one of four distinct tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE EVIDENCE RUBRIC                               │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ Tier                     │ Criteria & Agent Operational Action              │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 1. Evidence-Supported    │ Direct corroboration found in ≥2 files/configs.   │
│                          │ Action: Adopt silently; document as evidence.    │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 2. Reasonable Assumption │ Codebase is silent; industry default is low-risk.│
│                          │ Action: Adopt standard default; log assumption.  │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 3. Design Choice         │ Multiple valid architectures; choice non-blocking│
│                          │ Action: Select safest; record ADR & alternatives.│
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 4. Critical Ambiguity    │ Fundamental contradiction or missing spec that    │
│                          │ prevents deterministic planning.                 │
│                          │ Action: PAUSE pipeline. Present batched Q&A.     │
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### 9.2 Batched Clarification Protocol
- Clarifications are permitted **only once** per planning run, immediately concluding Stage 1.
- Maximum of **5 questions** presented in a single, structured interaction.
- Each question must articulate:
  1. The specific architectural or business ambiguity.
  2. Why the codebase cannot resolve it.
  3. Concrete options with a recommended default.
- If the developer does not respond or the harness runs headless, the DevKit adopts the recommended default, records it under `decisions.md`, and proceeds autonomously.

---

## 10. Intermediate State Management & Lifecycle

To ensure resilience, auditability, and context-window safety without external databases, the DevKit uses a **Hybrid State Model**.

### 10.1 Checkpoint Inventory (`.devkit/run-state/`)

```
.devkit/run-state/
├── intake.md          # Validated feature scope, slug, depth, category
├── repo-type.md       # Archetype classification & detection evidence
├── repo-map.md        # File inventory, dependency lists, build tools
├── architecture.md    # Inferred architectural layers, shared utilities
├── conventions.md     # Empirically extracted style & structural patterns
└── stage-log.md       # Running audit trail of execution timings & status
```

### 10.2 State Lifecycle States

```
[INITIATION] ──► Directory .devkit/run-state/ created.
     │
     ▼
[PROGRESSION] ─► After each stage, agent writes structured Markdown checkpoint.
     │           Provides in-flight observability to developer.
     ▼
[FINALIZATION] ─► Stage 8 finishes. Key audit info promoted to plan-run.log.
     │           Temporary run-state files are purged or archived.
     ▼
[COMPLETION] ──► Only persistent Blueprints in .devkit/plans/<slug>/ remain.
```

### 10.3 Fresh-Session Handoff & Interruption Recovery Protocol
If an agent execution crashes or is terminated mid-run (e.g., LLM context limits or process timeout):
1. **Detection:** A new agent session checks for the existence of `.devkit/run-state/`.
2. **Audit Inspection:** The agent reads `stage-log.md` to identify the last successfully completed stage.
3. **Context Reconstruction:** The agent reads the existing Markdown checkpoints (`intake.md`, `repo-map.md`, etc.) directly into its context.
4. **Resumption:** Planning resumes immediately at the next stage. **Zero re-interrogation of the developer and zero repeat analysis.**

---

## 11. Blueprint Artifact Generation & Storage Architecture

### 11.1 Directory Layout
Artifacts are stored inside the target repository under a standardized, discoverable namespace:

```
<repo-root>/
└── .devkit/
    ├── plans/
    │   ├── index.md (optional registry cataloging all plans)
    │   └── <feature-slug>/
    │       ├── feature-spec.md
    │       ├── implementation-plan.md
    │       ├── task-breakdown.md
    │       ├── validation-plan.md
    │       ├── decisions.md
    │       ├── run-summary.md
    │       └── plan-run.log
    └── run-state/ (ephemeral; excluded in git)
```

### 11.2 Standard Front-Matter Contract
Every Blueprint artifact begins with machine-readable YAML metadata:

```yaml
---
devkit_version: "0.2.0"
artifact_type: "task-breakdown" # feature-spec | implementation-plan | etc.
feature_id: "user-avatar-s3-upload"
feature_name: "User Avatar Upload with S3 Storage"
repo: "."
generated_at: "2026-11-04T16:00:00Z"
planning_depth: "auto"
status: "approved" # approved | draft | incomplete
schema_version: "1"
---
```

### 11.3 Feature Slug Algorithm & Collision Handling
1. **Extraction:** Take the first 6–8 descriptive words from the feature statement (omitting stop words: *a, the, with, to, for*).
2. **Sanitization:** Convert to lowercase, replace non-alphanumeric characters with hyphens, collapse consecutive hyphens, trim to 60 characters maximum.
3. **Collision Detection:**
   - Check if `<repo-root>/.devkit/plans/<slug>/` exists on disk.
   - If present, append `-2`, `-3`, etc., until an unused directory name is identified.

---

## 12. Quality Gate & Traceability Engine

Stage 8 executes an automated verification gate prior to artifact finalization.

### 12.1 Verification Gate Definitions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          QUALITY GATE VERIFICATIONS                         │
├───────┬───────────────────────────────┬──────┬──────────────────────────────┤
│ Gate  │ Check Description             │ Type │ Enforcement Action           │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-H1 │ 100% Path Grounding           │ Hard │ Plan fails if path not on    │
│       │ (All paths exist or [NEW FILE])│     │ disk and lacks [NEW FILE].   │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-H2 │ Acyclic Task Graph (DAG)      │ Hard │ Plan fails if cycle detected │
│       │                               │      │ in task prerequisites.       │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-H3 │ Requirement Traceability      │ Hard │ Plan fails if any FR-xxx     │
│       │ (FR ↔ TASK mapping)           │      │ lacks an assigned TASK-xxx.  │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-H4 │ Validation Traceability       │ Hard │ Plan fails if any AC-xxx     │
│       │ (AC ↔ TC mapping)             │      │ lacks an assigned TC-xxx.    │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-H5 │ Source Code Non-Mutation      │ Hard │ Plan fails if any non-devkit │
│       │                               │      │ file was modified or written.│
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-S1 │ Open Question Resolutions     │ Soft │ Warn if [OPEN] questions lack│
│       │                               │      │ suggested resolution paths.  │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-S2 │ Task Complexity Assignment    │ Soft │ Warn if any task lacks S/M/L │
│       │                               │      │ complexity estimate.         │
├───────┼───────────────────────────────┼──────┼──────────────────────────────┤
│ QG-S3 │ Risk Register Completeness    │ Soft │ Warn if risk register has    │
│       │                               │      │ zero entries.                │
└───────┴───────────────────────────────┴──────┴──────────────────────────────┘
```

- **Pass All Hard Gates:** Status set to `approved`.
- **Pass Hard Gates with Soft Warnings:** Status set to `draft` (warnings logged in `run-summary.md`).
- **Fail Any Hard Gate:** Status set to `incomplete` (blockers detailed in `run-summary.md`).

### 12.2 Bidirectional Traceability Architecture

```
User Story ──► Functional Requirement (FR-001) ──► Implementation Task (TASK-001)
                    │                                      │
                    ▼                                      ▼
             Acceptance Criteria (AC-001) ───────► Test Case Spec (TC-001)
```

---

## 13. Security, Safety & File Isolation Architecture

### 13.1 Strict Isolation to `.devkit/`
The DevKit operates under a strict isolation guarantee:
- **Application Source Code is Read-Only:** The planner inspects files to understand structure, but never writes, creates, or edits application code or tests.
- **Single Write Target:** All writes (run-state checkpoints and final blueprints) are strictly confined to `<repo-root>/.devkit/`.
- **Git Ignore Safeguard:** The DevKit automatically prompts or verifies that `.devkit/run-state/` is included in `.gitignore` to prevent polluting version control with ephemeral checkpoint data.

### 13.2 Protection Against Hallucinated Executions
To prevent downstream implementation agents from failing on phantom code, the DevKit disallows inventing directories or moving existing files unless explicitly specified in a refactor task. Every file modification target must be verified against disk during Stage 2 Reconnaissance.

---

## 14. Harness Adapter Design: Antigravity MVP

The **Antigravity Adapter** packages the portable DevKit core for seamless execution inside the Google Antigravity environment.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ANTIGRAVITY HARNESS ADAPTER                         │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Skill Definition: skills/feature-planner/SKILL.md                     │  │
│  │ • Front-matter: name, description, parameters                         │  │
│  │ • Prompt binding: Instructs agent to load Core Planning Instructions  │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Antigravity Agent Runtime Tools                                       │  │
│  │ • read_file: Used by Stages 2, 3, 8 for codebase & state inspection   │  │
│  │ • write_file: Used by all stages to write run-state & blueprints      │  │
│  │ • run_command: Used for git status / directory listing checks         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 14.1 Adapter Responsibilities in Antigravity
1. **Invocation Interface:** Intercepts user requests matching feature planning intents.
2. **Core Instruction Injection:** Injects the portable planning stage instructions into the model context.
3. **Execution Loop:** Allows the Antigravity agent to invoke its native file reading and writing tools autonomously across Stages 1–8.
4. **Summary Presentation:** Formats the final `run-summary.md` and provides clickable file links (`file://...`) in the chat interface.

---

## 15. Generic Harness Adapter Contract (Future-Proofing)

Any future harness (e.g., Claude Code, Cursor, Copilot CLI) can integrate with the DevKit by fulfilling a lightweight contract.

### 15.1 The Harness Adapter Contract Interface

```typescript
interface DevKitHarnessAdapter {
  /**
   * 1. Collect inputs from harness-specific UI or CLI
   */
  collectInputs(): Promise<{
    repoPath: string;
    featureStatement: string;
    stackHint?: string;
    depth?: "auto" | "shallow" | "deep";
  }>;

  /**
   * 2. Expose Core Planning Instructions to Agent Context
   */
  loadCoreInstructions(): string;

  /**
   * 3. Provide File Tooling to Agent
   * - Read access to repoPath
   * - Write access restricted to repoPath/.devkit/
   */
  getToolCapabilities(): {
    canReadFile: true;
    canWriteFile: true; // restricted to .devkit/
    canListDirectory: true;
  };

  /**
   * 4. Human-in-the-Loop Clarification Relay
   * - Triggered only if Stage 1 yields Critical Ambiguity
   */
  requestClarification(questions: Array<{
    id: string;
    question: string;
    options: string[];
    recommended: string;
  }>): Promise<Record<string, string>>;

  /**
   * 5. Present Final Output Summary to User
   */
  renderCompletionSummary(summaryPath: string): void;
}
```

---

## 16. Error Handling, Fault Recovery & Session Handoff

### 16.1 Fault Classifications and Responses

```
┌───────────────────────────┬─────────────────────────────────────────────────┐
│ Failure Mode              │ System Recovery Strategy                        │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Target Repo Inaccessible  │ Terminate early before Stage 1; return clear    │
│                           │ error without writing empty artifacts.          │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Non-Standard Repo Layout  │ Fall back to Unknown/Mixed archetype; conduct   │
│                           │ empirical search; mark Blueprints as draft.     │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Context Window Limit      │ Prioritize reading high-signal files; write run-│
│ (Approaching token cap)   │ state checkpoint; resume in fresh agent turn.   │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Soft Quality Gate Warning │ Generate all Blueprints; set status: draft;     │
│                           │ itemize specific warnings in run-summary.md.    │
├───────────────────────────┼─────────────────────────────────────────────────┤
│ Hard Quality Gate Blocker │ Halts plan approval; sets status: incomplete;   │
│                           │ documents blocking defect in plan-run.log.      │
└───────────────────────────┴─────────────────────────────────────────────────┘
```

---

## 17. Configuration & Extensibility

### 17.1 Configuration via `.devkit/config.yaml` (Optional)
The DevKit operates out-of-the-box with zero configuration. Teams wishing to customize behaviors may place an optional config file at `<repo-root>/.devkit/config.yaml`:

```yaml
version: "1"
planning:
  default_depth: "auto" # shallow | auto | deep
  max_files_scanned: 200 # safeguard against runaway scanning
  scan_ignore_patterns:
    - "**/node_modules/**"
    - "**/vendor/**"
    - "**/dist/**"
artifacts:
  output_dir: ".devkit/plans"
  include_mermaid_diagrams: true
```

If this file is absent, the DevKit applies sensible, safe internal defaults.

---

## 18. Traceability Matrix to Specification v0.2.0

| Spec v0.2.0 Section | HLD Section | Architectural Compliance Summary |
|---------------------|-------------|-----------------------------------|
| Section 3 (AD-1)    | Section 4, 14, 15 | Instruction-based core with no CLI dependency; thin Antigravity adapter; generic adapter contract. |
| Section 3 (AD-2)    | Section 5, 6 | Single-agent autonomous pipeline across all 8 stages; clear decoupled stage boundaries. |
| Section 3 (AD-3)    | Section 10 | Hybrid state management in `.devkit/run-state/` for recovery and fresh-session handoffs. |
| Section 3 (AD-4)    | Section 11 | Human-readable slug generation with collision detection; storage in `.devkit/plans/<slug>/`. |
| Section 3 (AD-5)    | Section 9 | 4-tier Evidence Rubric replacing numeric confidence percentages. |
| Section 5 (FR-1..9)  | Section 6 | Full functional coverage across intake, recon, architecture, spec, tasks, validation, and gates. |
| Section 6 (NFR-1..12)| Section 2, 12, 13 | Factual grounding, acyclic DAGs, zero source mutation, and strict `.devkit/` sandboxing. |
| Section 7 (AC-1..12) | Section 5, 12 | Verifiable mapping for harness independence, traceability, fresh-session reuse, and path safety. |
| Section 12 (Intel)  | Section 7 | Archetype classification (App, Lib, Data, Infra, Monorepo) and evidence priority hierarchy. |
| Section 13 (Conventions)| Section 8 | Evidence-driven convention extraction; Repository-overrides-all precedence rule. |
| Section 14 (Intervention)| Section 9 | Batched clarification protocol (max 1 pause, max 5 questions). |
| Section 15 (Quality)| Section 12 | Hard gates (fail/incomplete) and soft gates (draft) with bidirectional traceability. |

---

*End of High-Level Design — v1.0.0 — Ready for Low-Level Design (LLD)*
