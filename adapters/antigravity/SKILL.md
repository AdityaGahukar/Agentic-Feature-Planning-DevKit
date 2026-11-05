---
name: feature-planner
description: Autonomous, repository-aware feature planning devkit. Analyzes feature requirements and repository context to generate complete, actionable implementation blueprints (the Blueprint) without modifying application source code.
version: 0.2.0
tools:
  - read_file
  - write_file
  - run_command
---

# Feature Planner Skill (Antigravity Adapter)

This skill packages the portable **Agentic Feature Planning DevKit** for autonomous execution within the Google Antigravity environment.

## When to Activate
Activate this skill whenever the developer requests feature planning, architecture planning, or implementation blueprints for a new or existing feature in a repository.

---

## 1. Input Parameter Mapping

When triggered by developer chat or command, extract the following canonical parameters:
- `feature_statement`: The verbatim feature request or problem statement.
- `repo_root`: The active workspace directory (or explicit path if specified by developer).
- `stack_hint`: Optional technology stack hint provided by the developer (or `null`).
- `depth`: Planning depth (`auto` default, or `shallow` / `deep` if specified).
- `feature_id_override`: Custom slug override if specified (or `null`).

---

## 2. Execution Instructions

The executing agent must strictly follow the portable core orchestrator:

1. **Load Master Orchestrator:** Read and follow [`core/orchestrator.md`](../../core/orchestrator.md).
2. **Execute Stages 1 through 8 Sequentially:**
   - Advance through all stages autonomously without asking the user for confirmation between stages.
   - Strictly sandbox all file write operations to `<repo_root>/.devkit/`.
   - **Never create, modify, or delete application source code or existing tests during planning.**
3. **Interactive Clarification Relay (Stage 1 Only):**
   - If Stage 1 detects a Tier 4 Critical Ambiguity, format the batched question list per [`core/rubrics/evidence_rubric.md`](../../core/rubrics/evidence_rubric.md), present it in chat, and wait for user response.
   - Upon receiving user answers, record them in `.devkit/run-state/intake.md` and resume Stage 2 automatically.
4. **Completion Delivery:**
   - Follow instructions in [`adapters/antigravity/handler.md`](./handler.md) to format the final execution summary with clickable links.
