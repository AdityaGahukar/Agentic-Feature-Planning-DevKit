# Stage 8: Quality Gate & Blueprint Finalization Instruction

> **Stage ID:** STAGE-08  
> **Reads:** All generated Blueprints in `<repo_root>/.devkit/plans/<feature-slug>/`, run-state files in `.devkit/run-state/`  
> **Writes:** `<repo_root>/.devkit/plans/<feature-slug>/decisions.md`, `<repo_root>/.devkit/plans/<feature-slug>/run-summary.md`, `<repo_root>/.devkit/plans/<feature-slug>/plan-run.log`  
> **Template References:** `core/templates/decisions_template.md`, `core/templates/run_summary_template.md`, `core/templates/plan_run_log_template.md`  

---

## 1. Stage Objective

Stage 8 is the final automated quality gate. It verifies path grounding, DAG acyclicity, bidirectional requirement-to-task and AC-to-test traceability, and codebase immutability. It writes `decisions.md`, generates `run-summary.md`, finalizes `plan-run.log`, safely cleans up ephemeral checkpoints, and establishes the formal release status (`approved`, `draft`, or `incomplete`).

---

## 2. Step-by-Step Execution Procedure

### Step 8.1: Hard Quality Gate Execution
The agent executes the 5 hard gates sequentially. If any hard gate fails, the plan cannot be approved:

1. **Gate QG-H1: 100% Path Grounding Verification:**
   - Scan `task-breakdown.md`:
     * For every file listed under `Modify:`: verify that the file exists on disk or in `repo-map.md`.
     * For every file listed under `Create:`: verify it is formatted as `[NEW FILE: <path>]` and does not already exist on disk.
   - Result: `PASS` if 0 ungrounded paths exist; otherwise `FAIL`.

2. **Gate QG-H2: Acyclic Task DAG Verification:**
   - Extract all `TASK-xxx` IDs and their `Depends on:` relationships from `task-breakdown.md`.
   - Execute topological cycle detection (Kahn's algorithm):
     * Compute in-degrees for all nodes.
     * Traverse nodes with in-degree 0.
   - Result: `PASS` if visited count equals total node count; otherwise `FAIL` (cycle detected).

3. **Gate QG-H3: Requirement-to-Task Traceability Verification:**
   - Extract all `FR-xxx` IDs from `feature-spec.md`.
   - Extract all mapped `Requirements:` references from `task-breakdown.md`.
   - Compute set difference: `Missing_FR = Set_FR - Set_Mapped_FR`.
   - Result: `PASS` if `Missing_FR` is empty; otherwise `FAIL`.

4. **Gate QG-H4: Validation Traceability Verification:**
   - Extract all `AC-xxx` IDs from `feature-spec.md`.
   - Extract all `Linked to AC-xxx` references from `validation-plan.md`.
   - Compute set difference: `Missing_AC = Set_AC - Set_Mapped_AC`.
   - Result: `PASS` if `Missing_AC` is empty; otherwise `FAIL`.

5. **Gate QG-H5: Zero Source Code Mutation Verification:**
   - Check workspace status (e.g. `git status --porcelain`).
   - Verify that **zero** files outside `<repo_root>/.devkit/` have been created, modified, or deleted during the planning run.
   - Result: `PASS` if no non-devkit modifications exist; otherwise `FAIL`.

---

### Step 8.2: Soft Quality Gate Execution
Evaluate the 3 soft quality gates:
1. **Gate QG-S1: Open Question Resolutions:** Verify every `[OPEN]` item has a suggested resolution path.
2. **Gate QG-S2: Task Complexity Assignment:** Verify every task card has an assigned rating (`S`, `M`, `L`, `XL`).
3. **Gate QG-S3: Risk Register Completeness:** Verify the risk register contains at least one technical risk and mitigation.

---

### Step 8.3: Overall Status Determination
- **Status `approved`:** All 5 Hard Gates pass AND all Soft Gates pass.
- **Status `draft`:** All 5 Hard Gates pass, but 1 or more Soft Gates triggered warnings.
- **Status `incomplete`:** Any Hard Gate failed. Blocking defect notes must be detailed in summary.

---

### Step 8.4: Blueprint Deliverables Finalization
1. **Write `decisions.md`:**
   - Populate `core/templates/decisions_template.md` with:
     * Architecture Decision Records (ADRs) formulated during planning.
     * Documented Assumptions categorized by Evidence Rubric tiers.
     * Open Questions (`[OPEN]`).
   - Save to `<repo_root>/.devkit/plans/<feature-slug>/decisions.md`.
2. **Write `run-summary.md`:**
   - Populate `core/templates/run_summary_template.md` with:
     * Executive metadata (slug, repo type, depth, duration, status).
     * Quality Gate Verification Results Table.
     * Relative links to all generated Blueprint artifacts.
     * Next steps for the developer.
   - Save to `<repo_root>/.devkit/plans/<feature-slug>/run-summary.md`.
3. **Update Front-Matter Status Across Artifacts:**
   - Ensure `status` field in `feature-spec.md`, `implementation-plan.md`, `task-breakdown.md`, `validation-plan.md`, and `decisions.md` reflects the determined status (`approved`, `draft`, or `incomplete`).
4. **Promote `stage-log.md` to `plan-run.log`:**
   - Populate `core/templates/plan_run_log_template.md` with execution timings, chronological events, and any anomaly entries.
   - Save to `<repo_root>/.devkit/plans/<feature-slug>/plan-run.log`.

---

### Step 8.5: Safe State Cleanup
1. **If Status is `approved` or `draft`:**
   - Delete all temporary checkpoint files in `<repo_root>/.devkit/run-state/`.
   - Remove directory `<repo_root>/.devkit/run-state/`.
2. **If Status is `incomplete`:**
   - **Do NOT delete** `<repo_root>/.devkit/run-state/`. Preserve checkpoints for developer debugging.

---

## 3. Post-Condition Checklist
Before concluding execution, verify:
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/decisions.md` exists on disk.
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/run-summary.md` exists on disk.
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/plan-run.log` exists on disk.
- [ ] All 5 Hard Gates were evaluated and results documented.
- [ ] Temporary `.devkit/run-state/` files are safely cleaned up (if approved/draft).
- [ ] Zero files outside `<repo_root>/.devkit/` were modified.
