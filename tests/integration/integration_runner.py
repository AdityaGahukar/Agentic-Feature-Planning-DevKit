"""
Integration Runner for Multi-Archetype Planning Simulation.
Executes repository reconnaissance, classification, and planning simulation
aligned with Core Orchestrator rules and Quality Gates.
"""

import os
import json
import re
from typing import Dict, Any, Tuple

from tests.unit.slug_generator import generate_feature_slug
from tests.unit.dag_validator import validate_task_dag
from tests.unit.path_grounding import extract_target_paths_from_task_breakdown, verify_path_grounding
from tests.unit.traceability_validator import validate_traceability

def classify_repository_archetype(repo_root: str) -> Tuple[str, int, Dict[str, int]]:
    """
    Implements the scoring heuristics from core/rubrics/repo_classification_matrix.md.
    Returns: (detected_archetype, highest_score, score_breakdown)
    """
    scores = {
        "Monorepo": 0,
        "Infrastructure": 0,
        "Data Engineering": 0,
        "Library": 0,
        "Application": 0,
    }

    files_in_root = set(os.listdir(repo_root)) if os.path.exists(repo_root) else set()

    # 1. Monorepo signals
    monorepo_indicators = {"pnpm-workspace.yaml", "lerna.json", "nx.json", "turbo.json"}
    if any(f in files_in_root for f in monorepo_indicators):
        scores["Monorepo"] += 10
    if os.path.exists(os.path.join(repo_root, "packages")) or os.path.exists(os.path.join(repo_root, "apps")):
        scores["Monorepo"] += 8

    # 2. Infrastructure signals
    tf_files = [f for f in files_in_root if f.endswith(".tf")]
    has_helm = os.path.exists(os.path.join(repo_root, "helm")) or "Chart.yaml" in files_in_root or os.path.exists(os.path.join(repo_root, "helm", "Chart.yaml"))
    if tf_files or has_helm:
        scores["Infrastructure"] += 10
    app_dirs = {"src", "app", "lib", "pkg", "cmd"}
    if not any(d in files_in_root for d in app_dirs) and (tf_files or has_helm):
        scores["Infrastructure"] += 6

    # 3. Data Engineering signals
    dbt_present = "dbt_project.yml" in files_in_root
    dags_present = os.path.exists(os.path.join(repo_root, "dags")) or os.path.exists(os.path.join(repo_root, "pipelines"))
    if dbt_present or dags_present:
        scores["Data Engineering"] += 10
        scores["Data Engineering"] += 6

    # 4. Manifest inspection (package.json, requirements.txt, etc.)
    pkg_json_path = os.path.join(repo_root, "package.json")
    if os.path.exists(pkg_json_path):
        try:
            with open(pkg_json_path, "r") as f:
                pkg_data = json.load(f)
                deps = pkg_data.get("dependencies", {})
                
                # Check for web frameworks -> Application
                web_frameworks = {"express", "fastify", "next", "react", "vue", "koa", "django", "fastapi"}
                if any(w in deps for w in web_frameworks):
                    scores["Application"] += 8

                # Check for library packaging exports
                if "exports" in pkg_data or ("main" in pkg_data and "types" in pkg_data and not any(w in deps for w in web_frameworks)):
                    scores["Library"] += 8
        except Exception:
            pass

    # 5. Application entrypoint checks
    entrypoints = [
        os.path.join(repo_root, "src", "index.ts"),
        os.path.join(repo_root, "src", "server.ts"),
        os.path.join(repo_root, "src", "app.ts"),
        os.path.join(repo_root, "app.py"),
        os.path.join(repo_root, "main.go")
    ]
    if any(os.path.exists(e) for e in entrypoints):
        scores["Application"] += 8

    # Determine winning archetype
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_archetype, highest_score = sorted_scores[0]

    if highest_score < 8:
        return "Unknown", highest_score, scores

    return best_archetype, highest_score, scores

def simulate_feature_planning(
    repo_root: str,
    feature_statement: str,
    output_base_dir: str = None
) -> Dict[str, Any]:
    """
    Simulates the execution of the 8-stage planning workflow against a target repo.
    Returns the planning outcome and quality gate evaluation results.
    """
    if not output_base_dir:
        output_base_dir = os.path.join(repo_root, ".devkit", "plans")

    os.makedirs(output_base_dir, exist_ok=True)
    slug = generate_feature_slug(feature_statement, output_base_dir)
    plan_dir = os.path.join(output_base_dir, slug)
    os.makedirs(plan_dir, exist_ok=True)

    archetype, score, scores = classify_repository_archetype(repo_root)

    # Generate minimal conforming Blueprints for testing
    spec_content = f"""---
devkit_version: "0.2.0"
artifact_type: "feature-spec"
feature_id: "{slug}"
status: "approved"
---
# Feature Specification: {feature_statement}

### FR-001: Core capability
- **Acceptance Criteria:**
  - [ ] **AC-001-1:** Expected verified outcome
"""
    spec_path = os.path.join(plan_dir, "feature-spec.md")
    with open(spec_path, "w") as f:
        f.write(spec_content)

    tasks_content = f"""---
devkit_version: "0.2.0"
artifact_type: "task-breakdown"
feature_id: "{slug}"
status: "approved"
---
# Task Breakdown

### TASK-001: Implement Core Feature
- **Requirements:** FR-001
- **Depends on:** none
- **Target Files:**
  - Create: `[NEW FILE: {slug}_module.ts]`

```mermaid
flowchart TD
    TASK001["TASK-001: Core"]
```
"""
    tasks_path = os.path.join(plan_dir, "task-breakdown.md")
    with open(tasks_path, "w") as f:
        f.write(tasks_content)

    validation_content = f"""---
devkit_version: "0.2.0"
artifact_type: "validation-plan"
feature_id: "{slug}"
status: "approved"
---
# Validation Plan

### TC-001: Verify Core Feature
- **Traceability:** Linked to **AC-001-1** (FR-001)
"""
    val_path = os.path.join(plan_dir, "validation-plan.md")
    with open(val_path, "w") as f:
        f.write(validation_content)

    # Evaluate quality gates
    trace_res = validate_traceability(spec_content, tasks_content, validation_content)
    targets = extract_target_paths_from_task_breakdown(tasks_content)
    path_valid, path_errors = verify_path_grounding(targets, repo_root)

    return {
        "feature_slug": slug,
        "plan_dir": plan_dir,
        "archetype": archetype,
        "score": score,
        "scores": scores,
        "qg_traceability_pass": trace_res["is_fully_traceable"],
        "qg_path_grounding_pass": path_valid,
        "path_errors": path_errors
    }
