---
devkit_version: "0.2.0"
artifact_type: "implementation-plan"
feature_id: "{{feature_slug}}"
feature_name: "{{feature_name}}"
repo: "{{repo_path}}"
generated_at: "{{iso_timestamp}}"
planning_depth: "{{depth}}"
status: "{{status}}"
schema_version: "1"
---

# Implementation Plan: {{feature_name}}

## 1. Executive Summary
{{executive_summary_narrative}}

## 2. Repository Context
### 2.1 Repository Archetype
- **Detected Type:** `{{repo_type}}`
- **Classification Evidence:** {{repo_type_evidence}}

### 2.2 Inferred Architecture [INFERRED]
- **Architectural Pattern:** `{{inferred_pattern}}`
- **Component Layout:** {{component_layout_description}}

### 2.3 Relevant Modules & Boundaries
- **Target Module:** `{{target_module_path}}`
- **Affected Dependencies:** `{{affected_dependencies}}`

### 2.4 Conventions Applied
- **File Naming:** `{{naming_style}}`
- **Directory Patterns:** `{{directory_pattern}}`
- **Error Handling:** `{{error_handling_idiom}}`

## 3. Implementation Strategy
### 3.1 Approach Narrative
{{technical_approach_narrative}}

### 3.2 Key Architectural Decisions
- Summary of core decisions (see detailed records in [decisions.md](./decisions.md)).

### 3.3 Code Reuse Opportunities
- Existing abstractions, base classes, and helpers to reuse.

## 4. Impact Analysis
### 4.1 Files to Modify
| File Path | Description of Changes |
|---|---|
| `{{existing_file_path_1}}` | {{change_description_1}} |

### 4.2 Files to Create [NEW FILE]
| Prospective File Path | Purpose |
|---|---|
| `[NEW FILE: {{new_file_path_1}}]` | {{new_file_purpose_1}} |

### 4.3 Cross-Cutting Concerns
- Authentication, logging, data validation, and transaction handling.

### 4.4 Backward Compatibility Assessment
- Assessment of database schemas, API contracts, and client compatibility.

## 5. Technical Risk Register
| Risk ID | Description | Likelihood | Impact | Mitigation Strategy |
|---|---|---|---|---|
| RISK-001 | {{risk_description}} | Low / Medium / High | Low / Medium / High | {{mitigation_strategy}} |

## 6. Security Considerations
- Authentication, authorization, input validation, and sensitive data safeguards.

## 7. Task Summary
- Refer to [task-breakdown.md](./task-breakdown.md) for full dependency-ordered execution cards.

## 8. Definition of Done
- [ ] All functional requirements (FRs) implemented.
- [ ] All acceptance criteria (ACs) verified via automated tests.
- [ ] Zero linting or formatting regressions.
- [ ] No unintended modifications outside feature scope.

## 9. Related Artifacts
- [Feature Specification](./feature-spec.md)
- [Task Breakdown](./task-breakdown.md)
- [Validation Plan](./validation-plan.md)
- [Decisions & ADRs](./decisions.md)
