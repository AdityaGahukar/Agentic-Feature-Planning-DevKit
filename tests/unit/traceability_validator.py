"""
Bidirectional Requirement & Acceptance Criteria Traceability Matrix Validator.
Aligned with Quality Gates QG-H3, QG-H4 and LLD Sections 8.3, 8.4.
"""

import re
from typing import Dict, List, Set, Tuple

def extract_fr_and_ac_from_spec(feature_spec_md: str) -> Tuple[Set[str], Set[str]]:
    """
    Extracts all FR-xxx IDs and AC-xxx IDs from feature-spec.md.
    Example matches:
      FR-001, FR-002
      AC-001-1, AC-001-2, AC-002-1
    """
    fr_ids = set(re.findall(r'###\s*(FR-\d+)', feature_spec_md))
    
    # AC IDs match pattern AC-xxx-x or AC-xxx (supporting optional colon inside/outside bold)
    ac_ids = set(re.findall(r'\b(AC-\d+(?:-\d+)?)\b', feature_spec_md))
    
    return fr_ids, ac_ids

def extract_fr_from_tasks(task_breakdown_md: str) -> Set[str]:
    """
    Extracts all FR-xxx IDs mapped in task-breakdown.md under 'Requirements:'.
    Example:
      - **Requirements:** FR-001, FR-002
    """
    mapped_fr: Set[str] = set()
    for line in task_breakdown_md.splitlines():
        if re.search(r'-\s+\*\*Requirements:\*\*', line, re.IGNORECASE):
            matches = re.findall(r'FR-\d+', line)
            mapped_fr.update(matches)
    return mapped_fr

def extract_ac_from_validation_plan(validation_plan_md: str) -> Set[str]:
    """
    Extracts all AC-xxx IDs mapped in validation-plan.md under 'Traceability:'.
    Example:
      - **Traceability:** Linked to **AC-001-1** (FR-001)
    """
    mapped_ac: Set[str] = set()
    for line in validation_plan_md.splitlines():
        if re.search(r'-\s+\*\*Traceability:\*\*', line, re.IGNORECASE) or "Linked to" in line:
            matches = re.findall(r'AC-\d+(?:-\d+)?', line)
            mapped_ac.update(matches)
    return mapped_ac

def validate_traceability(
    feature_spec_md: str,
    task_breakdown_md: str,
    validation_plan_md: str
) -> Dict[str, any]:
    """
    Validates complete bidirectional traceability:
    1. QG-H3: All FRs have at least one assigned task.
    2. QG-H4: All ACs have at least one assigned test case.

    Returns:
      {
        'qg_h3_pass': bool,
        'unmapped_fr': List[str],
        'qg_h4_pass': bool,
        'untested_ac': List[str],
        'is_fully_traceable': bool
      }
    """
    spec_frs, spec_acs = extract_fr_and_ac_from_spec(feature_spec_md)
    task_frs = extract_fr_from_tasks(task_breakdown_md)
    test_acs = extract_ac_from_validation_plan(validation_plan_md)

    unmapped_fr = sorted(list(spec_frs - task_frs))
    untested_ac = sorted(list(spec_acs - test_acs))

    qg_h3_pass = (len(unmapped_fr) == 0 and len(spec_frs) > 0)
    qg_h4_pass = (len(untested_ac) == 0 and len(spec_acs) > 0)

    return {
        "qg_h3_pass": qg_h3_pass,
        "unmapped_fr": unmapped_fr,
        "qg_h4_pass": qg_h4_pass,
        "untested_ac": untested_ac,
        "is_fully_traceable": (qg_h3_pass and qg_h4_pass)
    }
