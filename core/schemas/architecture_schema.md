# Checkpoint State Schema: Architecture Context (`architecture.md`)

> **Location:** `<target-repo>/.devkit/run-state/architecture.md`  
> **Lifecycle:** Ephemeral (Created in Stage 3, cleared upon Stage 8 finalization)  
> **Written by:** Stage 3 (Architecture & Conventions Analysis)  
> **Read by:** Stage 4, Stage 5, Stage 6, Stage 7, Stage 8  

---

## Front-Matter Specification

```yaml
---
devkit_version: "0.2.0"
artifact_type: "run-state-architecture"
run_id: "<unique-run-id>"
feature_slug: "<feature-slug>"
inferred_pattern: "<pattern>"              # e.g., Layered-MVC | Clean-Architecture | Hexagonal | Modular-Slice
generated_at: "<ISO-8601-timestamp>"
status: "COMPLETED"
schema_version: "1"
---
```

---

## Required Markdown Sections

### 1. Architectural Pattern Inference
- **Inferred Pattern:** Dominant structural paradigm tagged as `[INFERRED]`.
- **Structural Evidence:** Directory arrangements, module separation, and dependency directions observed in code.

### 2. Module & Boundary Mapping
- Inventory of primary modules/packages, what each module owns, and public interfaces exposed.
- Identification of the feature's natural architectural "home" module.

### 3. Shared Utilities & Domain Abstractions
- Common base classes, domain entities, interfaces, utility helpers, and validation libraries available for reuse.

### 4. Data Layer & Persistence Models
- ORM/ODM in use (Prisma, TypeORM, SQLAlchemy, Hibernate, etc.).
- Schema definition formats, query builders, and database migration mechanisms.

### 5. API & Interface Patterns
- Protocol and communication style (REST, GraphQL, gRPC, event message queues).
- Request validation patterns, serialization wrappers, and response envelope idioms.

### 6. Cross-Cutting Concerns
- Authentication and authorization mechanisms.
- Error handling strategies and logging frameworks.
- Caching, transaction boundaries, and telemetry/metrics.
