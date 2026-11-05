# Stage 5: Impact & Risk Analysis Instruction

> **Stage ID:** STAGE-05  
> **Reads:** `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md`, `<repo_root>/.devkit/run-state/architecture.md`, `<repo_root>/.devkit/run-state/repo-map.md`  
> **Writes:** In-memory impact model (consumed directly by Stage 6)  
> **Rubric Reference:** `core/rubrics/evidence_rubric.md`  

---

## 1. Stage Objective

Stage 5 computes the codebase blast radius, identifies backward compatibility risks, evaluates security constraints, and builds a comprehensive technical risk register. This analysis ensures the task decomposition in Stage 6 is grounded in real file targets and accounts for edge cases.

---

## 2. Step-by-Step Execution Procedure

### Step 5.1: File Target Identification
Analyze the functional requirements in `feature-spec.md` against the module maps in `architecture.md`:
1. **Existing Files to Modify:**
   - Identify concrete, existing files that will require code edits.
   - For each file, record:
     * Verified relative path (must exist in `repo-map.md`).
     * Specific nature of changes (e.g. "Add route handler for /api/avatar", "Add avatarUrl field to User schema").
2. **Prospective Files to Create:**
   - Identify new files that must be introduced.
   - For each prospective file, format path strictly with the tag:
     `[NEW FILE: <path>]` (e.g. `[NEW FILE: src/services/avatarService.ts]`).
   - Ensure prospective file placement strictly adheres to the conventions extracted in Stage 3 (`conventions.md`).

---

### Step 5.2: Cross-Cutting & Backward Compatibility Assessment
1. **Cross-Cutting Concerns:**
   - Assess authentication & authorization (does the feature require new permissions or roles?).
   - Assess logging & telemetry (what events or metrics must be emitted?).
   - Assess transaction & caching boundaries (are multi-table operations atomic? Does Redis cache need invalidation?).
2. **Backward Compatibility:**
   - Database schema changes: Are new columns nullable or have defaults? Are existing columns removed or altered?
   - API contracts: Are existing endpoint payloads or responses changed? Are changes non-breaking?
   - Client compatibility: Will legacy clients break when interacting with modified services?

---

### Step 5.3: Security & Operational Blast Radius
1. **Security Vulnerability Surface:**
   - Input validation: Are untrusted user inputs sanitized and validated against schemas?
   - Authentication bypass: Are all new routes protected behind appropriate auth middlewares?
   - Data privacy: Are sensitive attributes masked from logs and public API responses?
2. **Resource & Performance Constraints:**
   - Database query performance (indexes required for new query filters).
   - Memory & CPU constraints (large file uploads, streaming vs buffering).

---

### Step 5.4: Technical Risk Register Construction
Construct a structured risk table containing at least 1–3 technical risks. Each entry must specify:
- **Risk ID:** `RISK-001`, `RISK-002`, etc.
- **Description:** Concise statement of the technical failure mode or edge case.
- **Likelihood:** `Low`, `Medium`, or `High`.
- **Impact:** `Low`, `Medium`, or `High`.
- **Mitigation Strategy:** Concrete, actionable preventive step or design pattern to eliminate or minimize the risk.

---

### Step 5.5: Checkpoint Transition
1. Package the impact model (files to modify, files to create, compatibility notes, risk register) into structured working memory.
2. Verify that all existing file targets have been confirmed against disk or `repo-map.md`.
3. Update `stage-log.md` marking Stage 5 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 6, verify:
- [ ] List of existing files to modify contains only verified repository paths.
- [ ] Prospective files are explicitly formatted as `[NEW FILE: <path>]`.
- [ ] Backward compatibility and security considerations are analyzed.
- [ ] Risk register contains at least one technical risk with a mitigation strategy.
- [ ] Zero files outside `.devkit/` were modified.
