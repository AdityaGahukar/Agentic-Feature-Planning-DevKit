# Feature Planning DevKit — Quickstart Guide

> **Get from a feature idea to a validated, repository-aware implementation plan in under 5 minutes.**

---

## 1. What is the DevKit?

When you ask an AI coding assistant to implement a new feature, it often jumps immediately into writing code. This causes hallucinated file paths, broken existing conventions, and failed tests.

The **Feature Planning DevKit** solves this by adding an autonomous **planning step** before coding begins. It inspects your project, extracts existing architecture patterns, and writes a complete, actionable **Blueprint** into your project without modifying any of your application source code.

- **Primary MVP Target:** Packaged natively for **Google Antigravity** as an autonomous skill.
- **Cross-Harness Portability:** The core engine (`core/`) is 100% portable Markdown instructions and can be executed in **Claude Code**, **Cursor**, or **Copilot** via direct instruction injection.

---

## 2. What do I need before using it?

1. An **AI coding assistant** (Google Antigravity for the native experience, or Claude Code / Cursor).
2. An **existing project codebase** where you want to plan a feature.
3. Access to this **`agentic-feature-planning-devkit`** repository (on GitHub or your local machine).

*(Note: Planning requires no databases, background daemons, or binary CLI installations. It runs entirely within your agentic environment.)*

---

## 3. How do I obtain and configure it?

> **Repository Note:** When publishing this repository to GitHub, replace `<your-org>` below with your GitHub username or organization (e.g. `https://github.com/my-org/agentic-feature-planning-devkit.git`).

You have two clean options to add the DevKit to your project:

### Option A: Git Submodule (Recommended for Teams)
Keep the DevKit connected to your project repository so any team member who clones your project gets planning capabilities automatically:

```bash
# In your target application repository root:
cd /path/to/my-project

# Add DevKit directly into your project's Antigravity skills directory:
git submodule add https://github.com/<your-org>/agentic-feature-planning-devkit.git .agents/skills/feature-planner
```

### Option B: Quick Installer / Local Copy
If you prefer not to use submodules, install only the required skill and core files into your project:

```bash
# In your target application repository root:
cd /path/to/my-project

# Run the installer from GitHub:
curl -fsSL https://raw.githubusercontent.com/<your-org>/agentic-feature-planning-devkit/main/install.sh | bash

# OR copy from a local clone of this DevKit repository:
mkdir -p .agents/skills/feature-planner
cp -r /path/to/agentic-feature-planning-devkit/adapters/antigravity/* .agents/skills/feature-planner/
cp -r /path/to/agentic-feature-planning-devkit/core .agents/skills/feature-planner/
```

---

## 4. How do I plan a feature?

### In Google Antigravity (Native Skill)

1. Open your target project in Antigravity or launch the CLI:
   ```bash
   cd /path/to/my-project
   agy
   ```
2. Simply ask in chat using natural language:
   ```text
   Plan feature: Add rate limiting to the login endpoint to prevent brute-force attacks.
   ```
   Antigravity will automatically detect the `.agents/skills/feature-planner` skill, inspect your codebase (read-only), and generate the complete plan.

### In Other Tools (Claude Code / Cursor / Windsurf)

The core planning instructions in `core/orchestrator.md` are completely tool-agnostic. To run the DevKit in Claude Code or Cursor:

1. Open your target project in Claude Code or Cursor.
2. Provide the following prompt (pointing to where `core/orchestrator.md` is located):
   ```markdown
   Act as an autonomous Feature Planner. Follow the instructions in:
   .agents/skills/feature-planner/core/orchestrator.md

   Target Repository: Current directory
   Feature Statement: "Add rate limiting to the login endpoint to prevent brute-force attacks."
   
   Safety Constraint: Planning is read-only. Write all outputs strictly into .devkit/.
   ```

---

## 5. Where will the generated plans appear?

The DevKit generates all planning artifacts inside a **`.devkit/`** directory at the root of your target project. 

**You do NOT need to create this directory manually.** The DevKit creates it automatically.

Your project will look like this:

```text
my-project/
├── src/                    <-- Untouched (0 modifications)
├── tests/                  <-- Untouched (0 modifications)
├── package.json            <-- Untouched (0 modifications)
├── README.md
└── .devkit/                <-- Created automatically by DevKit
    └── plans/
        └── login-rate-limiting/
            ├── feature-spec.md         # Requirements (US, FR, and testable ACs)
            ├── implementation-plan.md  # Architecture approach & touched files
            ├── task-breakdown.md       # Phased TASK cards with dependency DAG
            ├── validation-plan.md      # Test specifications mapped to ACs
            ├── decisions.md            # Architecture decisions & assumptions
            └── run-summary.md          # Quality Gate audit results
```

---

## 6. What should I do with the plans?

Review the generated files in `.devkit/plans/login-rate-limiting/`. 

Once you are satisfied with the acceptance criteria and task breakdown, ask Antigravity, Claude Code, or Cursor to implement the first task:

```text
"Review .devkit/plans/login-rate-limiting/task-breakdown.md. 
Please implement Phase 1, TASK-001."
```

Because every file path is grounded in your actual codebase and every requirement has an explicit test case, the implementation proceeds quickly and reliably.

---

## 7. Should I commit `.devkit/` to Git?

Choose whichever fits your workflow:

### Choice A: Team Planning (Recommended)
Commit the generated plans so your teammates can review, discuss, and implement them, while ignoring temporary runtime checkpoints:

Add this to your project's `.gitignore`:
```gitignore
# Ignore temporary planning run-state, but keep finished plans
.devkit/run-state/
```

### Choice B: Personal Planning
If you only want personal scratchpad plans and do not want `.devkit` pushed to GitHub at all:

Add this to your project's `.gitignore`:
```gitignore
# Ignore all DevKit plans and temporary state
.devkit/
```
