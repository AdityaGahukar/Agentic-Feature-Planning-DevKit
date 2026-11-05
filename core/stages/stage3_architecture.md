# Stage 3: Architecture & Conventions Extraction Instruction

> **Stage ID:** STAGE-03  
> **Reads:** `<repo_root>/.devkit/run-state/repo-map.md`, `<repo_root>/.devkit/run-state/repo-type.md`, relevant codebase source files  
> **Writes:** `<repo_root>/.devkit/run-state/architecture.md`, `<repo_root>/.devkit/run-state/conventions.md`  
> **Schema References:** `core/schemas/architecture_schema.md`, `core/schemas/conventions_schema.md`  
> **Rubric Reference:** `core/rubrics/evidence_rubric.md`  

---

## 1. Stage Objective

Stage 3 deduces the codebase's conceptual architecture and extracts empirical coding conventions. It maps module boundaries, data layers, and shared abstractions, and extracts coding patterns by inspecting real source files.

---

## 2. Step-by-Step Execution Procedure

### Step 3.1: Architecture Analysis & Boundary Mapping
1. **Infer Architectural Pattern:**
   - Inspect directory layouts, service abstractions, and controller boundaries.
   - Infer dominant paradigm (e.g., Layered-MVC, Clean/Hexagonal Architecture, Feature-Sliced Modular, Event-Driven, Microservice, Monolith).
   - **Crucial Rule:** All architectural inferences must be explicitly tagged as `[INFERRED]`. Never state unverified inferences as hard facts.
2. **Module & Boundary Mapping:**
   - Identify discrete functional modules or packages in the codebase.
   - Document what each module owns and exposes.
   - Identify the feature's natural architectural "home" module.
3. **Data Layer & Persistence:**
   - Identify ORM/ODM, database migration tools, schema definition files, and transaction management patterns.
4. **Shared Abstractions & Utilities:**
   - Catalog existing domain entities, base controllers, shared validation libraries, and utility helpers suitable for reuse.

---

### Step 3.2: Empirical Convention Extraction (Algorithm 2)
Sample up to 10 representative source files across the codebase and inspect them across 7 strict dimensions:

1. **File Naming Convention:**
   - Sample file names in `src/` or analogous code roots.
   - Count matches: `kebab-case` vs `camelCase` vs `PascalCase` vs `snake_case`.
   - Determine dominant convention. Record exact code examples as proof.
2. **Directory & Placement Patterns:**
   - Determine where analogous components live (e.g., services in `src/services/`, models in `src/models/`, routes in `src/routes/`).
3. **Import & Path Resolution Style:**
   - Check if path aliases (e.g. `@/components/...`, `~/utils/...`) or relative paths (`../../`) dominate.
   - Inspect barrel file (`index.ts` / `mod.rs`) usage.
4. **Error Handling Idioms:**
   - Inspect service/controller logic.
   - Check whether exceptions with middleware envelopes, Go-style `(val, err)` returns, or functional `Result<T, E>` types dominate.
5. **Logging & Observability Patterns:**
   - Check if logging uses structured JSON libraries (Winston, Pino, Logrus, Zap, Slf4j) or standard print calls.
6. **Testing Patterns & Idioms:**
   - Check test block structure (BDD `describe/it` vs `test_*`), fixture helpers, and mock libraries.
7. **API Response & Serialization Envelopes:**
   - If an API exists, inspect standard response structures: `{ data, error, meta }` vs naked payloads.

---

### Step 3.3: Convention Precedence Enforcement
Apply the **Convention Precedence Rule**:
```
Observed Repository Code > Framework Configs > Manifest Dependencies > External Framework Docs
```
- If the repository deviates from standard framework defaults (e.g., a React codebase using `PascalCase` filenames instead of `kebab-case`), the **repository pattern always wins**.
- Document every deviation in `conventions.md` as `[ASSUMPTION: evidence-supported]` citing the sample file as proof.

---

### Step 3.4: Checkpoint Generation
1. **Write `architecture.md`:**
   - Adhere to `core/schemas/architecture_schema.md`.
   - Record inferred architecture (`[INFERRED]`), module boundaries, data layer, shared abstractions, and cross-cutting concerns.
   - Save to `<repo_root>/.devkit/run-state/architecture.md`.
2. **Write `conventions.md`:**
   - Adhere to `core/schemas/conventions_schema.md`.
   - Record extracted conventions across the 7 dimensions, code evidence citations, and documented deviations.
   - Save to `<repo_root>/.devkit/run-state/conventions.md`.
3. Update `stage-log.md` marking Stage 3 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 4, verify:
- [ ] `<repo_root>/.devkit/run-state/architecture.md` exists on disk.
- [ ] `<repo_root>/.devkit/run-state/conventions.md` exists on disk.
- [ ] All architectural claims are tagged `[INFERRED]`.
- [ ] Convention deviations cite real file evidence.
- [ ] Zero files outside `.devkit/run-state/` were modified.
