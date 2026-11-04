# Checkpoint State Schema: Repository Type Classification (`repo-type.md`)

> **Location:** `<target-repo>/.devkit/run-state/repo-type.md`  
> **Lifecycle:** Ephemeral (Created in Stage 2, cleared upon Stage 8 finalization)  
> **Written by:** Stage 2 (Repository Reconnaissance)  
> **Read by:** Stage 3, Stage 4, Stage 5, Stage 6, Stage 7, Stage 8  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-repo-type"
run_id: "<unique-run-id>"
feature_slug: "<feature-slug>"
detected_archetype: "Application | Library | Data Engineering | Infrastructure | Monorepo | Unknown"
confidence_level: "HIGH | MEDIUM | LOW"
status: "COMPLETED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. Archetype Classification Result
- **Assigned Archetype:** One of `Application`, `Library`, `Data Engineering`, `Infrastructure`, `Monorepo`, or `Unknown`.
- **Classification Summary:** 1–2 sentences explaining why the repository belongs to this category.

### 2. Evidence Scoring Table
A breakdown of points scored per archetype based on the Repository Classification Matrix (`core/rubrics/repo_classification_matrix.md`):

| Archetype | Signals Detected | Score |
|---|---|---|
| Monorepo | Workspace manifests, multi-package layouts | N pts |
| Infrastructure | Terraform/Helm/K8s manifests | N pts |
| Data Engineering | Airflow DAGs, dbt projects, ETL scripts | N pts |
| Library / SDK | Packaging exports, high unit tests, no server | N pts |
| Application | Server entrypoints, web framework, UI/routes | N pts |

### 3. Planning Adaptations
- Concrete adaptations applied to the planning pipeline based on the detected archetype (e.g., focusing on API backward-compatibility for libraries, or database migration safety for applications).

### 4. Ambiguities & Limitations
- Any mixed-archetype characteristics observed (e.g., a monorepo containing both applications and libraries).
