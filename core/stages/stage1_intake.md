# Stage 1: Intake & Clarification Instruction

> **Stage ID:** STAGE-01  
> **Reads:** User input parameters (`repo_root`, `feature_statement`, `stack_hint`, `depth`, `feature_id_override`)  
> **Writes:** `<repo_root>/.devkit/run-state/intake.md`  
> **Schema Reference:** `core/schemas/intake_state_schema.md`  
> **Rubric Reference:** `core/rubrics/evidence_rubric.md`  

---

## 1. Stage Objective

Stage 1 validates input parameters, establishes the planning envelope, classifies feature intent, computes the canonical feature slug with collision detection, and evaluates whether any blocking **Critical Ambiguities** exist before costly repository analysis begins.

---

## 2. Step-by-Step Execution Procedure

### Step 1.1: Input Validation & Normalization
1. Verify that `repo_root` exists and is accessible. If invalid, abort with an error.
2. Verify that `feature_statement` is non-empty. If empty or fewer than 3 words, abort with an error asking for a descriptive feature request.
3. Normalize `depth`:
   - If specified as `shallow`, `auto`, or `deep`, accept.
   - If omitted or null, default to `auto`.
4. Classify `feature_category`:
   - `new-feature`: Adding previously non-existent capability or service.
   - `bug-fix`: Correcting unintended behavior or broken contract.
   - `refactor`: Structural reorganization without external behavioral change.
   - `migration`: Upgrading dependencies, schema evolution, or porting technologies.
   - `performance`: Optimizing latency, throughput, or memory footprint.

---

### Step 1.2: Feature Slug Generation & Collision Detection
If `feature_id_override` is provided, sanitize it (lowercase, kebab-case, max 60 chars) and use it.  
Otherwise, derive `feature_slug` deterministically:
1. **Extract Keywords:** Take the first 6–8 descriptive words from `feature_statement`.
   - Strip English stop words: `a`, `an`, `the`, `and`, `or`, `in`, `on`, `at`, `to`, `for`, `with`, `by`, `from`, `of`.
2. **Sanitize:**
   - Convert to lowercase.
   - Replace any non-alphanumeric character with a hyphen (`-`).
   - Collapse consecutive hyphens into a single hyphen.
   - Trim leading and trailing hyphens.
   - Truncate to a maximum length of 60 characters.
3. **Collision Detection:**
   - Check if `<repo_root>/.devkit/plans/<derived-slug>/` exists on disk.
   - If it exists, append `-2`. If `-2` exists, append `-3`, incrementing until an unused directory name is identified.
   - The resulting string is the canonical `feature_slug`.

---

### Step 1.3: Critical Ambiguity Assessment (Evidence Rubric)
Inspect the `feature_statement` against `core/rubrics/evidence_rubric.md`:
1. Evaluate if any decision meets the **Tier 4 Critical Ambiguity** criteria:
   - Does an ambiguity fundamentally alter the technical architecture or implementation approach?
   - Can it be inferred from typical codebase conventions or safe defaults?
   - Would guessing wrongly require complete rework?
2. **If Critical Ambiguity Exists:**
   - Format a batched, numbered list of questions (strictly **maximum 5**).
   - Each question must specify:
     * Ambiguity title & context.
     * Distinct options with architectural trade-offs.
     * A safe recommended default.
   - Output the question block to the developer interface and **PAUSE** execution.
   - When developer answers are returned, record the answers verbatim.
3. **If No Critical Ambiguity Exists:**
   - Record `ambiguities_status: NONE_DETECTED`.
   - Proceed immediately to Step 1.4 without interrupting the developer.

---

### Step 1.4: Checkpoint Generation (`intake.md`)
Construct `<repo_root>/.devkit/run-state/intake.md` adhering strictly to `core/schemas/intake_state_schema.md`:
1. Populate YAML front-matter with `devkit_version: "0.2.0"`, `run_id`, `feature_slug`, `feature_statement_hash` (SHA-256), `started_at`, `planning_depth`, `feature_category`, and `status: "COMPLETED"`.
2. Populate Markdown sections: Raw Inputs, Feature Intent & Scope Hypothesis, and Critical Ambiguity Assessment.
3. Write file to `<repo_root>/.devkit/run-state/intake.md`.
4. Update `stage-log.md` marking Stage 1 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 2, verify:
- [ ] `<repo_root>/.devkit/run-state/intake.md` exists on disk.
- [ ] `feature_slug` is non-empty, URL-safe, and collision-free.
- [ ] No unanswered Critical Ambiguities remain.
- [ ] Zero files outside `.devkit/run-state/` were modified.
