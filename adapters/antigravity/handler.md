# Antigravity Adapter Handler & Presentation Guidelines

> **Layer:** Harness Adapter Layer (Google Antigravity MVP)  
> **Target Document:** `adapters/antigravity/handler.md`  
> **Status:** Authoritative Adapter Handler Specification  

---

## 1. Intent Extraction & Parameter Mapping

When a developer interacts with the Antigravity assistant to plan a feature, the adapter maps the natural language prompt into canonical DevKit parameters:

| Chat Extraction Source | Canonical Parameter | Fallback / Default |
|---|---|---|
| User prompt text describing the feature or task | `feature_statement` | Required. Prompt user if missing. |
| Active workspace path (or explicit `--repo <path>`) | `repo_root` | Current working directory |
| Explicit tech stack mention (e.g. "using Prisma + Next.js") | `stack_hint` | `null` |
| Complexity or depth flags (`--depth shallow / deep`) | `depth` | `"auto"` |
| Custom slug or feature ID (`--feature-id <slug>`) | `feature_id_override` | `null` |

---

## 2. Interactive Clarification Relay (Stage 1 Only)

If Stage 1 identifies a **Tier 4 Critical Ambiguity**, the adapter must present the question block directly to the chat interface.

### Format Requirement:
```markdown
### ⚠️ Critical Clarification Required Before Planning

Before analyzing the repository, please clarify the following critical ambiguity:

1. **[Question Title]**
   - **Context:** [Why the codebase cannot resolve this ambiguity]
   - **Option A:** [Description and architectural implications]
   - **Option B:** [Description and architectural impact]
   - **Recommended Default:** [Option that will be chosen if unspecified]
```

- **Wait for response:** The agent yields turn to the developer.
- **Resume:** Upon receiving the developer's reply, the agent records the answers into `.devkit/run-state/intake.md` and immediately proceeds to Stage 2 without further prompt interruptions.

---

## 3. Tool Access Mapping

The Antigravity agent executes the core instructions using its native tools:

| DevKit Core Directive | Antigravity Native Tool | Safety Assertion |
|---|---|---|
| `READ_FILE(path)` | `read_file` tool | Read-only access to repository root |
| `WRITE_FILE(path, content)` | `write_file` tool | **MUST assert path starts with `.devkit/`** |
| `LIST_DIR(path)` | `run_command` (`ls` or `find`) | Read-only exploration |
| `CHECK_GIT_STATUS()` | `run_command` (`git status --porcelain`) | Read-only verification |

---

## 4. Completion Summary Presentation

Upon successful completion of Stage 8, the adapter formats the final response to the user. It must deliver a concise summary and **clickable file links** (using `file://` URIs) for all generated Blueprint deliverables.

### Standard Response Format:

```markdown
### 🎯 Feature Planning Blueprint Generated Successfully

The implementation plan for **[Feature Name]** has been generated and validated against repository conventions.

- **Feature Identifier:** `[feature-slug]`
- **Detected Archetype:** `[repo-type]`
- **Quality Gate Status:** `approved` (or `draft`)

#### Generated Blueprint Artifacts:
1. [`feature-spec.md`](file://[repo_root]/.devkit/plans/[slug]/feature-spec.md) — Formal User Stories, Functional Requirements & Acceptance Criteria
2. [`implementation-plan.md`](file://[repo_root]/.devkit/plans/[slug]/implementation-plan.md) — Architecture strategy, impact analysis & risk register
3. [`task-breakdown.md`](file://[repo_root]/.devkit/plans/[slug]/task-breakdown.md) — Phased task cards with Mermaid DAG
4. [`validation-plan.md`](file://[repo_root]/.devkit/plans/[slug]/validation-plan.md) — Unit/Integration test cases mapped to acceptance criteria
5. [`decisions.md`](file://[repo_root]/.devkit/plans/[slug]/decisions.md) — Architecture Decision Records (ADRs) & documented assumptions
6. [`run-summary.md`](file://[repo_root]/.devkit/plans/[slug]/run-summary.md) — Executive summary & quality gate results

#### Next Steps:
1. Review [`feature-spec.md`](file://[repo_root]/.devkit/plans/[slug]/feature-spec.md) to confirm acceptance criteria.
2. Review [`decisions.md`](file://[repo_root]/.devkit/plans/[slug]/decisions.md) for documented assumptions.
3. Pass [`task-breakdown.md`](file://[repo_root]/.devkit/plans/[slug]/task-breakdown.md) to an implementation agent or developer to begin coding.
```
