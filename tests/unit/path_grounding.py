"""
Path Grounding & Hallucination Verification Utility.
Aligned with Quality Gate QG-H1 and LLD Section 8.1.
"""

import os
import re
from typing import Dict, List, Set, Tuple

def extract_target_paths_from_task_breakdown(markdown_content: str) -> Dict[str, Dict[str, List[str]]]:
    """
    Parses task-breakdown.md to extract target file paths per task.
    Returns:
      {
        'TASK-001': {
          'modify': ['src/db.ts'],
          'create': ['src/models/user.ts']
        }
      }
    """
    results: Dict[str, Dict[str, List[str]]] = {}
    
    task_blocks = re.split(r'(?=###\s+TASK-\d+)', markdown_content)
    for block in task_blocks:
        match_id = re.search(r'###\s+(TASK-\d+)', block)
        if not match_id:
            continue
        task_id = match_id.group(1)
        
        modify_paths: List[str] = []
        create_paths: List[str] = []
        
        # Match lines like "- Modify: `path/to/file`" or "- Modify: path/to/file"
        for line in block.splitlines():
            clean_line = line.strip()
            if re.match(r'^[-\*]\s*Modify:', clean_line, re.IGNORECASE):
                # Extract paths between backticks or standard tokens
                matches = re.findall(r'`([^`]+)`', clean_line)
                if not matches:
                    raw = re.sub(r'^[-\*]\s*Modify:\s*', '', clean_line)
                    matches = [raw.strip()] if raw.strip() else []
                for p in matches:
                    if p.lower() not in {"none", "n/a", ""}:
                        modify_paths.append(p)
                        
            elif re.match(r'^[-\*]\s*Create:', clean_line, re.IGNORECASE):
                # Extract [NEW FILE: <path>]
                matches = re.findall(r'\[NEW FILE:\s*([^\]]+)\]', clean_line, re.IGNORECASE)
                if not matches:
                    # Fallback to backticks if NEW FILE tag was omitted
                    backtick_matches = re.findall(r'`([^`]+)`', clean_line)
                    matches = backtick_matches
                for p in matches:
                    if p.lower() not in {"none", "n/a", ""}:
                        create_paths.append(p)
                        
        results[task_id] = {
            "modify": modify_paths,
            "create": create_paths
        }
        
    return results

def verify_path_grounding(
    target_paths_per_task: Dict[str, Dict[str, List[str]]],
    repo_root: str,
    known_existing_paths: Set[str] = None
) -> Tuple[bool, List[str]]:
    """
    Verifies that:
    1. Every path to Modify physically exists on disk (or in known_existing_paths).
    2. Every path to Create does NOT already exist on disk (preventing false [NEW FILE] claims).

    Returns:
      (is_valid, list_of_error_messages)
    """
    errors: List[str] = []
    
    for task_id, path_groups in target_paths_per_task.items():
        # 1. Verify Modify paths
        for mod_path in path_groups.get("modify", []):
            normalized = os.path.normpath(mod_path).lstrip("/")
            full_disk_path = os.path.join(repo_root, normalized)
            
            exists_on_disk = os.path.exists(full_disk_path)
            exists_in_known = bool(known_existing_paths and (normalized in known_existing_paths or mod_path in known_existing_paths))
            
            if not exists_on_disk and not exists_in_known:
                errors.append(f"[{task_id}] Hallucinated modify path: '{mod_path}' does not exist.")
                
        # 2. Verify Create paths
        for create_path in path_groups.get("create", []):
            normalized = os.path.normpath(create_path).lstrip("/")
            full_disk_path = os.path.join(repo_root, normalized)
            
            exists_on_disk = os.path.exists(full_disk_path)
            exists_in_known = bool(known_existing_paths and (normalized in known_existing_paths or create_path in known_existing_paths))
            
            if exists_on_disk or exists_in_known:
                errors.append(f"[{task_id}] Invalid prospective path: '{create_path}' marked [NEW FILE] but already exists.")

    is_valid = (len(errors) == 0)
    return is_valid, errors
