"""
Unit tests for traceability_validator.py (Quality Gates QG-H3 and QG-H4).
"""

import unittest
from tests.unit.traceability_validator import (
    extract_fr_and_ac_from_spec,
    extract_fr_from_tasks,
    extract_ac_from_validation_plan,
    validate_traceability
)

class TestTraceabilityMatrix(unittest.TestCase):

    def setUp(self):
        self.valid_spec = """
# Feature Spec
### FR-001: User Profile Upload
- **Acceptance Criteria:**
  - [ ] **AC-001-1:** Upload succeeds with HTTP 201
  - [ ] **AC-001-2:** Upload rejects files > 5MB with HTTP 400

### FR-002: User Profile Delete
- **Acceptance Criteria:**
  - [ ] **AC-002-1:** Delete removes file and returns HTTP 204
"""

        self.valid_tasks = """
# Task Breakdown
### TASK-001: Model setup
- **Requirements:** FR-001

### TASK-002: Route endpoints
- **Requirements:** FR-001, FR-002
"""

        self.valid_tests = """
# Validation Plan
### TC-001: Test Upload 201
- **Traceability:** Linked to **AC-001-1** (FR-001)

### TC-002: Test Size Limit 400
- **Traceability:** Linked to **AC-001-2** (FR-001)

### TC-003: Test Delete 204
- **Traceability:** Linked to **AC-002-1** (FR-002)
"""

    def test_full_traceability_pass(self):
        res = validate_traceability(self.valid_spec, self.valid_tasks, self.valid_tests)
        self.assertTrue(res["qg_h3_pass"])
        self.assertTrue(res["qg_h4_pass"])
        self.assertTrue(res["is_fully_traceable"])
        self.assertEqual(len(res["unmapped_fr"]), 0)
        self.assertEqual(len(res["untested_ac"]), 0)

    def test_missing_task_mapping_fails_qg_h3(self):
        # Omit FR-002 from tasks
        broken_tasks = """
### TASK-001: Model setup
- **Requirements:** FR-001
"""
        res = validate_traceability(self.valid_spec, broken_tasks, self.valid_tests)
        self.assertFalse(res["qg_h3_pass"])
        self.assertIn("FR-002", res["unmapped_fr"])
        self.assertFalse(res["is_fully_traceable"])

    def test_missing_test_mapping_fails_qg_h4(self):
        # Omit AC-002-1 from tests
        broken_tests = """
### TC-001: Test Upload 201
- **Traceability:** Linked to **AC-001-1** (FR-001)

### TC-002: Test Size Limit 400
- **Traceability:** Linked to **AC-001-2** (FR-001)
"""
        res = validate_traceability(self.valid_spec, self.valid_tasks, broken_tests)
        self.assertFalse(res["qg_h4_pass"])
        self.assertIn("AC-002-1", res["untested_ac"])
        self.assertFalse(res["is_fully_traceable"])

if __name__ == "__main__":
    unittest.main()
