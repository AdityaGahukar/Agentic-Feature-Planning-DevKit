# Stage 2: Repository Reconnaissance Instruction

> **Stage ID:** STAGE-02  
> **Reads:** `<repo_root>/.devkit/run-state/intake.md`, target repository filesystem  
> **Writes:** `<repo_root>/.devkit/run-state/repo-map.md`, `<repo_root>/.devkit/run-state/repo-type.md`  
> **Schema References:** `core/schemas/repo_map_schema.md`, `core/schemas/repo_type_schema.md`  
> **Rubric Reference:** `core/rubrics/repo_classification_matrix.md`  

---

## 1. Stage Objective

Stage 2 conducts an empirical, read-only reconnaissance of the target repository. It catalogs the codebase layout, dependency manifests, build tooling, configurations, and test runners, and classifies the repository archetype without fabricating file paths or guessing technical facts.

---

## 2. Step-by-Step Execution Procedure

### Step 2.1: The 4-Pass Reconnaissance Routine
To ensure factual accuracy while conserving LLM context, execute reconnaissance in 4 deterministic passes:

#### Pass 1: Root Inventory & Structure Discovery
1. List the top-level directory structure and immediate subdirectories up to depth 3.
2. Explicitly skip scanning inside ignored or transient directories:
   - `node_modules`, `.git`, `.svn`, `vendor`, `target`, `dist`, `build`, `out`, `.next`, `__pycache__`, `.pytest_cache`, `.venv`, `env`.
3. Record directory layout, identifying standard folders (e.g. `src/`, `lib/`, `cmd/`, `pkg/`, `tests/`, `packages/`, `apps/`, `docs/`).

#### Pass 2: Manifest & Dependency Parsing
1. Identify and inspect all package and dependency manifests in the repository root and workspace roots:
   - Node.js: `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`
   - Rust: `Cargo.toml`, `Cargo.lock`
   - Python: `pyproject.toml`, `setup.py`, `Pipfile`, `requirements.txt`, `poetry.lock`
   - Go: `go.mod`, `go.sum`
   - Java / Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`
   - Ruby: `Gemfile`, `Gemfile.lock`
   - .NET / C#: `*.csproj`, `*.sln`
2. Extract declared runtime/production dependencies, developer dependencies, and engine/language version constraints.

#### Pass 3: Configuration & Environment Profile Inspection
1. Locate and inspect configuration files relevant to architecture and deployment:
   - Language/compiler configs: `tsconfig.json`, `jsconfig.json`
   - Framework configs: `next.config.*`, `vite.config.*`, `angular.json`, `django/settings.py`
   - Container & orchestration: `Dockerfile`, `docker-compose.yml`, `compose.yaml`
   - Environment samples: `.env.example`, `.env.template`
   - CI/CD workflows: `.github/workflows/`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`

#### Pass 4: Entrypoints & Test Infrastructure Inspection
1. Identify main entrypoints:
   - Web / API servers: `src/index.ts`, `src/server.ts`, `cmd/server/main.go`, `app.py`, `main.py`
   - Libraries: `src/index.ts`, `src/lib.rs`, exported public modules
2. Locate test directories and runner configurations:
   - Framework: Jest, Vitest, Pytest, Go test, JUnit, RSpec
   - Test files: `tests/`, `__tests__/`, `*.test.ts`, `*_test.go`, `test_*.py`
3. **Scan Budget Limit:** Limit deep content inspection to a maximum of **50 files**. Record all other files as path inventory only.

---

### Step 2.2: Repository Archetype Classification
Apply the scoring heuristics in `core/rubrics/repo_classification_matrix.md`:
1. Calculate evidence points across the 5 archetypes:
   - `Monorepo`: Workspace manifest (+10), multi-package roots (+8)
   - `Infrastructure`: Declarative IaC files (+10), absence of app source (+6)
   - `Data Engineering`: Pipeline/DAG configs (+10), ETL script directories (+6)
   - `Library / SDK`: Manifest packaging exports (+8), high unit test ratio (+6)
   - `Application`: Server bootstrap (+8), web framework (+8), UI/routes (+6)
2. Assign the archetype with the highest points (minimum threshold: 8 points).
3. If no archetype meets 8 points, assign `Unknown / Mixed`.
4. Document the score breakdown and detected archetype in memory.

---

### Step 2.3: Checkpoint Generation
1. **Write `repo-type.md`:**
   - Adhere to `core/schemas/repo_type_schema.md`.
   - Record assigned archetype, confidence level, evidence scoring table, and planning adaptations.
   - Save to `<repo_root>/.devkit/run-state/repo-type.md`.
2. **Write `repo-map.md`:**
   - Adhere to `core/schemas/repo_map_schema.md`.
   - Record verified directory tree, dependencies, entrypoints, configs, testing infrastructure, and skipped paths.
   - Save to `<repo_root>/.devkit/run-state/repo-map.md`.
3. Update `stage-log.md` marking Stage 2 as `COMPLETED`.

---

## 3. Post-Condition Checklist
Before transitioning to Stage 3, verify:
- [ ] `<repo_root>/.devkit/run-state/repo-type.md` exists and contains a valid archetype.
- [ ] `<repo_root>/.devkit/run-state/repo-map.md` exists and contains verified file paths.
- [ ] 100% of referenced files physically exist on disk (zero path fabrication).
- [ ] Zero files outside `.devkit/run-state/` were modified.
