# Stage 7: Validation Planning Instruction

> **Stage ID:** STAGE-07  
> **Reads:** `<repo_root>/.devkit/plans/<feature-slug>/feature-spec.md`, `<repo_root>/.devkit/plans/<feature-slug>/task-breakdown.md`, `<repo_root>/.devkit/run-state/repo-map.md`, `<repo_root>/.devkit/run-state/conventions.md`  
> **Writes:** `<repo_root>/.devkit/plans/<feature-slug>/validation-plan.md`  
> **Template Reference:** `core/templates/validation_plan_template.md`  

---

## 1. Stage Objective

Stage 7 formulates a complete validation plan ensuring that every acceptance criterion specified in `feature-spec.md` is covered by verifiable test specifications. It tailors the test strategy to the repository's detected test infrastructure, specifies fixtures and mocks, and outlines manual verification procedures where automated testing is impractical.

---

## 2. Step-by-Step Execution Procedure

### Step 7.1: Test Infrastructure Alignment
1. Extract detected testing infrastructure from `repo-map.md`:
   - Testing framework: Jest, Vitest, Pytest, Go test, JUnit, RSpec, etc.
   - Standard test execution command: e.g. `npm test`, `pytest tests/`, `go test ./...`
   - Test directory layout and naming conventions extracted in `conventions.md`.
2. Define the validation Definition of Done:
   - 100% of Acceptance Criteria (`AC-xxx`) covered by passing tests.

---

### Step 7.2: Test Case Formulation (100% AC Coverage)
Iterate through every Functional Requirement (`FR-xxx`) and its Acceptance Criteria (`AC-xxx`) in `feature-spec.md`:
1. For each `AC-xxx`, construct at least one explicit test case specification:
   - **Test ID:** `TC-001`, `TC-002`, etc.
   - **Title:** Descriptive assertion name (e.g. `Verify avatar upload returns 201 and public S3 URL`).
   - **Type:** One of `unit`, `integration`, `e2e`, or `manual`.
   - **Traceability Link:** Explicitly link to the parent criterion: `Linked to AC-xxx-x (FR-xxx)`.
   - **Target Test File:**
     * If modifying existing test file: verified path (e.g. `tests/routes/user.test.ts`).
     * If creating new test file: `[NEW FILE: tests/unit/avatarService.test.ts]`.
   - **Preconditions:** Initial state, database records, or mock setups required before running the test.
   - **Test Steps:** Numbered sequential execution steps.
   - **Expected Outcome:** Unambiguous assertable outcome (e.g. HTTP status, database row, mock verification).
   - **Test Data / Fixtures:** Payload shapes, sample files, or seed records needed.

---

### Step 7.3: Existing Tests Requiring Updates
1. Identify existing test suites that might fail due to schema changes or route additions.
2. For each affected test file:
   - Record exact path.
   - Describe necessary modifications to keep existing tests passing.

---

### Step 7.4: Environment & Fixture Setup
1. Detail test environment requirements:
   - Environment variables needed during test execution (e.g. `TEST_DATABASE_URL`, `MOCK_S3=true`).
   - External service mock strategies (e.g. Mock Service Worker, nock, unittest.mock, WireMock).

---

### Step 7.5: Manual Verification Procedures
1. For criteria that cannot be easily automated (e.g. browser file picker behavior, visual styling, hardware access):
   - Formulate explicit manual procedures (`MVP-001`, `MVP-002`).
   - Detail step-by-step instructions and expected visual or operational results.

---

### Step 7.6: Blueprint Generation (`validation-plan.md`)
1. Populate `core/templates/validation_plan_template.md` with:
   - Front-matter: `devkit_version: "0.2.0"`, `artifact_type: "validation-plan"`, `feature_id: "<slug>"`, `generated_at`, `planning_depth`, `status: "draft"`.
   - Populated sections: Test Strategy, Test Cases (100% AC mapped), Existing Tests to Update, Fixture Setup, Manual Procedures, and Coverage Gaps.
2. Write output to `<repo_root>/.devkit/plans/<feature-slug>/validation-plan.md`.
3. Update `stage-log.md` marking Stage 7 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 8, verify:
- [ ] `<repo_root>/.devkit/plans/<feature-slug>/validation-plan.md` exists on disk.
- [ ] 100% of Acceptance Criteria (`AC-xxx`) have at least one assigned Test Case (`TC-xxx`).
- [ ] Test paths and commands align with the repository's detected test framework.
- [ ] Zero files outside `.devkit/` were modified.
