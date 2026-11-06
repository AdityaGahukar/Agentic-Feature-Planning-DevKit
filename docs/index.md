# Agentic Feature Planning DevKit — Documentation Index

> **Version:** 1.0.0  
> **Traceability References:** Specification v0.2.0, HLD v1.0.0, LLD v1.0.0  

Welcome to the **Agentic Feature Planning DevKit** documentation and onboarding hub.

---

## 🚀 Getting Started

- **[5-Minute Quickstart (`docs/QUICKSTART.md`)](./QUICKSTART.md):** Get up and running planning your first feature in under 5 minutes.
- **[Complete User Guide (`docs/USER_GUIDE.md`)](./USER_GUIDE.md):** Full operational guide covering GitHub publishing, Antigravity invocation, alternative harnesses (Cursor, Claude Code), session recovery, and implementation workflows.
- **[Interactive HTML Overview Presentation (`docs/devkit_overview.html`)](./devkit_overview.html):** Polished, responsive technical presentation with live Mermaid diagrams for onboarding engineers and stakeholders.

---

## 📊 Visual System Architecture & Diagrams

Editable, version-controlled Mermaid diagram definitions are available under [`docs/diagrams/`](./diagrams/):

1. **[Developer User Flow (`docs/diagrams/developer_user_flow.mmd`)](./diagrams/developer_user_flow.mmd):** End-to-end journey from developer feature intent to executable Blueprint, including clarification pauses and resumption checks.
2. **[High-Level Architecture (`docs/diagrams/high_level_architecture.mmd`)](./diagrams/high_level_architecture.mmd):** System decomposition distinguishing harness adapters, portable core engine, read-only application code, and the `.devkit/` isolated sandbox.
3. **[8-Stage Planning Workflow (`docs/diagrams/planning_workflow.mmd`)](./diagrams/planning_workflow.mmd):** Stage-by-stage data flow, inputs, outputs, and Tier 4 Critical Ambiguity handling.
4. **[Agent Execution Sequence (`docs/diagrams/execution_sequence.mmd`)](./diagrams/execution_sequence.mmd):** Sequence of interactions between Developer, Host Adapter, Core Orchestrator, Repository, Checkpoints, and Blueprint outputs.
5. **[Checkpoint & Recovery Lifecycle (`docs/diagrams/checkpoint_recovery.mmd`)](./diagrams/checkpoint_recovery.mmd):** State machine demonstrating interrupted session resumption (Algorithm 3) and stale-state hash mismatch protection.
6. **[Blueprint Artifact Relationships (`docs/diagrams/blueprint_artifact_relationship.mmd`)](./diagrams/blueprint_artifact_relationship.mmd):** Class diagram modeling bidirectional traceability (`FR-xxx` ↔ `TASK-xxx`, `AC-xxx` ↔ `TC-xxx`, `AS-xxx`, `ADR-xxx`).

---

## 📐 Specifications & Engineering Design

- **[Functional Specification v0.2.0 (`specs/agentic_feature_planning_devkit_spec.md`)](../specs/agentic_feature_planning_devkit_spec.md):** Core requirements, scope, quality gates, and acceptance criteria.
- **[High-Level Design v1.0.0 (`design/agentic_feature_planning_devkit_hld.md`)](../design/agentic_feature_planning_devkit_hld.md):** Architectural patterns, boundary definitions, and layer decoupling.
- **[Low-Level Design v1.0.0 (`design/agentic_feature_planning_devkit_lld.md`)](../design/agentic_feature_planning_devkit_lld.md):** Concrete algorithms (Algorithms 1, 2, 3), canonical templates, and schemas.
- **[Implementation Plan (`design/agentic_feature_planning_devkit_implementation_plan.md`)](../design/agentic_feature_planning_devkit_implementation_plan.md):** 26 atomic tasks across 6 verified phases.
- **[Implementation Status Audit (`design/implementation_status_audit.md`)](../design/implementation_status_audit.md):** Full verification audit of all 26 tasks and 6 verification gates.
- **[MVP Verification & Compliance Report (`docs/mvp_verification_report.md`)](./mvp_verification_report.md):** Official test execution sign-off confirming 100% compliance across all 10 Specification Acceptance Criteria (`AC-1` to `AC-10`).
