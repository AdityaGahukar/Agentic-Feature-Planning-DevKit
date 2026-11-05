# Stage 4: Feature Specification Instruction

> **Stage ID:** STAGE-04  
> **Reads:** `<repo_root>/.devkit/run-state/intake.md`, `<repo_root>/.devkit/run-state/architecture.md`, `<repo_root>/.devkit/run-state/conventions.md`  
> **Writes:** `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md`  
> **Template Reference:** `core/templates/feature_spec_template.md`  
> **Rubric Reference:** `core/rubrics/evidence_rubric.md`  

---

## 1. Stage Objective

Stage 4 formulates the authoritative, repository-grounded feature specification. It translates user requirements into formal User Stories (`US-xxx`), Functional Requirements (`FR-xxx`), testable Acceptance Criteria (`AC-xxx`), Non-Functional Requirements (`NFR-xxx`), and explicit scope boundaries, grounded in the target repository's architectural patterns.

---

## 2. Step-by-Step Execution Procedure

### Step 4.1: Target Directory Initialization
1. Read `feature_slug` from `intake.md`.
2. Ensure directory `<repo_root>/.devkit/plans/<feature-slug>/` exists on disk.
3. If not present, create `<repo_root>/.devkit/plans/<feature-slug>/`.

---

### Step 4.2: Requirements Synthesis & Decomposition
1. **User Stories Formulation:**
   - Decompose the feature into at least 1–3 atomic user stories adhering to standard format:
     `US-xxx: As a <role>, I want <action>, so that <benefit>.`
2. **Functional Requirements (`FR-xxx`):**
   - Translate user stories into numbered, unambiguous functional requirements (`FR-001`, `FR-002`, etc.).
   - Each requirement must have a clear title and descriptive narrative.
3. **Acceptance Criteria (`AC-xxx`):**
   - Under each `FR-xxx`, define testable, binary-verifiable acceptance criteria:
     `AC-001-1`, `AC-001-2`, etc.
   - Criteria must describe concrete observable outcomes (e.g., "Returns HTTP 201 with created entity", "Emits UserCreatedEvent to message queue").
   - Avoid vague criteria like "Handles errors well" or "Performs fast".
4. **Non-Functional Requirements (`NFR-xxx`):**
   - Define performance, security, data integrity, and backward compatibility constraints aligned with codebase standards.
5. **Scope Boundaries:**
   - Explicitly enumerate **In-Scope** items.
   - Explicitly enumerate **Out-of-Scope** items to guard against scope creep during implementation.

---

### Step 4.3: Assumption & Open Question Classification
Apply `core/rubrics/evidence_rubric.md`:
1. **Assumptions:**
   - Every assumption made must be categorized:
     * `[ASSUMPTION: evidence-supported]`: Corroborated by codebase files; cite the file.
     * `[ASSUMPTION: reasonable-default]`: Safe industry default where codebase is silent.
     * `[ASSUMPTION: design-choice]`: Non-blocking architectural selection; documented with rationale.
2. **Open Questions (`[OPEN]`):**
   - Any non-blocking questions or future decisions must be recorded with suggested resolution paths.

---

### Step 4.4: Blueprint Generation (`feature-spec.md`)
1. Populate `core/templates/feature_spec_template.md` with:
   - Front-matter: `devkit_version: "0.2.0"`, `artifact_type: "feature-spec"`, `feature_id: "<slug>"`, `generated_at`, `planning_depth`, `status: "draft"`.
   - Populated sections: Overview, User Stories, Functional Requirements with ACs, NFRs, Scope Boundaries, Assumptions, Open Questions, and Related Artifact links.
2. Write output to `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md`.
3. Update `stage-log.md` marking Stage 4 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 5, verify:
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md` exists on disk.
- [ ] Contains at least 1 User Story.
- [ ] Every Functional Requirement has at least one testable Acceptance Criterion.
- [ ] In-Scope and Out-of-Scope boundaries are explicitly defined.
- [ ] All assumptions are categorized per Evidence Rubric tiers.
- [ ] Zero files outside `.devkit/` were modified.
