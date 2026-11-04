# Agentic Feature Planning DevKit

A reusable, plug-and-play developer productivity framework that analyzes feature requirements and repository context to generate complete, repository-aware, actionable implementation plans (the **Blueprint**) without modifying application source code.

## Documentation & Design Specifications

- **Functional Specification (v0.2.0):** [`specs/agentic_feature_planning_devkit_spec.md`](./specs/agentic_feature_planning_devkit_spec.md)
- **High-Level Design (v1.0.0):** [`design/agentic_feature_planning_devkit_hld.md`](./design/agentic_feature_planning_devkit_hld.md)
- **Low-Level Design (v1.0.0):** [`design/agentic_feature_planning_devkit_lld.md`](./design/agentic_feature_planning_devkit_lld.md)
- **Implementation Plan (v1.0.0):** [`design/agentic_feature_planning_devkit_implementation_plan.md`](./design/agentic_feature_planning_devkit_implementation_plan.md)

## Core Architectural Principles

1. **Harness-Agnostic Core:** The planning intelligence is written in pure Markdown instructions, schemas, and rubrics. It has zero proprietary dependencies and requires no external binary CLI.
2. **Autonomous Execution:** Drives an 8-stage planning workflow in a single agent session without manual developer prompting between stages.
3. **Evidence-Driven Intelligence:** Decisions and conventions are grounded in observed repository files, manifests, and tests. Framework defaults never override observed code conventions.
4. **Strict Sandboxed Non-Mutation:** Planning operations write exclusively to `.devkit/` inside the target repository. Application source code and existing tests are never modified.
5. **Session & Recovery Independence:** Persistent Blueprints in `.devkit/plans/<feature-slug>/` and intermediate checkpoints in `.devkit/run-state/` allow any human or agent to resume or execute without relying on ephemeral conversational history.

## Repository Organization

```
agentic-feature-planning-devkit/
├── core/                                        # Portable, harness-agnostic planning engine
│   ├── orchestrator.md                          # Master execution algorithm
│   ├── stages/                                  # Stages 1 to 8 instructions
│   ├── rubrics/                                 # Decision & classification rubrics
│   ├── templates/                               # Canonical Blueprint output templates
│   └── schemas/                                 # Run-state checkpoint schemas
├── adapters/                                    # Harness adapters
│   ├── antigravity/                             # Google Antigravity skill adapter (MVP)
│   └── generic_contract.md                      # Minimal adapter contract for future harnesses
└── tests/                                       # Test suite & mock repository fixtures
    ├── fixtures/                                # Mock codebases (App, Lib, Data, Infra, Monorepo)
    ├── unit/                                    # Deterministic rule & template tests
    └── integration/                             # Multi-archetype E2E and recovery tests
```
