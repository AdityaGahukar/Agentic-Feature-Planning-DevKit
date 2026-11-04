# Checkpoint State Schema: Stage Log (`stage-log.md`)

> **Location:** `<target-repo>/.devkit/run-state/stage-log.md`  
> **Lifecycle:** Ephemeral during run; promoted to `.devkit/plans/<slug>/plan-run.log` upon completion.  
> **Written by:** Master Orchestrator and all Stages 1–8  
> **Read by:** Master Orchestrator (resumption and audit)  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-stage-log"
run_id: "<unique-run-id>"
feature_slug: "<feature-slug>"
feature_statement_hash: "sha256:<hash>"
started_at: "<ISO-8601-timestamp>"
last_updated_at: "<ISO-8601-timestamp>"
current_stage: <integer>                   # 1 to 8
overall_status: "IN_PROGRESS | COMPLETED | FAILED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. Execution Overview Table

| Stage # | Stage Name | Status | Started At | Completed At | Duration (s) | Notes / Anomalies |
|---|---|---|---|---|---|---|
| 1 | Intake & Clarification | PENDING | - | - | - | - |
| 2 | Repository Reconnaissance | PENDING | - | - | - | - |
| 3 | Architecture & Conventions | PENDING | - | - | - | - |
| 4 | Feature Specification | PENDING | - | - | - | - |
| 5 | Impact & Risk Analysis | PENDING | - | - | - | - |
| 6 | Task Decomposition | PENDING | - | - | - | - |
| 7 | Validation Planning | PENDING | - | - | - | - |
| 8 | Quality Gate Verification | PENDING | - | - | - | - |

*Status Enum:* `PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `SKIPPED`.

### 2. Chronological Event Log
Ordered bulleted list of milestone events:
- `[<timestamp>] [STAGE 1] Validated repo read permissions.`
- `[<timestamp>] [STAGE 1] Derived slug: user-avatar-s3-upload.`
- `[<timestamp>] [STAGE 2] Classified repository archetype as Application.`
- `[<timestamp>] [STAGE 8] All hard quality gates passed.`

### 3. Anomaly & Warning Register
Detailed log of soft warnings, recoverable exceptions, or unexpected codebase conditions encountered.
