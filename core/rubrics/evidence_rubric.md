# The Evidence Rubric & Human Intervention Rules

This rubric defines the deterministic rules by which the DevKit evaluates technical choices, assumptions, and clarifying questions. The agent must NEVER fabricate confidence percentages (e.g. "I am 75% confident"). Every choice must be grounded in observable codebase evidence according to this 4-tier hierarchy.

---

## 1. The Four Evidence Tiers

### Tier 1: Evidence-Supported
- **Definition:** The decision is directly corroborated by existing repository code, dependency manifests, configuration files, or automated tests. At least two distinct signals in the repository support the choice.
- **Agent Action:** 
  - Adopt the choice immediately without asking the developer.
  - Record the decision in artifacts as `[ASSUMPTION: evidence-supported]`.
  - Cite the exact corroborating file paths in the assumption note.
- **Example:** The repository contains `prisma/schema.prisma` and imports `@prisma/client` in 5 service files. The feature requires database queries. The agent adopts Prisma.

### Tier 2: Reasonable Assumption
- **Definition:** The codebase is silent or provides no direct signal, but a standard industry convention provides a safe, low-risk, conservative default.
- **Agent Action:**
  - Adopt the default choice without asking the developer.
  - Record the decision in artifacts as `[ASSUMPTION: reasonable-default]`.
  - Document the risk if wrong as "Low".
- **Example:** The repository has REST endpoints with no pagination standard defined. The feature adds a listing endpoint. The agent defaults to standard `limit` and `offset` query parameters.

### Tier 3: Design Choice
- **Definition:** Multiple valid technical or architectural approaches exist with meaningful trade-offs. The codebase does not dictate the choice, but the decision is non-blocking and does not prevent implementation planning.
- **Agent Action:**
  - Select the most conservative, modular, and reversible option.
  - Create a formal Architecture Decision Record (ADR) in `decisions.md`.
  - List the rejected alternatives and the rationale for rejection.
  - Do NOT pause execution or ask the developer.
- **Example:** A new service needs to parse CSV files. It could use an external library or custom stream parser. The agent selects the standard library/existing parser, documents ADR-001, and notes the alternative.

### Tier 4: Critical Ambiguity
- **Definition:** A fundamental contradiction in requirements or missing core business logic that prevents deterministic planning. ALL THREE of the following conditions must be met:
  1. The answer fundamentally alters the technical architecture or implementation approach.
  2. The answer cannot be inferred from repository code or safe defaults.
  3. A wrong assumption would require rewriting major portions of the feature.
- **Agent Action:**
  - **PAUSE** execution immediately at the end of Stage 1.
  - Format a batched, numbered list of questions (maximum 5).
  - Present the questions to the developer with context, implications, and a recommended default.
  - Await developer answers, record them in `intake.md`, and resume automatically.

---

## 2. Batched Clarification Protocol & Constraints

When a Tier 4 Critical Ambiguity occurs, the agent must adhere to these strict constraints:
1. **Single Pause Only:** Clarifications are permitted **only once** per planning run, immediately following Stage 1 Intake. The agent is strictly prohibited from interrupting during Stages 2 through 8.
2. **Maximum 5 Questions:** Never present more than 5 questions in the batched prompt.
3. **Structured Question Format:**
   ```markdown
   ### Critical Clarification Required

   1. [Question Title]
      - **Context:** Why this cannot be inferred from the codebase.
      - **Option A:** [Description and architectural impact]
      - **Option B:** [Description and architectural impact]
      - **Recommended Default:** [Option selected if unanswered]
   ```
4. **Headless / Non-Answer Fallback:** If the developer does not respond or the harness runs in a non-interactive mode, the agent adopts the recommended default, logs the choice as `[ASSUMPTION: reasonable-default (unanswered)]`, and proceeds autonomously.
