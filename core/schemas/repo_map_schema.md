# Checkpoint State Schema: Repository Map (`repo-map.md`)

> **Location:** `<target-repo>/.devkit/run-state/repo-map.md`  
> **Lifecycle:** Ephemeral (Created in Stage 2, cleared upon Stage 8 finalization)  
> **Written by:** Stage 2 (Repository Reconnaissance)  
> **Read by:** Stage 3, Stage 4, Stage 5, Stage 6, Stage 7, Stage 8  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-repo-map"
run_id: "<unique-run-id>"
feature_slug: "<feature-slug>"
generated_at: "<ISO-8601-timestamp>"
total_files_scanned: <integer>            # capped by reconnaissance scan limit
status: "COMPLETED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. Directory Tree & Key Structure
A structured inventory of existing folders and files up to depth 3, with ignored paths omitted (`node_modules`, `.git`, `dist`, etc.).

### 2. Dependency Manifests & Tooling
- **Primary Languages:** Detected programming languages with extension prevalence.
- **Package Manifests:** Listed manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, etc.) with declared production and development dependencies.
- **Build & Package Managers:** Detected tools (e.g., `npm`, `pnpm`, `cargo`, `poetry`, `maven`, `gradle`).

### 3. Application Entrypoints & Routing
- Entrypoint files (e.g., `src/index.ts`, `cmd/server/main.go`, `app.py`).
- Identified API routes or controller registries.

### 4. Configuration & Environment Profiles
- Configuration files inspected (`.env.example`, `tsconfig.json`, `docker-compose.yml`, `settings.py`).

### 5. Testing Infrastructure
- Detected testing framework(s) (e.g., Jest, Pytest, Go test, JUnit).
- Test directory locations (`tests/`, `__tests__/`, `src/**/*.test.ts`).
- Standard test runner execution commands.

### 6. Code Quality & CI/CD
- Linter and formatter configurations (`.eslintrc`, `prettierrc`, `ruff.toml`).
- CI/CD workflow files (`.github/workflows/`, `.gitlab-ci.yml`).

### 7. Reconnaissance Limitations & Skipped Paths
- Explicitly documented list of any binary, encrypted, or large generated directories omitted from scanning.
