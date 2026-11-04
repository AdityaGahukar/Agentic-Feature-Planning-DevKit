# Checkpoint State Schema: Intake State (`intake.md`)

> **Location:** `<target-repo>/.devkit/run-state/intake.md`  
> **Lifecycle:** Ephemeral (Created in Stage 1, cleared upon Stage 8 finalization)  
> **Written by:** Stage 1 (Intake & Clarification)  
> **Read by:** Stage 2, Stage 3, Stage 4, Stage 8  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-intake"
run_id: "<unique-run-id>"                  # e.g., run_20261104T163000Z_a1f9
feature_slug: "<feature-slug>"            # e.g., user-avatar-s3-upload
feature_statement_hash: "sha256:<hash>"   # SHA-256 of raw feature statement
started_at: "<ISO-8601-timestamp>"
last_updated_at: "<ISO-8601-timestamp>"
planning_depth: "auto | shallow | deep"
feature_category: "new-feature | bug-fix | refactor | migration | performance"
status: "COMPLETED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. Raw Inputs
- **Feature Statement:** The verbatim text of the user's feature or problem statement.
- **Target Repository:** Absolute and workspace-relative paths to the target repository.
- **Stack Hint:** Technology stack hint provided by the developer (or `none`).
- **Requested Depth:** Depth parameter provided (`auto`, `shallow`, or `deep`).

### 2. Feature Intent & Scope Hypothesis
- **Primary Goal:** 1–2 sentences summarizing what the feature achieves.
- **Target Persona / User:** The actor benefiting from this feature.
- **Hypothesized Scope:**
  - Likely components or services touched.
  - Expected external integrations or persistence requirements.

### 3. Critical Ambiguity Assessment
- **Ambiguities Evaluated:** List of potential ambiguities considered during Stage 1.
- **Status:** `NONE_DETECTED` or `RESOLVED_VIA_QA`.
- **Clarification Q&A (if triggered):**
  - Record the batched questions presented to the developer and their received answers.
