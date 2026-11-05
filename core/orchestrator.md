# Master Core Planning Orchestrator

> **Layer:** Portable Core Layer (Harness-Agnostic)  
> **Target Document:** `core/orchestrator.md`  
> **Status:** Authoritative Pipeline Specification  
> **Spec Alignment:** Spec v0.2.0 (AD-1, AD-2, AD-3), HLD v1.0.0, LLD v1.0.0  

---

## 1. Overview & Execution Model

The Master Core Planning Orchestrator governs the autonomous execution of the 8-stage feature planning pipeline within a single agent session. The executing agent interprets this document as the master control loop, advancing through all stages sequentially without prompting the developer between stages.

### Core Invariants
1. **Single-Agent Autonomous Run:** The agent drives Stages 1 through 8 to completion from a single invocation.
2. **Zero Codebase Mutation:** All write operations are strictly sandboxed to `<repo-root>/.devkit/`. Application source code, configuration files, and existing test suites must remain untouched.
3. **Hybrid State Persistence:** After each stage, the agent writes a structured checkpoint summary to `.devkit/run-state/` to ensure observability and clean recovery handoffs.
4. **Harness Independence:** This orchestrator uses abstract file operations (`READ_FILE`, `WRITE_FILE`, `LIST_DIR`, `RUN_SHELL`). It contains no vendor-specific APIs or proprietary tool names.

---

## 2. Orchestration State Machine Algorithm

```
Algorithm 1: Autonomous Single-Agent Planning Pipeline
Inputs:
  - repo_root: Absolute or relative path to the target repository
  - feature_statement: Verbatim feature or problem request
  - stack_hint: Optional advisory tech stack hint (default: null)
  - depth: Planning depth ("auto" | "shallow" | "deep", default: "auto")
  - feature_id_override: Optional slug override (default: null)

Outputs:
  - Complete Blueprint suite in repo_root/.devkit/plans/<feature-slug>/
  - Run summary delivered to developer interface
```

### Execution Loop

#### Step 0: Pre-Flight Validation & Session Resumption Check
1. **Access Verification:**
   - Verify that `repo_root` exists and is readable.
   - If inaccessible, abort immediately with error: `"Target repository path is inaccessible: <repo_root>"`.
2. **State Directory Check & Stale State Prevention (Algorithm 3):**
   - Check if `<repo_root>/.devkit/run-state/` exists.
   - **If exists:**
     - Read `<repo_root>/.devkit/run-state/stage-log.md`.
     - Extract `feature_statement_hash` and `last_updated_at`.
     - Compute `current_hash = SHA256(feature_statement)`.
     - **If `current_hash != feature_statement_hash`:**
       - Existing run-state belongs to an unrelated feature!
       - Archive or purge stale state: Remove `<repo_root>/.devkit/run-state/`.
       - Create fresh `<repo_root>/.devkit/run-state/`.
     - **Else if `(current_time - last_updated_at) > 24 hours`:**
       - Checkpoint is stale (> 24h). Purge and start fresh.
     - **Else (`current_hash == feature_statement_hash` and age <= 24h):**
       - Valid interruption detected. Enter **Resumption Protocol** (Section 3).
   - **If does not exist:**
     - Create `<repo_root>/.devkit/run-state/`.
3. **Run Identity Initialization:**
   - Generate `run_id = "run_" + ISO_TIMESTAMP_UTC + "_" + RANDOM_HEX(4)`.
   - Write initial `<repo_root>/.devkit/run-state/stage-log.md` with:
     - All stages 1..8 set to `PENDING`.
     - `feature_statement_hash = SHA256(feature_statement)`.
     - `overall_status = "IN_PROGRESS"`.

---

#### Step 1: Execute Stage 1 (Intake & Clarification)
- Read and follow instructions in `core/stages/stage1_intake.md`.
- Mark Stage 1 as `IN_PROGRESS` in `stage-log.md`.
- Derive `feature_slug` and evaluate feature against `core/rubrics/evidence_rubric.md`.
- **Conditional Branch (Critical Ambiguity):**
  - If a Tier 4 Critical Ambiguity is detected:
    - Format batched question list (maximum 5).
    - Present to developer via harness interface and **PAUSE**.
    - Upon receiving answers, record them in `.devkit/run-state/intake.md`.
- Write `.devkit/run-state/intake.md`.
- Mark Stage 1 as `COMPLETED` in `stage-log.md`.

---

#### Step 2: Execute Stage 2 (Repository Reconnaissance)
- Read `intake.md`.
- Mark Stage 2 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage2_recon.md`.
- Scan directory trees, parse package manifests, detect archetype using `core/rubrics/repo_classification_matrix.md`.
- Write `.devkit/run-state/repo-map.md` and `.devkit/run-state/repo-type.md`.
- Mark Stage 2 as `COMPLETED` in `stage-log.md`.

---

#### Step 3: Execute Stage 3 (Architecture & Conventions Analysis)
- Read `repo-map.md` and `repo-type.md`.
- Mark Stage 3 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage3_architecture.md`.
- Map module boundaries, infer architecture (`[INFERRED]`), extract conventions across 7 dimensions.
- Write `.devkit/run-state/architecture.md` and `.devkit/run-state/conventions.md`.
- Mark Stage 3 as `COMPLETED` in `stage-log.md`.

---

#### Step 4: Execute Stage 4 (Feature Specification Formulation)
- Read `intake.md`, `architecture.md`, and `conventions.md`.
- Mark Stage 4 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage4_spec.md`.
- Create directory `<repo_root>/.devkit/plans/<feature-slug>/` if it does not exist.
- Formulate User Stories, Functional Requirements (FRs), verifiable Acceptance Criteria (ACs), scope boundaries, and assumptions.
- Write `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md` using `core/templates/feature_spec_template.md`.
- Mark Stage 4 as `COMPLETED` in `stage-log.md`.

---

#### Step 5: Execute Stage 5 (Impact & Risk Analysis)
- Read `feature-spec.md`, `architecture.md`, and `repo-map.md`.
- Mark Stage 5 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage5_impact_risk.md`.
- Identify files to modify, prospective files to create (`[NEW FILE]`), evaluate backward compatibility, and construct the technical risk register.
- Formulate the impact model in memory for Stage 6.
- Mark Stage 5 as `COMPLETED` in `stage-log.md`.

---

#### Step 6: Execute Stage 6 (Task Decomposition)
- Read `feature-spec.md`, Stage 5 impact model, and `conventions.md`.
- Mark Stage 6 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage6_tasks.md`.
- Decompose feature into dependency-ordered atomic tasks (`TASK-xxx`) with verified paths or `[NEW FILE]` tags.
- Construct the Mermaid task dependency DAG.
- Write `<repo_root>/.devkit/plans/<feature-slug>/task-breakdown.md` using `core/templates/task_breakdown_template.md`.
- Write `<repo_root>/.devkit/plans/<feature-slug>/implementation-plan.md` using `core/templates/implementation_plan_template.md`.
- Mark Stage 6 as `COMPLETED` in `stage-log.md`.

---

#### Step 7: Execute Stage 7 (Validation Planning)
- Read `feature-spec.md`, `task-breakdown.md`, and `repo-map.md`.
- Mark Stage 7 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage7_validation.md`.
- Map 100% of `AC-xxx` items to explicit `TC-xxx` test case specifications aligned with detected test runners.
- Write `<repo_root>/.devkit/plans/<feature-slug>/validation-plan.md` using `core/templates/validation_plan_template.md`.
- Mark Stage 7 as `COMPLETED` in `stage-log.md`.

---

#### Step 8: Execute Stage 8 (Quality Gate & Finalization)
- Read all generated artifacts in `.devkit/plans/<feature-slug>/` and run-state files.
- Mark Stage 8 as `IN_PROGRESS` in `stage-log.md`.
- Read and follow instructions in `core/stages/stage8_quality_gate.md`.
- Execute Hard Verification Gates (`QG-H1` to `QG-H5`) and Soft Gates (`QG-S1` to `QG-S3`).
- Write `<repo_root>/.devkit/plans/<feature-slug>/decisions.md` using `core/templates/decisions_template.md`.
- Write `<repo_root>/.devkit/plans/<feature-slug>/run-summary.md` using `core/templates/run_summary_template.md`.
- Promote `stage-log.md` to `<repo_root>/.devkit/plans/<feature-slug>/plan-run.log`.
- **Cleanup:**
  - If all Hard Gates pass: Remove temporary run-state files from `<repo_root>/.devkit/run-state/`.
  - If a Hard Gate fails: Preserve `.devkit/run-state/` for developer debugging.
- Mark Stage 8 as `COMPLETED` in `plan-run.log`.
- Deliver run summary and relative links to the developer interface.

---

## 3. Fresh-Session Resumption Protocol

If an agent session was terminated mid-run (e.g. timeout or context exhaustion):
1. **Inspect `stage-log.md`:** Check the last recorded stage status.
2. **Status Evaluation:**
   - Any stage marked `COMPLETED` has its checkpoint verified and is NOT re-executed.
   - Any stage marked `IN_PROGRESS` was interrupted mid-execution. Reset this stage to `PENDING` and **re-execute it from scratch** using prior completed checkpoints.
   - All subsequent `PENDING` stages execute normally in sequence.
3. **Zero History Dependency:** The resumed agent loads only the files in `.devkit/run-state/`. No prior conversational history is needed.

---

## 4. Error Handling & Abort Procedures

- **Target Repo Inaccessible:** Abort immediately with status `FAILED`; write no files.
- **Unrecoverable Tool Failure:** If a file write or read fails due to system permissions, log the failure in `stage-log.md`, mark `overall_status = "FAILED"`, and report the exact path error to the developer.
- **Hard Gate Failure:** The pipeline finishes Stage 8, sets artifact front-matter `status = "incomplete"`, logs exact blocking defects in `run-summary.md`, preserves `.devkit/run-state/`, and halts without declaring plan approval.
