# Execution Audit Log: {{feature_name}}

- **Run ID:** `{{run_id}}`
- **Feature Slug:** `{{feature_slug}}`
- **Feature Statement Hash:** `{{feature_statement_hash}}`
- **Target Repository:** `{{repo_path}}`
- **Execution Started At:** `{{started_at}}`
- **Execution Completed At:** `{{completed_at}}`
- **Overall Status:** `{{overall_status}}`

---

## 1. Stage Timing & Execution Summary

| Stage # | Stage Name | Status | Started At | Completed At | Duration (s) | Notes / Artifacts Written |
|---|---|---|---|---|---|---|
| 1 | Intake & Clarification | COMPLETED | {{s1_start}} | {{s1_end}} | {{s1_duration}} | intake.md |
| 2 | Repository Reconnaissance | COMPLETED | {{s2_start}} | {{s2_end}} | {{s2_duration}} | repo-map.md, repo-type.md |
| 3 | Architecture & Conventions | COMPLETED | {{s3_start}} | {{s3_end}} | {{s3_duration}} | architecture.md, conventions.md |
| 4 | Feature Specification | COMPLETED | {{s4_start}} | {{s4_end}} | {{s4_duration}} | feature-spec.md |
| 5 | Impact & Risk Analysis | COMPLETED | {{s5_start}} | {{s5_end}} | {{s5_duration}} | In-memory impact model |
| 6 | Task Decomposition | COMPLETED | {{s6_start}} | {{s6_end}} | {{s6_duration}} | task-breakdown.md, implementation-plan.md |
| 7 | Validation Planning | COMPLETED | {{s7_start}} | {{s7_end}} | {{s7_duration}} | validation-plan.md |
| 8 | Quality Gate Verification | COMPLETED | {{s8_start}} | {{s8_end}} | {{s8_duration}} | decisions.md, run-summary.md |

---

## 2. Chronological Event Audit Trail

{{chronological_event_bullets}}

---

## 3. Anomaly & Warning Log

{{anomaly_and_warning_entries}}
