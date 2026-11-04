---
devkit_version: "0.2.0"
artifact_type: "run-summary"
feature_id: "{{feature_slug}}"
feature_name: "{{feature_name}}"
repo: "{{repo_path}}"
generated_at: "{{iso_timestamp}}"
planning_depth: "{{depth}}"
status: "{{status}}"
schema_version: "1"
---

# Planning Run Summary: {{feature_name}}

## Executive Summary
- **Feature Identifier:** `{{feature_slug}}`
- **Target Repository:** `{{repo_path}}`
- **Detected Archetype:** `{{repo_type}}`
- **Planning Depth:** `{{depth}}`
- **Final Status:** `{{status}}` (approved | draft | incomplete)
- **Duration:** {{duration_seconds}}s

## Quality Gate Verification Results

| Check ID | Verification Gate | Result | Verification Notes |
|---|---|---|---|
| QG-H1 | 100% Path Grounding | ✅ PASS / ❌ FAIL | {{qg_h1_notes}} |
| QG-H2 | Acyclic Task Graph (DAG) | ✅ PASS / ❌ FAIL | {{qg_h2_notes}} |
| QG-H3 | Requirement Traceability | ✅ PASS / ❌ FAIL | {{qg_h3_notes}} |
| QG-H4 | Validation Traceability | ✅ PASS / ❌ FAIL | {{qg_h4_notes}} |
| QG-H5 | Source Code Non-Mutation | ✅ PASS / ❌ FAIL | {{qg_h5_notes}} |
| QG-S1 | Open Question Resolutions | ✅ PASS / ⚠️ WARN | {{qg_s1_notes}} |
| QG-S2 | Task Complexity Assignment | ✅ PASS / ⚠️ WARN | {{qg_s2_notes}} |
| QG-S3 | Risk Register Completeness | ✅ PASS / ⚠️ WARN | {{qg_s3_notes}} |

## Generated Blueprint Artifacts
1. [`feature-spec.md`](./feature-spec.md) — Requirements & Acceptance Criteria
2. [`implementation-plan.md`](./implementation-plan.md) — Architectural strategy & risk register
3. [`task-breakdown.md`](./task-breakdown.md) — Sequenced task cards with Mermaid DAG
4. [`validation-plan.md`](./validation-plan.md) — Test cases mapped to acceptance criteria
5. [`decisions.md`](./decisions.md) — ADRs, assumptions, and open questions
6. [`plan-run.log`](./plan-run.log) — Full chronological execution audit trail

## Top Architectural Decisions & Assumptions
- **Decision 1:** {{top_decision_summary}}
- **Assumption 1:** {{top_assumption_summary}}

## Next Steps for Developer
1. Review [`feature-spec.md`](./feature-spec.md) and confirm acceptance criteria.
2. Review [`decisions.md`](./decisions.md) for documented assumptions and open questions.
3. Pass [`task-breakdown.md`](./task-breakdown.md) to implementation developer or agent harness.
