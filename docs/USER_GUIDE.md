# Feature Planning DevKit — Practical User Guide

> **A straightforward guide to using the Feature Planning DevKit across your projects and agentic environments.**

---

## 1. What is the DevKit?

The **Feature Planning DevKit** is an autonomous planning engine that analyzes your codebase and writes a complete, structured implementation plan (called a **Blueprint**) before any coding begins.

When you give it a feature request, it:
1. **Scans your project (read-only):** Detects existing code structure, naming conventions, and test setups.
2. **Generates requirements & tasks:** Writes clear acceptance criteria, atomic tasks, and test specifications.
3. **Guarantees zero code modifications:** Writes strictly to `.devkit/`. It never edits or breaks your existing application code during planning.

---

## 2. Multi-Harness Architecture: MVP vs. Universal Portability

A key design feature of the DevKit is the strict separation between its **Core Intelligence** and its **Harness Adapters**:

```
agentic-feature-planning-devkit/
├── core/                  <-- 100% PORTABLE: Markdown instructions, schemas, rubrics.
│                              Zero proprietary dependencies. Runs on ANY LLM harness.
└── adapters/
    ├── antigravity/       <-- NATIVE MVP ADAPTER: Native skill discovery (.agents/skills/)
    └── generic_contract.md<-- Standard interface for future Claude/Cursor native plugins
```

- **Google Antigravity (Current MVP):** Fully supported with native skill auto-discovery (`SKILL.md`). You can simply talk to the agent in chat and it activates automatically.
- **Other Runtimes (Claude Code, Cursor, Copilot, Cline):** Fully compatible today! Because `core/orchestrator.md` is pure Markdown, any tool can execute it via instruction injection. Native extension packages for these runtimes are planned for post-MVP.

---

## 3. How do I get it?

### Publishing / Sourcing from GitHub
To publish this DevKit to GitHub for your team:
```bash
git remote add origin https://github.com/<your-org>/agentic-feature-planning-devkit.git
git branch -M main
git push -u origin main
```
*(Replace `<your-org>` with your GitHub organization or username).*

Developers can then obtain the DevKit using one of the methods below.

---

## 4. How do I set it up in my project?

You do **not** need a separate repository containing just `core/` and `adapters/`. Because the DevKit is tiny (~680 KB total), you can install it using either of these two methods:

### Method 1: Git Submodule (Best for Teams)
Keep the DevKit pinned inside your application repository so all team members have access:

```bash
# In your target application repository:
git submodule add https://github.com/<your-org>/agentic-feature-planning-devkit.git .agents/skills/feature-planner
```

### Method 2: One-Line Installer Script
Run the automated installer in your target project root:
```bash
# From GitHub:
curl -fsSL https://raw.githubusercontent.com/<your-org>/agentic-feature-planning-devkit/main/install.sh | bash

# OR from a local clone on your machine:
/path/to/agentic-feature-planning-devkit/install.sh
```
This automatically places the skill files and portable core into `.agents/skills/feature-planner/`.

### Method 3: Global Installation (Available across all local projects)
To make the skill automatically available in every project on your machine:
```bash
mkdir -p ~/.gemini/config/skills/feature-planner
cp -r /path/to/agentic-feature-planning-devkit/adapters/antigravity/* ~/.gemini/config/skills/feature-planner/
cp -r /path/to/agentic-feature-planning-devkit/core ~/.gemini/config/skills/feature-planner/
```

---

## 5. How do I plan a feature?

### In Google Antigravity (Native Skill Experience)

1. Open your target project:
   ```bash
   cd /path/to/my-project
   agy
   ```
2. Request feature planning in chat:
   ```text
   Plan feature: Add retry handling with exponential backoff to the Stripe payment client.
   ```
3. Antigravity detects the skill, scans your repository (read-only), and generates the complete Blueprint under `.devkit/plans/`.

### In Claude Code, Cursor, or Windsurf (Instruction Injection)

Because `core/orchestrator.md` is pure Markdown, you can run the DevKit directly:

1. Open your project in Claude Code or Cursor.
2. In the chat prompt (or in your project's `.cursorrules` / `CLAUDE.md`), provide this instruction:
   ```markdown
   Act as an autonomous Feature Planner. Follow the instructions in:
   .agents/skills/feature-planner/core/orchestrator.md

   Target Repository: Current workspace
   Feature Statement: "Add retry handling with exponential backoff to the Stripe payment client."
   
   Constraint: Planning is read-only. Write all outputs strictly into .devkit/.
   ```

---

## 6. What will it generate?

Every planning run produces six cohesive documents:

| Document | Purpose |
|---|---|
| **`feature-spec.md`** | User stories, functional requirements (`FR-xxx`), and testable acceptance criteria (`AC-xxx`). |
| **`implementation-plan.md`** | Architecture strategy, affected existing files, new files to create, and technical risks. |
| **`task-breakdown.md`** | Phased task cards (`TASK-xxx`) with file paths, instructions, and an editable Mermaid dependency diagram. |
| **`validation-plan.md`** | Concrete test cases (`TC-xxx`) mapped 1-to-1 to each acceptance criterion using your project's test framework. |
| **`decisions.md`** | Architecture Decision Records (ADRs) explaining choices made and alternative options rejected. |
| **`run-summary.md`** | Executive summary and quality gate audit results confirming zero circular tasks or invalid file paths. |

---

## 7. Where are the generated files stored?

All files are created inside a **`.devkit/`** directory in your project's root:

```text
my-project/
├── src/
├── tests/
├── package.json
└── .devkit/                         <-- Created automatically by DevKit
    ├── run-state/                   <-- Temporary checkpoint files (purged on completion)
    └── plans/
        └── retry-handling-stripe/   <-- Permanent Blueprint folder
            ├── feature-spec.md
            ├── implementation-plan.md
            ├── task-breakdown.md
            ├── validation-plan.md
            ├── decisions.md
            └── run-summary.md
```

You do not need to create `.devkit/` manually; the DevKit creates it automatically.

---

## 8. Should I push the generated files to GitHub?

You have two simple options:

### Choice A: Team Collaboration (Recommended)
Keep your plans in Git so that code reviewers, team members, or other AI agents can inspect and follow the Blueprint.

Add this line to your project's `.gitignore`:
```gitignore
# Keep generated plans, ignore temporary checkpoint files
.devkit/run-state/
```

### Choice B: Local / Personal Only
If you prefer not to check any planning files into version control:

Add this line to your project's `.gitignore`:
```gitignore
# Ignore all DevKit files
.devkit/
```

---

## 9. What if planning is interrupted?

If your session disconnects or an AI tool runs out of quota midway through planning:

1. **Your progress is preserved:** After every stage, intermediate state is saved inside `.devkit/run-state/`.
2. **Resume simply by asking again:** Open a new session and send the exact same feature prompt:
   ```text
   Plan feature: Add retry handling with exponential backoff to the Stripe payment client.
   ```
3. The DevKit validates the statement's SHA-256 hash and resumes immediately from the interrupted stage without re-running prior stages.

---

## 10. How do I update the DevKit?

- **If using Git Submodule:**
  ```bash
  git submodule update --remote .agents/skills/feature-planner
  ```
- **If using Installer / Copy:**
  ```bash
  curl -fsSL https://raw.githubusercontent.com/<your-org>/agentic-feature-planning-devkit/main/install.sh | bash
  ```

Because all generated plans are self-contained Markdown files inside `.devkit/plans/`, updating the DevKit will never modify or break your existing plans.
