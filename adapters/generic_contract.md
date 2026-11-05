# Generic Harness Adapter Contract (v1.0)

> **Document Version:** 1.0.0  
> **Status:** Standard Interface Contract for Future Agent Runtimes  
> **Applicable Runtimes:** Claude Code, Cursor, GitHub Copilot CLI, Cline, Aider, Custom LLM Harnesses  

---

## 1. Objective & Design Philosophy

The **Agentic Feature Planning DevKit** maintains a strictly harness-agnostic core. Any AI coding assistant or autonomous agent platform can execute the DevKit without rewriting planning logic, provided it implements the four primitive integration capabilities outlined in this contract.

---

## 2. The Four Adapter Primitives

Any conforming harness adapter must fulfill the following four capabilities:

### Primitive 1: Workspace Access & Sandboxed I/O
- **Repository Read Access:** The agent must be granted filesystem read access to inspect files, manifests, directories, and configuration profiles within the target repository.
- **Sandboxed Write Access:** The agent must be granted write access **strictly restricted to `<repo-root>/.devkit/`**. The harness or adapter must prevent write operations to application source files, existing tests, or build outputs during planning runs.

### Primitive 2: Instruction Injection
- The adapter must inject [`core/orchestrator.md`](../core/orchestrator.md) as the driving prompt or system instruction for the planning session.
- The agent must be directed to read individual stage instructions from `core/stages/` as instructed by the master orchestrator.

### Primitive 3: Human Clarification Relay (Interactive Harnesses)
- If Stage 1 detects a **Tier 4 Critical Ambiguity**, the adapter must relay the batched question list (maximum 5) to the user and wait for input.
- Once user input is received, the adapter injects the answers into the session context to resume Stage 2.
- **Headless Fallback:** In non-interactive or batch environments, the adapter must instruct the agent to select the safe recommended default automatically and log the choice under `decisions.md`.

### Primitive 4: CLI & Tool Independence
- The harness must **not** require an external compiled binary, database, or background service.
- Standard LLM tool-calling capabilities (`read_file`, `write_file`, and optionally a command runner for directory listings or `git status`) are completely sufficient.

---

## 3. Reference Implementation: Headless / Scripted Adapter (TypeScript / Python)

Below is an abstract reference implementation demonstrating how a future harness executes the DevKit:

```typescript
/**
 * Conforming Harness Adapter Skeleton
 */
interface DevKitInputs {
  repoRoot: string;
  featureStatement: string;
  stackHint?: string;
  depth?: "auto" | "shallow" | "deep";
  featureIdOverride?: string;
}

class GenericDevKitAdapter {
  constructor(private agent: HostAgentClient, private fs: FileSystemTool) {}

  async executePlanning(inputs: DevKitInputs): Promise<void> {
    // 1. Validate Target Repository
    if (!this.fs.exists(inputs.repoRoot)) {
      throw new Error(`Repository root not found: ${inputs.repoRoot}`);
    }

    // 2. Prepare Sandbox Directory
    const devkitDir = `${inputs.repoRoot}/.devkit`;
    this.fs.ensureDir(`${devkitDir}/run-state`);

    // 3. Construct System Prompt with Core Orchestrator
    const orchestratorPrompt = this.fs.readFile("core/orchestrator.md");
    const sessionPrompt = `
      ${orchestratorPrompt}

      TARGET REPOSITORY: ${inputs.repoRoot}
      FEATURE STATEMENT: "${inputs.featureStatement}"
      STACK HINT: ${inputs.stackHint || "none"}
      PLANNING DEPTH: ${inputs.depth || "auto"}
      SLUG OVERRIDE: ${inputs.featureIdOverride || "none"}
    `;

    // 4. Delegate to Host Agent
    await this.agent.runSession({
      systemPrompt: sessionPrompt,
      tools: {
        readFile: (path) => this.fs.readFile(path),
        writeFile: (path, content) => {
          // Strictly enforce sandboxing
          if (!path.startsWith(devkitDir)) {
            throw new Error(`Write operation rejected outside sandbox: ${path}`);
          }
          return this.fs.writeFile(path, content);
        },
        runCommand: (cmd) => this.agent.executeShell(cmd)
      }
    });
  }
}
```

---

## 4. Verification & Conformance Checklist
A harness adapter is certified DevKit-compliant when:
- [ ] Core instructions in `core/` are invoked without modifications.
- [ ] No file outside `.devkit/` is written or modified during planning.
- [ ] The generated output in `.devkit/plans/<slug>/` contains all 7 Blueprint files.
- [ ] All Hard Quality Gates (`QG-H1` through `QG-H5`) pass successfully.
