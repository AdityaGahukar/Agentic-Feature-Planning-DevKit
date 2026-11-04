# Checkpoint State Schema: Repository Conventions (`conventions.md`)

> **Location:** `<target-repo>/.devkit/run-state/conventions.md`  
> **Lifecycle:** Ephemeral (Created in Stage 3, cleared upon Stage 8 finalization)  
> **Written by:** Stage 3 (Architecture & Conventions Analysis)  
> **Read by:** Stage 4, Stage 5, Stage 6, Stage 7, Stage 8  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-conventions"
run_id: "<unique-run-id>"
feature_slug: "<feature-slug>"
dominant_naming_style: "kebab-case | camelCase | PascalCase | snake_case"
generated_at: "<ISO-8601-timestamp>"
status: "COMPLETED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. File & Directory Naming Conventions
- Dominant file naming style with regex verification count.
- Directory placement patterns for analogous files (e.g. services in `src/services/`, handlers in `cmd/`).
- Code sample evidence references.

### 2. Import & Module Resolution Style
- Module alias patterns (`@/components/...`) vs relative paths (`../../`).
- Barrel file (`index.ts` / `mod.rs`) usage conventions.

### 3. Error Handling Idioms
- Exception hierarchies, try/catch patterns, Go-style `(val, err)` returns, or Rust/TS `Result<T, E>` types.
- HTTP error response shapes and status code conventions.

### 4. Logging & Observability Patterns
- Logging library, format (structured JSON vs raw strings), and contextual metadata requirements.

### 5. Testing Idioms & Conventions
- Test block structure (`describe/it` vs `test_*`), fixture setup patterns, and mock frameworks in use.

### 6. API Envelope & Serialization Formats
- Response payload wrappers, pagination structures, and error envelopes.

### 7. Convention Deviations & Precedence Logging
- Documented list of deviations where the repository intentionally violates standard framework defaults, tagged as `[ASSUMPTION: evidence-supported]`.
