---
devkit_version: "0.2.0"
artifact_type: "feature-spec"
feature_id: "{{feature_slug}}"
feature_name: "{{feature_name}}"
repo: "{{repo_path}}"
generated_at: "{{iso_timestamp}}"
planning_depth: "{{depth}}"
status: "{{status}}"
schema_version: "1"
---

# Feature Specification: {{feature_name}}

## 1. Overview & Business Value
{{overview_narrative}}

## 2. User Stories
- **US-001:** As a {{role}}, I want {{action}}, so that {{benefit}}.
- **US-002:** As a {{role}}, I want {{action}}, so that {{benefit}}.

## 3. Functional Requirements

### FR-001: {{requirement_title}}
- **Description:** {{requirement_description}}
- **Acceptance Criteria:**
  - [ ] **AC-001-1:** {{testable_criterion_1}}
  - [ ] **AC-001-2:** {{testable_criterion_2}}

### FR-002: {{requirement_title}}
- **Description:** {{requirement_description}}
- **Acceptance Criteria:**
  - [ ] **AC-002-1:** {{testable_criterion_1}}

## 4. Non-Functional Requirements
- **NFR-001 (Performance):** {{latency_or_throughput_constraint}}
- **NFR-002 (Security):** {{auth_or_data_protection_constraint}}
- **NFR-003 (Compatibility):** {{backward_compatibility_constraint}}

## 5. Scope Boundaries
- **In-Scope:**
  - {{in_scope_item_1}}
  - {{in_scope_item_2}}
- **Out-of-Scope:**
  - {{out_of_scope_item_1}}

## 6. Documented Assumptions
- **AS-001:** [ASSUMPTION: evidence-supported] {{assumption_detail}}. Evidence: `{{evidence_file}}`.
- **AS-002:** [ASSUMPTION: reasonable-default] {{default_detail}}.

## 7. Open Questions [OPEN]
- **OQ-001:** {{question_detail}}. Suggested Resolution: {{resolution_path}}.

## 8. Related Artifacts
- [Implementation Plan](./implementation-plan.md)
- [Task Breakdown](./task-breakdown.md)
- [Validation Plan](./validation-plan.md)
- [Decisions & ADRs](./decisions.md)
