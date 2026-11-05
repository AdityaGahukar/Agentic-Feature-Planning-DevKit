"""
Kahn's Algorithm Task DAG Cycle Detector and Dependency Validator.
Aligned with Quality Gate QG-H2 and LLD Section 8.2.
"""

from collections import deque
import re
from typing import Dict, List, Set, Tuple

def parse_task_dependencies_from_markdown(markdown_content: str) -> Dict[str, List[str]]:
    """
    Parses task-breakdown.md content to extract tasks and their dependencies.
    Format expected:
      ### TASK-001: Title
      ...
      - **Depends on:** TASK-000, TASK-002
    Returns adjacency dict: { 'TASK-001': ['TASK-000', 'TASK-002'] }
    meaning TASK-001 requires TASK-000 and TASK-002 to complete first.
    """
    task_deps: Dict[str, List[str]] = {}
    
    # Split into task blocks
    task_blocks = re.split(r'(?=###\s+TASK-\d+)', markdown_content)
    
    for block in task_blocks:
        match_id = re.search(r'###\s+(TASK-\d+)', block)
        if not match_id:
            continue
        task_id = match_id.group(1)
        
        match_deps = re.search(r'-\s+\*\*Depends on:\*\*\s*(.*)', block, re.IGNORECASE)
        deps: List[str] = []
        if match_deps:
            raw_deps = match_deps.group(1).strip()
            if raw_deps.lower() not in {"none", "none.", "n/a", ""}:
                # Extract all TASK-xxx matches in dependency line
                deps = re.findall(r'TASK-\d+', raw_deps)
                
        task_deps[task_id] = deps
        
    return task_deps

def validate_task_dag(task_dependencies: Dict[str, List[str]]) -> Tuple[bool, List[str], Set[str]]:
    """
    Validates whether task dependencies form a valid Directed Acyclic Graph (DAG)
    using Kahn's algorithm (Topological Sort).

    Input:
      task_dependencies: { task_id: [prerequisite_task_ids] }
      Note: Prerequisite means an edge from prerequisite -> task.

    Returns:
      (is_valid, topological_sort_order, cycle_nodes)
    """
    all_nodes: Set[str] = set(task_dependencies.keys())
    
    # Also include any referenced dependencies as nodes if not explicitly defined
    for deps in task_dependencies.values():
        all_nodes.update(deps)

    if not all_nodes:
        return True, [], set()

    # Build forward graph: prerequisite -> dependent tasks
    forward_graph: Dict[str, List[str]] = {node: [] for node in all_nodes}
    in_degree: Dict[str, int] = {node: 0 for node in all_nodes}

    for task, deps in task_dependencies.items():
        for prereq in deps:
            forward_graph[prereq].append(task)
            in_degree[task] += 1

    # Queue all nodes with in-degree 0 (no prerequisites)
    queue = deque([node for node in all_nodes if in_degree[node] == 0])
    topological_order: List[str] = []

    while queue:
        current = queue.popleft()
        topological_order.append(current)

        for neighbor in forward_graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If count of visited nodes equals total nodes, graph is acyclic
    is_acyclic = (len(topological_order) == len(all_nodes))
    cycle_nodes = set() if is_acyclic else {node for node, deg in in_degree.items() if deg > 0}

    return is_acyclic, topological_order, cycle_nodes
