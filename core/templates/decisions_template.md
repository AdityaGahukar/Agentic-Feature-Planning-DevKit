---
devkit_version: "0.2.0"
artifact_type: "decisions"
feature_id: "{{feature_slug}}"
feature_name: "{{feature_name}}"
repo: "{{repo_path}}"
generated_at: "{{iso_timestamp}}"
planning_depth: "{{depth}}"
status: "{{status}}"
schema_version: "1"
---

# Architecture Decisions & Assumptions: {{feature_name}}

## 1. Architecture Decision Records (ADRs)

### ADR-001: {{decision_title}}
- **Status:** Decided
- **Context:**
  {{context_and_tradeoffs}}
- **Decision:**
  {{chosen_architecture_or_pattern}}
- **Rationale:**
  {{evidence_based_rationale}}
- **Alternatives Considered:**
  - **Option A:** {{alternative_a}} (rejected because: {{rejection_reason_a}})
  - **Option B:** {{alternative_b}} (rejected because: {{rejection_reason_b}})
- **Consequences:**
  {{positive_and_negative_consequences}}

## 2. Documented Assumptions

### AS-001: {{assumption_title}}
- **Level:** evidence-supported | reasonable-default | design-choice
- **Evidence Basis:** `{{corroborating_file_path}}`
- **Risk if Wrong:** {{risk_assessment}}
- **Validation Method:** {{how_assumption_is_verified_in_code}}

### AS-002: {{assumption_title}}
- **Level:** reasonable-default
- **Evidence Basis:** Standard industry convention in absence of repo configuration.
- **Risk if Wrong:** Low
- **Validation Method:** Covered by test suite.

## 3. Open Questions [OPEN]

### OQ-001: {{open_question_title}}
- **Impact:** High | Medium | Low
- **Description:** {{question_detail}}
- **Suggested Resolution:** {{suggested_path}}
- **Blocking Status:** Non-blocking / Resolvable during implementation

## 4. Related Artifacts
- [Feature Specification](./feature-spec.md)
- [Implementation Plan](./implementation-plan.md)
- [Run Summary](./run-summary.md)
