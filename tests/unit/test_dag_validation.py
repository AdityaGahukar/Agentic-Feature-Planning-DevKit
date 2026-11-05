"""
Unit tests for dag_validator.py (Quality Gate QG-H2).
"""

import unittest
from tests.unit.dag_validator import parse_task_dependencies_from_markdown, validate_task_dag

class TestDAGValidation(unittest.TestCase):

    def test_valid_sequential_dag(self):
        deps = {
            "TASK-001": [],
            "TASK-002": ["TASK-001"],
            "TASK-003": ["TASK-002"]
        }
        is_valid, topo_order, cycles = validate_task_dag(deps)
        self.assertTrue(is_valid)
        self.assertEqual(len(cycles), 0)
        self.assertEqual(topo_order, ["TASK-001", "TASK-002", "TASK-003"])

    def test_valid_branching_dag(self):
        deps = {
            "TASK-001": [],
            "TASK-002": ["TASK-001"],
            "TASK-003": ["TASK-001"],
            "TASK-004": ["TASK-002", "TASK-003"]
        }
        is_valid, topo_order, cycles = validate_task_dag(deps)
        self.assertTrue(is_valid)
        self.assertEqual(len(cycles), 0)
        self.assertEqual(topo_order[0], "TASK-001")
        self.assertEqual(topo_order[-1], "TASK-004")

    def test_direct_two_node_cycle(self):
        deps = {
            "TASK-001": ["TASK-002"],
            "TASK-002": ["TASK-001"]
        }
        is_valid, topo_order, cycles = validate_task_dag(deps)
        self.assertFalse(is_valid)
        self.assertIn("TASK-001", cycles)
        self.assertIn("TASK-002", cycles)

    def test_indirect_three_node_cycle(self):
        deps = {
            "TASK-001": ["TASK-003"],
            "TASK-002": ["TASK-001"],
            "TASK-003": ["TASK-002"],
            "TASK-004": ["TASK-003"] # dependent on cycle
        }
        is_valid, topo_order, cycles = validate_task_dag(deps)
        self.assertFalse(is_valid)
        self.assertEqual(cycles, {"TASK-001", "TASK-002", "TASK-003", "TASK-004"})

    def test_self_dependency_cycle(self):
        deps = {
            "TASK-001": ["TASK-001"]
        }
        is_valid, topo_order, cycles = validate_task_dag(deps)
        self.assertFalse(is_valid)
        self.assertIn("TASK-001", cycles)

    def test_markdown_parser_with_valid_content(self):
        sample_md = """
# Task Breakdown

### TASK-001: Data Model Setup
- **Type:** infrastructure
- **Complexity:** S
- **Requirements:** FR-001
- **Depends on:** none
- **Target Files:**
  - Modify: `src/db.ts`

### TASK-002: API Implementation
- **Type:** feature
- **Complexity:** M
- **Requirements:** FR-001, FR-002
- **Depends on:** TASK-001
- **Target Files:**
  - Create: `[NEW FILE: src/routes.ts]`

### TASK-003: Integration Tests
- **Type:** test
- **Complexity:** S
- **Requirements:** FR-001
- **Depends on:** TASK-001, TASK-002
"""
        parsed = parse_task_dependencies_from_markdown(sample_md)
        self.assertEqual(parsed["TASK-001"], [])
        self.assertEqual(parsed["TASK-002"], ["TASK-001"])
        self.assertEqual(parsed["TASK-003"], ["TASK-001", "TASK-002"])

        is_valid, topo, cycles = validate_task_dag(parsed)
        self.assertTrue(is_valid)
        self.assertEqual(topo, ["TASK-001", "TASK-002", "TASK-003"])

if __name__ == "__main__":
    unittest.main()
