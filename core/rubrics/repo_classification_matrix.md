# Repository Archetype Classification Matrix

This matrix specifies the deterministic evidence signals and scoring weights used in Stage 2 to classify the target repository into one of six distinct archetypes.

---

## 1. Archetype Scoring Rules

The agent inspects directory roots and dependency manifests to accumulate evidence points for each archetype. The archetype with the highest total score is assigned.

| Archetype | Signal Indicator | Weight | Corroborating Evidence |
|---|---|---|---|
| **Monorepo** | Workspace manifest: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`, `Cargo.toml` with `[workspace]` | +10 pts | Top-level workspace configuration file |
| | Multiple package manifests in subdirectories (`packages/*`, `apps/*`) | +8 pts | Multiple packages maintained under shared root |
| **Infrastructure / DevOps** | Declarative IaC files: `*.tf`, `Chart.yaml`, `kustomization.yaml`, `ansible.cfg` | +10 pts | Infrastructure provisioning files present |
| | Absence of traditional application code directories (`src/`, `app/`, `lib/`) | +6 pts | Repository is purely operational/declarative |
| **Data Engineering** | Pipeline definitions: Airflow DAGs, `dbt_project.yml`, Spark configs, Prefect workflows | +10 pts | Data orchestration configurations present |
| | Dedicated ETL script directories: `pipelines/`, `dags/`, `etl/`, `notebooks/*.ipynb` | +6 pts | Data transformation scripts |
| **Library / SDK** | Public packaging exports declared in manifest (`main`, `module`, `types`, `exports`) | +8 pts | Designed for downstream consumption |
| | High unit test ratio with complete absence of web/server framework dependencies | +6 pts | Reusable domain logic without HTTP runtime |
| **Application** | Web/API server entrypoints: `server.ts`, `app.py`, `main.go`, `src/index.ts` | +8 pts | Standalone runtime bootstrap file |
| | Web frameworks in dependencies: Express, Fastify, Next.js, Django, FastAPI, Spring | +8 pts | HTTP application framework declared |
| | UI component trees or HTTP route controller directories (`routes/`, `controllers/`, `views/`) | +6 pts | User-facing or API endpoint surface |

---

## 2. Classification Thresholds & Fallbacks

- **Primary Threshold:** An archetype must score **≥ 8 points** to be classified.
- **Tie-Breaking Rule:** If two archetypes tie with equal score:
  - If one is `Monorepo`, assign `Monorepo` (the monorepo contains sub-archetypes).
  - Otherwise, assign `Application` if user-facing code exists.
- **Fallback Rule:** If no archetype scores ≥ 8 points:
  - Assign `Unknown / Mixed`.
  - Log the ambiguity in `repo-type.md`.
  - Fall back to generic empirical code analysis without making architectural assumptions.

---

## 3. Planning Pipeline Adaptations by Archetype

| Detected Archetype | Focus Areas for Planning Pipeline |
|---|---|
| **Application** | Focus on user-facing behavior, route controllers, persistence migrations, transaction boundaries, and end-to-end integration flows. |
| **Library / SDK** | Focus on public API surface, backward compatibility, zero runtime side effects, minimal external dependencies, and strict unit test coverage. |
| **Data Engineering** | Focus on data idempotency, schema evolution, pipeline execution latency, backfill strategies, and pipeline failure recovery. |
| **Infrastructure** | Focus on declarative resource definitions, security blast radius, state management, idempotency, and rollback procedures. |
| **Monorepo** | Focus on isolating impacted package boundaries, cross-package dependency cycles, and shared library reusability. |
| **Unknown / Mixed** | Conduct cautious empirical analysis; avoid framework-specific assumptions; mark generated Blueprints as `draft`. |
