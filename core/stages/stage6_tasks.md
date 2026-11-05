# Stage 6: Task Decomposition & DAG Instruction

> **Stage ID:** STAGE-06  
> **Reads:** `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md`, Stage 5 impact model, `<repo_root>/.devkit/run-state/conventions.md`, `<repo_root>/.devkit/run-state/architecture.md`  
> **Writes:** `<repo_root>/.devkit/plans/<feature-slug>/task-breakdown.md`, `<repo_root>/.devkit/plans/<feature-slug>/implementation-plan.md`  
> **Template References:** `core/templates/task_breakdown_template.md`, `core/templates/implementation_plan_template.md`  

---

## 1. Stage Objective

Stage 6 transforms requirements and impact models into a dependency-ordered, phased, executable task list. Every task card must be self-contained so that another developer or agent harness can execute it without prior conversational context. It also visualizes the execution graph via a Mermaid Directed Acyclic Graph (DAG) and generates the comprehensive implementation plan.

---

## 2. Step-by-Step Execution Procedure

### Step 6.1: Phased Atomic Task Decomposition
Break the implementation down into discrete, sequenced tasks grouped into logical phases:
- **Phase 1: Foundation & Data Models:** Schemas, migrations, domain entities, base interfaces.
- **Phase 2: Business Logic & Service Layer:** Core domain logic, service abstractions, validations.
- **Phase 3: API & Presentation Layer:** Routes, controllers, serializers, UI components.
- **Phase 4: Integration & Verification:** Integration tests, manual verification, documentation.

#### Task Card Specification Requirements
Each task must be assigned a unique identifier (`TASK-001`, `TASK-002`, etc.) and contain:
1. **Title:** Concise, action-oriented name (e.g. `Implement Avatar Upload Service`).
2. **Type:** One of `infrastructure`, `feature`, `test`, or `documentation`.
3. **Complexity:** Estimated rating: `S` (<2 hours), `M` (half-day), `L` (full day), or `XL` (multi-day).
4. **Requirements Traceability:** Explicit links to the functional requirements it implements (`FR-001`, `FR-002`).
5. **Dependencies (`Depends on:`):** Comma-separated list of prerequisite tasks (or `none`).
6. **Target Files:**
   - Modify: Verified existing paths (must exist on disk).
   - Create: Strictly tagged as `[NEW FILE: <path>]`.
7. **Description & Instructions:** Detailed technical instructions guiding the executor step-by-step.
8. **Verification Criteria:** Checkbox criteria defining how the executor verifies task completion.
9. **Notes & Pitfalls:** Optional warnings or edge cases relevant to this task.

---

### Step 6.2: Path Grounding Enforcement
Execute the path grounding invariant before finalizing any task card:
1. Every file listed under "Modify:" must be verified to physically exist in `repo-map.md`.
2. Every file to be created must be marked with `[NEW FILE: <path>]`.
3. **Never invent imaginary directories** or assume non-existent utility files exist.

---

### Step 6.3: Mermaid Task Dependency Graph (DAG) Construction
1. Construct a Mermaid flowchart representing the dependency relationships:
   ```mermaid
   flowchart TD
       TASK001["TASK-001: Model setup"] --> TASK002["TASK-002: Service layer"]
       TASK001 --> TASK003["TASK-003: Migration script"]
       TASK002 & TASK003 --> TASK004["TASK-004: API endpoint"]
   ```
2. **Acyclicity Check:** Verify that the graph has zero circular dependencies (Task A cannot depend on Task B if Task B depends on Task A).

---

### Step 6.4: Blueprint Generation
1. **Write `task-breakdown.md`:**
   - Populate `core/templates/task_breakdown_template.md` with overview stats, phased task cards, and the Mermaid DAG.
   - Save to `<repo_root>/.devkit/plans/<feature-slug>/task-breakdown.md`.
2. **Write `implementation-plan.md`:**
   - Populate `core/templates/implementation_plan_template.md` with:
     * Executive Summary.
     * Repository Context (archetype, inferred architecture `[INFERRED]`, conventions).
     * Implementation Strategy & Approach narrative.
     * Impact Analysis (files to modify, prospective new files `[NEW FILE]`).
     * Technical Risk Register (from Stage 5).
     * Security Considerations.
     * Definition of Done.
   - Save to `<repo_root>/.devkit/plans/<feature-slug>/implementation-plan.md`.
3. Update `stage-log.md` marking Stage 6 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 7, verify:
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/task-breakdown.md` exists on disk.
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/implementation-plan.md` exists on disk.
- [ ] All task targets are verified existing paths or marked `[NEW FILE]`.
- [ ] The Mermaid dependency graph is strictly acyclic (DAG).
- [ ] Every functional requirement (`FR-xxx`) is mapped to at least one task.
- [ ] Zero files outside `.devkit/` were modified.
